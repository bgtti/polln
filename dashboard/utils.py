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
