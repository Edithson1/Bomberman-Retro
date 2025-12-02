import pygame
from entities.entity import Entity

class Explosion(Entity):
    def __init__(self, x, y, duration=300, tile_size=32):
        # Llama al constructor base, guarda posición y tamaño
        super().__init__(x, y, tile_size)

        # Tiempo total que dura la explosión (en milisegundos)
        self.duration = duration

        # Guardamos la duración original para calcular efectos visuales
        self.max_duration = duration

    # ------------------------------------------------------------
    # ACTUALIZACIÓN LÓGICA DE LA EXPLOSIÓN
    # ------------------------------------------------------------
    def update(self, dt, game):
        """
        Reduce el tiempo restante de la explosión.
        Cuando llega a 0, marcamos el objeto como muerto → desaparecerá.
        """

        self.duration -= dt

        # Cuando termina su duración, se elimina de la lista del juego
        if self.duration <= 0:
            self.dead = True

    # ------------------------------------------------------------
    # DIBUJO DE LA EXPLOSIÓN
    # ------------------------------------------------------------
    def draw(self, surface, offset_x=0, offset_y=0):
        """
        Dibuja un cuadrado que cambia de intensidad (Rojo → Amarillo)
        dependiendo del tiempo restante.
        """

        # Valor entre 1.0 y 0.0 que indica cuánto le queda
        alpha = self.duration / self.max_duration

        # Color base rojo → se vuelve más amarillento al inicio
        R = 255
        G = int(200 * alpha)   # se desvanece con el tiempo
        B = int(20 * alpha)
        color = (R, G, B)

        # Crear rectángulo en pantalla según la posición en la grilla
        rect = pygame.Rect(
            offset_x + self.x * self.tile_size,
            offset_y + self.y * self.tile_size,
            self.tile_size,
            self.tile_size
        )

        # Dibujo del centro de la explosión
        pygame.draw.rect(surface, color, rect)

        # Bordes para mayor contraste y visibilidad
        pygame.draw.rect(surface, (255, 100, 0), rect, 2)
