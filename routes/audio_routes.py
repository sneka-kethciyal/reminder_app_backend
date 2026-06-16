import os

from flask import Blueprint
from flask import jsonify
from flask import send_from_directory

from services.tts_service import create_audio
from services.message_service import get_voice_message
from services.firebase_service import get_reminder

audio_bp = Blueprint(
    "audio",
    __name__
)

AUDIO_FOLDER = "temp_audio"

os.makedirs(
    AUDIO_FOLDER,
    exist_ok=True
)


@audio_bp.route(
    "/generate-audio/<user_id>/<reminder_id>",
    methods=["GET"]
)
def generate_audio(
    user_id,
    reminder_id
):

    reminder = get_reminder(
        user_id,
        reminder_id
    )

    if not reminder:

        return jsonify({
            "success": False,
            "error": "Reminder not found"
        }), 404

    notification_mode = reminder.get(
        "notificationMode",
        "voice"
    )

    if notification_mode == "ringtone":

        return jsonify({
            "success": True,
            "mode": "ringtone",
            "ringtone": reminder.get(
                "notificationSound",
                "alarm"
            )
        })

    title = reminder.get(
        "title",
        "Reminder"
    )

    vm_status = reminder.get(
        "vmStatus",
        "not yet started"
    )

    full_count = reminder.get(
        "fullCount",
        0
    )

    current_count = reminder.get(
        "currentCount",
        0
    )

    balance_count = reminder.get(
        "balanceCount",
        0
    )

    completed_days = reminder.get(
        "completedDays",
        0
    )

    template_code, speech_text = get_voice_message(
        title=title,
        vm_status=vm_status,
        full_count=full_count,
        current_count=current_count,
        balance_count=balance_count,
        completed_days=completed_days
    )

    filename = f"{reminder_id}.mp3"

    filepath = os.path.join(
        AUDIO_FOLDER,
        filename
    )

    create_audio(
        speech_text,
        filepath
    )

    return jsonify({

        "success": True,

        "mode": "voice",

        "template": template_code,

        "vmStatus": vm_status,

        "title": title,

        "fullCount": full_count,

        "currentCount": current_count,

        "balanceCount": balance_count,

        "message": speech_text,

        "audioUrl":
        f"http://localhost:5000/audio/{filename}"
    })


@audio_bp.route(
    "/audio/<filename>",
    methods=["GET"]
)
def get_audio(filename):

    return send_from_directory(
        AUDIO_FOLDER,
        filename
    )