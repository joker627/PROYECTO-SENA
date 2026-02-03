// Toggle password visibility
document.querySelector('.toggle-password')?.addEventListener('click', function () {
    const passwordInput = document.getElementById('contrasena');
    const eyeIcon = this.querySelector('.eye-icon');
    const eyeOffIcon = this.querySelector('.eye-off-icon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.add('hidden');
        eyeOffIcon.classList.remove('hidden');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('hidden');
        eyeOffIcon.classList.add('hidden');
    }
});
