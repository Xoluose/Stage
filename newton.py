import pygame
import random
import math

# Dimensions de la fenêtre
WIDTH = 1024
HEIGHT = 800

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK=(0,0,0)

# Classe pour représenter les particules
class Particle:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = random.uniform(-0.1, 0.1)
        self.speed_limit = 3
        self.num_particles = random.randint(20, 30)
        self.r = int(math.sqrt(self.mass/2*(math.pi)))
        self.color=WHITE
        if self.r < 1:
            self.r=1

    def update(self, particles):
        ax = 0
        ay = 0
        G = 0.1  # Constante gravitationnelle

        for particle in particles:
            if particle != self:
                dx = particle.x - self.x
                dy = particle.y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance == 0:
                    force = 0
                else:
                    force = (G * self.mass * particle.mass) / (distance ** 2)
                angle = math.atan2(dy, dx)
                ax += math.cos(angle) * force / self.mass
                ay += math.sin(angle) * force / self.mass

                if distance <self.r:
                    self.mass += particle.mass
                    particles.remove(particle)
                    if particle.mass > self.mass:
                        self.vx = particle.vx
                        self.vy = particle.vy
                    self.r = math.sqrt(self.mass/2*(math.pi))
                    if self.r < 1:
                        self.r=1

                    self.color =(255,255-abs(self.vx*100),255-abs(self.vy*100))


        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        #if speed > self.speed_limit:
        #    scale_factor = self.speed_limit / speed
        #    self.vx *= scale_factor
        #    self.vy *= scale_factor

        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy

        #if self.mass >= 50:
       #     for _ in range(self.mass):
       #         new_particle = Particle(self.x, self.y, 1)
        #        particles.append(new_particle)
        #    self.mass = 0

        self.x = (self.x + WIDTH) % WIDTH
        self.y = (self.y + HEIGHT) % HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, self.color , (int(self.x), int(self.y)), self.r)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

particles = []

# Création des particules
n = 100  # Nombre de particules
for _ in range(n):
    x = random.uniform(0, WIDTH)
    y = random.uniform(0, HEIGHT)
    mass = random.uniform(1, 5)

    particle = Particle(x, y, mass)
    particles.append(particle)

# Boucle principale du programme
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for particle in particles:
        particle.update(particles)
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# Fermeture de Pygame
pygame.quit()
