import pygame
from entities.entity import Entity
from entities.explosion import Explosion
from entities.items import Item

class Bomb(Entity):
    def __init__(self, x, y, owner, power, timer=2000, tile_size=32):
        super().__init__(x, y, tile_size)

        # Jugador o enemigo que la colocó
        self.owner = owner

        # Tiempo hasta explotar (en ms)
        self.timer = timer

        # Alcance de explosión en tiles
        self.power = power

        # Estado de explosión
        self.exploded = False

        # Si debe eliminarse del juego
        self.dead = False

        # Cargar y preparar animaciones de la bomba
        self.load_sprites()

        # Total de frames de animación
        self.total_frames = len(self.frames)

        # La animación completa se repite 5 veces antes de explotar
        self.frame_cycle_time = timer / 5

        # Tiempo que dura cada frame de animación
        self.frame_time = self.frame_cycle_time / self.total_frames

        # Contadores internos de animación
        self.anim_timer = 0
        self.anim_frame = 0

    # -------------------------------------------------------------
    # CARGA DE SPRITES DE LA BOMBA
    # -------------------------------------------------------------
    def load_sprites(self):
        """
        Carga los frames bomb-0.png, bomb-1.png, bomb-2.png, ...
        hasta que no existan más archivos.
        """
        self.frames = []
        i = 0
        while True:
            try:
                img = pygame.image.load(f"assets/images/bomb/bomb-{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
                self.frames.append(img)
                i += 1
            except:
                # Si falla (no existe más imagen), terminamos
                break

        # Si no hay imágenes, crear un cuadrado simple de fallback
        if not self.frames:
            surf = pygame.Surface((self.tile_size, self.tile_size))
            self.frames = [surf]

    # -------------------------------------------------------------
    # ACTUALIZACIÓN DE LA BOMBA CADA FRAME
    # -------------------------------------------------------------
    def update(self, dt, game):
        """
        1. Avanza la animación
        2. Reduce el temporizador
        3. Si llega a cero → explota
        """
        # Avance de animación
        self.anim_timer += dt

        # Ciclos para avanzar frames
        while self.anim_timer >= self.frame_time:
            self.anim_timer -= self.frame_time
            self.anim_frame = (self.anim_frame + 1) % self.total_frames

        # Avanzar el temporizador
        self.timer -= dt
        if self.timer <= 0 and not self.exploded:
            self.explode(game)

    # -------------------------------------------------------------
    # EXPLOSIÓN DE LA BOMBA
    # -------------------------------------------------------------
    def explode(self, game):
        """
        Lógica completa al detonar:
        - Genera explosión central
        - Se propaga en 4 direcciones
        - Activa otras bombas (reacción en cadena)
        - Destruye ítems y bloques
        """
        if self.exploded:
            return  # evitar doble explosión

        self.exploded = True
        self.dead = True

        # Reducir contador de bombas activas del jugador
        self.owner.bombs_active -= 1

        # Limpia la bomba del mapa (para que no sea un obstáculo)
        game.map[self.y][self.x] = "."

        # Explosión central
        game.explosions.append(Explosion(self.x, self.y, tile_size=self.tile_size))

        # Direcciones (arriba, abajo, derecha, izquierda)
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in dirs:
            for r in range(1, self.power + 1):
                nx = self.x + dx * r
                ny = self.y + dy * r

                cell = game.map[ny][nx]

                # Si es muro sólido → para la explosión
                if cell == "S":
                    break

                # Añadir explosión visual en este tile
                game.explosions.append(Explosion(nx, ny, tile_size=self.tile_size))

                # ---------------------------------------------------------
                # ★ REACCIÓN EN CADENA: activar otras bombas que toque
                # ---------------------------------------------------------
                for other in game.bombs:
                    if other is not self and other.x == nx and other.y == ny:
                        if not other.exploded:
                            other.timer = 0  # hará que explote en el próximo update

                # ---------------------------------------------------------
                # ★ Si es un ítem → la explosión lo destruye, excepto KEY
                # ---------------------------------------------------------
                if cell == "I":
                    for item in game.items:
                        if item.x == nx and item.y == ny:
                            if item.item_type == "KEY":
                                break  # la llave NO se destruye
                            game.items.remove(item)
                            break

                    game.map[ny][nx] = "."
                    break

                # ---------------------------------------------------------
                # ★ Si es un bloque destructible
                # ---------------------------------------------------------
                if cell == "B":
                    for block in game.blocks:
                        if block.x == nx and block.y == ny:

                            # Si tenía ítem oculto → soltarlo
                            if getattr(block, "item_hidden", None):
                                game.items.append(
                                    Item(nx, ny, block.item_hidden, tile_size=self.tile_size)
                                )

                            game.blocks.remove(block)
                            break

                    game.map[ny][nx] = "."
                    break

    # -------------------------------------------------------------
    # DIBUJAR LA BOMBA EN LA PANTALLA
    # -------------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        """
        Dibuja el frame actual de la animación de la bomba.
        """
        frame = self.frames[self.anim_frame]

        surface.blit(
            frame,
            (offset_x + self.x * self.tile_size,
             offset_y + self.y * self.tile_size)
        )
