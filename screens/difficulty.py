import pygame
import config
from screens.base_screen import BaseScreen
from core.button import Button
from core.utils import play_music

class DifficultyScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app)

        # Lista de botones mostrados (Easy, Medium, Hard, Volver)
        self.buttons = []

        # Construcción inicial de la interfaz
        self._build_ui()

    # -------------------------------------------------------
    #   CREACIÓN DE BOTONES DE LA PANTALLA
    # -------------------------------------------------------
    def _build_ui(self):
        w, h = config.WIDTH, config.HEIGHT

        # Tamaño estándar de los botones de dificultad
        button_w, button_h = 260, 60

        spacing = 20                  # separación entre botones
        center_x = w // 2             # centro horizontal de la pantalla
        base_y = h * 0.35             # posición vertical inicial

        # ---------------------------------------------
        # Crear botones para cada dificultad del juego
        # config.DIFFICULTIES = ["Easy", "Medium", "Hard"]
        # ---------------------------------------------
        for i, diff in enumerate(config.DIFFICULTIES):

            rect = (
                center_x - button_w // 2,
                base_y + i * (button_h + spacing),
                button_w,
                button_h
            )

            # Se usa make_callback para capturar el valor "diff" correctamente
            def make_callback(d=diff):
                return lambda: self._set_difficulty(d)

            # Crear botón
            self.buttons.append(
                Button(rect, diff, self.app.font_medium, make_callback())
            )

        # ---------------------------------------------
        # Botón inferior izquierdo: Volver al menú
        # ---------------------------------------------
        back_rect = (20, h - 80, 200, 50)

        self.buttons.append(
            Button(back_rect, "menú", self.app.font_small,
                   lambda: self.go_menu())
        )

    # -------------------------------------------------------
    #   FUNCIÓN QUE SE EJECUTA AL SELECCIONAR UNA DIFICULTAD
    # -------------------------------------------------------
    def _set_difficulty(self, difficulty):

        # Guardar dificultad seleccionada
        self.app.save_data["selected_difficulty"] = difficulty

        # Reiniciar al nivel 0 de esa dificultad
        self.app.save_data["selected_level"] = 0

        # Ir a la pantalla de selección de nivel
        self.go_level()

    # -------------------------------------------------------
    #   CUANDO ENTRAMOS EN ESTA PANTALLA → reproducir música
    # -------------------------------------------------------
    def on_enter(self):
        self.app.current_music = play_music(
            config.MUSIC_DIFFICULTY,
            self.app.current_music
        )

    # -------------------------------------------------------
    #   PROCESAR EVENTOS (clicks, mouse-over, etc.)
    # -------------------------------------------------------
    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    # -------------------------------------------------------
    #   DIBUJAR LA PANTALLA COMPLETA: texto y botones
    # -------------------------------------------------------
    def draw(self):
        s = self.app.screen
        s.fill(config.COLOR_BG)

        w, h = config.WIDTH, config.HEIGHT

        # Título principal
        title = self.app.font_large.render(
            "Elige la dificultad",
            True,
            config.COLOR_TEXT
        )
        s.blit(title, title.get_rect(center=(w//2, h*0.15)))

        # Subtítulo informativo
        subtitle = self.app.font_small.render(
            "Desbloquea todas las fases de una dificultad para acceder a la siguiente.",
            True,
            config.COLOR_TEXT
        )
        s.blit(subtitle, subtitle.get_rect(center=(w//2, h*0.23)))

        # Dibujar todos los botones
        for b in self.buttons:
            b.draw(s)

    # -------------------------------------------------------
    #   CAMBIAR A LA PANTALLA DE SELECCIÓN DE NIVEL
    # -------------------------------------------------------
    def go_level(self):
        from screens.level_select import LevelSelectScreen
        self.app.change_screen(LevelSelectScreen(self.app))

    # -------------------------------------------------------
    #   VOLVER AL MENÚ PRINCIPAL
    # -------------------------------------------------------
    def go_menu(self):
        from screens.main_menu import MainMenuScreen
        self.app.change_screen(MainMenuScreen(self.app))
