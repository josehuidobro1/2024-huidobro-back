from app.service.review_service import create_review, update_Review, get_plate_reviews, getamountFiveStarReviews
from app.models.review import Review, Update_Review
from app.controllers.plate_controller import get_public_plates
from fastapi import HTTPException
from datetime import datetime


def validate_limit(campo, minimo, maximo, label):
    if not isinstance(campo, (int, float)):
        raise HTTPException(
            status_code=400, detail=f"{label} must be a number")
    if not (minimo <= campo <= maximo):
        raise HTTPException(
            status_code=400, detail=f"{label} must be between {minimo} and {maximo}")


def validate_review(review: Review | Update_Review):
    plates = get_public_plates()
    existing_id = [plate['id'] for plate in plates]
    if review.plate_Id not in existing_id:
        raise HTTPException(
            status_code=400, detail=f"Plate ID is not valid ")

    validate_limit(review.score, 0, 5, "score")

    if review.comments:
        for comment in review.comments:
            validate_limit(comment.score, 0, 5, "score comment")


def reviewLog(review: Review):
    try:
        validate_review(review)
        plate_exist = get_plate_reviews()
        existing_reviews = [rev['plate_Id'] for rev in plate_exist]
        if review.plate_Id in existing_reviews:
            raise HTTPException(
                status_code=400, detail=f"Plate has already reviews ")
        review_id = create_review(review)
        return {"message": "User review registered successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def UpdateReview(review_id: str, updated_data: Update_Review):
    try:
        reviews = get_plate_reviews()
        print(updated_data)
        print(f"\nscore {type(updated_data.score)}\n")
        existing_reviews = [rev['id'] for rev in reviews]
        if review_id not in existing_reviews:
            raise HTTPException(
                status_code=400, detail=f"That review does not exist  ")

        validate_review(updated_data)
        message = update_Review(review_id, updated_data)
        return {"Review": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_plateReviews():
    response = get_plate_reviews()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"Review": response}


def get_fiveStarReview(user_id: str):
    response = getamountFiveStarReviews(user_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
