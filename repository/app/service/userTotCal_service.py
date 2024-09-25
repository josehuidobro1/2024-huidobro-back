from ..config import db

def createUserTotCal_service(userTotCal):
    
    try:
        totCal_data_dict = userTotCal.dict()
        new_totCal = db.collection('UserTotalCal').document()
        new_totCal.set(totCal_data_dict)
        return {"message": "New Total added successfully", "id": new_totCal.id}
    except Exception as e:
        return {"error": str(e)}

def updateDailyCalories(calPerDay_id, calUpdate):
    usertotCal_ref = db.collection('UserTotalCal').document(calPerDay_id)
    try:
        # Update only the totCal field
        usertotCal_ref.update({
            'totCal': calUpdate
        })
        print(f"Updated total calories to {calUpdate} for document {calPerDay_id}")
        return {"message": f"Updated total calories to {calUpdate}."}
    except Exception as e:
        # Catch and return the error in a structured format
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_totalCAL(user_id):
    try:
        user_TotCal_query = db.collection(
            'UserTotalCal').where('id_user', '==', user_id)
        user_totCal = user_TotCal_query.stream()
        
        totCal_list = []
        for totCal in user_totCal:
            totCal_dict = totCal.to_dict()
            print(totCal_dict)
            totCal_dict['id'] = totCal.id
            totCal_list.append(totCal_dict)
        sorted_totCal_list = sorted(totCal_list, key=lambda x: x['day'])
        return {"message": "List fetched successfully", "totCals": totCal_list}
    except Exception as e:
        return {"error": str(e)}

    


