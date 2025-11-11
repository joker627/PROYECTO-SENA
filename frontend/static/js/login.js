document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.password-toggle').forEach(btn => {
        btn.addEventListener('click', function(e){
            // Evitar comportamiento por defecto y mantener foco
            if (e && typeof e.preventDefault === 'function') e.preventDefault();
            const input = this.parentElement.querySelector('input[type="password"], input[type="text"]');
            if (!input) return;
            const icon = this.querySelector('i');
            const wasPassword = input.type === 'password';
            // Toggle input type: if it was password => show (text), otherwise hide (password)
            input.type = wasPassword ? 'text' : 'password';
            // Update icon classes: show eye when hidden, eye-slash when visible
            if (icon) {
                if (input.type === 'text') {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
            // Update accessible label: now input.type === 'text' means visible -> label should say 'Ocultar contraseña'
            this.setAttribute('aria-label', input.type === 'text' ? 'Ocultar contraseña' : 'Mostrar contraseña');
            // Devolver el foco al input (buena UX)
            try { input.focus(); } catch(err) {}
        });
    });
});