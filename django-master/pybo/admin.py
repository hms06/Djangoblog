from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject','content']
    list_display = ['id','subject','short_content','create_date']
    def short_content(self, item):
        return item.content[:10]
