import pygame
from pygame.locals import *
import math

class Camera:
    def __init__(self, pos=(0, 0, 0), rotation=(0, 0)):
        self.pos = list(pos)
        self.rotation = list(rotation)
        self.move_speed = 0.05
        self.side_speed = 0.03
        self.move_direction = [0, 0, 0]
        self.side_direction = 0
        self.rotation_speed = 0.02
        self.rotation_direction = 0

    def move_forward(self):
        self.move_direction[0] = math.sin(self.rotation[1]) * self.move_speed
        self.move_direction[2] = -math.cos(self.rotation[1]) * self.move_speed

    def move_backward(self):
        self.move_direction[0] = -math.sin(self.rotation[1]) * self.move_speed
        self.move_direction[2] = math.cos(self.rotation[1]) * self.move_speed

    def move_left(self):
        self.side_direction = -1

    def move_right(self):
        self.side_direction = 1

    def rotate_left(self):
        self.rotation_direction = 1

    def rotate_right(self):
        self.rotation_direction = -1

    def stop_move(self):
        self.move_direction = [0, 0, 0]

    def stop_side_move(self):
        self.side_direction = 0

    def stop_rotation(self):
        self.rotation_direction = 0

    def update(self):
        dx = self.move_direction[0]
        dy = self.move_direction[1]
        dz = self.move_direction[2]
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += dz

        if self.side_direction != 0:
            side_angle = self.rotation[1] + math.pi / 2 * self.side_direction
            self.pos[0] += math.cos(side_angle) * self.side_speed
            self.pos[1] += math.sin(side_angle) * self.side_speed

        self.rotation[1] += self.rotation_direction * self.rotation_speed

class Sphere:
    def __init__(self, center=(0, 0, 0), radius=1, num_points=30):
        self.center = center
        self.radius = radius
        self.num_points = num_points
        self.vertices = self.generate_vertices()

    def generate_vertices(self):
        vertices = []
        for i in range(self.num_points):
            theta = 2 * math.pi * i / self.num_points
            for j in range(self.num_points):
                phi = math.pi * j / self.num_points
                x = self.center[0] + self.radius * math.sin(phi) * math.cos(theta)
                y = self.center[1] + self.radius * math.sin(phi) * math.sin(theta)
                z = self.center[2] + self.radius * math.cos(phi)
                vertices.append((x, y, z))
        return vertices

def project(camera, point):
    x, y, z = point
    x -= camera.pos[0]
    y -= camera.pos[1]
    z -= camera.pos[2]
    x, z = rotate2d((x, z), camera.rotation[1])
    y, z = rotate2d((y, z), camera.rotation[0])
    distance = 2
    fov = 256
    aspect_ratio = 4 / 3
    scale = fov / (z + distance)
    x = x * scale * aspect_ratio
    y = -y * scale
    return int(x), int(y)

def rotate2d(pos, theta):
    x, y = pos
    s, c = math.sin(theta), math.cos(theta)
    return x * c - y * s, y * c + x * s

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 640
screen_height = 480

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sphere')

# Initialize camera and sphere
camera = Camera((0, 0, -5))
sphere = Sphere()

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000.0  # Get time in seconds since last frame
    screen.fill(BLACK)  # Clear screen

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                camera.move_forward()
            elif event.key == K_DOWN:
                camera.move_backward()
            elif event.key == K_LEFT:
                camera.move_left()
            elif event.key == K_RIGHT:
                camera.move_right()
            elif event.key == K_a:
                camera.rotate_left()
            elif event.key == K_d:
                camera.rotate_right()
        elif event.type == KEYUP:
            if event.key in [K_UP, K_DOWN]:
                camera.stop_move()
            elif event.key in [K_LEFT, K_RIGHT]:
                camera.stop_side_move()
            elif event.key in [K_a, K_d]:
                camera.stop_rotation()

    camera.update()

    # Project and draw sphere vertices
    for vertex in sphere.vertices:
        projected_vertex = project(camera, vertex)
        pygame.draw.circle(screen, WHITE, projected_vertex, 1)

    pygame.display.flip()  # Update screen

pygame.quit()