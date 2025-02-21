import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import create_token

client = TestClient(app)


def test_get_user_unauthorized():
    response = client.get("/User/123")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing Authorization Header"}


def test_create_user_invalid_data():
    payload = {
        "id_user": "123",
        "name": "John",
        "surname": "Doe",
        "weight": -5,  # Valor inválido
        "height": 180,
        "birthDate": "2000-01-01T00:00:00",
        "goals": {
            "calories": 2000,
            "sodium": 2300,
            "fats": 70,
            "carbohydrates": 300,
            "protein": 50,
            "sugar": 90,
            "caffeine": 100
        },
        "validation": 1,
        "achievements": [],
        "allergies": []
    }
    headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjBjYmJiZDI2NjNhY2U4OTU4YTFhOTY4ZmZjNDQxN2U4MDEyYmVmYmUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaGVhbHRoeS1iaXRlLWNiNzMyIiwiYXVkIjoiaGVhbHRoeS1iaXRlLWNiNzMyIiwiYXV0aF90aW1lIjoxNzM5OTk2OTg0LCJ1c2VyX2lkIjoicUY5YnhzQjdUOFNxdUQyUXB0Qm5IdzhsamdBMyIsInN1YiI6InFGOWJ4c0I3VDhTcXVEMlFwdEJuSHc4bGpnQTMiLCJpYXQiOjE3Mzk5OTY5ODQsImV4cCI6MTc0MDAwMDU4NCwiZW1haWwiOiJqb3NlZmluYWh1aWRvYnJvMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJqb3NlZmluYWh1aWRvYnJvMUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.3IaC4gtrfWM80scSmEJb0Mm46U8DeH4lEJhiCqwkws7RCZpw-RDkbd7hePFa_p4mFSNJFcNOstpbNwPwXBufdlhgopbWl0k4qQ4Bf5lLKPlMZnqLz8y6OwxlHF6Rk24E4Xiiz1LpVAIiGC80tLv_no8rz41RKRCsZNxqrJ6gLYR2kt4f4nHIedBpry5u2Hn3wHzR86cqKaXIGrSr97IWe9WRkBPITDivAlZFVibO4k3Cm_EV0O_ncKkzcyauX-rgBmrIQk3To4O55sNwI6F7p3SziTmxlwI8Evzdy30N7OpEVsj6Ccgb998zAQv-NEg0kGaw6cG425eHDdWJzhGA0Q"}
    response = client.post("/user/", json=payload, headers=headers)

    assert response.status_code == 422
    assert "weight" in response.json()["detail"][0]["loc"]
