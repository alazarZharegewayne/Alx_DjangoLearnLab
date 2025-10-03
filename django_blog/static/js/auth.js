// Authentication-specific JavaScript for login and register pages

document.addEventListener('DOMContentLoaded', function() {
    console.log('Authentication scripts loaded');
    
    // Password strength indicator for registration page
    const passwordInput = document.getElementById('id_password1');
    if (passwordInput) {
        initPasswordStrengthChecker();
    }
    
    // Real-time form validation
    initFormValidation();
    
    // Auto-focus first form field
    autoFocusFirstField();
    
    // Enhanced form submission
    enhanceFormSubmission();
});

function initPasswordStrengthChecker() {
    const passwordInput = document.getElementById('id_password1');
    const strengthMeter = document.createElement('div');
    strengthMeter.className = 'password-strength mt-2';
    strengthMeter.innerHTML = `
        <div class="progress" style="height: 5px;">
            <div class="progress-bar" role="progressbar" style="width: 0%"></div>
        </div>
        <small class="strength-text text-muted"></small>
    `;
    
    passwordInput.parentNode.appendChild(strengthMeter);
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strength = calculatePasswordStrength(password);
        updateStrengthMeter(strengthMeter, strength);
    });
}

function calculatePasswordStrength(password) {
    let score = 0;
    
    if (!password) return { score: 0, text: 'Enter a password' };
    
    // Length check
    if (password.length >= 8) score += 25;
    if (password.length >= 12) score += 15;
    
    // Character variety
    if (/[a-z]/.test(password)) score += 10;
    if (/[A-Z]/.test(password)) score += 10;
    if (/[0-9]/.test(password)) score += 10;
    if (/[^a-zA-Z0-9]/.test(password)) score += 10;
    
    // Common pattern penalties
    if (/(.)\1{2,}/.test(password)) score -= 10; // Repeated characters
    if (/12345|abcde|qwerty/.test(password.toLowerCase())) score -= 20; // Common sequences
    
    // Determine strength level
    if (score >= 70) return { score: 100, text: 'Strong password' };
    if (score >= 50) return { score: 75, text: 'Good password' };
    if (score >= 30) return { score: 50, text: 'Fair password' };
    if (score >= 10) return { score: 25, text: 'Weak password' };
    return { score: 0, text: 'Very weak password' };
}

function updateStrengthMeter(meter, strength) {
    const progressBar = meter.querySelector('.progress-bar');
    const strengthText = meter.querySelector('.strength-text');
    
    progressBar.style.width = strength.score + '%';
    
    // Update color based on strength
    if (strength.score >= 70) {
        progressBar.className = 'progress-bar bg-success';
    } else if (strength.score >= 50) {
        progressBar.className = 'progress-bar bg-info';
    } else if (strength.score >= 30) {
        progressBar.className = 'progress-bar bg-warning';
    } else {
        progressBar.className = 'progress-bar bg-danger';
    }
    
    strengthText.textContent = strength.text;
}

function initFormValidation() {
    const forms = document.querySelectorAll('.auth-form form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    
    clearFieldError(field);
    
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required.');
        return false;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email address.');
            return false;
        }
    }
    
    // Password confirmation validation
    if (fieldName === 'password2' && value) {
        const password1 = document.getElementById('id_password1').value;
        if (password1 !== value) {
            showFieldError(field, 'Passwords do not match.');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function autoFocusFirstField() {
    const firstInput = document.querySelector('.auth-form input:not([type="hidden"])');
    if (firstInput) {
        firstInput.focus();
    }
}

function enhanceFormSubmission() {
    const forms = document.querySelectorAll('.auth-form form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const inputs = this.querySelectorAll('input[required]');
            
            // Validate all required fields
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showFormError(this, 'Please correct the errors above.');
                return;
            }
            
            // Add loading state to submit button
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('btn-loading');
            }
        });
    });
}

function showFormError(form, message) {
    let alertDiv = form.querySelector('.form-error-alert');
    if (!alertDiv) {
        alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger auth-alert form-error-alert';
        form.insertBefore(alertDiv, form.firstChild);
    }
    
    alertDiv.textContent = message;
}

// Toggle password visibility
function initPasswordToggle() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordField = document.getElementById(targetId);
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                passwordField.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPasswordToggle);
} else {
    initPasswordToggle();
}
