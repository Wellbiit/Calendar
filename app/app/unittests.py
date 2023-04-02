import unittest
import requests


class TestCalendarAPI(unittest.TestCase):
    global token

    def setUp(self) -> None:
        self.url = "http://127.0.0.1:5000"
        self.headers = {"Content-type": "Application/json"}
        self.login_data = {
            "nickname": "test_nickname",
            "password": "test_pwd",
            "email": "email@ema.com"
        }

    def test1_signup(self):
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isRegistered"])

    def test2_signup_with_same_data(self):
        response = requests.post(f"{self.url}/signup", json=self.login_data, headers=self.headers)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["isRegistered"], False)
        self.assertEqual(response.json()["reason"], "userExists")

    def test3_login_with_correct_data(self):
        global token
        response = requests.post(f"{self.url}/login", json=self.login_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.json())
        self.assertTrue(response.json()["isLogged"])

        token = response.json()["token"]

    def test4_delete_created_user(self):
        response = requests.get(f"{self.url}/delete_user_by/{self.login_data['nickname']}", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isDeleted"])


if __name__ == "__main__":
    unittest.main()


