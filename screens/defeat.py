import config
from screens.base_screen import BaseScreen
from core.button import Button
from core.utils import play_music


class DefeatScreen(BaseScreen):
    def __init__(self, app, difficulty, level_index):
        super().__init__(app)

        # Dificultad y nivel desde el cual se llegó a la derrota
        self.diff = difficulty
        self.index = level_index

        # Lista de botones a mostrar (Menú, Reintentar)
        self.buttons = []

        # Construir interfaz inicial
        self._build_ui()

    # ---------------------------------------------------------
    #   CREACIÓN DE BOTONES Y DISPOSICIÓN DE LA INTERFAZ
    # ---------------------------------------------------------
    def _build_ui(self):
        w, h = config.WIDTH, config.HEIGHT
        bw, bh = 220, 60       # tamaño de botones
        spacing = 0
        top = 40
        cx, cy = w // 2, h * 0.6

        # Se crean dos botones principales:
        # - Volver al menú
        # - Reintentar el mismo nivel
        self.buttons = [
            Button(
                (cx - bw // 2, top + cy - (bh + spacing // 2), bw, bh),
                "Menú",
                self.app.font_small,
                lambda: self.go_menu()
            ),

            Button(
                (cx - bw // 2, top + cy + (bh + spacing // 2), bw, bh),
                "Reintentar",
                self.app.font_small,
                lambda: self.go_gameplay()
            )
        ]

    # ---------------------------------------------------------
    #   MÚSICA AL ENTRAR EN LA PANTALLA DE DERROTA
    # ---------------------------------------------------------
    def on_enter(self):
        self.app.current_music = play_music(
            config.MUSIC_DEFEAT,
            self.app.current_music
        )

    # ---------------------------------------------------------
    #   MANEJO DE EVENTOS DE LOS BOTONES
    # ---------------------------------------------------------
    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    # ---------------------------------------------------------
    #   DIBUJAR PANTALLA COMPLETA DE DERROTA
    # ---------------------------------------------------------
    def draw(self):
        s = self.app.screen
        s.fill(config.COLOR_BG)

        w, h = config.WIDTH, config.HEIGHT

        # Título grande: "Derrota"
        t = self.app.font_large.render("Derrota", True, config.COLOR_TEXT)
        s.blit(t, t.get_rect(center=(w // 2, h * 0.2)))

        # Mensajes informativos (dificultad, nivel, motivación)
        info = [
            f"Dificultad: {self.diff}",
            f"Nivel: {self.index + 1}",
            "¡Inténtalo nuevamente!"
        ]

        y = h * 0.35
        for line in info:
            txt = self.app.font_medium.render(line, True, config.COLOR_TEXT)
            s.blit(txt, txt.get_rect(center=(w // 2, y)))
            y += 45

        # Dibujar botones (Menú, Reintentar)
        for b in self.buttons:
            b.draw(s)

    # ---------------------------------------------------------
    #   LÓGICA DEL BOTÓN "MENÚ"
    # ---------------------------------------------------------
    def go_menu(self):
        from screens.main_menu import MainMenuScreen
        self.app.change_screen(MainMenuScreen(self.app))

    # ---------------------------------------------------------
    #   LÓGICA DEL BOTÓN "REINTENTAR"
    # ---------------------------------------------------------
    def go_gameplay(self):
        from screens.gameplay import GamePlayScreen
        self.app.change_screen(
            GamePlayScreen(self.app, self.diff, self.index)
        )
