from . import views

from django.urls import path


urlpatterns = [
    # Explore Quizzes
    path('', views.explore_quizzes , name="explore-quizzes"),

    # Specific Question Sheet
    path('<int:question_sheet_id>/', views.question_sheet_by_id, name="question_sheet_by_id"),

    #Shayan Adnan,
    # Define your leaderboard url here!
    

    # Registration
    path('register/', views.tutor_register, name="register"),

    # Extra confirmation page to prevent accidentle log out
    path('confirm-logout/', views.confirm_logout, name="confirm-logout"),

    # Initialze a Question Sheet form with one Question as default
    path('create-question-sheet/', views.create_question_sheet, name='create_question_sheet'),
    # [Internal Usage] Use to get Question form
    path('get-question-form/', views.get_question_form, name='get_question_form'),

    # Todo: Change the url as saad/ tutor name not like tutor/
    # Tutor Profile Page
    path('tutor/', views.tutor_profile, name="tutor"),

]
