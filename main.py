import pygame
from core.app import App

def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except:
        pass

    App().run()

if __name__ == "__main__":
    main()
