import pygame
from entities.entity import Entity

# ===============================================================
#  BLOQUE INDESTRUCTIBLE (WALL / BLOQUE SÓLIDO)
#  - No puede ser destruido por bombas
#  - Aparece donde el mapa tiene 'S'
# ===============================================================
class IndestructibleBlock(Entity):
    def __init__(self, x, y, tile_size=32):
        super().__init__(x, y, tile_size)

        # Cargar la imagen del bloque sólido desde assets
        self.image = pygame.image.load("assets/images/wall.jpg").convert_alpha()

        # Escalar para coincidir con el tamaño de tile
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def draw(self, surface, offset_x=0, offset_y=0):
        """
        Dibuja el bloque en su posición correspondiente dentro del mapa.
        """
        surface.blit(
            self.image,
            (
                offset_x + self.x * self.tile_size,
                offset_y + self.y * self.tile_size
            )
        )


# ===============================================================
#  BLOQUE DESTRUCTIBLE (BREAKABLE BLOCK)
#  - Se destruye con una bomba
#  - Puede contener un ítem oculto (item_hidden)
#  - Aparece donde el mapa tiene 'B'
# ===============================================================
class DestructibleBlock(Entity):
    def __init__(self, x, y, item_hidden=None, tile_size=32):
        super().__init__(x, y, tile_size)

        # Ítem oculto dentro del bloque (o None si no tiene)
        self.item_hidden = item_hidden

        # Imagen del bloque destructible
        self.image = pygame.image.load("assets/images/bridge.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def draw(self, surface, offset_x=0, offset_y=0):
        """
        Renderiza el bloque en pantalla.
        Si una bomba lo destruye, GamePlayScreen se encarga de eliminarlo.
        """
        surface.blit(
            self.image,
            (
                offset_x + self.x * self.tile_size,
                offset_y + self.y * self.tile_size
            )
        )
