import pygame
import math

class Planet:
    def __init__(self, x: int, y: int, mass: float, radius: int, color: tuple) -> None:
        self.x: int = x
        self.y: int = y
        self.mass: float = mass
        self.radius: int = radius
        self.color: tuple[int, int, int] = color
        self.atmosphere_color: tuple[int, int, int, int] = (100, 100, 255, 50)
        self.atmosphere_radius: int = radius + 50
        self.landing_zone_height: int = 10
        self.atmosphere_surface = self._create_atmosphere_surface()
        
    def _create_atmosphere_surface(self):
        atmosphere_surface = pygame.Surface((self.atmosphere_radius * 2, 
                                        self.atmosphere_radius * 2), 
                                        pygame.SRCALPHA)
        for r in range(self.radius, self.atmosphere_radius):
            alpha = int(255 * (1 - (r - self.radius) / 
                    (self.atmosphere_radius - self.radius)))
            pygame.draw.circle(atmosphere_surface, 
                            (*self.atmosphere_color[:3], alpha), 
                            (self.atmosphere_radius, self.atmosphere_radius), 
                            r, 
                            1)
        return atmosphere_surface

    def draw(self, screen, world_offset_x: float, world_offset_y: float) -> None:
        screen_width, screen_height = screen.get_size()
        # Zmiana sposobu obliczania pozycji na ekranie
        screen_x = screen_width//2 - (self.x - world_offset_x)
        screen_y = screen_height//2 - (self.y - world_offset_y)
        
        # Rysuj atmosferę
        screen.blit(self.atmosphere_surface, 
                   (screen_x - self.atmosphere_radius, 
                    screen_y - self.atmosphere_radius))
        
        # Rysuj planetę
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)
        
        # Rysuj strefę lądowania
        landing_points = self.get_landing_points(20)
        for point in landing_points:
            x = screen_x + math.cos(point) * self.radius
            y = screen_y + math.sin(point) * self.radius
            pygame.draw.line(screen, (0, 255, 0),
                           (x, y),
                           (x + math.cos(point) * self.landing_zone_height,
                            y + math.sin(point) * self.landing_zone_height))
    
    def get_landing_points(self, num_points: int) -> list[float]:
        """Zwraca listę kątów (w radianach) dla stref lądowania"""
        return [2 * math.pi * i / num_points for i in range(num_points)]
    
    def check_landing(self, ship_x: float, ship_y: float, ship_velocity: pygame.Vector2) -> bool:
        """Sprawdza czy statek może wylądować"""
        # Oblicz odległość statku od środka planety
        dx = ship_x - self.x
        dy = ship_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Sprawdź czy statek jest blisko powierzchni
        if abs(distance - self.radius) > self.landing_zone_height:
            return False
        
        # Sprawdź prędkość lądowania
        if ship_velocity.length() > 1.0:  # Maksymalna bezpieczna prędkość lądowania
            return False
        
        # Sprawdź kąt podejścia
        approach_angle = math.atan2(dy, dx)
        landing_points = self.get_landing_points(20)
        
        # Sprawdź czy statek jest blisko którejś ze stref lądowania
        for point in landing_points:
            if abs(approach_angle - point) < 0.1:  # Tolerancja kąta lądowania
                return True
                
        return False
    
    def get_gravity_force(self, ship_x: float, ship_y: float) -> pygame.Vector2:
        """Oblicza siłę grawitacji działającą na statek"""
        G = 0.1  # Stała grawitacyjna (dostosuj według potrzeb)
        dx = self.x - ship_x
        dy = self.y - ship_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return pygame.Vector2(0, 0)
            
        force = G * self.mass / (distance * distance)
        return pygame.Vector2(dx/distance * force, dy/distance * force)