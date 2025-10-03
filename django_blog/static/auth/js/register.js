// Register page specific JavaScript
console.log('Register page static files loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    // Enhanced form submission
    const registerForm = document.querySelector('.register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating Account...';
            }
        });
    }
    
    // Password match validation
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    
    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (password1.value !== password2.value && password2.value.length > 0) {
                password2.classList.add('is-invalid');
                let errorDiv = password2.parentNode.querySelector('.password-match-error');
                if (!errorDiv) {
                    errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback password-match-error';
                    password2.parentNode.appendChild(errorDiv);
                }
                errorDiv.textContent = 'Passwords do not match.';
            } else {
                password2.classList.remove('is-invalid');
                const errorDiv = password2.parentNode.querySelector('.password-match-error');
                if (errorDiv) {
                    errorDiv.remove();
                }
            }
        });
    }
    
    // Clear errors on input
    const inputs = document.querySelectorAll('.register-form input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
});
