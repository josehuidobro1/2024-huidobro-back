from ..config import db


def user_schedule(schedule_data):
    try:
        # Convert the Pydantic model to a dictionary
        schedule_data_dict = schedule_data.dict()

        # Add the document to Firestore
        new_userSchedule_ref = db.collection('Schedule').document()
        new_userSchedule_ref.set(schedule_data_dict)

        return {"message": "Schedule added successfully to user", "id": new_userSchedule_ref.id}
    except Exception as e:
        return {"error adding schedule user_schedule() ": str(e)}


def get_user_schedule(id_user):
    try:
        user_schedule_query = db.collection(
            'Schedule').where('id_user', '==', id_user)
        user_schedule = user_schedule_query.stream()
        schedule_list = []
        for schedule in user_schedule:
            schedule_dict = schedule.to_dict()
            schedule_dict['id'] = schedule.id
            schedule_list.append(schedule_dict)
        return {"message": "List fetched successfully", "schedules": schedule_list}
    except Exception as e:
        return {"error get_user_schedule": str(e)}


def delete_schedule_user(id_user):
    try:
        # Referencia al documento del foodo
        schedule_ref = db.collection(
            'Schedule').where('id_user', '==', id_user)
        schedules = schedule_ref.stream()

        deleted_count = 0
        for schedule in schedules:
            schedule.reference.delete()
            deleted_count += 1

        if deleted_count > 0:
            return {"message": f"Successfully deleted {deleted_count} schedule(s) for user {id_user}"}
        else:
            return {"message": f"No schedules found for user {id_user}"}
    except Exception as e:
        return {"erro delete_schedule_user": str(e)}


def update_schedule_user(id, userschedule_data):
    try:
        updated_data = userschedule_data.dict()
        schedule_ref = db.collection('Schedule').document(id)
        schedule_ref.update(updated_data)

        return {"message": "Schedule updated successfully"}
    except Exception as e:
        return {"error update_schedule_user ": str(e)}
