import os.path
import sys
import yaml
import base64

from wasteDetection.exception import AppException
from wasteDetection.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info("Read yaml file successfully")
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise AppException(e, sys) from e
    



def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info("Successfully write_yaml_file")

    except Exception as e:
        raise AppException(e, sys)
    



def decodeImage(imgstring, fileName):
    try:
        # Decode Base64 string
        imgdata = base64.b64decode(imgstring)

        # Save the decoded image to the `data` directory
        file_path = os.path.join("./data/", fileName)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(imgdata)
        logging.info(f"Image successfully saved at {file_path}")
    except Exception as e:
        logging.error(f"Error decoding image: {e}")
        raise AppException(e, sys)



def encodeImageIntoBase64(croppedImagePath):
    try:
        if not os.path.exists(croppedImagePath):
            raise FileNotFoundError(f"File not found: {croppedImagePath}")

        with open(croppedImagePath, "rb") as f:
            encoded_image = base64.b64encode(f.read())
            logging.info(f"Image successfully encoded from {croppedImagePath}")
            return encoded_image
    except Exception as e:
        logging.error(f"Error encoding image into Base64: {e}")
        raise AppException(e, sys)


    
    