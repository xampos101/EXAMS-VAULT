// Exam Vault - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const documentTypeSelect = document.getElementById('document_type');
    const universitySelect = document.getElementById('university');
    const departmentSelect = document.getElementById('department');
    const semesterSelect = document.getElementById('semester');
    const categorySelect = document.getElementById('category');
    const searchInput = document.getElementById('search');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const resultsContainer = document.getElementById('resultsContainer');
    const loadingState = document.getElementById('loadingState');
    const noResultsState = document.getElementById('noResultsState');
    const examCardTemplate = document.getElementById('examCardTemplate');
    const viewerModal = document.getElementById('viewerModal');
    const viewerContent = document.getElementById('viewerContent');
    const closeViewer = document.getElementById('closeViewer');

    let debounceTimer;

    // Load exams on page load
    loadExams();

    // Document type change
    documentTypeSelect.addEventListener('change', function() {
        loadExams();
    });

    // University change - load departments
    universitySelect.addEventListener('change', function() {
        const universityId = this.value;
        if (universityId) {
            loadDepartments(universityId);
            departmentSelect.disabled = false;
        } else {
            departmentSelect.innerHTML = '<option value="">Επιλέξτε Πανεπιστήμιο</option>';
            departmentSelect.disabled = true;
        }
        loadExams();
    });

    // Department change
    departmentSelect.addEventListener('change', function() {
        loadExams();
    });

    // Semester change
    semesterSelect.addEventListener('change', function() {
        loadExams();
    });

    // Category change
    categorySelect.addEventListener('change', function() {
        loadExams();
    });

    // Search input with debounce
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            loadExams();
        }, 300);
    });

    // Reset filters
    resetFiltersBtn.addEventListener('click', function() {
        filterForm.reset();
        departmentSelect.innerHTML = '<option value="">Επιλέξτε Πανεπιστήμιο</option>';
        departmentSelect.disabled = true;
        loadExams();
    });

    // Viewer modal handlers
    closeViewer.addEventListener('click', function() {
        viewerModal.classList.add('hidden');
        viewerContent.innerHTML = '';
    });

    viewerModal.addEventListener('click', function(e) {
        if (e.target === viewerModal) {
            viewerModal.classList.add('hidden');
            viewerContent.innerHTML = '';
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !viewerModal.classList.contains('hidden')) {
            viewerModal.classList.add('hidden');
            viewerContent.innerHTML = '';
        }
    });

    // Load departments for a university
    function loadDepartments(universityId) {
        fetch(`/api/departments/?university=${universityId}`)
            .then(response => response.json())
            .then(data => {
                departmentSelect.innerHTML = '<option value="">Όλα τα Τμήματα</option>';
                data.departments.forEach(department => {
                    const option = document.createElement('option');
                    option.value = department;
                    option.textContent = department;
                    departmentSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error loading departments:', error);
            });
    }

    // Load exams based on filters
    function loadExams() {
        // Show loading state
        loadingState.classList.remove('hidden');
        noResultsState.classList.add('hidden');
        resultsContainer.innerHTML = '';

        // Build query string
        const params = new URLSearchParams();
        if (documentTypeSelect.value) params.append('document_type', documentTypeSelect.value);
        if (universitySelect.value) params.append('university', universitySelect.value);
        if (departmentSelect.value) params.append('department', departmentSelect.value);
        if (semesterSelect.value) params.append('semester', semesterSelect.value);
        if (categorySelect.value) params.append('category', categorySelect.value);
        if (searchInput.value.trim()) params.append('search', searchInput.value.trim());

        // Fetch exams
        fetch(`/api/exams/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                loadingState.classList.add('hidden');

                if (data.exams.length === 0) {
                    noResultsState.classList.remove('hidden');
                    return;
                }

                noResultsState.classList.add('hidden');
                displayExams(data.exams);
            })
            .catch(error => {
                console.error('Error loading exams:', error);
                loadingState.classList.add('hidden');
                noResultsState.classList.remove('hidden');
            });
    }

    // Display exams in cards
    function displayExams(exams) {
        resultsContainer.innerHTML = '';

        exams.forEach((exam, index) => {
            const card = examCardTemplate.content.cloneNode(true);
            
            // Fill in exam data
            card.querySelector('.exam-subject-name').textContent = exam.subject_name;
            card.querySelector('.exam-university').textContent = exam.university_name;
            card.querySelector('.exam-department').textContent = exam.department;
            card.querySelector('.exam-semester').textContent = exam.semester;
            
            // Handle exam period and year (only for exam papers)
            const periodElement = card.querySelector('.exam-period');
            const yearElement = card.querySelector('.exam-year');
            const dateLabel = card.querySelector('.exam-date-label');
            const dateValue = card.querySelector('.exam-date-value');
            
            if (exam.document_type_value === 'Θέμα Εξεταστικής' && exam.exam_period && exam.exam_year) {
                periodElement.textContent = exam.exam_period;
                yearElement.textContent = exam.exam_year;
                dateLabel.textContent = 'Τελευταια Εξεταστικη';
            } else {
                dateLabel.textContent = 'Τύπος Εγγράφου';
                dateValue.innerHTML = `<span class="font-medium text-white">${exam.document_type}</span>`;
            }
            
            card.querySelector('.exam-category').textContent = exam.category;
            
            // Download link
            const downloadLink = card.querySelector('.exam-download-link');
            downloadLink.href = exam.file_url;
            downloadLink.download = exam.file_name;
            
            // View button
            const viewButton = card.querySelector('.exam-view-link');
            viewButton.addEventListener('click', function() {
                openViewer(exam);
            });

            // Add delay for staggered animation
            const cardElement = card.querySelector('.exam-card-enter');
            cardElement.style.animationDelay = `${index * 0.05}s`;

            resultsContainer.appendChild(card);
        });
    }
    
    // Open viewer modal
    function openViewer(exam) {
        viewerContent.innerHTML = '';
        
        if (exam.is_pdf) {
            // PDF viewer
            viewerContent.innerHTML = `
                <iframe src="${exam.file_url}" class="w-full h-full rounded-lg" frameborder="0"></iframe>
            `;
        } else if (exam.is_image) {
            // Image viewer
            viewerContent.innerHTML = `
                <img src="${exam.file_url}" alt="${exam.subject_name}" class="max-w-full max-h-full object-contain rounded-lg">
            `;
        } else {
            // Other file types - show download option
            viewerContent.innerHTML = `
                <div class="text-center text-white">
                    <svg class="w-24 h-24 mx-auto mb-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                    </svg>
                    <p class="text-xl mb-4">Αυτός ο τύπος αρχείου δεν μπορεί να προβληθεί</p>
                    <a href="${exam.file_url}" download="${exam.file_name}" class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-600 to-cyan-600 text-white font-bold rounded-xl hover:shadow-lg transition-all">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                        </svg>
                        Κατέβασμα Αρχείου
                    </a>
                </div>
            `;
        }
        
        viewerModal.classList.remove('hidden');
    }
});
