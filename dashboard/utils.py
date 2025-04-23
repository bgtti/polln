import qrcode
import os
from django.conf import settings

def return_three_digit(number):
    """
    Takes an int and returns a 3-digit string.
    """
    if number < 10:
        new_number = f"00{str(number)}"
    elif number < 100:
        new_number = f"0{str(number)}"
    elif number < 1000:
        new_number = f"{str(number)}"
    else:
        raise ValueError(
            "This app reached 999 users or a user has over 999 projects and needs an upgrade, congratulations. Check how prj_code is handled.")
    return new_number

def create_prj_code(user_id, project_id):
    """
    Takes the user's id and project's id and spits out a 6-digit string.
    """
    code_part_1 = return_three_digit(user_id)
    code_part_2 = return_three_digit(project_id)
    
    return f"{code_part_1}{code_part_2}"


def qr_code_generator(project_code):
    """
    Requires one argument: the project code: prj_code on the Project db model.
    Generates QR code that leads to project' poll url.
    Function based on qrcode library: https://pypi.org/project/qrcode/
    """
    image_name = f"qr_{project_code}.png"
    save_dir = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    save_path = os.path.join(save_dir, image_name)

    # If QR code already exists, skip regeneration
    if os.path.exists(save_path):
        return f"{settings.MEDIA_URL}qr_codes/{image_name}"
    
    os.makedirs(save_dir, exist_ok=True)

    # Build QR code content
    base_url = settings.BASE_URL  # from settings.py / .env
    url = f"{base_url}/poll/{project_code}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(back_color=(255, 255, 255), fill_color=(0, 0, 0))

    try:
        img.save(save_path)
        return f"{settings.MEDIA_URL}qr_codes/{image_name}"
    except Exception as error:
        # print(f"Failed to save QR code image: {error}")
        return None


def delete_qr_code(project_code):
    """
    Requires one argument: the project code: prj_code on the Project db model.
    Deletes the QR code image associated with the given project code.
    To be used when project is deleted.
    """
    image_name = f"qr_{project_code}.png"

    delete_path = os.path.join(settings.MEDIA_ROOT, "qr_codes", image_name)

    try:
        os.remove(delete_path)
        return True
    except OSError as error:
        # print(f"Failed to delete QR code image: {error}")
        return False

def compareTwoStrings(string1, string2):
    """
    Compares the equality of two strings. Returns true if strings are equal and false if they are not.
    """
    normalized_1 = string1.lower().replace(" ", "")
    normalized_2 = string2.lower().replace(" ", "")
    return normalized_1 == normalized_2

