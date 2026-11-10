import json
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "save_json.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def save_json(data, filename):
    try:
        folder = os.path.dirname(filename)

        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logging.info("JSON file saved successfully: %s", filename)
        print("JSON saved:", filename)

    except (OSError, TypeError, ValueError) as e:
        logging.exception("Error saving JSON file: %s", e)
        print("Error saving JSON:", e)