from ..config import db
from datetime import datetime, timedelta
from app.service.review_service import getamountFiveStarReviews


def create_plate(plate_data):
    try:
        # Convert the Pydantic model to a dictionary
        plate_data_dict = plate_data.dict()

        # Add the document to Firestore
        new_Plate_ref = db.collection('Plate').document()
        new_Plate_ref.set(plate_data_dict)

        return new_Plate_ref.id
    except Exception as e:
        return {"error": str(e)}


def get_user_plates(id_user):
    try:
        user_Plates_query = db.collection(
            'Plate').where('id_User', '==', id_user)
        user_Plates = user_Plates_query.stream()

        Plate_list = []
        for Plate in user_Plates:
            Plate_dict = Plate.to_dict()
            Plate_dict['id'] = Plate.id
            Plate_list.append(Plate_dict)
        return {"message": "List fetched successfully", "Plates": Plate_list}
    except Exception as e:
        return {"error": str(e)}


def delete_Plate_service(userPlate_id):
    try:
        # Referencia al documento del plateo
        plate_ref = db.collection('Plate').document(userPlate_id)
        plate_ref.delete()
        return {"message": "user  plate  delete successful"}
    except Exception as e:
        return {"error": str(e)}


def update_Plate(userPlate_id, plate_data):
    try:
        updated_data = plate_data.dict()
        Plate_ref = db.collection('Plate').document(userPlate_id)
        Plate_ref.update(updated_data)
        return {"message": "Plate updated successfully"}
    except Exception as e:
        return {"error": str(e)}
        


def getPlateByID(plate_id):
    try:
        # Referencia al documento del plateo
        plate_ref = db.collection('Plate').document(plate_id)
        plate_doc = plate_ref.get()
        return {"plate": plate_doc.to_dict(), "message": "plate get successful"}
    except Exception as e:
        return {"error": str(e)}


def get_public_plates():
    try:
        # Query to get all public plates
        user_Plates_query = db.collection('Plate').where('public', '==', True)
        user_Plates = user_Plates_query.stream()

        Plate_list = []
        for Plate in user_Plates:
            Plate_dict = Plate.to_dict()
            Plate_dict['id'] = Plate.id

            # Replace ingredientId with full ingredient details from Food table
            enriched_ingredients = []
            for ingredient in Plate_dict.get('ingredients', []):
                food_doc = db.collection('Food').document(
                    ingredient['ingredientId']).get()
                if food_doc.exists:
                    food_data = food_doc.to_dict()
                    ingredient.update({
                        "name": food_data.get("name"),
                        "calories_portion": food_data.get("calories_portion"),
                        "sodium_portion": food_data.get("sodium_portion"),
                        "fats_portion": food_data.get("fats_portion"),
                        "carbohydrates_portion": food_data.get("carbohydrates_portion"),
                        "protein_portion": food_data.get("protein_portion"),
                        "measure": food_data.get("measure"),
                        "measure_portion": food_data.get("measure_portion")
                    })
                enriched_ingredients.append(ingredient)
            Plate_dict['ingredients'] = enriched_ingredients

            # Add reviews for the current plate
            reviews_query = db.collection('Review').where(
                'plate_Id', '==', Plate_dict['id'])
            reviews = reviews_query.stream()
            Plate_dict['reviews'] = [
                {"id": review.id, **review.to_dict()} for review in reviews]

            Plate_list.append(Plate_dict)

        return Plate_list
    except Exception as e:
        return {"error": str(e)}
def update_user_platestoverified(user_id):
    try:
        plates = get_user_plates(user_id)["Plates"]
        count_4_star_plates = getamountFiveStarReviews(user_id)
        level = 0
        if count_4_star_plates >= 5:
            level = 2
        elif count_4_star_plates >= 3:
            level = 1
        else:
            level = 0

        for plate in plates:
            if plate['verified'] != level:
                plate['verified'] = level

            Plate_ref = db.collection('Plate').document(plate["id"])
            Plate_ref.update(plate)

        return "Plate validation updated successfully"

    except Exception as e:
        return {"error": str(e)}
def get_public_plates_notUser(user_id):
    try:
        # Query to get all public plates
        user_Plates_query = db.collection('Plate').where('public', '==', True)
        user_Plates = user_Plates_query.stream()

        Plate_list = []
        for Plate in user_Plates:
            Plate_dict = Plate.to_dict()
            
            # Check if the plate does not belong to the provided user_id
            if Plate_dict.get('id_User') != user_id:
                Plate_dict['id'] = Plate.id
                Plate_list.append(Plate_dict)
                
        return Plate_list
    
    except Exception as e:
        return {"error": str(e)}




