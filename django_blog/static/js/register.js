document.addEventListener('DOMContentLoaded', function() {
    console.log('Register page loaded');
    
    const form = document.querySelector('.register-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating Account...';
            }
        });
    }
    
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    
    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (password1.value !== password2.value) {
                password2.classList.add('is-invalid');
            } else {
                password2.classList.remove('is-invalid');
            }
        });
    }
});
