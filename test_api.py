import requests

ENDPOINT = "https://two024-huidobro-back.onrender.com"


def test_can_call_enpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_user():
    payload = {
        "id_user": "bsdk29hkn",
        "email": "test@example.com",
        "name": "Test",
        "surname": "User",
        "weight": 70,
        "height": 170,
        "birthDate": "2002-02-19T12:39:50.400Z",
        "goals": {
            "calories": 0,
            "sodium": 0,
            "fats": 0,
            "carbohydrates": 0,
            "protein": 0,
            "sugar": 0,
            "caffeine": 0
        },
        "validation": 0,
        "achievements": [],
        "allergies": []
    }
    response = requests.post(ENDPOINT + "/user/", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(data)
