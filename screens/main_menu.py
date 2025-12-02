import pygame
from screens.base_screen import BaseScreen
from core.button import Button
from core.utils import play_music
import config
from screens.difficulty import DifficultyScreen
from screens.level_select import LevelSelectScreen


class MainMenuScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app)

        # Lista de botones principales del menú
        self.buttons = []

        # Lista de textos informativos del panel "Cómo jugar"
        self.info = []

        # Construcción inicial de todos los elementos visuales
        self._build_ui()

    # ---------------------------------------------------------
    #   CREACIÓN DE BOTONES Y TEXTO DEL MENÚ PRINCIPAL
    # ---------------------------------------------------------
    def _build_ui(self):
        w, h = config.WIDTH, config.HEIGHT

        # ---------------------------------------------
        # Botones principales: Niveles y Dificultad
        # ---------------------------------------------
        self.buttons = [
            # Botón para ir a selección de niveles
            Button(
                (w // 1.5, h * 0.35, 260, 60),
                "Niveles",
                self.app.font_medium,
                lambda: self.app.change_screen(LevelSelectScreen(self.app))
            ),

            # Botón para ir a selección de dificultad
            Button(
                (w // 1.5, h * 0.65, 260, 60),
                "Dificultad",
                self.app.font_medium,
                lambda: self.app.change_screen(DifficultyScreen(self.app))
            )
        ]

        # ---------------------------------------------
        # Texto informativo del panel lateral
        # ---------------------------------------------
        self.info = [
            "BombMan:",
            "- Movimiento con flechas",
            "- Bomba con ESPACIO",
            "- Explosiones en cruz",
            "- Destruye bloques y enemigos"
        ]

    # ---------------------------------------------------------
    #   AL ENTRAR → reproducir música del menú
    # ---------------------------------------------------------
    def on_enter(self):
        self.app.current_music = play_music(
            config.MUSIC_MENU,
            self.app.current_music
        )

    # ---------------------------------------------------------
    #   MANEJO DE EVENTOS PARA BOTONES
    # ---------------------------------------------------------
    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    # ---------------------------------------------------------
    #   DIBUJO COMPLETO DE LA PANTALLA DEL MENÚ PRINCIPAL
    # ---------------------------------------------------------
    def draw(self):
        s = self.app.screen
        s.fill(config.COLOR_BG)

        # -----------------------------------------------------
        # Títulos principales: "Bombman" + "Menú Principal"
        # -----------------------------------------------------
        title = self.app.font_large.render("Bombman", True, config.COLOR_TEXT)
        s.blit(title, title.get_rect(center=(config.WIDTH // 2, 60)))

        subtitle = self.app.font_medium.render("Menú Principal", True, config.COLOR_TEXT)
        s.blit(subtitle, subtitle.get_rect(center=(config.WIDTH // 2, 120)))

        # -----------------------------------------------------
        # Panel lateral negro traslúcido con borde
        # -----------------------------------------------------
        panel_x = 140
        panel_y = 190
        panel_w = 430
        panel_h = 260

        # Fondo del panel (tono oscuro)
        pygame.draw.rect(
            s,
            (0, 0, 0, 120),
            (panel_x, panel_y, panel_w, panel_h),
            border_radius=12
        )

        # Borde del panel
        pygame.draw.rect(
            s,
            config.COLOR_TEXT,
            (panel_x, panel_y, panel_w, panel_h),
            2,
            border_radius=12
        )

        # -----------------------------------------------------
        # Texto dentro del panel: "Cómo jugar"
        # -----------------------------------------------------
        y = panel_y + 20

        header = self.app.font_medium.render("Cómo Jugar", True, config.COLOR_TEXT)
        s.blit(header, (panel_x + 20, y))
        y += header.get_height() + 10

        # Listado de reglas y controles
        for line in self.info:
            t = self.app.font_small.render(line, True, config.COLOR_TEXT)
            s.blit(t, (panel_x + 20, y))
            y += t.get_height() + 15

        # -----------------------------------------------------
        # Dibujar botones ("Niveles" y "Dificultad")
        # -----------------------------------------------------
        for b in self.buttons:
            b.draw(s)

