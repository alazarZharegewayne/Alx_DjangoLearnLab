document.addEventListener('DOMContentLoaded', function() {
    console.log('Login page loaded');
    
    const form = document.querySelector('.login-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Signing In...';
            }
        });
    }
    
    const usernameField = document.getElementById('id_username');
    if (usernameField) {
        usernameField.focus();
    }
});
