// Funcionalidad del botón "Volver arriba"
document.addEventListener('DOMContentLoaded', function() {
    const scrollToTopBtn = document.getElementById('scrollToTop');
    
    if (scrollToTopBtn) {
        // Mostrar/ocultar botón según el scroll
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        });

        // Scroll suave al hacer click
        scrollToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Animación de entrada para elementos del footer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observar columnas del footer
    const footerColumns = document.querySelectorAll('.footer-column, .footer-about');
    footerColumns.forEach(column => {
        column.style.opacity = '0';
        column.style.transform = 'translateY(20px)';
        column.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(column);
    });
});
