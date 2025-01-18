from ..config import db


def allergies():
    try:
        allergies_ref = db.collection('Allergies')
        allergies = allergies_ref.stream()
        allergies_list = []

        for allergies in allergies:
            allergies_dict = allergies.to_dict()
            allergies_dict['id'] = allergies.id
            allergies_list.append(allergies_dict)

        return {"allergies": allergies_list, "message": "Allergies get successful"}
    except Exception as e:
        return {"error": str(e)}, 500


def post_allergie(allergie):
    try:
        new_allergie_ref = db.collection('Allergies').document()
        new_allergie_ref.set(allergie)
        return {"message": "allergie added successfully", "id": new_allergie_ref.id}
    except Exception as e:
        return {"error": str(e)}


def put_allergie(allergie_id, allergie_data):
    try:
        updated_data = allergie_data.dict()
        allergie_ref = db.collection('Allergies').document(allergie_id)
        print(updated_data)

        allergie_ref.update(updated_data)

        return {"message": "Allergie data updated successfully"}

    except Exception as e:
        print(e)
        return {"error": str(e)}
