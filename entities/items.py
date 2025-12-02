import pygame
import os
from entities.entity import Entity

class Item(Entity):
    def __init__(self, x, y, item_type, tile_size=32, base_path="assets/images/items"):
        super().__init__(x, y, tile_size)

        # Tipo de item: FIRE, BOMB, SPEED, KEY, etc.
        self.item_type = item_type

        # Carpeta donde están las imágenes de animación del ítem
        self.base_path = base_path

        # Cargar las imágenes que animan el ítem
        self.frames = self.load_frames(item_type)

        # Control de animación
        self.current_frame = 0           # frame actual
        self.animation_speed = 10        # cada cuántos frames avanzar
        self.frame_counter = 0           # contador que decide cuándo cambiar

    # ------------------------------------------------------------
    # CARGA DE SPRITES DEL ÍTEM
    # ------------------------------------------------------------
    def load_frames(self, item_type):
        """
        Carga todas las imágenes desde:
        assets/images/items/<ITEM_TYPE>/image-1.jpg
        assets/images/items/<ITEM_TYPE>/image-2.jpg
        etc.
        Hasta que deje de existir un archivo.
        """

        folder_path = os.path.join(self.base_path, item_type)
        frames = []
        index = 1

        # Intentar cargar image-1.jpg, image-2.jpg, image-3.jpg, ...
        while True:
            img_path = os.path.join(folder_path, f"image-{index}.jpg")

            # Si no existe, se detiene la carga
            if not os.path.exists(img_path):
                break

            # Cargar imagen
            image = pygame.image.load(img_path).convert_alpha()

            # Redimensionar a tamaño del tile
            image = pygame.transform.scale(image, (self.tile_size, self.tile_size))

            frames.append(image)
            index += 1

        # Si no hay imágenes → error de configuración
        if not frames:
            raise ValueError(f"No se encontraron imágenes para el item '{item_type}' en {folder_path}")

        return frames

    # ------------------------------------------------------------
    # EFECTOS AL RECOGER EL ÍTEM
    # ------------------------------------------------------------
    def apply(self, player):
        """
        Cuando el jugador pisa el ítem, este método modifica sus stats
        dependiendo del tipo de ítem.
        """

        if self.item_type == "FIRE":
            player.bomb_range += 1

        elif self.item_type == "BOMB":
            player.bomb_capacity += 1

        elif self.item_type == "SPEED":
            # Reduce move_duration → se mueve más rápido
            player.move_duration -= 30

        elif self.item_type == "SLOW":
            # Aumenta move_duration → movimiento más lento
            player.move_duration += 30

        elif self.item_type == "PASS_WALL":
            # Permite atravesar bloques por 5 segundos
            player.can_walk_through_blocks = True
            player.walk_blocks_timer = 5000

        elif self.item_type == "PASS_BOMB":
            # Permite caminar sobre bombas por 5 segundos
            player.can_walk_through_bombs = True
            player.walk_bombs_timer = 5000

        elif self.item_type == "SHIELD":
            # Protege de la siguiente explosión o daño
            player.shield = True

        elif self.item_type == "KEY":
            # La llave abre el portal del nivel
            player.has_key = True

    # ------------------------------------------------------------
    # ACTUALIZAR ANIMACIÓN DEL ÍTEM
    # ------------------------------------------------------------
    def update_animation(self):
        """
        Incrementa el frame con un contador para crear animación lenta.
        """

        self.frame_counter += 1

        # Cambiar de frame cuando se cumpla el tiempo
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    # ------------------------------------------------------------
    # DIBUJAR ÍTEM EN PANTALLA
    # ------------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        # Avanzar animación
        self.update_animation()

        # Frame actual
        img = self.frames[self.current_frame]

        # Dibujarlo basado en su posición dentro del mapa
        surface.blit(
            img,
            (
                offset_x + self.x * self.tile_size,
                offset_y + self.y * self.tile_size
            )
        )
