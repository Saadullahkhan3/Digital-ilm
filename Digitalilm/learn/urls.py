from . import views

from django.urls import path


urlpatterns = [
    # Explore Quizzes
    path('', views.explore_quizzes , name="explore-quizzes"),

    # Specific Question Sheet, below both are same, just url name different!
    path('<int:question_sheet_id>/', views.question_sheet_by_id, name="question_sheet"),    # When only question id typed
    path('<int:question_sheet_id>/sheet/', views.question_sheet_by_id, name="question_sheet_by_id"),    # When sheet/ is typed

    # Leader board
    path('<int:question_sheet_id>/leaderboard/', views.leaderboard_by_id, name="leaderboard_by_id"),    

    # Registration
    path('register/', views.tutor_register, name="register"),

    # Extra confirmation page to prevent accidentle log out
    path('confirm-logout/', views.confirm_logout, name="confirm-logout"),

    # Question Sheet form with Question
    path('create-question-sheet/', views.create_question_sheet, name='create_question_sheet'),
    path('<int:question_sheet_id>/delete/', views.delete_sheet, name="delete_sheet"),
    path('<int:question_sheet_id>/edit/', views.edit_sheet, name="edit_sheet"),

    # [Internal Usage] Use to get Question form
    path('get-question-form/', views._get_question_form, name='get_question_form'),

    # Todo: Change the url as saad/ tutor name not like tutor/
    # Tutor Profile Page
    path('tutor/', views.tutor_profile, name="tutor"),
]
