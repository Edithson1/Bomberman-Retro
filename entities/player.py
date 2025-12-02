import pygame
from entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y, tile_size=32):
        super().__init__(x, y, tile_size)

        # Posición en píxeles (para animación suave)
        self.px = x * tile_size
        self.py = y * tile_size

        # Dirección inicial del personaje
        self.direction = "down"

        # Variables de animación
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_speed = 200  # cada cuántos ms cambia de frame
        self.moving = False

        # Cargar sprites del jugador
        self.load_sprites()

        # Movimiento interpolado (suave)
        self.move_duration = 200  # ms que tarda en moverse un tile
        self.move_timer = 0
        self.target_px = self.px
        self.target_py = self.py

        # Estado general
        self.has_key = False
        self.speed = 2

        # Estadísticas de bombas
        self.bomb_range = 1
        self.bomb_capacity = 1
        self.bombs_active = 0

        # Sistema de vidas e invencibilidad
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0  # cuánto tiempo queda invencible

        # Power-ups temporales
        self.can_walk_through_blocks = False
        self.can_walk_through_bombs = False
        self.walk_blocks_timer = 0
        self.walk_bombs_timer = 0

        # Bombas que puede atravesar (solo la que acaba de colocar)
        self.bombs_currently_passable = set()

        # Controles del teclado
        self.move_up = self.move_down = False
        self.move_left = self.move_right = False

    # ------------------------------------------------------------
    # CARGA DE SPRITES
    # ------------------------------------------------------------
    def load_sprites(self):
        # Cada dirección tiene 4 imágenes
        self.sprites = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        # Carga imágenes del disco
        for direction in self.sprites.keys():
            for i in range(4):
                img = pygame.image.load(
                    f"assets/images/bombman/{direction}-{i}.png"
                ).convert_alpha()

                img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
                self.sprites[direction].append(img)

    # ------------------------------------------------------------
    # SISTEMA DE DAÑO
    # ------------------------------------------------------------
    def take_damage(self, game):
        # Si está invencible, no recibe daño
        if self.invincible:
            return

        # Si tiene escudo, se consume y da invencibilidad larga
        if getattr(self, "shield", False):
            self.shield = False
            self.invincible = True
            self.invincible_timer = 5000
            return

        # Perder una vida
        self.lives -= 1
        self.invincible = True
        self.invincible_timer = 1000  # 1 segundo sin recibir daño

        # Sin vidas → derrota
        if self.lives <= 0:
            game.go_defeat()

    # ------------------------------------------------------------
    # CONTROL DE TECLAS Y MOUSE
    # ------------------------------------------------------------
    def handle_input(self, event):

        # Click izquierdo → coloca bomba
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.try_place_bomb()

        # Flechas de movimiento
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    self.move_up = True
            if event.key == pygame.K_DOWN:  self.move_down = True
            if event.key == pygame.K_LEFT:  self.move_left = True
            if event.key == pygame.K_RIGHT: self.move_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:    self.move_up = False
            if event.key == pygame.K_DOWN:  self.move_down = False
            if event.key == pygame.K_LEFT:  self.move_left = False
            if event.key == pygame.K_RIGHT: self.move_right = False

    # ------------------------------------------------------------
    # COLOCAR BOMBA
    # ------------------------------------------------------------
    def try_place_bomb(self):
        # No puede colocar más bombas de las permitidas
        if self.bombs_active >= self.bomb_capacity:
            return False

        # Tile actual del jugador
        tile_x = int(self.px // self.tile_size)
        tile_y = int(self.py // self.tile_size)

        # No se pueden poner bombas sobre:
        # O = portal, B = bloque, E = enemigo
        cell = self.game.map[tile_y][tile_x]
        if cell in ("O", "B", "E"):
            return False

        # No puedes poner 2 bombas en el mismo tile
        for b in self.game.bombs:
            if b.x == tile_x and b.y == tile_y:
                return False

        # Crear y registrar la bomba
        from entities.bomb import Bomb
        bomb = Bomb(tile_x, tile_y, self, self.bomb_range, tile_size=self.tile_size)

        self.game.bombs.append(bomb)
        self.bombs_active += 1

        # Mientras el jugador esté sobre su propia bomba, la puede atravesar
        self.bombs_currently_passable.add((tile_x, tile_y))
        return True

    # ------------------------------------------------------------
    # ACTUALIZACIÓN POR FRAME
    # ------------------------------------------------------------
    def update(self, dt, game):
        # Guardar referencia al game
        self.game = game

        # Si está moviéndose → animación + interpolación
        if self.moving:
            self.move_timer -= dt

            # Animación mientras se mueve
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer -= self.anim_speed
                self.anim_frame = (self.anim_frame + 1) % 4

            # Movimiento terminado
            if self.move_timer <= 0:
                self.px = self.target_px
                self.py = self.target_py
                self.moving = False
                self.anim_frame = 0
            else:
                # Movimiento interpolado entre píxeles
                t = 1 - (self.move_timer / self.move_duration)
                self.px = self.start_px + (self.target_px - self.start_px) * t
                self.py = self.start_py + (self.target_py - self.start_py) * t

            # Actualiza posición en celdas
            self.x = int(self.px // self.tile_size)
            self.y = int(self.py // self.tile_size)
            return

        # --------------------------------------------------------
        # Si NO se está moviendo, procesar teclas
        # --------------------------------------------------------
        dx = dy = 0
        if self.move_up:    dy = -1
        if self.move_down:  dy = 1
        if self.move_left:  dx = -1
        if self.move_right: dx = 1

        # Evitar movimiento diagonal
        if dx != 0 and dy != 0:
            dy = 0

        # Iniciar un movimiento si hay una dirección
        if dx != 0 or dy != 0:
            self.start_move(dx, dy, game)
        else:
            self.anim_frame = 0  # quieto

        # Recolectar ítems
        self.pick_up_items(game)

        # Manejo de invencibilidad temporal
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

        # Tiempo restante del power-up "atravesar bloques"
        if self.can_walk_through_blocks:
            self.walk_blocks_timer -= dt
            if self.walk_blocks_timer <= 0:
                self.can_walk_through_blocks = False
                # Si al terminar queda atrapado → expulsarlo
                if self.is_inside_block_or_bomb(game):
                    self.force_eject_from_block(game)

        # Igual para "atravesar bombas"
        if self.can_walk_through_bombs:
            self.walk_bombs_timer -= dt
            if self.walk_bombs_timer <= 0:
                self.can_walk_through_bombs = False
                if self.is_inside_block_or_bomb(game):
                    self.force_eject_from_block(game)

    # ------------------------------------------------------------
    # INICIAR UN MOVIMIENTO
    # ------------------------------------------------------------
    def start_move(self, dx, dy, game):
        new_cx = self.x + dx
        new_cy = self.y + dy

        # Actualizar dirección visual
        if dx == 1:  self.direction = "right"
        if dx == -1: self.direction = "left"
        if dy == -1: self.direction = "up"
        if dy == 1:  self.direction = "down"

        # Si la celda está bloqueada, no se mueve
        if self.is_blocked(new_cx, new_cy, game):
            return

        # Manejo de bomba atravesable
        self.handle_bomb_collision(new_cx, new_cy, game)

        # Guardar desde dónde empieza la interpolación
        self.start_px = self.px
        self.start_py = self.py

        # Posición destino en pixeles
        self.target_px = new_cx * self.tile_size
        self.target_py = new_cy * self.tile_size

        # Activar movimiento
        self.moving = True
        self.move_timer = self.move_duration

    # ------------------------------------------------------------
    # COLISIONES CON MUROS Y BOMBAS
    # ------------------------------------------------------------
    def is_blocked(self, cx, cy, game):
        # Fuera del mapa
        if cx < 0 or cx >= len(game.map[0]) or cy < 0 or cy >= len(game.map):
            return True

        cell = game.map[cy][cx]

        # Muro sólido
        if cell == "S":
            return True

        # Bloque destructible (solo si no tiene WallPass)
        if cell == "B" and not self.can_walk_through_blocks:
            return True

        # Bombas
        for b in game.bombs:
            if b.x == cx and b.y == cy:
                # BombPass permite pasar
                if self.can_walk_through_bombs:
                    return False
                # Bomba actual recién puesta → permitir pasar
                if (cx, cy) in self.bombs_currently_passable:
                    return False
                return True

        return False

    # Comprueba si está atrapado dentro de algo sólido
    def is_inside_block_or_bomb(self, game):
        cx, cy = self.x, self.y

        if game.map[cy][cx] == "B":
            return True

        for b in game.bombs:
            if b.x == cx and b.y == cy:
                return True

        return False

    # Empuja al jugador fuera del bloque o bomba cuando termina un power-up
    def force_eject_from_block(self, game):
        dirs = [(0,-1), (0,1), (-1,0), (1,0)]
        cx, cy = self.x, self.y

        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < len(game.map[0]) and 0 <= ny < len(game.map):
                if not self.is_blocked(nx, ny, game):
                    # Mover directamente al sector libre
                    self.px = nx * self.tile_size
                    self.py = ny * self.tile_size
                    self.x = nx
                    self.y = ny
                    return

    # Remueve de bombs_currently_passable las bombas que ya no está pisando
    def handle_bomb_collision(self, cx, cy, game):
        to_remove = []
        for (bx, by) in self.bombs_currently_passable:
            if not (cx == bx and cy == by):
                to_remove.append((bx, by))

        for b in to_remove:
            self.bombs_currently_passable.remove(b)

    # ------------------------------------------------------------
    # RECOLECCIÓN DE ITEMS
    # ------------------------------------------------------------
    def pick_up_items(self, game):
        items_to_remove = []

        # Si el jugador está encima del item → aplicarlo
        for item in game.items:
            if self.x == item.x and self.y == item.y:
                item.apply(self)
                items_to_remove.append(item)

        # Removerlos del mundo
        for item in items_to_remove:
            game.items.remove(item)

    # ------------------------------------------------------------
    # DIBUJAR SPRITE
    # ------------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        # Escoge el frame correcto según la dirección y animación
        img = self.sprites[self.direction][self.anim_frame]

        # Dibujar personaje en pantalla
        surface.blit(
            img,
            (offset_x + int(self.px),
             offset_y + int(self.py))
        )
