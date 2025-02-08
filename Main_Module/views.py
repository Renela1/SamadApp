from datetime import timedelta
from statistics import mean
import jalali_date
from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from .form import *
from .model import *
from .signals import *
from Authentication_Module.models import *
import math
from django.db import transaction

print('this is git commited')

# |--------------------------------------------------|#
# |-NOTE: STUDENT AND GRADES RELATED FORMS AND VIEWS-|#
# |--------------------------------------------------|#

abslout_date = jalali_date.date2jalali(datetime.date.today()).strftime('%Y-%m-%d')
date = jalali_date.date2jalali(datetime.date.today())
month_filter = date.month


def index(request):
    with transaction.atomic():  # Ensure the operation is atomic
        grades = Grades.objects.all()
        final_grades = FinalGrades.objects.all()
        students = StudentAccount.objects.all()

        for grade in final_grades:
            if grade.archived != True:
                grade.archived = True
                grade.save()

        for grade in grades:
            if grade.archived != True:
                grade.archived = True
                grade.save()

        for student in students:
            current_class = student.classes
            current_base = current_class.base

            # Ensure the current base is a number and can be incremented
            try:
                current_base_number = int(current_base.base_grade)
            except ValueError:
                print(f"Invalid base for class {current_class.class_name}: {current_base.base_grade}")
                continue

            # Calculate the next base number
            if current_base_number != 12 and student.allowed_to_promoted == True:
                next_base_number = current_base_number + 1
                print(current_base_number)

                # Check if the next base already exists, or create it
                next_base, created = Base.objects.get_or_create(base_grade=str(next_base_number))

                # Ensure no duplicate class records are created
                next_class_name = current_class.class_name
                next_class, _ = Classes.objects.get_or_create(class_name=next_class_name, base=next_base)

                # Update the student's class to the new class
                student.classes = next_class
                student.save()

                if created:
                    print(f"Created new base")

            elif current_base_number == 12 and student.status == False and student.allowed_to_promoted == True:
                student.graduate = True
                student.save()

            elif current_base_number == 12 and student.status == True:
                student.graduate = False
                student.save()

            elif current_base_number >= 12 and student.status == True:
                student.classes = student.classes

    context = {'classes': students}
    return render(request, "main/main.html", context)


# viewing lists of courses and subjects and editing them


def courses_view(request, slug, slug2, slug3):
    report = Grades.objects.filter(subject=slug, classes=slug2, date=slug3)

    context = {'report': report}
    return render(request, 'main/table.html', context)


@check_role_teacher
def courses_date(request, slug, slug2):
    report = Grades.objects.filter(subject=slug, classes=slug2)

    context = {'report': report}
    return render(request, 'main/course_date.html', context)


# list of courses every teacher has

@check_role_teacher
def courses(request, slug):
    report = ClCourses.objects.filter(student=request.user.id, slug=slug)
    report_a = ClCourses.objects.filter(student=request.user.id, slug=slug)
    a = 'A'
    b = 'B'
    c = 'C'
    classes = f'/attendance/{slug}/{abslout_date}'
    print(report)
    context = {'report': report, 'classes': classes, 'report_a': report_a, 'a': a, 'b': b, 'c': c, 'date': abslout_date}
    return render(request, 'main/courses.html', context)


def all_courses(request, slug):
    course = Course.objects.all()
    classes = Classes.objects.get(slug=slug)
    detail = BaseFields.objects.filter(id=request.user.id).first()
    class_id = classes.id
    context = {
        'course': course, 'slug': class_id, 'detail': detail,
    }
    return render(request, 'main/all_courses.html', context)


# function for each student to view thrier report card

def report_card(request, month):
    dates = datetime.date.today().month

    date = jalali_date.date2jalali(datetime.date.today()).month
    months = str(month)

    detail = StudentAccount.objects.get(id=request.user.id)
    student_a = Grades.objects.filter(student=request.user, time__icontains=f'-{months}-').order_by('date')

    detail.status = False
    detail.save()

    grades = Grades.objects.filter(student_id=detail.id, time__icontains=f'-{months}-').order_by('id')

    month_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    jalali_months = ['دی', 'بهمن', 'فروردین', 'اسفند', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان',
                     'آذر', 'دی']

    current_month = jalali_months[int(month)]

    group = Group.objects.get(name='staff')

    unique_dates_a = list(student_a.values_list('date', flat=True).distinct())

    grades_by_subject_a = {}
    averages_by_subject_a = {}
    grades_by_subject_b = {}

    for grade in student_a:
        subject = grade.subject

        if subject not in grades_by_subject_a:
            grades_by_subject_a[subject] = {date: None for date in unique_dates_a}
            grades_by_subject_b[subject] = {date: None for date in unique_dates_a}

        if grade.grade_type == 'A':

            if grade.grades_100 >= 1.0:
                grades_by_subject_a[subject][grade.date] = (f'{grade.grades_100 / 5} | {grade.grades_20 / 5}')
                grades_by_subject_b[subject][grade.date] = ((grade.grades_100 * (75 / 100)) / 5) + (
                        (grade.grades_20 * (25 / 100)) / 5)

            elif grade.grades_100 <= 1.0:
                grades_by_subject_a[subject][grade.date] = (f'{grade.grades_20}')
                grades_by_subject_b[subject][grade.date] = (grade.grades_20)

            elif grade.grades_20 <= 1.0:
                grades_by_subject_a[subject][grade.date] = (f'{grade.grades_100}')
                grades_by_subject_b[subject][grade.date] = (grade.grades_100)

        elif grade.grade_type == 'B':

            grades_by_subject_a[subject][grade.date] = (f'{(grade.grades_100 * 5) + (grade.grades_20)}')
            grades_by_subject_b[subject][grade.date] = (grade.grades_100 * 5) + (grade.grades_20)

        elif grade.grade_type == 'C':

            grades_by_subject_a[subject][grade.date] = grade.grades_20
            grades_by_subject_b[subject][grade.date] = grade.grades_20

    total_sum = 0
    total_count = 0
    for subject, grades_dict in grades_by_subject_b.items():

        all_grades = [grade for grade in grades_dict.values() if grade is not None]
        # Get all non-None grades
        for subject, grades_dict in grades_by_subject_b.items():

            all_grades = [grade for grade in grades_dict.values() if grade is not None]  # Filter None values
            if all_grades:
                average = mean(all_grades)
                rounded_average = get_up_to_nearest_25(average)  # Round to nearest 0.25
                threshold = 10 if subject.grade_type == 'C' else 14 or 12 if subject.grade_type == "B" else 14
                passed = rounded_average >= threshold
                averages_by_subject_a[subject] = {
                    'average': rounded_average,
                    'status': 'پاس شده' if passed else 'مردود',

                }

                Grades.objects.filter(subject=subject, student=request.user).update(passed=passed)

                if passed == False:
                    detail.status = True
                    detail.save()

                total_sum += rounded_average
                total_count += 1

    total_average = total_sum / total_count if total_count > 0 else 0
    print(f' avg : {total_average}')
    rounded_total_average = get_up_to_nearest_25(total_average)
    table_rows_a = []
    for subject, grades_dict in grades_by_subject_a.items():
        row = [subject]  # Start the row with the subject name
        for date in unique_dates_a:
            row.append(grades_dict.get(date))  # Add grade or None for each date
        try:
            row.append(averages_by_subject_a[subject]['average'])
            row.append(averages_by_subject_a[subject]['status'])

        except:
            row.append('-')

        table_rows_a.append(row)

    data = []

    for grade in grades:
        if grade.grades_20 != None and grade.grades_100 != None:
            data.append({
                'subject': grade.subject.subject,
                'date': grade.date.strftime('%Y-%m-%d'),
                'grades': get_up_to_nearest_25(((grade.grades_100 * (75 / 100)) / 5) + ((grade.grades_20 * (
                        25 / 100)) / 5)) if grade.subject.grade_type == 'A' else get_up_to_nearest_25(
                    grade.grades_20) and (grade.grades_100 * 5) + (
                                                                                     grade.grades_20) if grade.subject.grade_type == "B" else grade.grades_20,

            })
        if grade is float:
            print(((grade.grades_100 * 5) + (grade.grades_20)))
        else:
            print(0)
    context = {'student_a': student_a, 'group': group, 'rounded_total_average':rounded_total_average,
               'detail': detail, 'unique_dates_a': unique_dates_a,
               'current_month': current_month, 'month_count': month_count, 'table_rows': table_rows_a,
               'grades': data}

    return render(request, 'main/reportcard.html', context)


def student_progress_view(request, curse_name):
    student = StudentAccount.objects.filter(id=request.user.id).first()
    detail = StudentAccount.objects.filter(id=request.user.id).first()
    report = Grades.objects.filter(student_id=student.id, subject__subject=curse_name).order_by('date')
    grades = Grades.objects.filter(student_id=student.id, subject__subject=curse_name).order_by('id')

    data = []

    for grade in grades:
        print(grade.grades_20)
        if grade.grades_20 != None and grade.grades_100 != None:
            data.append({
                'subject': grade.subject.subject,
                'date': grade.date.strftime('%Y-%m-%d'),
                'grades': get_up_to_nearest_25(((grade.grades_100 * (75 / 100)) / 5) + ((grade.grades_20 * (
                        25 / 100)) / 5)) if grade.subject.grade_type == 'A' else get_up_to_nearest_25(
                    grade.grades_20) and (grade.grades_100 * 5) + (
                                                                                     grade.grades_20) if grade.subject.grade_type == "B" else grade.grades_20,

            })

        else:
            print(0)
    unique_dates = list(report.values_list('date', flat=True).distinct())

    # Organize grades by subject and date
    grades_by_subject = {}

    for grade in report:
        subject = grade.subject
        if subject not in grades_by_subject:
            grades_by_subject[subject] = {date: None for date in unique_dates}  # Initialize all dates as None
        grades_by_subject[subject][grade.date] = get_up_to_nearest_25(((grade.grades_100 *
                                                                        (75 / 100)) / 5) + ((grade.grades_20 *
                                                                                             (
                                                                                                     25 / 100)) / 5)) if grade.subject.grade_type == 'A' else get_up_to_nearest_25(
            grade.grades_20) and get_up_to_nearest_25(
            (grade.grades_100 * 5) + (grade.grades_20)) if grade.subject.grade_type == "B" else grade.grades_20

    table_rows = []

    for subject, grades_dict in grades_by_subject.items():
        row = [subject]  # Start the row with the subject name
        for date in unique_dates:
            row.append(grades_dict.get(date))  # Add grade or None for each date
        table_rows.append(row)

    context = {'report': report, 'detail': detail, 'table_rows': table_rows,
               'unique_dates': unique_dates, 'grades_by_subject': grades_by_subject, 'grades': data, 'student': student}

    return render(request, 'main/student_progress.html', context)


def student_progress(request, slug, curse_name):
    student = StudentAccount.objects.filter(id=slug).first()
    detail = StudentAccount.objects.filter(id=slug).first()
    report = Grades.objects.filter(student_id=student.id, subject__subject=curse_name).order_by('date')
    grades = Grades.objects.filter(student_id=student.id, subject__subject=curse_name).order_by('id')

    data = []

    for grade in grades:
        data.append({
            'subject': grade.subject.subject,
            'date': jalali_date.date2jalali(grade.date).strftime('%Y-%m-%d'),
            'grades': get_up_to_nearest_25(((grade.grades_100 * (75 / 100)) / 5) + ((grade.grades_20 * (
                    25 / 100)) / 5)) if grade.subject.grade_type == 'A' else get_up_to_nearest_25(
                grade.grades_20) and (grade.grades_100 * 5) + (
                                                                                 grade.grades_20) if grade.subject.grade_type == "B" else grade.grades_20,

        })
        print(((grade.grades_100 * 5) + (grade.grades_20)))

    unique_dates = list(report.values_list('date', flat=True).distinct())

    # Organize grades by subject and date
    grades_by_subject = {}

    for grade in report:
        subject = grade.subject
        if subject not in grades_by_subject:
            grades_by_subject[subject] = {date: None for date in unique_dates}  # Initialize all dates as None
        grades_by_subject[subject][grade.date] = get_up_to_nearest_25(((grade.grades_100 *
                                                                        (75 / 100)) / 5) + ((grade.grades_20 *
                                                                                             (
                                                                                                     25 / 100)) / 5)) if grade.subject.grade_type == 'A' else get_up_to_nearest_25(
            grade.grades_20) and get_up_to_nearest_25(
            (grade.grades_100 * 5) + (grade.grades_20)) if grade.subject.grade_type == "B" else grade.grades_20

    table_rows = []

    for subject, grades_dict in grades_by_subject.items():
        row = [subject]  # Start the row with the subject name
        for date in unique_dates:
            row.append(grades_dict.get(date))  # Add grade or None for each date
        table_rows.append(row)

    context = {'report': report, 'detail': detail, 'table_rows': table_rows,
               'unique_dates': unique_dates, 'grades_by_subject': grades_by_subject, 'grades': data, 'student': student}

    return render(request, 'main/detail_progress.html', context)


# students list

@check_role_staff
def class_list(request):
    lists = Classes.objects.all()

    context = {'lists': lists, 'date': abslout_date}
    return render(request, 'main/list.html', context)


# ask mani what the hell this is

class ReportTemplateView(TemplateView):
    template_name = 'main/students.html'

    def get_context_data(self, slug, *args, **kwargs):
        abslout_date = jalali_date.date2jalali(datetime.date.today()).strftime('%Y-%m-%d')
        date = jalali_date.date2jalali(datetime.date.today())
        month_filter = date.month
        date_month = datetime.date.today().month
        context = super().get_context_data(**kwargs)
        context['users'] = StudentAccount.objects.filter(classes=slug)
        context['month'] = int(date_month)
        context['month_filter'] = month_filter

        return context


# viewing each student'sreport card

def get_up_to_nearest_25(number):
    return math.ceil(number * 4) / 4


def student_view(request, slug, month):
    dates = datetime.date.today().month

    date = jalali_date.date2jalali(datetime.date.today()).month
    months = str(month)

    detail = StudentAccount.objects.get(id=slug)
    student_a = Grades.objects.filter(student=slug, time__icontains=f'-{months}-').order_by('date')
  
    detail.status = False
    detail.save()

    month_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    jalali_months = ['دی', 'بهمن', 'فروردین', 'اسفند', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان',
                     'آذر', 'دی']

    current_month = jalali_months[int(month)]

    group = Group.objects.get(name='staff')

    unique_dates_a = list(student_a.values_list('date', flat=True).distinct())

    grades_by_subject_a = {}
    averages_by_subject_a = {}
    grades_by_subject_b = {}

    for grade in student_a:
        subject = grade.subject

        if subject not in grades_by_subject_a:
            grades_by_subject_a[subject] = {date: None for date in unique_dates_a}
            grades_by_subject_b[subject] = {date: None for date in unique_dates_a}

        if grade.grade_type == 'A':

            if grade.grades_100 >= 1.0:
                grades_by_subject_a[subject][grade.date] = (f'{grade.grades_100 / 5} | {grade.grades_20 / 5}')
                grades_by_subject_b[subject][grade.date] = ((grade.grades_100 * (75 / 100)) / 5) + (
                        (grade.grades_20 * (25 / 100)) / 5)

            elif grade.grades_100 <= 1.0:
                grades_by_subject_a[subject][grade.date] = (f'{grade.grades_20}')
                grades_by_subject_b[subject][grade.date] = (grade.grades_20)

        elif grade.grade_type == 'B':

            grades_by_subject_a[subject][grade.date] = (f'{((grade.grades_100 * 5) + (grade.grades_20))}')
            grades_by_subject_b[subject][grade.date] = ((grade.grades_100 * 5) + (grade.grades_20))

        elif grade.grade_type == 'C':

            grades_by_subject_a[subject][grade.date] = grade.grades_20
            grades_by_subject_b[subject][grade.date] = grade.grades_20

    total_sum = 0
    total_count = 0
    for subject, grades_dict in grades_by_subject_b.items():

        all_grades = [grade for grade in grades_dict.values() if grade is not None]
        # Get all non-None grades
        for subject, grades_dict in grades_by_subject_b.items():

            all_grades = [grade for grade in grades_dict.values() if grade is not None]  # Filter None values
            if all_grades:
                average = mean(all_grades) if not None else 0
                rounded_average = get_up_to_nearest_25(average)  # Round to nearest 0.25
                threshold = 10 if subject.grade_type == 'C' else 14 and 12 if subject.grade_type == "B" else 14
                passed = rounded_average >= threshold
                averages_by_subject_a[subject] = {
                    'average': rounded_average if not None else '-',
                    'status': 'پاس شده' if passed else 'مردود',

                }

                Grades.objects.filter(subject=subject, student=slug).update(passed=passed)

                if passed == False:
                    detail.status = True
                    detail.save()

                total_sum += rounded_average
                total_count += 1

    total_average = total_sum / total_count if total_count > 0 else 0
    print(f' avg : {total_average}')
    rounded_total_average = get_up_to_nearest_25(total_average)

    grades = Grades.objects.filter(student_id=detail.id, time__icontains=f'-{months}-').order_by('id')

    data = []

    for grade in grades:
        if grade.grades_20 != None and grade.grades_100 != None:
            data.append({
                'subject': grade.subject.subject,
                'date': grade.date.strftime('%Y-%m-%d'),
                'grades': get_up_to_nearest_25(((grade.grades_100 * (75 / 100)) / 5) + ((grade.grades_20 * (
                        25 / 100)) / 5)) if grade.subject.grade_type == 'A' else get_up_to_nearest_25(
                    grade.grades_20) and (grade.grades_100 * 5) + (
                                                                                     grade.grades_20) if grade.subject.grade_type == "B" else grade.grades_20,

            })
        if grade is float:
            print(((grade.grades_100 * 5) + (grade.grades_20)))
        else:
            print(0)

    table_rows_a = []
    table_average = []
    for subject, grades_dict in grades_by_subject_a.items():
        row = [subject]  # Start the row with the subject name
        for date in unique_dates_a:
            row.append(grades_dict.get(date))  # Add grade or None for each date

        try:
            row.append(averages_by_subject_a[subject]['average'])
            row.append(averages_by_subject_a[subject]['status'])

        except:
            row.append('-')

        table_rows_a.append(row)

    context = {'student_a': student_a, 'group': group, 'rounded_total_average': rounded_total_average,
               'detail': detail, 'unique_dates_a': unique_dates_a, 'table_average': table_average,
               'current_month': current_month, 'month_count': month_count, 'table_rows_a': table_rows_a,
               'grades':data}

    return render(request, 'main/students_detail.html', context)




def student_final(request, slug, turn):
    turn = int(turn)
    detail = StudentAccount.objects.get(id=slug)
    detail.status = False
    detail.save()
    student_a = FinalGrades.objects.filter(student=slug, turn=turn).order_by('date')

    group = Group.objects.get(name='staff')

    unique_dates_a = list(student_a.values_list('date', flat=True).distinct())

    grades_by_subject = {}
    grades_by_subject_a = {}
    averages_by_subject_a = {}
    grades_by_subject_b = {}

    for grade in student_a:
        subject = grade.subject

        if subject not in grades_by_subject_a:
            grades_by_subject[subject] = {date: None for date in unique_dates_a}
            grades_by_subject_a[subject] = {date: None for date in unique_dates_a}
            grades_by_subject_b[subject] = {date: None for date in unique_dates_a}

        if grade.grade_type == 'A':

            avg = ((grade.grades_amali * (75 / 100)) / 5) + ((grade.grades_theory * (25 / 100)) / 5)
            grades_by_subject[subject] = grade.overal_grade
            grades_by_subject_a[subject] = (f'{grade.grades_amali} || {grade.grades_theory}')
            grades_by_subject_b[subject][grade.date] = (avg + grade.overal_grade) / 2


        elif grade.grade_type == 'B':
            avg2 = ((grade.grades_amali * 5) + (grade.grades_theory))
            grades_by_subject[subject] = grade.overal_grade
            grades_by_subject_a[subject] = ((grade.grades_amali * 5) + (grade.grades_theory))
            grades_by_subject_b[subject][grade.date] = (avg2 + grade.overal_grade) / 2

        elif grade.grade_type == 'C':

            grades_by_subject[subject] = grade.overal_grade
            grades_by_subject_a[subject] = grade.grades_theory
            grades_by_subject_b[subject][grade.date] = (grade.overal_grade + grade.grades_theory) / 2

    total_sum = 0
    total_count = 0
    for subject, grades_dict in grades_by_subject_b.items():

        all_grades = [grade for grade in grades_dict.values() if grade is not None]
        # Get all non-None grades
        for subject, grades_dict in grades_by_subject_b.items():

            all_grades = [grade for grade in grades_dict.values() if grade is not None]  # Filter None values
            if all_grades:

                average = mean(all_grades)
                rounded_average = get_up_to_nearest_25(average)  # Round to nearest 0.25
                threshold = 10 if subject.grade_type == 'C' else 14 and 12 if subject.grade_type == "B" else 14
                passed = rounded_average >= threshold

                averages_by_subject_a[subject] = {
                    'average': rounded_average,
                    'status': 'پاس شده' if passed else 'مردود',

                }

                FinalGrades.objects.filter(subject=subject, student=slug, turn=turn).update(passed=passed)
                print(rounded_average)

                if passed == False:
                    detail.status = True
                    detail.save()

                total_sum += rounded_average
                total_count += 1

    total_average = total_sum / total_count if total_count > 0 else 0
    print(f' avg : {total_average}')
    rounded_total_average = get_up_to_nearest_25(total_average)

    table_rows_a = []
    for subject, grades_dict in grades_by_subject_a.items():
        row = [subject]  # Start the row with the subject name
        row.append(grades_dict)

        row.append(grades_by_subject[subject])
        print('false') if grades_by_subject[subject] >= 10 else print(grades_by_subject[subject])

        try:
            row.append(averages_by_subject_a[subject]['average'])
            row.append(averages_by_subject_a[subject]['status'])

        except:
            row.append('-')

        table_rows_a.append(row)

    context = {'student_a': student_a, 'group': group, 'averages_by_subject_a': averages_by_subject_a,
               'detail': detail, 'unique_dates_a': unique_dates_a, 'grades_by_subject_b': grades_by_subject_b,
               'table_rows_a': table_rows_a, 'rounded_total_average': rounded_total_average, 'turn':turn}

    return render(request, 'main/students_final.html', context)


def report_final(request, turn):
    turn = int(turn)
    detail = StudentAccount.objects.get(id=request.user.id)
    student_a = FinalGrades.objects.filter(student=request.user, turn=turn).order_by('date')

    group = Group.objects.get(name='staff')

    unique_dates_a = list(student_a.values_list('date', flat=True).distinct())

    grades_by_subject = {}
    grades_by_subject_a = {}
    averages_by_subject_a = {}
    grades_by_subject_b = {}

    for grade in student_a:
        subject = grade.subject

        if subject not in grades_by_subject_a:
            grades_by_subject[subject] = {date: None for date in unique_dates_a}
            grades_by_subject_a[subject] = {date: None for date in unique_dates_a}
            grades_by_subject_b[subject] = {date: None for date in unique_dates_a}

        if grade.grade_type == 'A':

            avg = ((grade.grades_amali * (75 / 100)) / 5) + ((grade.grades_theory * (25 / 100)) / 5)
            grades_by_subject[subject] = grade.overal_grade
            grades_by_subject_a[subject] = (f'{grade.grades_amali} || {grade.grades_theory}')
            grades_by_subject_b[subject][grade.date] = (avg + grade.overal_grade) / 2


        elif grade.grade_type == 'B':
            grades_by_subject[subject] = grade.overal_grade
            grades_by_subject_a[subject] = (grade.grades_amali * 5) + (grade.grades_theory)
            grades_by_subject_b[subject][grade.date] = (grade.grades_amali * 5) + (grade.grades_theory)

        elif grade.grade_type == 'C':

            grades_by_subject[subject] = grade.overal_grade
            grades_by_subject_a[subject] = grade.grades_theory
            grades_by_subject_b[subject][grade.date] = (grade.overal_grade + grade.grades_theory) / 2

    total_sum = 0
    total_count = 0
    for subject, grades_dict in grades_by_subject_b.items():

        all_grades = [grade for grade in grades_dict.values() if grade is not None]
        # Get all non-None grades
        for subject, grades_dict in grades_by_subject_b.items():

            all_grades = [grade for grade in grades_dict.values() if grade is not None]  # Filter None values
            if all_grades:
                average = mean(all_grades)
                rounded_average = get_up_to_nearest_25(average)  # Round to nearest 0.25
                threshold = 10 if subject.grade_type == 'C' else 14 or 12 if subject.grade_type == "B" else 14
                passed = rounded_average >= threshold
                averages_by_subject_a[subject] = {
                    'average': rounded_average,
                    'status': 'پاس شده' if passed else 'مردود',

                }

                FinalGrades.objects.filter(subject=subject, student=request.user, turn=turn).update(passed=passed)

                if passed == False:
                    detail.status = True
                    detail.save()

                total_sum += rounded_average
                total_count += 1

    total_average = total_sum / total_count if total_count > 0 else 0
    print(f' avg : {total_average}')
    rounded_total_average = get_up_to_nearest_25(total_average)

    table_rows_a = []
    for subject, grades_dict in grades_by_subject_a.items():
        row = [subject]  # Start the row with the subject name

        row.append(grades_by_subject_a[subject])
        row.append(grades_by_subject[subject])
        try:
            row.append(averages_by_subject_a[subject]['average'])  # Add rounded average
            row.append(averages_by_subject_a[subject]['status'])
        except:
            row.append('-')

        table_rows_a.append(row)

    context = {'student_a': student_a, 'group': group,
               'detail': detail, 'unique_dates_a': unique_dates_a,
               'table_rows': table_rows_a, 'turn':turn,
               'rounded_total_average':rounded_total_average}

    return render(request, 'main/final_report.html', context)


# form for setting the status of individual students

def attendance_check(request, slug, date):
    try:
        if date != abslout_date:
            print('wr0ng')
            return redirect(f'/attendance/{slug}/{abslout_date}')
    except:
        return redirect(f'/attendance/{slug}/{abslout_date}')

    todos = Attendance.objects.filter(slug=slug, completion_date=date)
    staff = Group.objects.get(name='staff')

    context = {'todos': todos, 'staff': staff}
    return render(request, 'main/attendance.html', context)


# marking status to True and sending message after a set time
# NOTE: Timer method is used to clear the statuses after a set time aswel

def mark_complete(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed = True
    todo.save()

    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def mark_complete2(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed2 = True
    todo.save()

    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def mark_complete3(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed3 = True
    todo.save()

    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def mark_complete4(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed4 = True
    todo.save()

    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


# reverse marking from True to False

def mark_incomplete(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed = False
    todo.completion_date = None

    todo.save()
    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def mark_incomplete2(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed2 = False
    todo.completion_date = None

    todo.save()
    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def mark_incomplete3(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed3 = False
    todo.completion_date = None

    todo.save()
    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def mark_incomplete4(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    todo.completed4 = False
    todo.completion_date = None

    todo.save()
    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


def message_parents(request, slug, todo_id):
    todo = Attendance.objects.get(slug=slug, id=todo_id)
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    Attendance.objects.create(student=todo.student, completed=todo.completed, completed2=todo.completed2,
                              completed3=todo.completed3, completed4=todo.completed4,
                              completion_date=str(jalali_date_obj))

    messages.success(request, f'غیبت {todo.student} ثبت شد')

    return HttpResponseRedirect(reverse('main:attendance', args=(slug,)))


# view lists of students and their status

def attendance(request):
    student = Attendance.objects.all

    context = {'student': student}
    return render(request, 'main/checkbox.html', context)


# delete users

def delete(request, pk):
    student = Grades.objects.get(id=pk)

    if request.method == 'POST':

        student = Grades.objects.all().update(grades=0.0)
        return redirect('/')

    else:

        context = {'item': student}
        return render(request, 'main/delete.html', context)


@check_role_teacher
def add_grade_a(request, parent_id, subject):
    today = datetime.datetime.now()  # Current date
    delayed_date = today - timedelta(days=20)
    # getting objects that need to be queried
    parent_instance = get_object_or_404(Classes, id=parent_id)
    course = get_object_or_404(Course, subject=subject)
    stu = StudentAccount.objects.filter(classes=parent_id, graduate=False)

    # creating the queries to filter data dynamically
    description_query = Description.objects.filter(subject=course)
    grade_query = Grades.objects.filter(subject=course, archived=False).order_by('student', 'date')

    # creating our formsets for inline editing for grades of each class
    GradeUpdate = inlineformset_factory(Classes, Grades, fk_name='classes', extra=0, can_delete=False,
                                        form=GradesForm)
    formset = GradeUpdate(instance=parent_instance, queryset=grade_query.order_by('student', 'subject'))

    # fromset of the description box for each class
    DescriptionForm = inlineformset_factory(Classes, Description, fk_name='classes', can_delete=False, extra=0,
                                            form=TextForm)
    text_formset = DescriptionForm(instance=parent_instance, queryset=description_query)

    time = datetime.time(8, 15, 0)
    time2 = datetime.time(10, 00, 0)
    time3 = datetime.time(12, 30, 0)
    print(f'time:{time}')

    # getting the hijri shamsi date and time for models
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    date_to_str = jalali_date_obj.strftime('%Y-%m-%d')
    print(date_to_str)
    jdate = jdatetime.datetime.now()

    # checking the request
    if request.method == "POST":

        formset = GradeUpdate(request.POST, instance=parent_instance)
        text_formset = DescriptionForm(request.POST, instance=parent_instance)

        if text_formset.is_valid():
            text_formset.save()

        # creating new objects for models when clicking the button with name:add-new
        if 'add_new' in request.POST:
            for i in stu:
                Grades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                      grade_type='A')
                print(jdate)

            Description.objects.create(classes=parent_instance, subject=course, date=date_to_str, text_box='')

            return redirect(f'/add_grade_a/{parent_id}/{course}')

        # validating the formsets and saving the data
        for form in formset:

            if formset.is_valid():
                all_valid = True
                for form in formset:
                    if form.cleaned_data:  # Check if the form has cleaned data
                        field_value = form.cleaned_data.get('grades_100')
                        field_value_2 = form.cleaned_data.get('grades_20')

                    try:
                        if field_value and field_value > 100 or field_value_2 > 100 and course.grade_type == "A":  # Example condition
                            form.add_error('grades_100',
                                           "نمره فیلد ها نمیتواند بالای 100 باشد ")  # Add error to specific field
                            all_valid = False

                    except:
                        all_valid = True

                if all_valid:
                    # Save all forms in the formset if validation passes
                    formset.save()

                    return redirect(f'/add_grade_a/{parent_id}/{course}')

            # checking if the teacher has premission to view or edit forms of the subject requested
    try:
        teacher_course = ClCourses.objects.get(student=request.user.id, subject=course, slug=parent_instance)

        if course == teacher_course.subject and parent_instance == teacher_course.slug:
            print(f'you have this course {subject} {parent_instance}')

        if teacher_course.course_type != "A":
            return HttpResponse('you dont teach this subject')

    except:
        try:
            request.user.staff.role = Group.objects.get(name='principal')
        except:
            return HttpResponse('you dont teach this subject')

    clas = str(parent_instance)
    classes = clas.replace(' ', '')

    # groups all the grades of each student as a list for that student
    # NOTE: prevents having multiple student records for each grade that gets added
    grouped_data = {}
    for form in formset:
        student = form.instance.student
        subject = form.instance.subject

        if student not in grouped_data:
            grouped_data[student] = {}

        if subject not in grouped_data[student]:
            grouped_data[student][subject] = []
        grouped_data[student][subject].append(form)

    grouped_date = {}

    context = {
        "formset": formset, 'instance': parent_instance, 'course': course,
        'grouped_data': grouped_data, 'stu': stu, 'grouped_date': grouped_date,
        'text_formset': text_formset, 'description_query': description_query, 'classes': classes
    }

    return render(request, "main/add_a.html", context)


def add_grade_p(request, parent_id, subject):
    today = datetime.datetime.now()  # Current date
    delayed_date = today - timedelta(days=20)
    # getting objects that need to be queried
    parent_instance = get_object_or_404(Classes, id=parent_id)
    course = get_object_or_404(Course, subject=subject)
    stu = StudentAccount.objects.filter(classes=parent_id, graduate=False)

    # creating the queries to filter data dynamically
    description_query = Description.objects.filter(subject=course)
    grade_query = Grades.objects.filter(subject=course, archived=False).order_by('student', 'date')

    # creating our formsets for inline editing for grades of each class
    GradeUpdate = inlineformset_factory(Classes, Grades, fk_name='classes', extra=0, can_delete=False,
                                        form=GradesForm)
    formset = GradeUpdate(instance=parent_instance, queryset=grade_query.order_by('student', 'subject'))

    # fromset of the description box for each class
    DescriptionForm = inlineformset_factory(Classes, Description, fk_name='classes', can_delete=False, extra=0,
                                            form=TextForm)
    text_formset = DescriptionForm(instance=parent_instance, queryset=description_query)

    time = datetime.time(8, 15, 0)
    time2 = datetime.time(10, 00, 0)
    time3 = datetime.time(12, 30, 0)
    print(f'time:{time}')

    # getting the hijri shamsi date and time for models
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    date_to_str = jalali_date_obj.strftime('%Y-%m-%d')
    print(date_to_str)
    jdate = jdatetime.datetime.now()

    # checking the request
    if request.method == "POST":

        formset = GradeUpdate(request.POST, instance=parent_instance)
        text_formset = DescriptionForm(request.POST, instance=parent_instance)

        if text_formset.is_valid():
            text_formset.save()
        # creating new objects for models when clicking the button with name:add-new
        if 'add_new' in request.POST:
            for i in stu:
                Grades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                      grade_type='B')
                print(jdate)

            Description.objects.create(classes=parent_instance, subject=course, date=date_to_str, text_box='')

            return redirect(f'/add_grade_b/{parent_id}/{course}')

        # validating the formsets and saving the data
        for form in formset:

            if formset.is_valid():
                all_valid = True
                for form in formset:
                    if form.cleaned_data:  # Check if the form has cleaned data
                        field_value = form.cleaned_data.get('grades_100')
                        field_value_2 = form.cleaned_data.get('grades_20')

                    try:
                        if field_value and field_value > 3 and course.grade_type == "B":  # Example condition
                            form.add_error('grades_100',
                                           "نمره فیلد ها نمیتواند بالای 3 باشد ")  # Add error to specific field
                            all_valid = False
                        elif field_value_2 > 5 and course.grade_type == "B":
                            form.add_error('grades_20', "نمره فیلد ها نمیتواند بالای 5 باشد ")
                            all_valid = False
                    except:
                        all_valid = True

                if all_valid:
                    # Save all forms in the formset if validation passes
                    formset.save()

                    return redirect(f'/add_grade_b/{parent_id}/{course}')
            # checking if the teacher has premission to view or edit forms of the subject requested
    try:
        teacher_course = ClCourses.objects.get(student=request.user.id, subject=course, slug=parent_instance)

        if course == teacher_course.subject and parent_instance == teacher_course.slug:
            print(f'you have this course {subject} {parent_instance}')
        if teacher_course.course_type != "B":
            return HttpResponse('you dont teach this subject')

    except:
        try:
            request.user.staff.role = Group.objects.get(name='principal')
        except:
            return HttpResponse('you dont teach this subject')

    clas = str(parent_instance)
    classes = clas.replace(' ', '')

    # groups all the grades of each student as a list for that student
    # NOTE: prevents having multiple student records for each grade that gets added
    grouped_data = {}
    for form in formset:
        student = form.instance.student
        subject = form.instance.subject

        if student not in grouped_data:
            grouped_data[student] = {}

        if subject not in grouped_data[student]:
            grouped_data[student][subject] = []
        grouped_data[student][subject].append(form)

    grouped_date = {}

    context = {
        "formset": formset, 'instance': parent_instance, 'course': course,
        'grouped_data': grouped_data, 'stu': stu, 'grouped_date': grouped_date,
        'text_formset': text_formset, 'description_query': description_query, 'classes': classes
    }

    return render(request, "main/add_b.html", context)


@check_role_teacher
def add_grade_c(request, parent_id, subject):
    today = datetime.datetime.now()  # Current date
    delayed_date = today - timedelta(days=20)
    # getting objects that need to be queried
    parent_instance = get_object_or_404(Classes, id=parent_id)
    course = get_object_or_404(Course, subject=subject)
    stu = StudentAccount.objects.filter(classes=parent_id, graduate=False)

    # creating the queries to filter data dynamically
    description_query = Description.objects.filter(subject=course)
    grade_query = Grades.objects.filter(subject=course, archived=False).order_by('student', 'date')

    # creating our formsets for inline editing for grades of each class
    GradeUpdate = inlineformset_factory(Classes, Grades, fk_name='classes', extra=0, can_delete=False,
                                        form=GradesForm_C)
    formset = GradeUpdate(instance=parent_instance, queryset=grade_query.order_by('student', 'subject'))

    # fromset of the description box for each class
    DescriptionForm = inlineformset_factory(Classes, Description, fk_name='classes', can_delete=False, extra=0,
                                            form=TextForm)
    text_formset = DescriptionForm(instance=parent_instance, queryset=description_query)

    time = datetime.time(8, 15, 0)
    time2 = datetime.time(10, 00, 0)
    time3 = datetime.time(12, 30, 0)
    print(f'time:{time}')

    # getting the hijri shamsi date and time for models
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    date_to_str = jalali_date_obj.strftime('%Y-%m-%d')
    print(date_to_str)
    jdate = jdatetime.datetime.now()

    # checking the request
    if request.method == "POST":

        formset = GradeUpdate(request.POST, instance=parent_instance)
        text_formset = DescriptionForm(request.POST, instance=parent_instance)

        if text_formset.is_valid():
            text_formset.save()
        # creating new objects for models when clicking the button with name:add-new
        if 'add_new' in request.POST:
            for i in stu:
                Grades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                      grade_type='C')
                print(jdate)

            Description.objects.create(classes=parent_instance, subject=course, date=date_to_str, text_box='')

            return redirect(f'/add_grade_c/{parent_id}/{course}')

        # validating the formsets and saving the data
        for form in formset:

            if formset.is_valid():
                all_valid = True
                for form in formset:
                    if form.cleaned_data:  # Check if the form has cleaned data
                        field_value = form.cleaned_data.get('grades_100')
                        field_value_2 = form.cleaned_data.get('grades_20')

                        try:
                            if field_value and field_value > 20 or field_value_2 > 20 and course.grade_type == "C":  # Example condition

                                form.add_error('grades_20',
                                               "نمره فیلد ها نمیتواند بالای20 باشد ")  # Add error to specific field
                                all_valid = False
                        except:
                            all_valid = True

                if all_valid:
                    # Save all forms in the formset if validation passes
                    formset.save()

                    return redirect(f'/add_grade_c/{parent_id}/{course}')

            # checking if the teacher has premission to view or edit forms of the subject requested
    try:
        teacher_course = ClCourses.objects.get(student=request.user.id, subject=course, slug=parent_instance)

        if course == teacher_course.subject and parent_instance == teacher_course.slug:
            print(f'you have this course {subject} {parent_instance}')
        if teacher_course.course_type != "C":
            return HttpResponse('you dont teach this subject')

    except:
        try:
            request.user.staff.role = Group.objects.get(name='principal')
        except:
            return HttpResponse('you dont teach this subject')

    clas = str(parent_instance)
    classes = clas.replace(' ', '')

    # groups all the grades of each student as a list for that student
    # NOTE: prevents having multiple student records for each grade that gets added
    grouped_data = {}
    for form in formset:
        student = form.instance.student
        subject = form.instance.subject

        if student not in grouped_data:
            grouped_data[student] = {}

        if subject not in grouped_data[student]:
            grouped_data[student][subject] = []
        grouped_data[student][subject].append(form)

    grouped_date = {}

    context = {
        "formset": formset, 'instance': parent_instance, 'course': course,
        'grouped_data': grouped_data, 'stu': stu, 'grouped_date': grouped_date,
        'text_formset': text_formset, 'description_query': description_query, 'classes': classes
    }

    return render(request, "main/add_c.html", context)


def add_grade(request, student, subject):
    # Retrieve the student and subject based on the IDs
    student = get_object_or_404(StudentAccount, id=student)
    subject = get_object_or_404(Course, subject=subject)

    # Create a new Grades instance with the student and subject, and leave the grade empty
    Grades.objects.create(student=student, subject=subject)
    return redirect('add_grades')


def update_grades(request, parent_id, completion_date):
    print(abslout_date)
    print(completion_date)
    if completion_date == abslout_date:

        parent_instance = get_object_or_404(Classes, id=parent_id)

        stu = StudentAccount.objects.filter(classes=parent_id)
        count = Attendance.objects.filter(slug=parent_instance, completion_date=completion_date).count()
        query = Attendance.objects.filter(completion_date=completion_date)
        attended = Attendance.objects.filter(slug=parent_instance, completion_date=completion_date)
        AttendanceFormset = inlineformset_factory(Classes, Attendance, fk_name='slug', extra=0, can_delete=False,
                                                  form=TodoForm)
        formset = AttendanceFormset(instance=parent_instance, queryset=query)

        if request.method == "POST":
            formset = AttendanceFormset(request.POST, instance=parent_instance, queryset=query)

            if 'add_new' in request.POST:
                for i in stu:
                    Attendance.objects.create(student=i, completed=0, completed2=0, completed3=0, completed4=0,
                                              slug=parent_instance, completion_date=abslout_date)
                return redirect(f'/update/{parent_id}/{abslout_date}')

            if 'send-message' in request.POST:

                for i in attended:
                    if i.completed == True or i.completed2 == True or i.completed3 == True or i.completed4 == True:
                        messages.success(request,
                                         f'پیام برای والدین دانش آموز {i.student.first_name} {i.student.last_name} ارسال شد')

            if formset.is_valid():
                formset.save(commit=True)

                return redirect(f'/update/{parent_id}/{abslout_date}')

        context = {
            "formset": formset, 'instance': parent_instance, 'stu': stu,
            'count': count, 'date': abslout_date, 'attended': attended
        }

    else:
        return redirect(f'/update/{parent_id}/{abslout_date}')
    return render(request, "main/update.html", context)


def student_list(request, subject, classes):
    student = StudentAccount.objects.filter(classes=classes)
    classes = get_object_or_404(Classes, id=classes)
    course = get_object_or_404(Course, subject=subject)

    context = {'student': student, 'course': course, 'classes': classes}
    return render(request, 'main/student_list.html', context)


@check_role_teacher
def class_final_grade(request, parent_id, subject, turn):
    turn = int(turn)
    today = datetime.datetime.now()  # Current date
    delayed_date = today - timedelta(days=20)
    # getting objects that need to be queried
    parent_instance = get_object_or_404(Classes, id=parent_id)
    course = get_object_or_404(Course, subject=subject)
    stu = StudentAccount.objects.filter(classes=parent_id)
    grade_count = FinalGrades.objects.filter(classes=parent_instance, subject=course).count()
    # creating the queries to filter data dynamically

    grade_query = FinalGrades.objects.filter(subject=course, turn=turn).order_by('student', 'date')

    # creating our formsets for inline editing for grades of each class
    GradeUpdate = inlineformset_factory(Classes, FinalGrades, fk_name='classes', extra=0, can_delete=False,
                                        form=ClassOveral)
    formset = GradeUpdate(instance=parent_instance, queryset=grade_query.order_by('student', 'subject'))

    time = datetime.time(8, 15, 0)

    print(f'time:{time}')

    # getting the hijri shamsi date and time for models
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    date_to_str = jalali_date_obj.strftime('%Y-%m-%d')
    print(course.grade_type)
    jdate = jdatetime.datetime.now()

    # checking the request
    if request.method == "POST":

        formset = GradeUpdate(request.POST, instance=parent_instance)

        # creating new objects for models when clicking the button with name:add-new
        if 'add_new' in request.POST:
            for i in stu:
                FinalGrades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                           grade_type=course.grade_type, turn=turn)
                print(jdate)

            return redirect(f'/class_finall_grade/{parent_id}/{course}/{turn}')

        # validating the formsets and saving the data
        if formset.is_valid():
            formset.save()

            return redirect(f'/class_finall_grade/{parent_id}/{course}/{turn}')

            # checking if the teacher has premission to view or edit forms of the subject requested
    try:
        teacher_course = ClCourses.objects.get(student=request.user.id, subject=course, slug=parent_instance)

        if course == teacher_course.subject and parent_instance == teacher_course.slug:
            print(f'you have this course {subject} {parent_instance}')

    except:
        return HttpResponse('you dont teach this subject')

    clas = str(parent_instance)
    classes = clas.replace(' ', '')

    # groups all the grades of each student as a list for that student
    # NOTE: prevents having multiple student records for each grade that gets added
    grouped_data = {}
    for form in formset:
        student = form.instance.student
        subject = form.instance.subject

        if student not in grouped_data:
            grouped_data[student] = {}

        if subject not in grouped_data[student]:
            grouped_data[student][subject] = []
        grouped_data[student][subject].append(form)

    grouped_date = {}

    context = {
        "formset": formset, 'instance': parent_instance, 'course': course,
        'grouped_data': grouped_data, 'stu': stu, 'grouped_date': grouped_date,
        'classes': classes, 'grade_count': grade_count, 'turn': turn
    }

    return render(request, "main/class_final_grade.html", context)


@check_role_teacher
def final_grade(request, parent_id, subject, turn):

    turn = int(turn)
    today = datetime.datetime.now()  # Current date
    delayed_date = today - timedelta(days=20)
    
    # getting objects that need to be queried
    parent_instance = get_object_or_404(Classes, id=parent_id)
   
    course = get_object_or_404(Course, subject=subject)
    stu = StudentAccount.objects.filter(classes=parent_id)
    grade_count = FinalGrades.objects.filter(classes=parent_instance, subject=course, turn=turn).count()
    # creating the queries to filter data dynamically

    grade_query = FinalGrades.objects.filter(subject=course, turn=turn).order_by('student', 'date')
    
    # creating our formsets for inline editing for grades of each class
    if course.grade_type == 'C':
        GradeUpdate = inlineformset_factory(Classes, FinalGrades, fk_name='classes', extra=0, can_delete=False,
                                            form=FinalFormGrade_C)
    else:
        GradeUpdate = inlineformset_factory(Classes, FinalGrades, fk_name='classes', extra=0, can_delete=False,
                                            form=FinalFormGrade)
    formset = GradeUpdate(instance=parent_instance, queryset=grade_query.order_by('student', 'subject'))

    time = datetime.time(8, 15, 0)

    print(f'time:{time}')

    # getting the hijri shamsi date and time for models
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    date_to_str = jalali_date_obj.strftime('%Y-%m-%d')
    print(course.grade_type)
    jdate = jdatetime.datetime.now()

    print(turn)
    # checking the request
    if request.method == "POST":

        formset = GradeUpdate(request.POST, instance=parent_instance)
  
        # creating new objects for models when clicking the button with name:add-new
        if 'add_new' in request.POST:
            if turn == 1:
                for i in stu:
                    FinalGrades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                        grade_type=course.grade_type, turn=1, vahed=course.vahed)
                    print(jdate)

                return redirect(f'/finall_grade/{parent_id}/{course}/1')
  
            elif turn == 2:
                for i in stu:
                    FinalGrades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                        grade_type=course.grade_type, turn=2, vahed=course.vahed)
                    print(jdate)

                return redirect(f'/finall_grade/{parent_id}/{course}/2')


        # validating the formsets and saving the data
        for form in formset:

            if formset.is_valid():
                all_valid = True
                for form in formset:
                    if form.cleaned_data:  # Check if the form has cleaned data
                        field_value_2 = form.cleaned_data.get('grades_theory')
                        field_value = form.cleaned_data.get('grades_amali')
                

                        try:
                            if field_value and field_value > 100 and course.grade_type == "A":  # Example condition

                                form.add_error('grades_amali',
                                               "نمره فیلد ها نمیتواند بالای100 باشد ")  # Add error to specific field
                                all_valid = False

                            elif field_value_2 and field_value_2 > 20 and course.grade_type == "C":  # Example condition

                                form.add_error('grades_theory',
                                               "نمره فیلد ها نمیتواند بالای20 باشد ")  # Add error to specific field
                                all_valid = False

                        except:
                            all_valid = True

                if all_valid:
                    # Save all forms in the formset if validation passes
                    formset.save()

                    return redirect(f'/finall_grade/{parent_id}/{course}/{turn}')

            # checking if the teacher has premission to view or edit forms of the subject requested
    try:
        teacher_course = ClCourses.objects.get(student=request.user.id, subject=course, slug=parent_instance)

        if course == teacher_course.subject and parent_instance == teacher_course.slug:
            print(f'you have this course {subject} {parent_instance}')

    except:
        return HttpResponse('you dont teach this subject')

    clas = str(parent_instance)
    classes = clas.replace(' ', '')

    # groups all the grades of each student as a list for that student
    # NOTE: prevents having multiple student records for each grade that gets added
    grouped_data = {}
    for form in formset:
        student = form.instance.student
        subject = form.instance.subject

        if student not in grouped_data:
            grouped_data[student] = {}

        if subject not in grouped_data[student]:
            grouped_data[student][subject] = []
        grouped_data[student][subject].append(form)

    grouped_date = {}

    a = 'A'
    b = 'B'
    c = 'C'

    context = {
        "formset": formset, 'instance': parent_instance, 'course': course,
        'grouped_data': grouped_data, 'stu': stu, 'grouped_date': grouped_date,
        'classes': classes, 'grade_count':grade_count, 'turn':turn, 'a': a, 'b': b, 'c': c
    }

    return render(request, "main/final_grade.html", context)


def final_courses(request, slug):
    report = ClCourses.objects.filter(student=request.user.id, slug=slug)
    report_a = ClCourses.objects.filter(student=request.user.id, slug=slug)
    a = 'A'
    b = 'B'
    c = 'C'
    classes = f'/attendance/{slug}/{abslout_date}'
    print(report)
    context = {'report': report, 'classes': classes, 'report_a': report_a, 'a': a, 'b': b, 'c': c}
    return render(request, 'main/final_courses.html', context)


def summer_grades(request, parent_id, subject):
    today = datetime.datetime.now()  # Current date
    delayed_date = today - timedelta(days=20)
    # getting objects that need to be queried
    parent_instance = get_object_or_404(Classes, id=parent_id)

    course = get_object_or_404(Course, subject=subject)
    stu = StudentAccount.objects.filter(classes=parent_id, status=True)
    grade_count = FinalGrades.objects.filter(classes=parent_instance, subject=course).count()
    # creating the queries to filter data dynamically

    grade_query = FinalGrades.objects.filter(subject=course, passed=False, turn=3).order_by('student', 'date')

    # creating our formsets for inline editing for grades of each class
    if course.grade_type == 'C':
        GradeUpdate = inlineformset_factory(Classes, FinalGrades, fk_name='classes', extra=0, can_delete=False,
                                            form=FinalFormGrade_C)
    else:
        GradeUpdate = inlineformset_factory(Classes, FinalGrades, fk_name='classes', extra=0, can_delete=False,
                                            form=FinalFormGrade)
    formset = GradeUpdate(instance=parent_instance, queryset=grade_query.order_by('student', 'subject'))

    time = datetime.time(8, 15, 0)

    print(f'time:{time}')

    # getting the hijri shamsi date and time for models
    jalali_date_obj = jalali_date.date2jalali(datetime.date.today())
    date_to_str = jalali_date_obj.strftime('%Y-%m-%d')
    print(course.grade_type)
    jdate = jdatetime.datetime.now()

    # checking the request
    if request.method == "POST":

        formset = GradeUpdate(request.POST, instance=parent_instance)

        # creating new objects for models when clicking the button with name:add-new
        if 'add_new_3' in request.POST:
            for i in stu:
                FinalGrades.objects.create(student=i, subject=course, classes=parent_instance, time=delayed_date,
                                           grade_type=course.grade_type, turn=3, passed=False)
                print(jdate)

            return redirect(f'/summer_grade/{parent_id}/{course}/')

        # validating the formsets and saving the data
        if formset.is_valid():
            formset.save()

            return redirect(f'/summer_grade/{parent_id}/{course}/')

            # checking if the teacher has premission to view or edit forms of the subject requested
    try:
        teacher_course = ClCourses.objects.get(student=request.user.id, subject=course, slug=parent_instance)

        if course == teacher_course.subject and parent_instance == teacher_course.slug:
            print(f'you have this course {subject} {parent_instance}')

    except:

        try:
            request.user.staff.role = Group.objects.get(name='principal')
        except:
            return HttpResponse('you dont teach this subject')

    clas = str(parent_instance)
    classes = clas.replace(' ', '')

    # groups all the grades of each student as a list for that student
    # NOTE: prevents having multiple student records for each grade that gets added
    grouped_data = {}
    for form in formset:
        student = form.instance.student
        subject = form.instance.subject

        if student not in grouped_data:
            grouped_data[student] = {}

        if subject not in grouped_data[student]:
            grouped_data[student][subject] = []
        grouped_data[student][subject].append(form)

    grouped_date = {}

    context = {
        'formset': formset,
        'instance': parent_instance,
        'course': course,
        'grouped_data': grouped_data,
        'stu': stu,
        'grouped_date': grouped_date,
        'classes': classes,
        'grade_count': grade_count,
    }

    return render(request, 'main/summer.html', context)


def yearly_final(request, slug):
    detail = StudentAccount.objects.get(id=slug)
    detail.status = False
    detail.save()
    # Fetch the final grades for the student
    final_grades = FinalGrades.objects.filter(student=slug).select_related('subject').order_by('turn')

    # Get unique turns for the columns
    unique_turns = list(final_grades.values_list('turn', flat=True).distinct())

    # Organize grades by subject and turn
    grades_by_subject = {}
    overal_grade = {}
    averages_by_subject = {}

    for grade in final_grades:
        subject = grade.subject
        if subject not in grades_by_subject:
            grades_by_subject[subject] = {turn: None for turn in unique_turns}
            overal_grade[subject] = {turn: None for turn in unique_turns}  # Initialize all turns as None

        if grade.grade_type == 'A':

            o_avg = ((grade.grades_amali * (75 / 100)) / 5) + ((grade.grades_theory * (25 / 100) / 5))
            grades_by_subject[subject][grade.turn] = ((o_avg + grade.overal_grade) / 2)
            overal_grade[subject][grade.turn] = ((o_avg * 2) + grade.overal_grade) if grade.turn == 1 else (
                    (o_avg * 4) + grade.overal_grade)

        elif grade.grade_type == 'B':

            avg = ((grade.grades_amali * 5) + (grade.grades_theory))
            grades_by_subject[subject][grade.turn] = (avg + grade.overal_grade) / 2
            overal_grade[subject][grade.turn] = ((avg * 2) + grade.overal_grade) if grade.turn == 1 else (
                    (avg * 4) + grade.overal_grade)

        elif grade.grade_type == 'C':
            grades_by_subject[subject][grade.turn] = ((grade.grades_theory) + grade.overal_grade) / 2
            overal_grade[subject][grade.turn] = (
                    (grade.grades_theory * 2) + grade.overal_grade) if grade.turn == 1 else (
                    (grade.grades_theory * 4) + grade.overal_grade)

    total_sum = 0
    total_count = 0
    total_vahed = 0

    for subject, grades_dict in overal_grade.items():
        all_grades = [grade for grade in grades_dict.values() if grade is not None]  # Filter None values
        if all_grades:

            average = mean(all_grades) / 4
            rounded_average = get_up_to_nearest_25(average)  # Round to nearest 0.25

            overal_average = get_up_to_nearest_25(average * subject.vahed)

            threshold = 10 if subject.grade_type == 'C' else 14 or 12 if subject.grade_type == "B" else 14
            passed = rounded_average >= threshold

            averages_by_subject[subject] = {
                'average': rounded_average,
                'status': 'پاس شده' if passed else 'مردود',

            }

            FinalGrades.objects.filter(subject=subject, student=slug).update(passed=passed)
            print(passed)

            if passed == False:
                detail.status = True
                detail.save()

            total_sum += get_up_to_nearest_25(overal_average)
            total_vahed += subject.vahed
            total_count += 1

    total_average = get_up_to_nearest_25(total_sum / total_vahed)

    table_rows = []
    for subject, grades_dict in grades_by_subject.items():
        row = [subject]  # Start the row with the subject name
        for turn in unique_turns:
            row.append(grades_dict.get(turn, '-'))

        # Add grade or placeholder for each turn
        try:
            row.append(averages_by_subject[subject]['average'])
            row.append(averages_by_subject[subject]['status'])

        except:
            row.append('-')

        table_rows.append(row)

    context = {
        'detail': detail,
        'unique_turns': unique_turns,
        'table_rows_a': table_rows,
        'rounded_total_average': total_average,
    }

    return render(request, 'main/yaerly_final.html', context)


def allow_promotion(request, parent_id):
    parent_instance = get_object_or_404(Classes, id=parent_id)

    AllowanceForm = inlineformset_factory(Classes, StudentAccount, fk_name='classes', extra=0, can_delete=False,
                                          form=StudentPromotion)
    formset = AllowanceForm(instance=parent_instance)
    if request.method == 'POST':
        formset = AllowanceForm(request.POST, instance=parent_instance)
        if formset.is_valid():
            formset.save()

    context = {'student': parent_instance, 'formset': formset}
    return render(request, 'main/allow.html', context)


# |---------------------------------------------------|#|
# |-NOTE: END OF STUDENT AND GRADES RELATED FUNCTIONS-|#|
# |---------------------------------------------------|#|
