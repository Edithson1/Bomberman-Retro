class BaseScreen:
    """
    Clase base para todas las pantallas del juego (menús, gameplay,
    selección de niveles, victoria, derrota, etc.).

    Sirve como plantilla para que cada pantalla implemente sus propios
    métodos de entrada, manejo de eventos, actualización y dibujo.
    """

    def __init__(self, app):
        """
        Guarda una referencia al controlador principal (app),
        que contiene:
        - ventana (screen)
        - fuentes
        - música
        - datos guardados
        - método para cambiar pantallas
        """
        self.app = app

    def on_enter(self):
        """
        Llamado automáticamente cuando la pantalla se activa.
        Ideal para:
        - iniciar música
        - reiniciar variables internas
        - reproducir animaciones de entrada
        """
        pass

    def handle_event(self, event):
        """
        Manejo de eventos individuales de pygame.
        Cada pantalla decide cómo responder a:
        - teclas
        - clicks del mouse
        - movimientos de mouse
        """
        pass

    def update(self):
        """
        Lógica interna por cuadro.
        Por ejemplo:
        - actualizar animaciones
        - mover entidades
        - verificar colisiones
        - contar tiempo
        """
        pass

    def draw(self):
        """
        Dibujo completo de la pantalla.
        Aquí cada pantalla define:
        - fondo
        - imágenes
        - botones
        - texto
        - HUD
        """
        pass
