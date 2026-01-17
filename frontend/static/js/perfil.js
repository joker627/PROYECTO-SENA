/**
 * Perfil - Optimizado
 */
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('avatarInput');
    const img = document.querySelector('.profile-avatar img');
    
    if (input && img) {
        input.onchange = function() {
            if (this.files?.[0]) {
                const reader = new FileReader();
                reader.onload = (e) => img.src = e.target.result;
                reader.readAsDataURL(this.files[0]);
            }
        };
    }
});
