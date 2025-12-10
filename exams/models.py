from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator


class University(models.Model):
    """Πανεπιστήμιο"""
    name = models.CharField(max_length=200, verbose_name="Όνομα")
    location = models.CharField(max_length=100, verbose_name="Τοποθεσία")

    class Meta:
        verbose_name = "Πανεπιστήμιο"
        verbose_name_plural = "Πανεπιστήμια"
        ordering = ['name']

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Μάθημα"""
    CATEGORY_CHOICES = [
        ('Υποχρεωτικό', 'Υποχρεωτικό'),
        ('Επιλογής', 'Επιλογής'),
        ('Εργαστήριο', 'Εργαστήριο'),
    ]

    name = models.CharField(max_length=200, verbose_name="Όνομα Μαθήματος")
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="Πανεπιστήμιο")
    department = models.CharField(max_length=200, verbose_name="Τμήμα")
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Εξάμηνο"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Κατηγορία"
    )

    class Meta:
        verbose_name = "Μάθημα"
        verbose_name_plural = "Μαθήματα"
        ordering = ['university', 'department', 'semester', 'name']

    def __str__(self):
        return f"{self.name} - {self.university.name} ({self.department})"


class ExamPaper(models.Model):
    """Έγγραφο (Θέμα Εξέτασης ή Σημείωση)"""
    DOCUMENT_TYPE_CHOICES = [
        ('Θέμα Εξεταστικής', 'Θέμα Εξεταστικής'),
        ('Σημείωση', 'Σημείωση'),
    ]
    
    EXAM_PERIOD_CHOICES = [
        ('Ιουνίου', 'Ιουνίου'),
        ('Σεπτεμβρίου', 'Σεπτεμβρίου'),
        ('Φεβρουαρίου/Ιανουαρίου', 'Φεβρουαρίου/Ιανουαρίου'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Μάθημα")
    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES,
        default='Θέμα Εξεταστικής',
        verbose_name="Τύπος Εγγράφου"
    )
    exam_period = models.CharField(
        max_length=30,
        choices=EXAM_PERIOD_CHOICES,
        blank=True,
        null=True,
        verbose_name="Περίοδος Εξέτασης",
        help_text="Απαιτείται μόνο για θέματα εξεταστικής"
    )
    exam_year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        blank=True,
        null=True,
        verbose_name="Έτος",
        help_text="Απαιτείται μόνο για θέματα εξεταστικής"
    )
    group_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Όνομα Ομάδας",
        help_text="π.χ., Ομάδα Α, Set 2"
    )
    file = models.FileField(
        upload_to='exam_papers/',
        verbose_name="Αρχείο",
        help_text="PDF, PNG, JPG, DOCX",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg', 'docx'])]
    )
    admin_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Σημειώσεις Διαχειριστή"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ημερομηνία Δημιουργίας")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ημερομηνία Ενημέρωσης")

    class Meta:
        verbose_name = "Έγγραφο"
        verbose_name_plural = "Έγγραφα"
        ordering = ['-exam_year', '-created_at', 'subject']

    def __str__(self):
        group_str = f" - {self.group_name}" if self.group_name else ""
        if self.document_type == 'Θέμα Εξεταστικής' and self.exam_period and self.exam_year:
            return f"{self.subject.name} - {self.exam_period} {self.exam_year}{group_str}"
        return f"{self.subject.name} - {self.get_document_type_display()}{group_str}"

    def get_file_extension(self):
        """Returns the file extension"""
        if self.file:
            return self.file.name.split('.')[-1].lower()
        return None

    def is_pdf(self):
        """Check if file is PDF"""
        return self.get_file_extension() == 'pdf'

    def is_image(self):
        """Check if file is an image"""
        return self.get_file_extension() in ['png', 'jpg', 'jpeg', 'gif']

