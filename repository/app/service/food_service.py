from ..config import db

def create_food(food_data):
    try:
        new_food_ref = db.collection('Food').document()
        new_food_ref.set(food_data)
        return {"message": "food added successfully", "id": new_food_ref.id}
    except Exception as e:
        return {"error": str(e)}
def foods():
    try:
        food_ref = db.collection('Food')
        food = food_ref.stream()
        food_list = []

        for food in food:
            food_dict = food.to_dict()
            food_dict['id'] = food.id
            food_list.append(food_dict)
            
        return {"food": food_list, "message": "food get successful"}
    except Exception as e:
        return {"error": str(e)}, 500
def food_by_id(food_id):
    try:
        # Referencia al documento del foodo
        food_ref = db.collection('Food').document(food_id)
        food_doc =food_ref.get()
        return {"food": food_doc.to_dict(), "message": "food get successful"}
    except Exception as e:
        return {"error": str(e)}