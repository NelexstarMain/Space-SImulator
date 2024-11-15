import pygame

class SpaceShip:
    MAX_SPEED = 35
    BASE_ACCELERATION = 0.7
    
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.fuel: int = 100
        self.vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.acceleration: pygame.Vector2 = pygame.Vector2(0, 0)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
    
    def update(self, direction, joystick_distance) -> None:
        # Oblicz przyspieszenie na podstawie wejścia joysticka i jego odległości od środka
        if direction.length() > 0:
            # joystick_distance powinno być w zakresie 0-1
            acceleration_strength = self.BASE_ACCELERATION / int(joystick_distance)
            self.acceleration = direction * acceleration_strength
        else:
            self.acceleration = pygame.Vector2(0, 0)
        
        # Aktualizuj prędkość
        self.velocity += self.acceleration
        
        
        # Ogranicz prędkość maksymalną
        if self.velocity.length() > self.MAX_SPEED:
            self.velocity.scale_to_length(self.MAX_SPEED)
        
        # Aktualizuj wektor kierunku (dla kompasu)
        if self.velocity.length() > 0:
            self.vector = self.velocity.normalize()
        
        # Aktualizuj pozycję
        self.x += int(self.velocity.x)
        self.y += int(self.velocity.y)
    
    def draw(self, screen) -> None:
        screen_width, screen_height = screen.get_size()
        rect = pygame.Rect(screen_width//2 - 10, screen_height//2 - 10, 20, 20)
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)