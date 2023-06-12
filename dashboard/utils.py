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
    # base_url = "http://127.0.0.1:8000" # while in local
    base_url = "https://polln.bgtti.dev" # in production
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

    image_name = f"qr_{project_code}.png"

    # Save to static folder: static/dashboard/media
    # save_path = os.path.join(settings.BASE_DIR, "static", "dashboard", "media", image_name) # while in local/development
    save_path = os.path.join(settings.STATIC_ROOT, "dashboard", "media", image_name) # for deployment

    try:
        img.save(save_path)
        return True
    except Exception as error:
        print(f"Failed to save QR code image: {error}")
        return False


def delete_qr_code(project_code):
    """
    Requires one argument: the project code: prj_code on the Project db model.
    Deletes the QR code image associated with the given project code.
    To be used when project is deleted.
    """
    image_name = f"qr_{project_code}.png"

    # Delete from static folder: static/dashboard/media
    # delete_path = os.path.join(
    #     settings.BASE_DIR, "static", "dashboard", "media", image_name) # for production
    
    delete_path = os.path.join(settings.STATIC_ROOT, "dashboard", "media", image_name) # for deployment

    try:
        os.remove(delete_path)
        return True
    except OSError as error:
        print(f"Failed to delete QR code image: {error}")
        return False

def compareTwoStrings(string1, string2):
    """
    Compares the equality of two strings. Returns true if strings are equal and false if they are not.
    """
    string_1 = string1.lower()
    string_1 = string_1.replace(" ", "")
    string_2 = string2.lower()
    string_2 = string_2.replace(" ", "")

    if string_1 == string_2:
        return True
    else:
        return False

