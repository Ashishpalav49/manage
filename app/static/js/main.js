// Client-side JavaScript for Hospital Management System

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    // Auto close alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (typeof bootstrap !== 'undefined') {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.style.display = 'none';
            }
        }, 5000);
    });
    
    // Initialize tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Appointment date validation
    const appointmentDateInput = document.getElementById('appointment_date');
    if (appointmentDateInput) {
        appointmentDateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            
            if (selectedDate < today) {
                this.setCustomValidity('Appointment date cannot be in the past');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Doctor specialization suggestions
    const specializationInput = document.getElementById('specialization');
    if (specializationInput) {
        const specializations = [
            'Cardiology', 'Dermatology', 'Endocrinology', 'Gastroenterology',
            'Hematology', 'Neurology', 'Oncology', 'Ophthalmology',
            'Orthopedics', 'Pediatrics', 'Psychiatry', 'Radiology',
            'Rheumatology', 'Urology', 'General Medicine', 'Surgery'
        ];
        
        const datalist = document.createElement('datalist');
        datalist.id = 'specialization-list';
        
        specializations.forEach(spec => {
            const option = document.createElement('option');
            option.value = spec;
            datalist.appendChild(option);
        });
        
        document.body.appendChild(datalist);
        specializationInput.setAttribute('list', 'specialization-list');
    }
    
    // Print patient details
    const printButton = document.getElementById('print-patient');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Add event listeners for dashboard action buttons
    addDashboardEventListeners();
});

function addDashboardEventListeners() {
    // Admin dashboard action buttons
    const adminActionButtons = [
        'add-doctor', 'add-patient', 'schedule-appointment', 
        'generate-reports', 'system-settings', 'manage-doctors',
        'manage-patients', 'manage-appointments'
    ];
    
    adminActionButtons.forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const href = this.getAttribute('href');
                if (href) {
                    window.location.href = href;
                }
            });
        }
    });
    
    // Patient dashboard action buttons
    const patientActionButtons = [
        'book-appointment', 'view-medical-history', 'update-profile',
        'request-medical-records', 'contact-support'
    ];
    
    patientActionButtons.forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const href = this.getAttribute('href');
                if (href) {
                    window.location.href = href;
                }
            });
        }
    });
    
    // Add event delegation for dynamically loaded content
    document.body.addEventListener('click', function(e) {
        // Check if the clicked element is a button or link with specific classes
        if (e.target.closest('.btn-primary') || e.target.closest('.btn-success') || 
            e.target.closest('.btn-info') || e.target.closest('.list-group-item')) {
            
            const clickedElement = e.target.closest('.btn-primary') || 
                                  e.target.closest('.btn-success') || 
                                  e.target.closest('.btn-info') ||
                                  e.target.closest('.list-group-item');
            
            const href = clickedElement.getAttribute('href');
            if (href && href !== '#' && !href.startsWith('javascript:')) {
                e.preventDefault();
                window.location.href = href;
            }
        }
    });
}

// Confirm deletion - using event delegation for dynamically added elements
document.body.addEventListener('click', function(e) {
    if (e.target.closest('.btn-danger[data-confirm="true"]')) {
        const confirmButton = e.target.closest('.btn-danger[data-confirm="true"]');
        if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
            e.preventDefault();
        }
    }
});