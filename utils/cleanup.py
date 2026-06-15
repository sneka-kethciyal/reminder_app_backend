import os
import time


def cleanup_audio_files():

    folder = "temp_audio"

    now = time.time()

    for file in os.listdir(folder):

        filepath = os.path.join(
            folder,
            file
        )

        if os.path.isfile(filepath):

            age = (
                now -
                os.path.getmtime(filepath)
            )

            if age > 86400:
                os.remove(filepath)