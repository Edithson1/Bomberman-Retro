import pygame
from config import WIDTH, HEIGHT, FPS
from core.save_manager import SaveManager
from core.utils import load_font
from screens.main_menu import MainMenuScreen


class App:
    """
    Clase principal del juego.
    Se encarga de:
      - Crear la ventana
      - Cargar fuentes
      - Controlar la pantalla activa
      - Mantener el loop principal
      - Manejar guardado/carga de progreso
    """

    def __init__(self):
        # ------------------------------------------------------
        # Crear ventana de tamaño definido en config.py
        # ------------------------------------------------------
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bombman App")

        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()

        # ------------------------------------------------------
        # Cargar tipografías desde archivo o fallback
        # ------------------------------------------------------
        self.font_small = load_font(18)
        self.font_medium = load_font(26)
        self.font_large = load_font(40)

        # ------------------------------------------------------
        # Cargar archivo de guardado (niveles desbloqueados)
        # ------------------------------------------------------
        self.save_data = SaveManager.load()

        # Música actualmente activa (para evitar recargar)
        self.current_music = None

        # ------------------------------------------------------
        # Inicializar la pantalla principal del menú
        # ------------------------------------------------------
        self.current_screen = MainMenuScreen(self)
        self.current_screen.on_enter()   # Llama a la música y configuraciones iniciales

    # ======================================================
    # Cambia la pantalla actual
    # screen → instancia de cualquier clase derivada de BaseScreen
    # ======================================================
    def change_screen(self, screen):
        self.current_screen = screen
        screen.on_enter()  # Cada pantalla define qué hacer al entrar en ella

    # ======================================================
    # Loop principal del juego
    # Controla eventos, actualiza estados, dibuja y mantiene FPS
    # ======================================================
    def run(self):
        while True:
            # -------------------------
            # Manejo de eventos
            # -------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Guardar progreso antes de cerrar
                    SaveManager.save(self.save_data)
                    pygame.quit()
                    return

                # Pasar eventos a la pantalla actual
                self.current_screen.handle_event(event)

            # -------------------------
            # Lógica de juego
            # -------------------------
            self.current_screen.update()

            # -------------------------
            # Dibujar pantalla
            # -------------------------
            self.current_screen.draw()

            # Mostrar frame
            pygame.display.flip()

            # Mantener FPS estables
            self.clock.tick(FPS)

