
from django.urls import path
from . import views


urlpatterns = [
    path('<int:question_sheet_id>', views.get_question_sheet_by_id, name="question_sheet_id"),
    # path()
]
