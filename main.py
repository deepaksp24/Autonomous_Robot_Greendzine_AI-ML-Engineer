import pygame
from a_star import a_star 

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1010, 810
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Warehouse Robot Simulation with Mini-Map')
running = True

box = pygame.image.load('images/single_box100.png').convert_alpha()
robot = pygame.image.load('images/robot10.png').convert_alpha()
block = pygame.image.load('images/block_box100.png').convert_alpha()
travsed = pygame.image.load('images/travesed100.png').convert_alpha()

warehouse = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
]


start = (0, 0) # starting point of robot 
end = (7, 9)
path = a_star(warehouse, start, end) 
travsed_set = set() 

rx, ry = start[1] * 100 + 50, start[0] * 100 + 50
path_index = 0  # Keep track of the current step in the path
move_speed = 10  # Movement speed of the robot

# Mini-map parameters
MINI_MAP_SCALE = 0.1  # mini mao size
MINI_MAP_CELL_SIZE = int(100 * MINI_MAP_SCALE)  # Scaled cell size
MINI_MAP_X, MINI_MAP_Y = WINDOW_WIDTH - (10 * MINI_MAP_CELL_SIZE) - 10, 10  # Top-right corner position

pygame.time.delay(10000)

font = pygame.font.Font(None, 36)
start_ticks = pygame.time.get_ticks()  # Record start time


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    minutes = elapsed_ticks // 60000
    seconds = (elapsed_ticks % 60000) // 1000
    timer_text = f"Time: {minutes:02}:{seconds:02}"

    # camera offset for camera
    camera_x_offset = rx - WINDOW_WIDTH // 2
    camera_y_offset = ry - WINDOW_HEIGHT // 2

    display_surface.fill('dark gray')

    # Draw warehouse grid with camera offset
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            cell_x = j * 100 - camera_x_offset
            cell_y = i * 100 - camera_y_offset
            if (i,j) in travsed_set:
                display_surface.blit(travsed, (cell_x, cell_y))
            elif warehouse[i][j] == 0:
                display_surface.blit(box, (cell_x, cell_y))
            else:
                display_surface.blit(block, (cell_x, cell_y))

    # Move robot along the path if not reached the end
    if  path_index < len(path):
        cell_y, cell_x = path[path_index]  # Get the next cell in the path
        target_x, target_y = cell_x * 100 + 50, cell_y * 100 + 50

        # Check if the robot is close enough to the target center
        if abs(rx - target_x) <= move_speed and abs(ry - target_y) <= move_speed:
            rx, ry = target_x, target_y  # Snap to target to avoid oscillation
            travsed_set.add((cell_y,cell_x))
            path_index += 1  # Move to the next cell in the path
        else:
            # Move the robot smoothly towards the target cell
            if rx < target_x: rx += move_speed
            elif rx > target_x: rx -= move_speed
            if ry < target_y: ry += move_speed
            elif ry > target_y: ry -= move_speed

    # Draw the robot with camera offset
    display_surface.blit(robot, (rx - camera_x_offset, ry - camera_y_offset))

    # Draw mini-map in the top-right corner
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            mini_cell_x = MINI_MAP_X + j * MINI_MAP_CELL_SIZE
            mini_cell_y = MINI_MAP_Y + i * MINI_MAP_CELL_SIZE
            color = (200, 200, 200) if warehouse[i][j] == 0 else (100, 100, 100)  # Box or block color
            pygame.draw.rect(display_surface, color, (mini_cell_x, mini_cell_y, MINI_MAP_CELL_SIZE, MINI_MAP_CELL_SIZE))

    # Draw robot position on the mini-map
    robot_mini_x = MINI_MAP_X + (rx // 100) * MINI_MAP_CELL_SIZE
    robot_mini_y = MINI_MAP_Y + (ry // 100) * MINI_MAP_CELL_SIZE
    pygame.draw.rect(display_surface, (255, 0, 0), (robot_mini_x, robot_mini_y, MINI_MAP_CELL_SIZE, MINI_MAP_CELL_SIZE))

    timer_surface = font.render(timer_text, True, (255, 255, 255))
    display_surface.blit(timer_surface, (10, 10))  # Top-left corner
    
    pygame.time.delay(2000) # delay of 2 sec 
    pygame.display.update()

pygame.quit()
