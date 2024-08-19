import pygame
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
ELEVATOR_WIDTH = 100
ELEVATOR_HEIGHT = 100
DOOR_WIDTH = ELEVATOR_WIDTH // 2
DOOR_HEIGHT = ELEVATOR_HEIGHT
FLOOR_COUNT = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Elevator Game")

clock = pygame.time.Clock()

elevator = pygame.Rect((SCREEN_WIDTH - ELEVATOR_WIDTH) // 2, SCREEN_HEIGHT - ELEVATOR_HEIGHT, ELEVATOR_WIDTH, ELEVATOR_HEIGHT)
floor_height = SCREEN_HEIGHT // FLOOR_COUNT
current_floor = FLOOR_COUNT - 1
target_floor = current_floor
speed = 5
door_open = False
door_timer = 0

font = pygame.font.Font(None, 36)

def draw_floors():
    for i in range(FLOOR_COUNT):
        pygame.draw.line(screen, GRAY, (0, SCREEN_HEIGHT - (i + 1) * floor_height), (SCREEN_WIDTH, SCREEN_HEIGHT - (i + 1) * floor_height), 2)
        label = font.render(f"Floor {i+1}", True, BLACK)
        screen.blit(label, (10, SCREEN_HEIGHT - (i + 1) * floor_height + 10))

def draw_elevator():
    pygame.draw.rect(screen, BLACK, elevator)
    if door_open:
        pygame.draw.rect(screen, WHITE, (elevator.x, elevator.y, DOOR_WIDTH, DOOR_HEIGHT))
        pygame.draw.rect(screen, WHITE, (elevator.x + DOOR_WIDTH, elevator.y, DOOR_WIDTH, DOOR_HEIGHT))

def move_elevator():
    global door_open, door_timer
    target_y = SCREEN_HEIGHT - (target_floor + 1) * floor_height
    if elevator.y > target_y:
        elevator.y -= speed
        door_open = False
    elif elevator.y < target_y:
        elevator.y += speed
        door_open = False
    else:
        if not door_open:
            door_timer += 1
            if door_timer >= FPS:
                door_open = True
                door_timer = 0

def draw_floor_indicator():
    indicator_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
    pygame.draw.rect(screen, RED, indicator_rect)
    floor_text = font.render(f"{target_floor+1}", True, WHITE)
    screen.blit(floor_text, (indicator_rect.x + 10, indicator_rect.y + 5))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                target_floor = 0
            elif event.key == pygame.K_2:
                target_floor = 1
            elif event.key == pygame.K_3:
                target_floor = 2
            elif event.key == pygame.K_4:
                target_floor = 3
            elif event.key == pygame.K_5:
                target_floor = 4
            elif event.key == pygame.K_UP:
                speed = min(speed + 1, 10)
            elif event.key == pygame.K_DOWN:
                speed = max(speed - 1, 1)

    move_elevator()

    screen.fill(WHITE)

    draw_floors()
    draw_elevator()
    draw_floor_indicator()

    pygame.display.flip()

    clock.tick(FPS)
