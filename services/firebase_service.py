from firebase_config import db

def get_reminder(user_id, reminder_id):

    doc = (
        db.collection("users")
        .document(user_id)
        .collection("reminders")
        .document(reminder_id)
        .get()
    )

    if doc.exists:
        return doc.to_dict()

    return None