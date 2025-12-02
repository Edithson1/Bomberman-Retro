import pygame
import random
from entities.entity import Entity
from collections import deque

class Enemy(Entity):
    def __init__(self, x, y, tile_size=32, name="Enemy"):
        super().__init__(x, y, tile_size)

        # Nombre del enemigo (útil si hay diferentes tipos)
        self.name = name

        # Posiciones en pixeles para interpolación suave
        self.px = x * tile_size
        self.py = y * tile_size

        # Dirección inicial y animación
        self.direction = "down"
        self.anim_frame = 0
        self.anim_timer = 0

        # Duración de movimiento entre tiles (ms)
        self.move_duration = 250
        # Velocidad de animación basada en movimiento
        self.anim_speed = self.move_duration // 4

        self.moving = False          # Está avanzando entre tiles
        self.move_timer = 0          # Temporizador de movimiento
        self.start_px = self.px      # Punto inicial para interpolación
        self.start_py = self.py
        self.target_px = self.px     # Punto final
        self.target_py = self.py

        # Para IA:
        self.path = []               # Ruta hacia el jugador (via BFS)
        self.free_mode = False       # Si no encuentra camino → movimiento libre
        self.last_dir = None         # Última dirección de movimiento libre

        # Cargar sprites del enemigo
        self.load_sprites()

    # ------------------------------------------------------
    # CARGA DE SPRITES
    # ------------------------------------------------------
    def load_sprites(self):
        """
        Carga sprites para cada dirección.
        Si no existen imágenes, usa un fallback (cuadrado rojo).
        """
        self.sprites = {
            "down": [], "up": [], "left": [], "right": []
        }

        directions = ["down", "up", "left", "right"]

        for d in directions:
            for i in range(4):
                try:
                    img = pygame.image.load(
                        f"assets/images/enemy/{d}-{i}.png"
                    ).convert_alpha()
                except:
                    # Sprite alternativo si falta la imagen
                    img = pygame.Surface((self.tile_size, self.tile_size))
                    img.fill((255, 80, 80))

                # Escalar por si las imágenes son muy grandes
                img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
                self.sprites[d].append(img)

    # ------------------------------------------------------
    # UPDATE PRINCIPAL DEL ENEMIGO
    # ------------------------------------------------------
    def update(self, dt, game):
        """
        Cada frame se ejecuta:
        1. Si está moviéndose → interpolar + animar
        2. Si NO está moviéndose → decidir acción con IA
        """
        self.game = game

        # -------------------------------------------------
        # SI ESTÁ MOVIÉNDOSE ENTRE TILES
        # -------------------------------------------------
        if self.moving:
            self.move_timer -= dt

            # Actualiza animación
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer -= self.anim_speed
                self.anim_frame = (self.anim_frame + 1) % 4

            # Finaliza movimiento
            if self.move_timer <= 0:
                self.px = self.target_px
                self.py = self.target_py
                self.moving = False
                self.anim_frame = 0
            else:
                # Interpolación suave entre tiles
                t = 1 - (self.move_timer / self.move_duration)
                self.px = self.start_px + (self.target_px - self.start_px) * t
                self.py = self.start_py + (self.target_py - self.start_py) * t

            # Actualizar coordenadas en la grilla
            self.x = int(self.px // self.tile_size)
            self.y = int(self.py // self.tile_size)
            return

        # -------------------------------------------------
        # SI NO ESTÁ MOVIENDO → IA decide qué hacer
        # -------------------------------------------------
        self.think(game)

    # ------------------------------------------------------
    # DECISIÓN: PATHFINDING O MODO LIBRE
    # ------------------------------------------------------
    def think(self, game):
        """
        Intenta seguir al jugador usando BFS.
        Si no hay ruta (bloqueado por muros), usa movimiento libre aleatorio.
        """
        player = game.player

        # Buscar ruta hacia el jugador
        self.path = self.find_path((self.x, self.y), (player.x, player.y), game)

        if self.path:
            self.free_mode = False
            next_cx, next_cy = self.path.pop(0)
            self.start_move(next_cx, next_cy, game)
        else:
            # Si no hay camino posible → movimiento aleatorio
            self.free_mode = True
            self.free_move(game)

    # ------------------------------------------------------
    # INICIO DE MOVIMIENTO HACIA UN TILE
    # ------------------------------------------------------
    def start_move(self, cx, cy, game):
        """
        Inicia un movimiento hacia la celda (cx, cy).
        También calcula la dirección para seleccionar el sprite adecuado.
        """
        if self.is_blocked(cx, cy, game):
            return

        # Determinar dirección basada en delta
        dx = cx - self.x
        dy = cy - self.y

        if dx == 1: self.direction = "right"
        elif dx == -1: self.direction = "left"
        elif dy == -1: self.direction = "up"
        elif dy == 1: self.direction = "down"

        # Guardar punto inicial
        self.start_px = self.px
        self.start_py = self.py

        # Punto final
        self.target_px = cx * self.tile_size
        self.target_py = cy * self.tile_size

        # Comienza movimiento
        self.moving = True
        self.move_timer = self.move_duration

    # ------------------------------------------------------
    # MOVIMIENTO LIBRE ALEATORIO
    # ------------------------------------------------------
    def free_move(self, game):
        """
        Movimiento aleatorio cuando no existe un camino hacia el jugador.
        Intenta continuar en la misma dirección antes de cambiar a otra.
        """
        dirs = [(0,-1),(0,1),(-1,0),(1,0)]

        # Intentar seguir en la misma dirección primero
        if self.last_dir:
            dx, dy = self.last_dir
            cx = self.x + dx
            cy = self.y + dy
            if not self.is_blocked(cx, cy, game):
                return self.start_move(cx, cy, game)

        # Si no, probar direcciones aleatorias
        random.shuffle(dirs)

        for dx, dy in dirs:
            cx = self.x + dx
            cy = self.y + dy
            if not self.is_blocked(cx, cy, game):
                self.last_dir = (dx, dy)
                return self.start_move(cx, cy, game)

        # Si no puede moverse → queda quieto
        self.last_dir = None

    # ------------------------------------------------------
    # PATHFINDING BFS
    # ------------------------------------------------------
    def find_path(self, start, goal, game):
        """
        Implementación simple de BFS para seguir al jugador.
        Devuelve una lista de celdas para llegar al objetivo.
        """
        queue = deque([start])
        visited = {start: None}

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == goal:
                break

            for dx, dy in [(0,-1),(0,1),( -1,0),(1,0)]:
                nx = cx + dx
                ny = cy + dy

                if (nx, ny) in visited:
                    continue
                if self.is_blocked(nx, ny, game):
                    continue

                visited[(nx, ny)] = (cx, cy)
                queue.append((nx, ny))

        if goal not in visited:
            return None

        # Reconstrucción del camino
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = visited[node]
        path.reverse()
        return path

    # ------------------------------------------------------
    # CELDA BLOQUEADA
    # ------------------------------------------------------
    def is_blocked(self, cx, cy, game):
        """
        Revisa si el tile es sólido o tiene una bomba.
        Enemigos NO pueden atravesar nada.
        """
        if cx < 0 or cx >= len(game.map[0]) or cy < 0 or cy >= len(game.map):
            return True

        cell = game.map[cy][cx]
        if cell in ("S", "B"):  # muro sólido o bloque destructible
            return True

        # Bombas también bloquean al enemigo
        for b in game.bombs:
            if b.x == cx and b.y == cy:
                return True

        return False

    # ------------------------------------------------------
    # DIBUJO EN PANTALLA
    # ------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        """
        Dibuja el sprite en base a la dirección y el frame actual.
        """
        img = self.sprites[self.direction][self.anim_frame]
        surface.blit(
            img,
            (offset_x + int(self.px),
             offset_y + int(self.py))
        )
