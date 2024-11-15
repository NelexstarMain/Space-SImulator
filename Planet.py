import pygame
import math

class Planet:
    def __init__(self, x: int, y: int, mass: float, radius: int, color: tuple) -> None:
        self.x: int = x
        self.y: int = y
        self.mass: float = mass
        self.radius: int = radius
        self.color: tuple[int, int, int] = color
        self.atmosphere_color: tuple[int, int, int, int] = (self.color[0], self.color[1], self.color[2], 20)
        self.atmosphere_radius: int = radius * 2
        self.landing_zone_height: int = 10
        self.vector = pygame.Vector2(0, 0)


    def draw(self, screen, world_offset_x: float, world_offset_y: float) -> None:
        screen_width, screen_height = screen.get_size()
        # Zmiana sposobu obliczania pozycji na ekranie
        screen_x = screen_width//2 - (self.x - world_offset_x)
        screen_y = screen_height//2 - (self.y - world_offset_y)
     
        # Rysuj planetę

        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

        
        

    
    def get_gravity_force(self, ship_x: float, ship_y: float) -> pygame.Vector2:
        """Oblicza siłę grawitacji działającą na statek"""
        G = -10 
        dx = self.x - ship_x
        dy = self.y - ship_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return pygame.Vector2(0, 0)
            
        force = G * self.mass / (distance * distance)
        return pygame.Vector2(dx/distance * force, dy/distance * force)