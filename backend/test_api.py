import os
import unittest
from fastapi.testclient import TestClient

import main
from resume.skill_extractor import extract_skills, extract_soft_skills
from resume.job_matcher import analyze_job_match


class TestAPIEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(main.app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("database", data)

    def test_history_endpoint(self):
        response = self.client.get("/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIsInstance(data.get("history"), list)

    def test_job_match_endpoint(self):
        payload = {
            "resume_text": "Experienced Python and SQL developer with Git skills.",
            "job_description": "Seeking Python and Docker engineer."
        }
        response = self.client.post("/job-match", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIn("Python", data.get("resume_skills", []))
        self.assertIn("Python", data.get("matched_skills", []))
        self.assertIn("Docker", data.get("missing_skills", []))

    def test_job_match_validation(self):
        response = self.client.post("/job-match", json={"resume_text": "", "job_description": ""})
        self.assertEqual(response.status_code, 400)

    def test_skill_extractor_logic(self):
        text = "Skilled in Python, React, PostgreSQL, Docker, and Team Collaboration."
        tech_skills = extract_skills(text)
        soft_skills = extract_soft_skills(text)
        self.assertIn("Python", tech_skills)
        self.assertIn("React", tech_skills)
        self.assertIn("PostgreSQL", tech_skills)
        self.assertTrue(len(soft_skills) > 0)


if __name__ == "__main__":
    unittest.main()
