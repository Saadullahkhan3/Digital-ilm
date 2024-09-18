from django.contrib import admin
from .models import QuestionSheet, Question, Student

# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

class AdminQuestionSheet(admin.ModelAdmin):
    list_display = ("title", "id")
    inlines = (QuestionInline,)

class AdminStudent(admin.ModelAdmin):
    list_display = ("name", "score", "attempted_sheet")

admin.site.register(QuestionSheet, AdminQuestionSheet)
admin.site.register(Student, AdminStudent)
admin.site.register(Question)

