from .models import QuestionSheet



def seed_created_and_update_in_question_sheet_model():
    return "Disabled, updated = models.DateTimeField(auto_now=True) in QuestionSheet model has been enabled"

    for sheet in QuestionSheet.objects.all():
        # total_students = sheet.students.all().count()
        
        print(f"After -> Sheet: {sheet.title}, Created, Updated: {sheet.created}, {sheet.updated}")

        # Assigning appropirate values
        # sheet.attempted_count = total_students
        sheet.created = sheet.tutor.date_joined
        sheet.updated = sheet.tutor.date_joined		# auto_now_add=True should be false as we are saving the model by own
        
        print(f"After -> Sheet: {sheet.title}, Created, Updated: {sheet.created}, {sheet.updated}")
        
        sheet.save()

