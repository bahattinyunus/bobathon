import unittest
from datetime import datetime

from campusroute.ai_assistant import CampusAIAssistant
from campusroute.campus import load_campus
from campusroute.schedule import parse_schedule

SAMPLE_SCHEDULE = """\
day,start,end,course,room
Mon,09:00,10:50,CS201,eng-b204
Mon,13:00,14:50,MATH203,SCI-202
Wed,09:00,10:50,CS201,ENG-B204
""".splitlines()


class AssistantTest(unittest.TestCase):
    def setUp(self):
        self.campus = load_campus()
        self.sessions = parse_schedule(SAMPLE_SCHEDULE)
        self.assistant = CampusAIAssistant(self.campus, self.sessions, [])

    def test_greeting(self):
        res = self.assistant.process("merhaba")
        self.assertEqual(res.intent, "greeting")
        self.assertIn("IBM Bob", res.reply)

    def test_schedule_query(self):
        # 1 March 2027 is a Monday at 12:00
        now = datetime(2027, 3, 1, 12, 0)
        res = self.assistant.process("sıradaki dersim ne zaman?", now=now)
        self.assertEqual(res.intent, "schedule")
        self.assertIn("MATH203", res.reply)
        self.assertIsNotNone(res.route)

    def test_food_query(self):
        res = self.assistant.process("bana bir kafe bul acıktım")
        self.assertEqual(res.intent, "food_recommendation")
        self.assertIn("Çınar Café", res.reply)
        self.assertIsNotNone(res.route)

    def test_quiet_study_query(self):
        res = self.assistant.process("sessizce ders çalışacak bir yer öner")
        self.assertEqual(res.intent, "study_recommendation")
        self.assertIsNotNone(res.route)

    def test_hours_query(self):
        # Monday noon -> library is open
        now = datetime(2027, 3, 1, 12, 0)
        res = self.assistant.process("kütüphane açık mı?", now=now)
        self.assertEqual(res.intent, "hours_query")
        self.assertIn("AÇIK", res.reply)

    def test_route_query_avoid_stairs(self):
        res = self.assistant.process("mühendisliğe merdivensiz nasıl giderim?")
        self.assertEqual(res.intent, "route")
        self.assertFalse(res.route["has_stairs"])


if __name__ == "__main__":
    unittest.main()
