from app.service.notifications_service import delete_noti_service, get_user_notifications, changeNotificationToRead
from fastapi import HTTPException, Request


def getNotis(user_id: str):
    try:
        response = get_user_notifications(user_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def NotificationRead(noti_id: str):
    try:
        response = changeNotificationToRead(noti_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_notification(notification_id: str):
    response = delete_noti_service(notification_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response
