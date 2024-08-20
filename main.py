import pygame
import sys
import random

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
BUTTON_SIZE = 40
MAX_CAPACITY = 500  # Max weight capacity of an elevator in arbitrary units
PASSENGER_WEIGHT_RANGE = (50, 100)  # Weight range for passengers
ACCELERATION = 0.5  # Acceleration for elevators
MAX_SPEED = 5  # Maximum speed for elevators

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Elevator Game")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
door_open_time = 2 * FPS  # Time to keep doors open

elevator_movement_sound = pygame.mixer.Sound('elevator_move.wav')
door_open_sound = pygame.mixer.Sound('door_open.wav')
door_close_sound = pygame.mixer.Sound('door_close.wav')
floor_arrival_sound = pygame.mixer.Sound('floor_arrival.wav')

class Passenger:
    def __init__(self, start_floor):
        self.start_floor = start_floor
        self.destination_floor = random.randint(0, FLOOR_COUNT - 1)
        while self.destination_floor == start_floor:
            self.destination_floor = random.randint(0, FLOOR_COUNT - 1)
        self.weight = random.randint(*PASSENGER_WEIGHT_RANGE)

    def draw(self, x, y):
        pygame.draw.circle(screen, YELLOW, (x, y), 15)
        label = font.render(str(self.destination_floor + 1), True, BLACK)
        screen.blit(label, (x - 10, y - 10))

class Elevator:
    def __init__(self, x_pos):
        self.rect = pygame.Rect(x_pos, SCREEN_HEIGHT - ELEVATOR_HEIGHT, ELEVATOR_WIDTH, ELEVATOR_HEIGHT)
        self.target_floor = FLOOR_COUNT - 1
        self.current_floor = FLOOR_COUNT - 1
        self.speed = 0
        self.door_open = False
        self.door_timer = 0
        self.door_offset = 0
        self.call_queue = []
        self.passengers = []
        self.total_weight = 0

    def move(self):
        if not self.call_queue:
            return

        if self.total_weight > MAX_CAPACITY:
            return

        self.target_floor = self.call_queue[0]
        target_y = SCREEN_HEIGHT - (self.target_floor + 1) * (SCREEN_HEIGHT // FLOOR_COUNT)

        if self.rect.y > target_y:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
            self.rect.y -= self.speed
            self.door_open = False
        elif self.rect.y < target_y:
            self.speed = min(self.speed + ACCELERATION, MAX_SPEED)
            self.rect.y += self.speed
            self.door_open = False
        else:
            self.speed = 0
            if not self.door_open:
                self.door_timer += 1
                if self.door_timer >= door_open_time:
                    pygame.mixer.Sound.play(door_open_sound)
                    self.door_open = True
                    self.door_timer = 0
                    self.load_passengers()
                    self.call_queue.pop(0)
            else:
                self.door_timer += 1
                if self.door_timer >= door_open_time:
                    pygame.mixer.Sound.play(door_close_sound)
                    self.door_open = False
                    self.door_timer = 0

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)
        if self.door_open:
            pygame.draw.rect(screen, WHITE, (self.rect.x + self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))
            pygame.draw.rect(screen, WHITE, (self.rect.x + ELEVATOR_WIDTH - DOOR_WIDTH - self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))
            self.draw_passengers()
        else:
            pygame.draw.rect(screen, BLACK, (self.rect.x + self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))
            pygame.draw.rect(screen, BLACK, (self.rect.x + ELEVATOR_WIDTH - DOOR_WIDTH - self.door_offset, self.rect.y, DOOR_WIDTH, DOOR_HEIGHT))

    def draw_passengers(self):
        for i, passenger in enumerate(self.passengers):
            passenger.draw(self.rect.x + 20 + (i % 2) * 40, self.rect.y + 20 + (i // 2) * 40)

    def set_target_floor(self, floor):
        if floor not in self.call_queue:
            self.call_queue.append(floor)
            self.call_queue.sort(key=lambda x: abs(self.current_floor - x))

    def load_passengers(self):
        global waiting_passengers
        boarding_passengers = [p for p in waiting_passengers[self.current_floor] if p.destination_floor not in self.call_queue]
        for passenger in boarding_passengers:
            if self.total_weight + passenger.weight <= MAX_CAPACITY:
                self.passengers.append(passenger)
                self.total_weight += passenger.weight
                waiting_passengers[self.current_floor].remove(passenger)
                self.set_target_floor(passenger.destination_floor)

    def unload_passengers(self):
        exiting_passengers = [p for p in self.passengers if p.destination_floor == self.current_floor]
        for passenger in exiting_passengers:
            self.passengers.remove(passenger)
            self.total_weight -= passenger.weight

waiting_passengers = {floor: [Passenger(floor) for _ in range(random.randint(0, 3))] for floor in range(FLOOR_COUNT)}

elevators = [Elevator((i * (SCREEN_WIDTH // ELEVATOR_COUNT) + (SCREEN_WIDTH // ELEVATOR_COUNT - ELEVATOR_WIDTH) // 2)) for i in range(ELEVATOR_COUNT)]

class CallButton:
    def __init__(self, x, y, floor):
        self.rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)
        self.floor = floor
        self.active = False

    def draw(self):
        color = RED if self.active else GREEN
        pygame.draw.rect(screen, color, self.rect)

    def press(self):
        self.active = True
        closest_elevator = min(elevators, key=lambda e: (len(e.call_queue), abs(e.current_floor - self.floor)))
        closest_elevator.set_target_floor(self.floor)

call_buttons = []
for i in range(FLOOR_COUNT):
    call_buttons.append(CallButton(SCREEN_WIDTH - BUTTON_SIZE - 10, SCREEN_HEIGHT - (i + 1) * (SCREEN_HEIGHT // FLOOR_COUNT) + 10, i))

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
        status_text = font.render(f"E{i+1} W:{elevator.total_weight}", True, WHITE)
        screen.blit(status_text, (elevator.rect.x + 20, elevator.rect.y - 60))

def update_call_buttons():
    for button in call_buttons:
        if button.active:
            button.draw()
        else:
            button.draw()

def draw_waiting_passengers():
    for floor, passengers in waiting_passengers.items():
        for i, passenger in enumerate(passengers):
            x = 50 + i * 50
            y = SCREEN_HEIGHT - (floor + 1) * (SCREEN_HEIGHT // FLOOR_COUNT) + 20
            passenger.draw(x, y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for elevator in elevators:
                    elevator.speed = min(elevator.speed + 1, 10)
            elif event.key == pygame.K_DOWN:
                for elevator in elevators:
                    elevator.speed = max(elevator.speed - 1, 1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in call_buttons:
                if button.rect.collidepoint(pos):
                    button.press()

    for elevator in elevators:
        elevator.move()
        elevator.unload_passengers()

    screen.fill(WHITE)

    draw_floors()
    for elevator in elevators:
        elevator.draw()
    draw_floor_indicator()
    update_call_buttons()
    draw_waiting_passengers()

    pygame.display.flip()
    clock.tick(FPS)
