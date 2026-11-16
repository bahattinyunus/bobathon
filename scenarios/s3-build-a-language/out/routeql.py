"""RouteQL v1 interpreter (CampusRoute kiosk scripting language).

Conforms strictly to routeql-spec.md.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Set up import path for campusroute
HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
APP_DIR = WORKSPACE / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

try:
    from campusroute.campus import Campus, UnknownPlaceError, load_campus
    from campusroute.routing import NoRouteError, shortest_route
    from campusroute.search import search
except ImportError as err:
    print(f"Error importing campusroute: {err}", file=sys.stderr)
    sys.exit(2)

KEYWORDS = {"let", "route", "to", "via", "avoid", "stairs", "find", "print"}


class Token:
    def __init__(self, kind: str, value: str, col: int):
        self.kind = kind
        self.value = value
        self.col = col

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.value!r})"


class RouteQLError(Exception):
    def __init__(self, line_num: int, message: str):
        super().__init__(message)
        self.line_num = line_num
        self.message = message


def tokenize_line(line: str, line_num: int) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(line)

    while i < n:
        ch = line[i]

        # Whitespace
        if ch in " \t\r\n":
            i += 1
            continue

        # Comment
        if ch == "#":
            break

        # String
        if ch == '"':
            start_col = i + 1
            i += 1
            s_val = []
            closed = False
            while i < n:
                c = line[i]
                if c == "\n" or c == "\r":
                    break
                if c == '"':
                    closed = True
                    i += 1
                    break
                s_val.append(c)
                i += 1
            if not closed:
                raise RouteQLError(line_num, "unterminated string")
            tokens.append(Token("STRING", "".join(s_val), start_col))
            continue

        # Symbols
        if ch == "=":
            tokens.append(Token("EQUALS", "=", i + 1))
            i += 1
            continue
        if ch == ",":
            tokens.append(Token("COMMA", ",", i + 1))
            i += 1
            continue

        # Identifiers or keywords: [A-Za-z_][A-Za-z0-9_]*
        if ch.isalpha() or ch == "_":
            start_col = i + 1
            w = []
            while i < n and (line[i].isalnum() or line[i] == "_"):
                w.append(line[i])
                i += 1
            word = "".join(w)
            if word in KEYWORDS:
                tokens.append(Token("KEYWORD", word, start_col))
            else:
                tokens.append(Token("IDENT", word, start_col))
            continue

        # Any other character is invalid syntax
        raise RouteQLError(line_num, f"syntax error: unexpected character {ch!r}")

    return tokens


# AST Nodes
class Statement:
    def __init__(self, line_num: int):
        self.line_num = line_num


class LetStmt(Statement):
    def __init__(self, line_num: int, name: str, value: str):
        super().__init__(line_num)
        self.name = name
        self.value = value


class PrintStmt(Statement):
    def __init__(self, line_num: int, is_var: bool, value: str):
        super().__init__(line_num)
        self.is_var = is_var
        self.value = value


class FindStmt(Statement):
    def __init__(self, line_num: int, query: str):
        super().__init__(line_num)
        self.query = query


class RouteStmt(Statement):
    def __init__(
        self,
        line_num: int,
        start: Tuple[bool, str],
        goal: Tuple[bool, str],
        via: List[Tuple[bool, str]],
        avoid_stairs: bool,
    ):
        super().__init__(line_num)
        self.start = start  # (is_var, value)
        self.goal = goal
        self.via = via
        self.avoid_stairs = avoid_stairs


def parse_place(token: Token, line_num: int) -> Tuple[bool, str]:
    if token.kind == "STRING":
        return False, token.value
    if token.kind == "IDENT":
        return True, token.value
    raise RouteQLError(line_num, "syntax error: expected place (string or identifier)")


def parse_line(tokens: List[Token], line_num: int) -> Optional[Statement]:
    if not tokens:
        return None

    first = tokens[0]
    if first.kind != "KEYWORD":
        raise RouteQLError(line_num, "syntax error: expected statement")

    kw = first.value

    if kw == "let":
        # let IDENT "=" STRING
        if len(tokens) != 4:
            raise RouteQLError(line_num, "syntax error: expected 'let <ident> = <string>'")
        if tokens[1].kind != "IDENT":
            raise RouteQLError(line_num, f"syntax error: invalid variable name {tokens[1].value!r}")
        if tokens[2].kind != "EQUALS":
            raise RouteQLError(line_num, "syntax error: expected '=' in let statement")
        if tokens[3].kind != "STRING":
            raise RouteQLError(line_num, "syntax error: expected string literal after '='")
        return LetStmt(line_num, tokens[1].value, tokens[3].value)

    if kw == "print":
        # print (STRING | IDENT)
        if len(tokens) != 2:
            raise RouteQLError(line_num, "syntax error: expected 'print <string|ident>'")
        target = tokens[1]
        if target.kind == "STRING":
            return PrintStmt(line_num, False, target.value)
        if target.kind == "IDENT":
            return PrintStmt(line_num, True, target.value)
        raise RouteQLError(line_num, "syntax error: expected string or identifier after print")

    if kw == "find":
        # find STRING
        if len(tokens) != 2 or tokens[1].kind != "STRING":
            raise RouteQLError(line_num, "syntax error: expected 'find <string>'")
        return FindStmt(line_num, tokens[1].value)

    if kw == "route":
        # route place "to" place [ "via" place { "," place } ] [ "avoid" "stairs" ]
        pos = 1
        num_tokens = len(tokens)
        if pos >= num_tokens:
            raise RouteQLError(line_num, "syntax error: expected start place after route")
        start = parse_place(tokens[pos], line_num)
        pos += 1

        if pos >= num_tokens or tokens[pos].kind != "KEYWORD" or tokens[pos].value != "to":
            raise RouteQLError(line_num, "syntax error: expected 'to' in route statement")
        pos += 1

        if pos >= num_tokens:
            raise RouteQLError(line_num, "syntax error: expected goal place after 'to'")
        goal = parse_place(tokens[pos], line_num)
        pos += 1

        via_places: List[Tuple[bool, str]] = []
        if pos < num_tokens and tokens[pos].kind == "KEYWORD" and tokens[pos].value == "via":
            pos += 1
            if pos >= num_tokens:
                raise RouteQLError(line_num, "syntax error: expected place after 'via'")
            via_places.append(parse_place(tokens[pos], line_num))
            pos += 1
            while pos < num_tokens and tokens[pos].kind == "COMMA":
                pos += 1
                if pos >= num_tokens:
                    raise RouteQLError(line_num, "syntax error: expected place after ','")
                via_places.append(parse_place(tokens[pos], line_num))
                pos += 1

        avoid_stairs = False
        if pos < num_tokens and tokens[pos].kind == "KEYWORD" and tokens[pos].value == "avoid":
            pos += 1
            if pos >= num_tokens or tokens[pos].kind != "KEYWORD" or tokens[pos].value != "stairs":
                raise RouteQLError(line_num, "syntax error: expected 'stairs' after 'avoid'")
            avoid_stairs = True
            pos += 1

        if pos != num_tokens:
            raise RouteQLError(line_num, f"syntax error: unexpected token '{tokens[pos].value}'")

        return RouteStmt(line_num, start, goal, via_places, avoid_stairs)

    raise RouteQLError(line_num, f"syntax error: unknown keyword '{kw}'")


def parse_program(lines: List[str]) -> List[Statement]:
    statements: List[Statement] = []
    for idx, raw_line in enumerate(lines, start=1):
        tokens = tokenize_line(raw_line, idx)
        stmt = parse_line(tokens, idx)
        if stmt is not None:
            statements.append(stmt)
    return statements


def execute_program(statements: List[Statement]) -> None:
    variables: Dict[str, str] = {}
    campus: Optional[Campus] = None

    def get_campus() -> Campus:
        nonlocal campus
        if campus is None:
            campus = load_campus()
        return campus

    def resolve_place_val(is_var: bool, val: str, line_num: int) -> str:
        if is_var:
            if val not in variables:
                raise RouteQLError(line_num, f"undefined variable '{val}'")
            return variables[val]
        return val

    for stmt in statements:
        if isinstance(stmt, LetStmt):
            variables[stmt.name] = stmt.value
            continue

        if isinstance(stmt, PrintStmt):
            if stmt.is_var:
                if stmt.value not in variables:
                    raise RouteQLError(stmt.line_num, f"undefined variable '{stmt.value}'")
                text = variables[stmt.value]
            else:
                text = stmt.value
            print(text)
            continue

        if isinstance(stmt, FindStmt):
            c = get_campus()
            hits = search(c, stmt.query, limit=3)
            print(f'find "{stmt.query}":')
            if hits:
                for hit in hits:
                    print(f"  - {hit.label}")
            else:
                print("  (no matches)")
            continue

        if isinstance(stmt, RouteStmt):
            c = get_campus()
            start_str = resolve_place_val(stmt.start[0], stmt.start[1], stmt.line_num)
            goal_str = resolve_place_val(stmt.goal[0], stmt.goal[1], stmt.line_num)

            try:
                start_place = c.resolve(start_str)
            except UnknownPlaceError as e:
                raise RouteQLError(stmt.line_num, str(e)) from e

            try:
                goal_place = c.resolve(goal_str)
            except UnknownPlaceError as e:
                raise RouteQLError(stmt.line_num, str(e)) from e

            via_place_ids = []
            for is_v, v_name in stmt.via:
                via_str = resolve_place_val(is_v, v_name, stmt.line_num)
                try:
                    p = c.resolve(via_str)
                    via_place_ids.append(p.id)
                except UnknownPlaceError as e:
                    raise RouteQLError(stmt.line_num, str(e)) from e

            try:
                route = shortest_route(
                    c,
                    start_place.id,
                    goal_place.id,
                    avoid_stairs=stmt.avoid_stairs,
                    via=via_place_ids,
                )
            except NoRouteError as e:
                raise RouteQLError(stmt.line_num, str(e)) from e

            header = f"{start_place.name} -> {goal_place.name}: {route.meters} m, {route.minutes} min"
            if route.has_stairs:
                header += " (stairs)"
            print(header)
            path_names = [c.places[pid].name for pid in route.path]
            print("  " + " > ".join(path_names))
            continue


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python routeql.py <file.rql>", file=sys.stderr)
        sys.exit(2)

    target_path = Path(sys.argv[1])
    if not target_path.exists() or not target_path.is_file():
        print(f"File not found: {target_path}", file=sys.stderr)
        sys.exit(2)

    try:
        source = target_path.read_text(encoding="utf-8")
    except Exception as err:
        print(f"Error reading file {target_path}: {err}", file=sys.stderr)
        sys.exit(2)

    lines = source.splitlines()

    # Step 1: Parse first (if any syntax error, no output, exit 1)
    try:
        statements = parse_program(lines)
    except RouteQLError as err:
        print(f"Error on line {err.line_num}: {err.message}", file=sys.stderr)
        sys.exit(1)

    # Step 2: Execute statements (runtime errors exit 1, earlier output preserved)
    try:
        execute_program(statements)
    except RouteQLError as err:
        print(f"Error on line {err.line_num}: {err.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
