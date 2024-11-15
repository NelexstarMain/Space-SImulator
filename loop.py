import pygame
from SpaceShip import SpaceShip
from JoyStick import JoyStick

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
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()