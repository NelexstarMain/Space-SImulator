import pygame
import math

class SpaceShip:
    MAX_SPEED = 20
    BASE_ACCELERATION = 0.5
    
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.radius = 10
        self.vector: pygame.Vector2 = pygame.Vector2(0, 0)
        self.acceleration: pygame.Vector2 = pygame.Vector2(0, 0)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.mass = 10
        self.colided_with = []
    
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
        
    def handle_collision(self, others: list):
        self.colided_with = []
        for other in others:
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < (self.radius + other.radius):
                # Normalizacja wektora kolizji
                nx = dx / distance
                ny = dy / distance
                
                # Odsunięcie statku
                PUSH_FACTOR = 1.1  # Zmniejszony z 100 na 1.1
                overlap = (self.radius + other.radius - distance)
                
                # Odsunięcie statku na bezpieczną odległość
                self.x -= nx * overlap * PUSH_FACTOR
                self.y -= ny * overlap * PUSH_FACTOR
                
                # Obliczenie odbicia
                dot_product = (self.velocity.x * nx + self.velocity.y * ny)
                
                # Odbicie tylko jeśli statek zbliża się do planety
                if dot_product < 0:
                    # Składowa prędkości prostopadła do powierzchni
                    normal_vel_x = dot_product * nx
                    normal_vel_y = dot_product * ny
                    
                    # Odbicie składowej prostopadłej
                    self.velocity.x = self.velocity.x - 2 * normal_vel_x
                    self.velocity.y = self.velocity.y - 2 * normal_vel_y
                    
                    # Tłumienie odbicia
                    damping = 0.8
                    self.velocity *= damping
                    
                    # Minimalna prędkość po odbiciu
                    MIN_VELOCITY = 0.5
                    if self.velocity.length() < MIN_VELOCITY:
                        self.velocity = pygame.Vector2(0, 0)
                
                # Aktualizuj wektor kierunku
                if self.velocity.length() > 0:
                    self.vector = self.velocity.normalize()