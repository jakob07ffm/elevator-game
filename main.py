import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
ELEVATOR_WIDTH = 100
ELEVATOR_HEIGHT = 100
DOOR_WIDTH = 50
DOOR_HEIGHT = ELEVATOR_HEIGHT
FLOOR_COUNT = 5
ELEVATOR_COUNT = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Elevator Game")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
door_open_time = 2 * FPS  # Time to keep doors open
door_speed = 10

class Elevator:
    def __init__(self, x_pos):
        self.rect = pygame.Rect(x_pos, SCREEN_HEIGHT - ELEVATOR_HEIGHT, ELEVATOR_WIDTH, ELEVATOR_HEIGHT)
        self.target_floor = FLOOR_COUNT - 1
        self.current_floor = FLOOR_COUNT - 1
        self.speed = 5
        self.door_open = False
        self.door_timer = 0
        self.door_offset = 0

    def move(self):
        target_y = SCREEN_HEIGHT - (self.target_floor + 1) * (SCREEN_HEIGHT // FLOOR_COUNT)
        if self.rect.y > target_y:
            self.rect.y -= self.speed
            self.door_open = False
        elif self.rect.y < target_y:
            self.rect.y += self.speed
            self.door_open = False
        else:
            if not self.door_open:
                self.door_timer += 1
                if self.door_timer >= door_open_time:
                    self.door_open = True
                    self.door_timer = 0

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)
        if self.door_open:
            pygame.draw.rect(screen, WHITE, (self.rect.x + self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))
            pygame.draw.rect(screen, WHITE, (self.rect.x + ELEVATOR_WIDTH - DOOR_WIDTH - self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))
        else:
            pygame.draw.rect(screen, BLACK, (self.rect.x + self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))
            pygame.draw.rect(screen, BLACK, (self.rect.x + ELEVATOR_WIDTH - DOOR_WIDTH - self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))

    def set_target_floor(self, floor):
        self.target_floor = floor

elevators = [Elevator((i * (SCREEN_WIDTH // ELEVATOR_COUNT) + (SCREEN_WIDTH // ELEVATOR_COUNT - ELEVATOR_WIDTH) // 2)) for i in range(ELEVATOR_COUNT)]

def draw_floors():
    for i in range(FLOOR_COUNT):
        pygame.draw.line(screen, GRAY, (0, SCREEN_HEIGHT - (i + 1) * (SCREEN_HEIGHT // FLOOR_COUNT)), (SCREEN_WIDTH, SCREEN_HEIGHT - (i + 1) * (SCREEN_HEIGHT // FLOOR_COUNT)), 2)
        label = font.render(f"Floor {i+1}", True, BLACK)
        screen.blit(label, (10, SCREEN_HEIGHT - (i + 1) * (SCREEN_HEIGHT // FLOOR_COUNT) + 10))

def draw_floor_indicator():
    for i, elevator in enumerate(elevators):
        indicator_rect = pygame.Rect(SCREEN_WIDTH - 70, 50 + i * 60, 60, 50)
        pygame.draw.rect(screen, RED, indicator_rect)
        floor_text = font.render(f"{elevator.target_floor + 1}", True, WHITE)
        screen.blit(floor_text, (indicator_rect.x + 15, indicator_rect.y + 10))
        pygame.draw.rect(screen, BLUE, (elevator.rect.x + 20, elevator.rect.y - 30, ELEVATOR_WIDTH - 40, 20))
        status_text = font.render(f"Elevator {i+1}", True, WHITE)
        screen.blit(status_text, (elevator.rect.x + 20, elevator.rect.y - 60))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                for elevator in elevators:
                    elevator.set_target_floor(0)
            elif event.key == pygame.K_2:
                for elevator in elevators:
                    elevator.set_target_floor(1)
            elif event.key == pygame.K_3:
                for elevator in elevators:
                    elevator.set_target_floor(2)
            elif event.key == pygame.K_4:
                for elevator in elevators:
                    elevator.set_target_floor(3)
            elif event.key == pygame.K_5:
                for elevator in elevators:
                    elevator.set_target_floor(4)
            elif event.key == pygame.K_UP:
                for elevator in elevators:
                    elevator.speed = min(elevator.speed + 1, 10)
            elif event.key == pygame.K_DOWN:
                for elevator in elevators:
                    elevator.speed = max(elevator.speed - 1, 1)

    for elevator in elevators:
        elevator.move()

    screen.fill(WHITE)

    draw_floors()
    for elevator in elevators:
        elevator.draw()
    draw_floor_indicator()

    pygame.display.flip()
    clock.tick(FPS)
