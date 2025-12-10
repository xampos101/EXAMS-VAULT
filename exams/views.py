from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import University, Subject, ExamPaper


def index(request):
    """Main page with filters and results"""
    universities = University.objects.all().order_by('name')
    return render(request, 'exams/index.html', {
        'universities': universities,
    })


def api_exams(request):
    """API endpoint for filtering exams via AJAX"""
    # Get filter parameters
    university_id = request.GET.get('university')
    department = request.GET.get('department')
    semester = request.GET.get('semester')
    category = request.GET.get('category')
    document_type = request.GET.get('document_type')
    search_query = request.GET.get('search', '').strip()

    # Start with all exam papers
    exams = ExamPaper.objects.select_related('subject', 'subject__university').all()

    # Apply filters
    if university_id:
        exams = exams.filter(subject__university_id=university_id)

    if department:
        exams = exams.filter(subject__department__icontains=department)

    if semester:
        exams = exams.filter(subject__semester=int(semester))

    if category:
        exams = exams.filter(subject__category=category)

    if document_type:
        exams = exams.filter(document_type=document_type)

    if search_query:
        exams = exams.filter(subject__name__icontains=search_query)

    # Order results
    exams = exams.order_by('-exam_year', 'exam_period', 'subject__name')

    # Serialize results
    results = []
    for exam in exams:
        results.append({
            'id': exam.id,
            'subject_name': exam.subject.name,
            'university_name': exam.subject.university.name,
            'department': exam.subject.department,
            'semester': exam.subject.semester,
            'category': exam.subject.get_category_display(),
            'document_type': exam.get_document_type_display(),
            'document_type_value': exam.document_type,
            'exam_period': exam.get_exam_period_display() if exam.exam_period else '',
            'exam_year': exam.exam_year or '',
            'group_name': exam.group_name or '',
            'file_url': exam.file.url if exam.file else '',
            'file_name': exam.file.name.split('/')[-1] if exam.file else '',
            'is_pdf': exam.is_pdf(),
            'is_image': exam.is_image(),
        })

    return JsonResponse({'exams': results})


def api_departments(request):
    """API endpoint to get departments for a university"""
    university_id = request.GET.get('university')
    
    if not university_id:
        return JsonResponse({'departments': []})

    departments = Subject.objects.filter(
        university_id=university_id
    ).values_list('department', flat=True).distinct().order_by('department')

    return JsonResponse({'departments': list(departments)})


