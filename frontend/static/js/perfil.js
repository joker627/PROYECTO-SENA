/**
 * Maneja las interacciones de la página de perfil.
 */

document.addEventListener('DOMContentLoaded', () => {
    const avatarInput = document.getElementById('avatarInput');
    const avatarImg = document.querySelector('.profile-avatar img');

    if (avatarInput) {
        avatarInput.addEventListener('change', function (e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    if (avatarImg) {
                        avatarImg.src = e.target.result;
                    }
                }
                reader.readAsDataURL(this.files[0]);

                // Nota: La subida real de la imagen se implementaría aquí o en un botón aparte
                console.log("Imagen seleccionada:", this.files[0].name);
            }
        });
    }
});
