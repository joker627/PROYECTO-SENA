"""Pruebas de carga con Locust para API SignTechnology."""

from locust import HttpUser, task, between
import random
import logging

logger = logging.getLogger(__name__)

class SignTechnologyUser(HttpUser):
    """Usuario simulado para pruebas de carga."""
    
    wait_time = between(1, 3)  # Espera entre 1-3 segundos entre requests
    token = None
    
    def on_start(self):
        """Se ejecuta al iniciar cada usuario - hace login."""
        response = self.client.post("/api/v1/auth/login", json={
            "correo": "jorgemanuelsantanablanco2@gmail.com",
            "contrasena": "manueldev"
        })
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.client.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            logger.error(
                f"Login failed with status code {response.status_code}. "
                "Unable to authenticate user for load testing."
            )
            # Stop this user to prevent subsequent failed requests
            self.stop()
    
    @task(3)
    def get_estadisticas(self):
        """Obtiene estadísticas del sistema (peso 3)."""
        self.client.get("/api/v1/estadisticas/")
    
    @task(2)
    def get_usuarios(self):
        """Lista usuarios paginados (peso 2)."""
        self.client.get("/api/v1/usuarios/?skip=0&limit=20")
    
    @task(2)
    def get_contribuciones(self):
        """Lista contribuciones (peso 2)."""
        self.client.get("/api/v1/contribuciones/?skip=0&limit=20")
    
    @task(2)
    def get_reportes(self):
        """Lista reportes (peso 2)."""
        self.client.get("/api/v1/reportes/?skip=0&limit=20")
    
    @task(1)
    def get_perfil(self):
        """Obtiene perfil del usuario (peso 1)."""
        self.client.get("/api/v1/usuarios/me")
    
    @task(1)
    def get_stats_contribuciones(self):
        """Estadísticas de contribuciones (peso 1)."""
        self.client.get("/api/v1/contribuciones/stats")
    
    @task(1)
    def get_stats_reportes(self):
        """Estadísticas de reportes (peso 1)."""
        self.client.get("/api/v1/reportes/stats")
