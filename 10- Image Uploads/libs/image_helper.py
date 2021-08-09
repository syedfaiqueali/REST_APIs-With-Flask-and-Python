import os
import re  # Regex
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # Set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Takes FileStorage and saves it to a folder."""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Takes image name and folder and return full path."""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """Takes filename and either returns an img on any of the accepted format or 'None'."""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take FileStorage and returns the filename.
    Can call this func with both filenames and FileStorage ;returns a filename.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check our regex and returns whether the string matches or not."""
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)  # png|svg|jpe|jpg|jpeg
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"  # [First char][Second char ans so on] .format
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """Return full name of image in the path.
    get_basename('some_folder/img_name.jpg') => 'image.png'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]  # [0] => ..some_folder ;[1] => img_name.jpg


def get_extension():
    """Returns file extension."""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]  # [0] => image_name ;[1] => .png|.jpeg etc
