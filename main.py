import pygame
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
ELEVATOR_WIDTH = 100
ELEVATOR_HEIGHT = 100
FLOOR_COUNT = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Elevator Game")

clock = pygame.time.Clock()

elevator = pygame.Rect((SCREEN_WIDTH - ELEVATOR_WIDTH) // 2, SCREEN_HEIGHT - ELEVATOR_HEIGHT, ELEVATOR_WIDTH, ELEVATOR_HEIGHT)
floor_height = SCREEN_HEIGHT // FLOOR_COUNT
current_floor = FLOOR_COUNT - 1
target_floor = current_floor
speed = 5

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

    target_y = SCREEN_HEIGHT - (target_floor + 1) * floor_height

    if elevator.y > target_y:
        elevator.y -= speed
    elif elevator.y < target_y:
        elevator.y += speed

    screen.fill(WHITE)

    for i in range(FLOOR_COUNT):
        pygame.draw.line(screen, GRAY, (0, SCREEN_HEIGHT - (i + 1) * floor_height), (SCREEN_WIDTH, SCREEN_HEIGHT - (i + 1) * floor_height), 2)

    pygame.draw.rect(screen, BLACK, elevator)

    pygame.display.flip()

    clock.tick(FPS)
