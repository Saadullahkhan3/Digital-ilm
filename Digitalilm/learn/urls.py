
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home2 , name="home2"),
    path('<int:question_sheet_id>/', views.get_question_sheet_by_id, name="question_sheet_id"),
    path('tutor/', views.RegisterTutor, name="register-tutor"),

    path('create-question-sheet/', views.create_question_sheet2, name='create_question_sheet'),
    path('get-question-form/', views.get_question_form, name='get_question_form'),

    path('tutor-ok/', views.after_tutor_register, name="tutor-ok")


]
