// Login page specific JavaScript
console.log('Login page static files loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus username field
    const usernameField = document.getElementById('id_username');
    if (usernameField) {
        usernameField.focus();
    }
    
    // Enhanced form submission
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Signing In...';
            }
        });
    }
    
    // Clear errors on input
    const inputs = document.querySelectorAll('.login-form input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });
});
