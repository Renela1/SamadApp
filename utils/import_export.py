import openpyxl
from Authentication_Module.models import StudentAccount


def import_data_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        first_name, last_name, password, user_name, nationality, home_number, phone_number, is_staff, father_name, father_number, mother_number, classes_id = row

        StudentAccount.objects.create(first_name=first_name, last_name=last_name, password=nationality,
                                      user_name=user_name, nationality=nationality, home_number=home_number,
                                      phone_number=phone_number, is_staff=is_staff, father_name=father_name,
                                      father_number=father_number, mother_number=mother_number, classes_id=classes_id)

    print("Data imported successfully!")
