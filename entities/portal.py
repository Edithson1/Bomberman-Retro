import pygame
from entities.entity import Entity

class Portal(Entity):
    def __init__(self, x, y, tile_size=32):
        # Llama al constructor base (Entity ya maneja posición x,y y tamaño)
        super().__init__(x, y, tile_size)

        # Estado de la puerta
        #   False → cerrada (no puedes entrar)
        #   True  → abierta (si tienes llave puedes ganar)
        self.open = False

        # Cargar imágenes desde disco SOLO UNA VEZ
        # (evita recargar en cada frame y mejora rendimiento)
        self.img_open = pygame.image.load("assets/images/open_door.jpg").convert_alpha()
        self.img_closed = pygame.image.load("assets/images/closed_door.jpg").convert_alpha()

        # Ajustar todas las imágenes al tamaño de celda del mapa
        self.img_open = pygame.transform.scale(self.img_open, (self.tile_size, self.tile_size))
        self.img_closed = pygame.transform.scale(self.img_closed, (self.tile_size, self.tile_size))

    # --------------------------------------------------------
    #   DIBUJAR PORTAL (depende de si está abierto o cerrado)
    # --------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        # Posición física del tile en la pantalla
        rect = (
            offset_x + self.x * self.tile_size,
            offset_y + self.y * self.tile_size,
            self.tile_size,
            self.tile_size
        )

        # Elegir la imagen que corresponde al estado
        img = self.img_open if self.open else self.img_closed

        # Dibujar el portal
        surface.blit(img, rect)
