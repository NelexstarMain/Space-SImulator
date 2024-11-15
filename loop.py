import pygame
from SpaceShip import SpaceShip
from JoyStick import JoyStick
from Planet import Planet
import random

planets = [Planet(random.randint(-10000, 10000), random.randint(-10000, 10000), random.randint(1000, 10000), random.randint(100, 2000), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))) for _ in range(10)]

def main():
    pygame.init()
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 750
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Statek zawsze na środku ekranu
    ship = SpaceShip(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    joystick = JoyStick(100, SCREEN_HEIGHT - 100, 0, 0, (0, 255, 0))
    
    # Pozycja świata względem statku
    world_offset_x = 0
    world_offset_y = 0
    
    # Lista punktów śladu względem świata
    trail_points = []
    
    # Siatka punktów dla orientacji
    GRID_SIZE = 500
    
    clicked = False
    
    running = True
    while running:
        
        screen.fill((0, 0, 0))
        
        
        screen_rect = screen.get_rect()
        for planet in planets:
            screen_x = SCREEN_WIDTH//2 - (world_offset_x - planet.x)
            screen_y = SCREEN_HEIGHT//2 - (world_offset_y - planet.y)
            # Only draw if planet is visible
            if (screen_x + planet.atmosphere_radius > 0 and 
                screen_x - planet.atmosphere_radius < SCREEN_WIDTH and
                screen_y + planet.atmosphere_radius > 0 and 
                screen_y - planet.atmosphere_radius < SCREEN_HEIGHT):
                planet.draw(screen, world_offset_x, world_offset_y)
            
                
        if clicked:
            joystick.check()
            joystick.draw(screen)
            direction_vector = joystick.vector1
            ship.update(direction_vector, direction_vector.length())
            

            world_offset_x -= ship.velocity.x 
            world_offset_y -= ship.velocity.y 
            trail_points.append((world_offset_x, world_offset_y))
        else:

            ship.update(pygame.Vector2(0, 0), 0)
            world_offset_x -= ship.velocity.x
            world_offset_y -= ship.velocity.y
            trail_points.append((world_offset_x, world_offset_y))
                    
        
        # Rysowanie siatki
        grid_offset_x = world_offset_x % GRID_SIZE
        grid_offset_y = world_offset_y % GRID_SIZE
        
        # Rysowanie pionowych linii siatki
        for x in range(int(grid_offset_x), SCREEN_WIDTH + GRID_SIZE, GRID_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
            
        # Rysowanie poziomych linii siatki
        for y in range(int(grid_offset_y), SCREEN_HEIGHT + GRID_SIZE, GRID_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
        
        # Rysowanie śladu
        if len(trail_points) > 1:
            # Przekształcamy punkty śladu na koordynaty ekranu
            screen_trail = [(SCREEN_WIDTH//2 - (x - trail_points[-1][0]),
                           SCREEN_HEIGHT//2 - (y - trail_points[-1][1])) 
                          for x, y in trail_points]
            pygame.draw.lines(screen, (50, 50, 255), False, screen_trail, 2)
        
        # Rysowanie statku (zawsze na środku)
        ship.draw(screen)
        
        
        # Rysowanie wskaźnika kierunku (kompas)
        compass_radius = 50
        compass_x = SCREEN_WIDTH - 70
        compass_y = SCREEN_HEIGHT - 70
        pygame.draw.circle(screen, (50, 50, 50), (compass_x, compass_y), compass_radius, 1)
        
        # Kierunek ruchu na kompasie
        if ship.vector.length() > 0:
            direction_x = compass_x + ship.vector.x * compass_radius
            direction_y = compass_y + ship.vector.y * compass_radius
            pygame.draw.line(screen, (255, 0, 0), (compass_x, compass_y), 
                           (direction_x, direction_y), 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                joystick.check()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            
        # W głównej pętli while
        draw_minimap(screen, planets, world_offset_x, world_offset_y, 
             (ship.x, ship.y))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
    
def draw_minimap(screen, planets, world_offset_x, world_offset_y, ship_pos):
    MAP_SIZE = 200
    MAP_X = 20
    MAP_Y = 20
    MAP_SCALE = 0.01
    
    minimap_surface = pygame.Surface((MAP_SIZE, MAP_SIZE))
    minimap_surface.fill((20, 20, 20))
    pygame.draw.rect(minimap_surface, (50, 50, 50), (0, 0, MAP_SIZE, MAP_SIZE), 1)
    
    map_center_x = MAP_SIZE // 2
    map_center_y = MAP_SIZE // 2
    
    # Poprawione obliczanie pozycji planet
    for planet in planets:
        # Oblicz względną pozycję planety względem statku
        rel_x = (world_offset_x - planet.x) * MAP_SCALE
        rel_y = (world_offset_y - planet.y) * MAP_SCALE
        
        # Przekształć na koordynaty minimapy
        map_x = map_center_x + rel_x
        map_y = map_center_y + rel_y
        
        # Rysuj tylko jeśli planeta jest w granicach minimapy
        if (0 <= map_x <= MAP_SIZE and 0 <= map_y <= MAP_SIZE):
            planet_size = max(2, min(8, planet.mass / 2000))
            pygame.draw.circle(minimap_surface, (200, 200, 200), 
                             (int(map_x), int(map_y)), 
                             int(planet_size))
    
    # Statek zawsze w środku
    pygame.draw.circle(minimap_surface, (255, 0, 0), 
                      (map_center_x, map_center_y), 3)
    
    pygame.draw.rect(minimap_surface, (100, 100, 100), 
                    (0, 0, MAP_SIZE, MAP_SIZE), 2)
    
    screen.blit(minimap_surface, (MAP_X, MAP_Y))
    
if __name__ == "__main__":
    main()