import pygame

class JoyStick:
    def __init__(self, 
                 start_x: int,
                 start_y: int,
                 x: int,
                 y: int,
                 color: tuple[int, int, int]
            
        ) -> None:
        
        self.start_x: int = start_x
        self.start_y: int = start_y
        self.x: int = x
        self.y: int = y
        self.max_radius: int = 100
        self.radius = 0
        self.color: tuple = (0, 255, 0)
        self.vector1: pygame.Vector2 = pygame.Vector2(0, 0)
        
    def check(self) -> None:
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        
        self.vector1 = pygame.math.Vector2(mouse_x - self.start_x, mouse_y - self.start_y)
        
        if self.vector1.length() > self.max_radius:
            self.vector1.scale_to_length(self.max_radius)
            self.x = int(self.start_x + self.vector1.x)
            self.y = int(self.start_y + self.vector1.y)
        else:
            self.x = mouse_x
            self.y = mouse_y
            
        self.radius = self.vector1.length()
        if self.vector1.length() > 0:
            self.vector1.normalize()
            
    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, (self.start_x, self.start_y), self.radius, 2)
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.x, self.y))