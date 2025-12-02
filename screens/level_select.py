import pygame
import config
from screens.base_screen import BaseScreen
from core.button import Button
from core.utils import play_music
from screens.difficulty import DifficultyScreen


class LevelSelectScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app)

        # Lista de botones (menú, dificultad, flechas de scroll)
        self.buttons = []

        # Construcción inicial de elementos UI
        self._build_ui()

    # ---------------------------------------------------------
    #   CREACIÓN DE BOTONES PRINCIPALES DE LA PANTALLA
    # ---------------------------------------------------------
    def _build_ui(self):
        w, h = config.WIDTH, config.HEIGHT

        # -----------------------------
        # Botón: volver al menú principal
        # -----------------------------
        self.buttons.append(
            Button(
                (20, h - 80, 200, 50),
                "Menú",
                self.app.font_small,
                lambda: self.go_menu()
            )
        )

        # -----------------------------
        # Botón: volver a selección de dificultad
        # -----------------------------
        self.buttons.append(
            Button(
                (240, h - 80, 200, 50),
                "Dificultad",
                self.app.font_small,
                lambda: self.app.change_screen(DifficultyScreen(self.app))
            )
        )

        # -----------------------------
        # Flechas izquierda/derecha para desplazarse entre niveles
        # -----------------------------
        mid_y = h * 0.55

        # Flecha izquierda
        self.buttons.append(
            Button(
                (w * 0.05, mid_y - 30, 60, 60),
                "<",
                self.app.font_large,
                self._scroll_left
            )
        )

        # Flecha derecha
        self.buttons.append(
            Button(
                (w * 0.90, mid_y - 30, 60, 60),
                ">",
                self.app.font_large,
                self._scroll_right
            )
        )

    # ---------------------------------------------------------
    #   DESPLAZARSE A UN NIVEL ANTERIOR (si está disponible)
    # ---------------------------------------------------------
    def _scroll_left(self):
        level = self.app.save_data["selected_level"]
        if level > 0:
            self.app.save_data["selected_level"] -= 1

    # ---------------------------------------------------------
    #   DESPLAZARSE A UN NIVEL SIGUIENTE (si está disponible)
    # ---------------------------------------------------------
    def _scroll_right(self):
        level = self.app.save_data["selected_level"]
        if level < config.LEVELS_PER_DIFFICULTY - 1:
            self.app.save_data["selected_level"] += 1

    # ---------------------------------------------------------
    #   CUANDO ENTRAMOS A ESTA PANTALLA → cargar música
    # ---------------------------------------------------------
    def on_enter(self):
        self.app.current_music = play_music(
            config.MUSIC_LEVEL_SELECT,
            self.app.current_music
        )

    # ---------------------------------------------------------
    #   CALCULAR POSICIONES DE LOS ÍCONOS DE NIVELES
    # ---------------------------------------------------------
    def _compute_level_icons(self):
        """
        Devuelve una lista de pygame.Rect indicando la posición de cada
        ícono de nivel (centrados horizontalmente).
        """
        w = config.WIDTH
        h = config.HEIGHT
        N = config.LEVELS_PER_DIFFICULTY

        icon_w = 120
        icon_h = 140
        padding = 20

        # Calcular ancho total del carrusel de niveles
        total_width = N * icon_w + (N - 1) * padding
        start_x = (w - total_width) // 2
        y = int(h * 0.55 - icon_h // 2)

        # Generar rectángulos de cada icono
        rects = []
        for i in range(N):
            rects.append(
                pygame.Rect(start_x + i * (icon_w + padding), y, icon_w, icon_h)
            )

        return rects

    # ---------------------------------------------------------
    #   MANEJO DE EVENTOS (teclado + mouse)
    # ---------------------------------------------------------
    def handle_event(self, event):

        # Procesar eventos de botones
        for b in self.buttons:
            b.handle_event(event)

        # ENTER o ESPACIO → intentar entrar al nivel seleccionado
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                diff = self.app.save_data["selected_difficulty"]
                lvl_index = self.app.save_data["selected_level"]
                unlocked = self.app.save_data["levels_unlocked"][diff]

                # Solo permite jugar si el nivel está desbloqueado
                if unlocked[lvl_index]:
                    self.go_gameplay(diff, lvl_index)

        # Click en íconos de nivel
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            rects = self._compute_level_icons()
            diff = self.app.save_data["selected_difficulty"]
            unlocked = self.app.save_data["levels_unlocked"][diff]

            # Detectar si se hizo click sobre un nivel
            for idx, r in enumerate(rects):
                if r.collidepoint(event.pos):

                    # Si está desbloqueado → jugar
                    if unlocked[idx]:
                        self.app.save_data["selected_level"] = idx
                        self.go_gameplay(diff, idx)

                    break

    # ---------------------------------------------------------
    #   DIBUJAR TODA LA PANTALLA DE SELECCIÓN DE NIVEL
    # ---------------------------------------------------------
    def draw(self):
        s = self.app.screen
        s.fill(config.COLOR_BG)
        w, h = config.WIDTH, config.HEIGHT

        diff = self.app.save_data["selected_difficulty"]
        lvl_index = self.app.save_data["selected_level"]
        unlocked = self.app.save_data["levels_unlocked"][diff]

        # Título
        t = self.app.font_large.render("Selecciona un nivel", True, config.COLOR_TEXT)
        s.blit(t, t.get_rect(center=(w // 2, 80)))

        # Dificultad actual
        d = self.app.font_medium.render(f"Dificultad: {diff}", True, config.COLOR_TEXT)
        s.blit(d, d.get_rect(center=(w // 2, 140)))

        # Íconos de niveles
        rects = self._compute_level_icons()
        for idx, r in enumerate(rects):

            # Color según si está seleccionado o no
            color = (40, 40, 80) if idx != lvl_index else (100, 40, 160)

            # Fondo del ícono
            pygame.draw.rect(s, color, r, border_radius=12)
            pygame.draw.rect(s, (180, 180, 255), r, 3, border_radius=12)

            # Número del nivel
            label = self.app.font_large.render(str(idx + 1), True, config.COLOR_TEXT)
            s.blit(label, label.get_rect(center=(r.centerx, r.centery - 20)))

            # Texto "LEVEL"
            sub = self.app.font_small.render("LEVEL", True, config.COLOR_TEXT)
            s.blit(sub, sub.get_rect(center=(r.centerx, r.bottom - 25)))

            # Si está bloqueado → sombrear + icono candado
            if not unlocked[idx]:
                overlay = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                s.blit(overlay, r.topleft)

                # Candado (imagen o fallback a emoji)
                try:
                    lock_img = pygame.image.load(config.LOCK_IMAGE_PATH).convert_alpha()
                    tamaño = 50
                    lock_img = pygame.transform.smoothscale(lock_img, (tamaño, tamaño))
                    lock_rect = lock_img.get_rect(center=r.center)
                    s.blit(lock_img, lock_rect)
                except:
                    lock = self.app.font_medium.render("🔒", True, config.COLOR_TEXT)
                    s.blit(lock, lock.get_rect(center=r.center))

        # Dibujar botones inferiores
        for b in self.buttons:
            b.draw(s)

    # ---------------------------------------------------------
    #   CAMBIAR A MENÚ PRINCIPAL
    # ---------------------------------------------------------
    def go_menu(self):
        from screens.main_menu import MainMenuScreen
        self.app.change_screen(MainMenuScreen(self.app))

    # ---------------------------------------------------------
    #   IR A GAMEPLAY DESDE NIVEL SELECCIONADO
    # ---------------------------------------------------------
    def go_gameplay(self, diff, idx):
        from screens.gameplay import GamePlayScreen
        self.app.change_screen(
            GamePlayScreen(self.app, diff, idx)
        )