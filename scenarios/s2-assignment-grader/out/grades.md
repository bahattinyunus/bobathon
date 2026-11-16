# CS201 Lab 4: Grading Evaluation Reports

Automated scores are a draft. The instructor makes the final decision.

---

## Student A

### Criterion Breakdown

| # | Criterion | Score | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | Correctness (30) | 30 / 30 | `"while heap: ... candidate = d + weight ... dist[neighbor] = candidate"` | Excellent Dijkstra implementation using a priority queue with early exit. |
| 2 | Edge Cases (15) | 15 / 15 | `"if start not in graph or goal not in graph: raise ValueError ... if goal not in settled: return math.inf, []"` | Handles unknown nodes, unreachable nodes, and start == goal cleanly. |
| 3 | Tests (20) | 20 / 20 | `class ShortestPathTest(unittest.TestCase)` with 5 comprehensive test cases covering weights vs hops, edge cases, and unreachable nodes. | Well-structured test suite with accurate expected values. |
| 4 | Complexity Analysis (15) | 15 / 15 | `"O((V + E) log V) with a binary heap ... space is O(V)"` correctly justified by heap operations and map sizes. | Clear and accurate analysis matching the code as written. |
| 5 | Code Quality (10) | 10 / 10 | Includes descriptive docstrings, type annotations, clean variable names, and an `itertools.count()` tie-breaker for tuple safety. | Production-grade code formatting and style. |
| 6 | Reflection (10) | 10 / 10 | Explicitly addresses the non-negative weight constraint and Dijkstra's greedy invariant. | Insightful reflection on theoretical limitations. |

**Total Score: 100 / 100**

#### Strengths
1. Robust priority queue handling with lazy deletion and tuple tie-breaking.
2. Complete test coverage including custom assertions for all required edge cases.

#### Areas to Improve
1. Consider adding an adjacency type-check or validator for defensive library use.
2. Explore bidirectional Dijkstra as an optional extension for large graphs.

---

## Student B

### Criterion Breakdown

| # | Criterion | Score | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | Correctness (30) | 20 / 30 | `"for n in unvisited: if dist[n] < dist[u]: u = n ... unvisited.remove(u)"` | Finds shortest paths on connected positive-weight graphs, but will fail with KeyError on disconnected goals when reconstructing path. |
| 2 | Edge Cases (15) | 4 / 15 | `while x != start: path.insert(0, x); x = prev[x]` (crashes when goal is unreachable, does not raise ValueError on unknown start/goal). | Add explicit validation for node existence and check if `goal in prev` before path reconstruction. |
| 3 | Tests (20) | 8 / 20 | Only two tests provided (`test1`, `test2`), missing disconnected graph and invalid node tests. | Expand test suite to include edge cases such as disconnected graphs and invalid nodes. |
| 4 | Complexity Analysis (15) | 4 / 15 | Claims `"O(n log n) because it uses a priority queue"`, but the code uses a linear list search and list remove. | Analyze the runtime based on the actual operations in your code (`O(V²)` for the nested scan and removal). |
| 5 | Code Quality (10) | 6 / 10 | Brief variable names (`u`, `v`, `x`, `alt`), missing docstring, inefficient `path.insert(0, ...)`. | Add docstrings explaining parameters and use `path.append` followed by `path.reverse()`. |
| 6 | Reflection (10) | 5 / 10 | Brief reflection, does not mention negative weights or the impact of linear scanning. | Discuss algorithm assumptions including non-negative edge weights. |

**Total Score: 47 / 100**

#### Strengths
1. Successfully implements the core greedy relaxation idea of Dijkstra's algorithm.
2. Correctly passes the basic example route and identical start/goal test.

#### Areas to Improve
1. Replace linear search over `unvisited` with `heapq` to achieve true `O((V + E) log V)` performance.
2. Protect path reconstruction against unreachable target nodes to avoid `KeyError`.

---

## Student C

### Criterion Breakdown

| # | Criterion | Score | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | Correctness (30) | 10 / 30 | `q = deque([[start]]) ... q.popleft()` | Implemented Breadth-First Search (BFS) rather than Dijkstra; finds fewest edges, not minimum total distance on weighted graphs. |
| 2 | Edge Cases (15) | 2 / 15 | No checks for unknown nodes, returns `None` implicitly if unreachable instead of `(math.inf, [])`. | Add explicit error handling for invalid input nodes and handle unreachable destinations. |
| 3 | Tests (20) | 0 / 20 | `"I tested it by running it on the example and it printed the right answer."` (No `unittest` test cases). | Write structured test cases using Python's `unittest` module. |
| 4 | Complexity Analysis (15) | 3 / 15 | Cites `O((V+E) log V)` for binary heaps, but the implementation is unweighted BFS with full path copies in queue (`O(V · (V+E))`). | Match theoretical complexity analysis directly to the data structures used in the submitted code. |
| 5 | Code Quality (10) | 4 / 10 | Stores full path arrays inside queue elements (`q.append(p + [n])`), causing high memory overhead; missing docstring. | Use a `prev` predecessor dictionary to reconstruct paths instead of duplicating arrays in memory. |
| 6 | Reflection (10) | 3 / 10 | States `"My solution works for all cases"`, overlooking weighted edge differences. | Contrast BFS hop-counting with weighted graph shortest-path requirements. |

**Total Score: 22 / 100**

#### Strengths
1. Clean usage of Python's standard `collections.deque` for FIFO traversal.
2. Clear and concise path accumulation logic.

#### Areas to Improve
1. Use edge weights with a priority queue rather than hop-based BFS for weighted networks.
2. Include formal unit tests verifying edge cases and algorithm invariants.

---

## Comparative Score Summary

| Criterion | Student A | Student B | Student C |
|---|:---:|:---:|:---:|
| 1. Correctness (30) | 30 | 20 | 10 |
| 2. Edge Cases (15) | 15 | 4 | 2 |
| 3. Tests (20) | 20 | 8 | 0 |
| 4. Complexity Analysis (15) | 15 | 4 | 3 |
| 5. Code Quality (10) | 10 | 6 | 4 |
| 6. Reflection (10) | 10 | 5 | 3 |
| **Total (100)** | **100** | **47** | **22** |
