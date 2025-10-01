from flask import render_template

def register_error_handlers(app):
    """
    Registra los manejadores de errores personalizados para la aplicación Flask.
    """
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Maneja errores 404 - Página no encontrada"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Maneja errores 403 - Acceso prohibido"""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores 500 - Error interno del servidor"""
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Maneja errores 400 - Solicitud incorrecta"""
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Maneja errores 405 - Método no permitido"""
        return render_template('errors/405.html'), 405
    
    # Manejador genérico para otros errores
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Maneja excepciones no capturadas"""
        # Si es un error HTTP, usar el código de estado original
        if hasattr(error, 'code'):
            return render_template('errors/500.html'), error.code
        # Para otros errores, devolver 500
        return render_template('errors/500.html'), 500