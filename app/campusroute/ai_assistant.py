"""Intelligent Campus AI Assistant (Rule-based NLP and Intent Engine).

Pure Python standard library. Understands Turkish and English student queries,
resolves intents, checks hours/crowd, and generates contextual routing guidance.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from . import occupancy, opening_hours, routing, schedule, search
from .campus import Campus, Place


def _fold(text: str) -> str:
    """Normalize and fold Turkish/English text for semantic matching."""
    text = (text or "").lower()
    text = text.replace("ı", "i").replace("ğ", "g").replace("ü", "u")
    text = text.replace("ş", "s").replace("ö", "o").replace("ç", "c")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split())


@dataclass
class AssistantResponse:
    reply: str
    intent: str
    route: Optional[Dict[str, Any]] = None
    suggested_places: Optional[List[Dict[str, Any]]] = None
    action: Optional[str] = None


class CampusAIAssistant:
    """Intelligent Natural Language Assistant for CampusRoute."""

    def __init__(self, campus: Campus, sessions=None, reports=None):
        self.campus = campus
        self.sessions = sessions or []
        self.reports = reports or []

    def process(self, query: str, now: Optional[datetime] = None, current_place: str = "gate-main") -> AssistantResponse:
        now = now or datetime.now()
        q_clean = _fold(query)

        # 1. INTENT: Quiet / Study Place (Must come before schedule to distinguish "ders çalış" from "sıradaki ders")
        if any(w in q_clean for w in ["ders calis", "calisacak", "sessiz", "sakin", "quiet", "study"]):
            return self._handle_quiet_study(now, current_place)

        # 2. INTENT: Schedule / Next Class
        if any(w in q_clean for w in ["dersim", "sinav", "class", "lecture", "siradaki", "next", "program", "ders ne zaman"]):
            return self._handle_schedule(q_clean, now, current_place)

        # 3. INTENT: Cafe / Food / Coffee
        if any(w in q_clean for w in ["kafe", "cafe", "kahve", "coffee", "yemek", "aciktim", "food", "kantin", "eat"]):
            return self._handle_food_drink(now, current_place)

        # 4. INTENT: Opening Hours Query ("Kütüphane açık mı?", "Is library open?")
        if any(w in q_clean for w in ["acik mi", "kapali mi", "kaca kadar", "saat", "open", "kapanis", "closed"]):
            place_match = self._find_place_in_text(q_clean)
            if place_match:
                return self._handle_hours_query(place_match, now)

        # 5. INTENT: Route / Directions ("... nasıl giderim", "route to ...")
        if any(w in q_clean for w in ["nasil giderim", "rota", "route", "git", "yol", "how to get", "go to", "yuruyus"]):
            return self._handle_routing_query(q_clean, current_place)

        # 6. Fallback: Search place and route
        place_match = self._find_place_in_text(q_clean)
        if place_match:
            avoid_stairs = any(w in q_clean for w in ["merdivensiz", "engelsiz", "avoid stairs", "stair"])
            return self._route_to_place(current_place, place_match.id, avoid_stairs=avoid_stairs)

        return AssistantResponse(
            reply=(
                "Merhaba! Ben IBM Bob Kampüs Asistanı. Size kampüste rota bulma, açık mekanları listeleme, "
                "sessiz çalışma yerleri önerme veya ders programınızı kontrol etme konularında yardımcı olabilirim.\n\n"
                "💡 **Örnek Sorular:**\n"
                "- *'En yakın açık kafe nerede?'*\n"
                "- *'Kütüphaneye merdivensiz nasıl giderim?'*\n"
                "- *'Sıradaki dersim ne zaman?'*\n"
                "- *'Kütüphane şu an açık mı?'*"
            ),
            intent="greeting",
        )

    def _find_place_in_text(self, text: str) -> Optional[Place]:
        """Detect any campus building or room mentioned in text using stems, aliases, and fuzzy search."""
        q_folded = _fold(text)

        # High-priority stems and keywords
        STEMS = {
            "kutuphan": "lib",
            "library": "lib",
            "muhendis": "eng-b",
            "engineering": "eng-b",
            "eng a": "eng-a",
            "eng b": "eng-b",
            "b204": "eng-b",
            "a101": "eng-a",
            "cafe": "caf",
            "kafe": "caf",
            "cinar": "caf",
            "kantin": "caf",
            "spor": "sport",
            "gym": "sport",
            "havuz": "sport",
            "pool": "sport",
            "yurt": "dorm",
            "dorm": "dorm",
            "saglik": "health",
            "clinic": "health",
            "revir": "health",
            "doktor": "health",
            "fen": "sci",
            "science": "sci",
            "amfi": "inonu",
            "inonu": "inonu",
            "auditorium": "inonu",
            "ana giris": "gate-main",
            "main gate": "gate-main",
            "giris": "gate-main",
            "gate": "gate-main",
            "meydan": "quad",
            "quad": "quad",
        }

        for stem, pid in STEMS.items():
            if stem in q_folded:
                return self.campus.places.get(pid)

        # Check place names and aliases
        for place in self.campus.places.values():
            if _fold(place.name) in q_folded:
                return place
            for alias in place.aliases:
                if _fold(alias) in q_folded:
                    return place

        # Token-based search fallback
        tokens = [t for t in q_folded.split() if len(t) > 2 and t not in ("nasil", "giderim", "acik", "kadar", "olan", "yer")]
        for token in tokens:
            hits = search.search(self.campus, token, limit=1)
            if hits and hits[0].score >= 60:
                pid = hits[0].place_id if hits[0].kind == "room" else hits[0].id
                return self.campus.places.get(pid)

        return None

    def _handle_schedule(self, _text: str, now: datetime, current_place: str) -> AssistantResponse:
        current = schedule.current_session(self.sessions, now)
        upcoming = schedule.next_session(self.sessions, now)

        lines = []
        route_dict = None
        if current:
            lines.append(f"📚 Şu anda devam eden dersiniz: **{schedule.format_session(current)}**.")
        if upcoming:
            sess, when = upcoming
            mins = schedule.minutes_until(now, when)
            room = self.campus.rooms.get(sess.room)
            lines.append(f"⏰ Sıradaki dersiniz: **{schedule.format_session(sess)}** ({mins} dakika sonra).")
            if room:
                place = self.campus.places.get(room.place)
                if place:
                    lines.append(f"📍 Derslik: {place.name} ({room.code}, Kat {room.floor}).")
                    try:
                        r = routing.shortest_route(self.campus, current_place, place.id)
                        route_dict = r.to_dict(self.campus)
                        lines.append(f"🚶‍♂️ Mevcut konumunuzdan yürüme süresi: **{r.minutes} dakika** ({r.meters} m).")
                    except Exception:
                        pass
        else:
            lines.append("Bugün için kayıtlı başka bir dersiniz görünmüyor. Kampüste serbest zamanın tadını çıkarabilirsiniz!")

        return AssistantResponse(reply="\n\n".join(lines), intent="schedule", route=route_dict)

    def _handle_quiet_study(self, now: datetime, current_place: str) -> AssistantResponse:
        study_places = [p for p in self.campus.places.values() if p.kind in ("library", "academic", "other") and p.id != "gate-main"]
        scored = []
        for p in study_places:
            level = occupancy.crowd_level(self.reports, p.id, now) or "moderate"
            is_op = opening_hours.is_open(p.hours, now) if p.hours else True
            score = 100
            if not is_op:
                score -= 80
            if level == "quiet":
                score += 30
            elif level == "packed":
                score -= 40
            scored.append((score, p, level, is_op))

        scored.sort(key=lambda x: -x[0])
        best = scored[0][1]
        best_level = scored[0][2]

        r = routing.shortest_route(self.campus, current_place, best.id)
        reply = (
            f"📖 Ders çalışmak için şu an en uygun yer: **{best.name}**.\n"
            f"- Canlı Yoğunluk: **{best_level.title()}**\n"
            f"- Yürüme Mesafesi: **{r.meters} m** (yaklaşık **{r.minutes} dk**).\n"
            f"Rotanızı haritada işaretledim!"
        )
        return AssistantResponse(reply=reply, intent="study_recommendation", route=r.to_dict(self.campus))

    def _handle_food_drink(self, now: datetime, current_place: str) -> AssistantResponse:
        cafes = [p for p in self.campus.places.values() if "cafe" in p.id or "caf" in p.id or "kafe" in _fold(p.name)]
        if not cafes:
            cafes = [p for p in self.campus.places.values() if p.kind == "services"]

        target = cafes[0]
        is_op = opening_hours.is_open(target.hours, now) if target.hours else True
        r = routing.shortest_route(self.campus, current_place, target.id)

        status_str = "Açık ✨" if is_op else "Şu an kapalı olabilir ⚠️"
        reply = (
            f"☕ Size en yakın dinlenme ve kahve noktası: **{target.name}** ({status_str}).\n"
            f"- Mesafe: **{r.meters} metre** (yaklaşık **{r.minutes} dakika** yürüyüş).\n"
            f"Afiyet olsun! Rota harita üzerinde gösterildi."
        )
        return AssistantResponse(reply=reply, intent="food_recommendation", route=r.to_dict(self.campus))

    def _handle_hours_query(self, place: Place, now: datetime) -> AssistantResponse:
        if not place.hours:
            return AssistantResponse(
                reply=f"ℹ️ **{place.name}** için özel bir çalışma saati kısıtlaması bulunmuyor (genel kampüs saatlerine tabidir).",
                intent="hours_query",
            )
        is_op = opening_hours.is_open(place.hours, now)
        status_txt = "ŞU ANDA AÇIK ✅" if is_op else "ŞU ANDA KAPALI ❌"
        reply = f"🕐 **{place.name}** {status_txt}.\n- Çalışma Saatleri: `{place.hours}`"
        return AssistantResponse(reply=reply, intent="hours_query")

    def _handle_routing_query(self, text: str, current_place: str) -> AssistantResponse:
        avoid_stairs = any(w in text for w in ["merdivensiz", "engelsiz", "avoid stairs", "step free", "sandalye"])
        place = self._find_place_in_text(text)
        if not place:
            return AssistantResponse(
                reply="Gideceğiniz yeri tam anlayamadım. Lütfen bina adını veya oda kodunu belirtin (örneğin: 'Kütüphaneye nasıl giderim?')",
                intent="route_unknown",
            )
        return self._route_to_place(current_place, place.id, avoid_stairs)

    def _route_to_place(self, start_id: str, goal_id: str, avoid_stairs: bool) -> AssistantResponse:
        try:
            r = routing.shortest_route(self.campus, start_id, goal_id, avoid_stairs=avoid_stairs)
            start_name = self.campus.places[start_id].name
            goal_name = self.campus.places[goal_id].name
            stair_note = " (merdivensiz / engelsiz rota)" if avoid_stairs else ""
            reply = (
                f"🗺️ **{start_name} → {goal_name}** rotanız hazırlandı{stair_note}:\n"
                f"- Mesafe: **{r.meters} m**\n"
                f"- Tahmini Süre: **{r.minutes} dakika**\n"
                f"- Kalori: ~{round(r.meters * 0.05)} kcal\n\n"
                f"Yol tarifi adımları harita üzerinde renklendirildi."
            )
            return AssistantResponse(reply=reply, intent="route", route=r.to_dict(self.campus))
        except Exception as err:
            return AssistantResponse(reply=f"Rota hesaplanırken bir hata oluştu: {err}", intent="route_error")
