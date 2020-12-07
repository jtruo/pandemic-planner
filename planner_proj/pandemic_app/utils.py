from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from django.db.models import DateField, F

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, userid=0):
		self.year = year
		self.month = month
		self.userid = userid
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter tasks by day
	def formatday(self, day, assignments, lectures, exams):
    	
		assignments_per_day = assignments.filter(due_date__day=day)
		lectures_per_day = lectures.filter(day__day=day)
		exams_per_day = exams.filter(exam_date__day=day)

		d = ''

		for exam in exams_per_day:
    			class_for_exam = Class.objects.get(id=exam.class_id)
    			d += f'<li> Exam for: {class_for_exam.class_name} </li>'

		for assignment in assignments_per_day:
				d += f'<li> Assignment: {assignment.ass_name} </li>'

		for lecture in lectures_per_day:
				class_for_lecture = Class.objects.get(id=lecture.class_id)
				d += f'<li> Lecture for: {class_for_lecture.class_name} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>' 

	# formats a week as a tr 
	def formatweek(self, theweek, assignments, lectures, exams):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, assignments, lectures, exams)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter tasks by year and month
	def formatmonth(self, withyear=True):
    	
		# Get each type of task and send it to be formatted
		assignments = Assignment.objects.filter(due_date__year=self.year, due_date__month=self.month, user_id=self.userid)
		lectures = Lecture.objects.filter(day__year=self.year, day__month=self.month, user_id=self.userid)
		exams = Exam.objects.filter(exam_date__year=self.year, exam_date__month=self.month, user_id=self.userid)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, assignments, lectures, exams)}\n'
		return cal
