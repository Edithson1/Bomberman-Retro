import config
from screens.base_screen import BaseScreen
from core.button import Button
from core.utils import play_music
from core.save_manager import SaveManager


class VictoryScreen(BaseScreen):
    def __init__(self, app, difficulty, level_index, score):
        super().__init__(app)

        # Datos de estado
        self.diff = difficulty
        self.index = level_index
        self.score = score

        # Lista de botones interactivos
        self.buttons = []

        # Construcción de toda la interfaz
        self._build_ui()

    # ---------------------------------------------------------
    #   CREACIÓN DE BOTONES (Menú, Reintentar, Siguiente nivel)
    # ---------------------------------------------------------
    def _build_ui(self):
        w, h = config.WIDTH, config.HEIGHT
        bw, bh = 220, 60
        spacing = 10
        top = 50
        cx, cy = w // 2, h * 0.6

        # Botones ubicados uno debajo del otro
        self.buttons = [
            # Botón para volver al menú principal
            Button((cx - bw // 2, top + cy - (bh + spacing), bw, bh),
                   "Volver al menú",
                   self.app.font_small,
                   lambda: self.go_menu()),

            # Botón para reiniciar el nivel actual
            Button((cx - bw // 2, top + cy, bw, bh),
                   "Reintentar",
                   self.app.font_small,
                   lambda: self.go_gameplay(self.diff, self.index)),

            # Botón para avanzar al siguiente nivel (si está disponible)
            Button((cx - bw // 2, top + cy + (bh + spacing), bw, bh),
                   "Siguiente nivel",
                   self.app.font_small,
                   self._next_level)
        ]

    # ---------------------------------------------------------
    #   MANEJO DE EVENTOS → solo botones
    # ---------------------------------------------------------
    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    # ---------------------------------------------------------
    #   PROCESO DE DESBLOQUEO DE SIGUIENTE NIVEL
    #   → usa SaveManager para actualizar los datos
    # ---------------------------------------------------------
    def up_level(self):
        data = self.app.save_data

        # unlock_next devuelve:
        #   (nuevos_datos, nueva_dificultad, nuevo_indice_de_nivel)
        data, new_d, new_i = SaveManager.unlock_next(data, self.diff, self.index)

        # Guardar estado actualizado del progreso
        SaveManager.save(data)

        return data, new_d, new_i

    # ---------------------------------------------------------
    #   BOTÓN "Siguiente nivel"
    # ---------------------------------------------------------
    def _next_level(self):
        data, new_d, new_i = self.up_level()

        # Si no existe un nivel siguiente → volver al menú
        if new_d is None:
            self.go_menu()
        else:
            # Actualizar selección actual
            data["selected_difficulty"] = new_d
            data["selected_level"] = new_i

            # Saltar directamente al gameplay del nuevo nivel
            self.go_gameplay(new_d, new_i)

    # ---------------------------------------------------------
    #   REPRODUCIR MÚSICA DE VICTORIA AL ENTRAR
    # ---------------------------------------------------------
    def on_enter(self):
        self.app.current_music = play_music(
            config.MUSIC_VICTORY,
            self.app.current_music
        )

    # ---------------------------------------------------------
    #   DIBUJO COMPLETO DE LA PANTALLA DE VICTORIA
    # ---------------------------------------------------------
    def draw(self):
        s = self.app.screen
        s.fill(config.COLOR_BG)
        w, h = config.WIDTH, config.HEIGHT

        # Título principal
        title = self.app.font_large.render("¡Victoria!", True, config.COLOR_TEXT)
        s.blit(title, title.get_rect(center=(w // 2, h * 0.2)))

        # Información del nivel terminado
        lines = [
            f"Dificultad: {self.diff}",
            f"Nivel: {self.index + 1}",
            f"Puntuación: {self.score}"
        ]

        y = h * 0.35
        for line in lines:
            t = self.app.font_medium.render(line, True, config.COLOR_TEXT)
            s.blit(t, t.get_rect(center=(w // 2, y)))
            y += 45

        # Dibujar botones
        for b in self.buttons:
            b.draw(s)

    # ---------------------------------------------------------
    #   REDIRIGE A GAMEPLAY
    #   (Se vuelve a guardar nivel desbloqueado por seguridad)
    # ---------------------------------------------------------
    def go_gameplay(self, new_d, new_i):
        from screens.gameplay import GamePlayScreen
        self.app.change_screen(GamePlayScreen(self.app, new_d, new_i))

        # Se vuelve a ejecutar por seguridad (puedes dejarlo o eliminarlo)
        self.up_level()

    # ---------------------------------------------------------
    #   REDIRIGE AL MENÚ PRINCIPAL
    #   (también actualiza estado del progreso)
    # ---------------------------------------------------------
    def go_menu(self):
        print("hola")
        from screens.main_menu import MainMenuScreen
        self.app.change_screen(MainMenuScreen(self.app))

        # Guardar progreso actualizado
        self.up_level()
