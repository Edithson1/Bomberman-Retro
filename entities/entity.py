import pygame

class Entity:
    def __init__(self, x, y, tile_size=32):
        """
        Clase base para TODO lo que existe en el mundo del juego:
        jugador, enemigos, bombas, bloques, ítems, etc.

        - x, y → coordenadas en la grilla (tiles)
        - tile_size → tamaño del tile en pixeles
        - dead → indica si la entidad debe eliminarse
        """
        self.x = x                  # posición en la grilla
        self.y = y
        self.tile_size = tile_size  # tamaño del sprite/tile
        self.dead = False           # si está muerto, el juego lo eliminará

    # ------------------------------------------------------------
    # DIBUJO BÁSICO
    # ------------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        """
        Método vacío.
        Las clases hijas lo *sobrescriben* para dibujarse
        (ej: Player, Enemy, Bomb, Item...).
        """
        pass

    # ------------------------------------------------------------
    # RECTÁNGULO COLLISIONABLE
    # ------------------------------------------------------------
    @property
    def rect(self):
        """
        Devuelve un pygame.Rect que representa el área que
        ocupa la entidad en la pantalla.

        Se usa para detectar colisiones o dibujar.
        """
        return pygame.Rect(
            self.x * self.tile_size,
            self.y * self.tile_size,
            self.tile_size,
            self.tile_size
        )

    # ------------------------------------------------------------
    # ACTUALIZACIÓN DE LA ENTIDAD
    # ------------------------------------------------------------
    def update(self, dt, game):
        """
        Método base que las entidades pueden sobrescribir.

        - dt = tiempo transcurrido (delta time)
        - game = referencia al controlador del juego
        """
        pass
