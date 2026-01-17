/**
 * Login - Optimizado
 */
document.querySelector('.toggle-password')?.addEventListener('click', function() {
    const input = document.getElementById('contrasena');
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    this.querySelector('.eye-icon').classList.toggle('hidden', show);
    this.querySelector('.eye-off-icon').classList.toggle('hidden', !show);
});
