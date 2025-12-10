from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import University, Subject, ExamPaper


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['name', 'location']
    list_filter = ['location']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'department', 'semester', 'category']
    list_filter = ['university', 'category', 'semester']
    search_fields = ['name', 'department', 'university__name']
    autocomplete_fields = ['university']


class ExamPaperForm(ModelForm):
    class Meta:
        model = ExamPaper
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        document_type = cleaned_data.get('document_type')
        exam_period = cleaned_data.get('exam_period')
        exam_year = cleaned_data.get('exam_year')
        
        if document_type == 'Θέμα Εξεταστικής':
            if not exam_period:
                raise ValidationError({
                    'exam_period': 'Η περίοδος εξέτασης είναι υποχρεωτική για θέματα εξεταστικής.'
                })
            if not exam_year:
                raise ValidationError({
                    'exam_year': 'Το έτος είναι υποχρεωτικό για θέματα εξεταστικής.'
                })
        
        return cleaned_data


@admin.register(ExamPaper)
class ExamPaperAdmin(admin.ModelAdmin):
    form = ExamPaperForm
    list_display = ['subject', 'document_type', 'exam_period', 'exam_year', 'group_name', 'created_at']
    list_filter = ['document_type', 'exam_period', 'exam_year', 'subject__university', 'subject__category']
    search_fields = ['subject__name', 'group_name', 'admin_notes']
    autocomplete_fields = ['subject']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Βασικές Πληροφορίες', {
            'fields': ('subject', 'document_type')
        }),
        ('Πληροφορίες Εξεταστικής', {
            'fields': ('exam_period', 'exam_year', 'group_name'),
            'description': 'Συμπληρώστε μόνο αν το έγγραφο είναι "Θέμα Εξεταστικής"'
        }),
        ('Αρχείο', {
            'fields': ('file',)
        }),
        ('Σημειώσεις', {
            'fields': ('admin_notes',)
        }),
        ('Μεταδεδομένα', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


