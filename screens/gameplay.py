import pygame
import config
from screens.base_screen import BaseScreen
from core.utils import play_music
from core.maps import LEVEL_MAPS
from core.entity_generator import generate_entities

class GamePlayScreen(BaseScreen):
    def __init__(self, app, difficulty, level_index):
        super().__init__(app)

        # -------------------------------
        # DATOS DE NIVEL Y DIFICULTAD
        # -------------------------------
        self.diff = difficulty                  # dificultad elegida
        self.level_index = level_index          # índice del nivel actual
        self.start_ticks = pygame.time.get_ticks()  # tiempo inicial usado para calcular score

        # Configuración dependiente de la dificultad
        cfg = config.DIFFICULTY_CONFIG[self.diff]
        self.enemy_speed_mod = cfg["enemy_speed"]
        self.enemy_ai_type = cfg["enemy_ai"]
        self.powerup_drop_rate = cfg["powerup_drop_rate"]
        self.bomb_timer_default = cfg["bomb_time"]
        self.time_limit = cfg["time_limit"]
        self.extra_fire = cfg["extra_fire"]
        self.initial_player_lives = cfg["player_lives"]

        # -------------------------------
        # ENTIDADES Y ESTRUCTURAS DEL JUEGO
        # -------------------------------
        self.blocks = []
        self.enemies = []
        self.items = []
        self.bombs = []
        self.explosions = []
        self.player = None
        self.portal = None

        # Tamaño de tiles (cuadrícula)
        self.tile = 32

        # Copia la matriz del mapa como lista de listas editable
        self.map = [list(row) for row in LEVEL_MAPS[level_index]]

        # Genera entidades según la matriz del nivel
        generate_entities(self, self.map)

        # Aplica configuración inicial al jugador
        if self.player:
            self.player.lives = self.initial_player_lives
            self.player.bomb_range += self.extra_fire

        # Cargar imagen del piso (pasto verde)
        self.grass_img = pygame.image.load("assets/images/grass.jpg").convert_alpha()
        self.grass_img = pygame.transform.scale(self.grass_img, (self.tile, self.tile))

    def on_enter(self):
        """Acciones al entrar en la pantalla: reproducir música del nivel."""
        self.app.current_music = play_music(config.MUSIC_GAME, self.app.current_music)

    def handle_event(self, event):
        """Procesa entradas del usuario: movimiento, bombas, escape, etc."""
        if self.player:
            self.player.handle_input(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_level()

    def update(self, dt=16):
        """Actualiza toda la lógica del juego, enemigos, bombas, explosiones, colisiones, etc."""

        # -----------------------
        # Actualizar jugador
        # -----------------------
        if self.player and not self.player.dead:
            self.player.update(dt, self)

        # -----------------------
        # Actualizar bombas
        # -----------------------
        for b in self.bombs:
            b.update(dt, self)
        self.bombs = [b for b in self.bombs if not b.dead]

        # -----------------------
        # Actualizar explosiones
        # -----------------------
        for e in self.explosions:
            e.update(dt, self)
        self.explosions = [e for e in self.explosions if not e.dead]

        # -----------------------
        # Actualizar enemigos
        # -----------------------
        for en in self.enemies:
            en.update(dt, self)

        # -----------------------
        # Daño al jugador por explosiones
        # -----------------------
        if self.player and not self.player.dead:
            for e in self.explosions:
                if int(self.player.x) == e.x and int(self.player.y) == e.y:
                    self.player.take_damage(self)
                    break

        # -----------------------
        # Eliminación de enemigos golpeados por explosión
        # -----------------------
        enemies_to_remove = []
        for en in self.enemies:
            for e in self.explosions:
                if en.x == e.x and en.y == e.y:
                    enemies_to_remove.append(en)
                    break
        for en in enemies_to_remove:
            self.enemies.remove(en)

        # -----------------------
        # Daño al jugador por contacto con enemigos
        # -----------------------
        if self.player and not self.player.dead:
            for en in self.enemies:
                if int(self.player.x) == en.x and int(self.player.y) == en.y:
                    self.player.take_damage(self)
                    break

        # -----------------------
        # Función del portal (puerta de salida)
        # -----------------------
        if self.portal:
            self.portal.open = self.player.has_key  # se abre si el jugador tiene la llave

            # El jugador pisa el portal
            if int(self.player.x) == self.portal.x and int(self.player.y) == self.portal.y:
                if self.portal.open:
                    score = self._score()
                    self.go_victory(score)

        # -----------------------
        # Límite de tiempo (si existe)
        # -----------------------
        if self.time_limit is not None:
            self.time_limit -= dt
            if self.time_limit <= 0:
                self.go_defeat()

    def draw_hud(self, s):
        """Dibuja HUD estilo Bomberman NES."""
        font = self.app.font_small

        # Tiempo restante (en segundos)
        time_left = max(0, int(self.time_limit / 1000)) if self.time_limit else 0

        # Puntuación
        score = self._score()

        # Vidas
        lives = self.player.lives if self.player else 0

        # HUD tipo clásico NES
        text_left = font.render(f"TIEMPO {time_left}", True, (255, 255, 255))
        text_mid = font.render(f"{score}", True, (255, 255, 255))
        text_right = font.render(f"TI {lives}", True, (255, 255, 255))

        # Posición de cada elemento en pantalla
        s.blit(text_left, (30, 10))
        s.blit(text_mid, (config.WIDTH // 2 - text_mid.get_width() // 2, 10))
        s.blit(text_right, (config.WIDTH - 120, 10))

        # -----------------------
        # HUD técnico (información extra)
        # -----------------------
        p = self.player
        if not p:
            return

        tech_lines = [
            f"Bombas: {p.bombs_active}/{p.bomb_capacity}",
            f"Fuego: {p.bomb_range}",
            f"Velocidad: {int(p.speed)}",
            f"WallPass: {'Sí' if p.can_walk_through_blocks else 'No'}",
            f"BombPass: {'Sí' if p.can_walk_through_bombs else 'No'}",
        ]

        y = config.HEIGHT - 160
        for line in tech_lines:
            t = font.render(line, True, (255, 255, 255))
            s.blit(t, (30, y))
            y += t.get_height()

    def get_map_offset(self):
        """Centra dinámicamente el mapa dentro de la pantalla."""
        grid_w = len(self.map[0]) * self.tile
        grid_h = len(self.map) * self.tile

        offset_x = (config.WIDTH - grid_w) // 2
        offset_y = (config.HEIGHT - grid_h) // 2
        return offset_x, offset_y

    def draw(self):
        """Dibuja todo: fondo, tiles, entidades, explosiones, HUD."""
        s = self.app.screen
        s.fill((180, 180, 180))  # fondo gris estilo NES

        offset_x, offset_y = self.get_map_offset()

        # Dibujar piso del mapa
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                s.blit(self.grass_img, (offset_x + x * self.tile,
                                        offset_y + y * self.tile))

        # Dibujar bloques, ítems, bombas, explosiones, enemigos y jugador
        for b in self.blocks:     b.draw(s, offset_x, offset_y)
        for it in self.items:     it.draw(s, offset_x, offset_y)
        for bomb in self.bombs:   bomb.draw(s, offset_x, offset_y)
        for ex in self.explosions:ex.draw(s, offset_x, offset_y)
        if self.portal:           self.portal.draw(s, offset_x, offset_y)
        for en in self.enemies:   en.draw(s, offset_x, offset_y)
        if self.player:           self.player.draw(s, offset_x, offset_y)

        # Nivel actual en la esquina inferior izquierda
        bottom_font = self.app.font_small
        lvl_text = bottom_font.render(f"NIVEL: {self.level_index + 1} - {self.diff}", True, (255, 255, 255))
        s.blit(lvl_text, (20, config.HEIGHT - 40))

        # Dibujar HUD principal
        self.draw_hud(s)

    # -----------------------------------
    # SCORE, VICTORIA Y DERROTA
    # -----------------------------------

    def _score(self):
        """Calcula puntaje según tiempo transcurrido."""
        elapsed = pygame.time.get_ticks() - self.start_ticks
        return max(0, 10000 - elapsed // 5)

    def go_victory(self, score):
        """Pantalla de victoria."""
        from screens.victory import VictoryScreen
        self.app.change_screen(
            VictoryScreen(self.app, self.diff, self.level_index, score)
        )

    def go_defeat(self):
        """Pantalla de derrota."""
        from screens.defeat import DefeatScreen
        self.app.change_screen(
            DefeatScreen(self.app, self.diff, self.level_index)
        )

    def go_level(self):
        """Regresar a pantalla de selección de nivel."""
        from screens.level_select import LevelSelectScreen
        self.app.change_screen(LevelSelectScreen(self.app))