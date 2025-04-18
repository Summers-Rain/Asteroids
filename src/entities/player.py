import pygame
import random
import math
from src.utilities.circleshape import CircleShape
from src.constants import *
from src.entities.bullet import Shot
from src.entities.particle import Particle

class Player(CircleShape, pygame.sprite.Sprite):
    containers = None # Will be set to a sprite group later for automatic management

    def __init__(self, x, y):
        # Initialize both parent classes
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Add a list to store particles
        self.particles = []

        # Position and movement vectors
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        # Create sprite surface and rectangle
        self.image = pygame.Surface((PLAYER_RADIUS*2, PLAYER_RADIUS*2), pygame.SRCALPHA) # Transparent surface
        self.rect = self.image.get_rect()   # Get bounding rectangle
        self.rect.center = (int(x), int(y)) # center rectangle on initial position

        self.lives = INITIAL_LIVES  # Starting number of lives (I will probably alway's know what this does haha)

        # Respawn state flags
        self.is_dead = False # Player Died and waiting to respawn
        self.is_respawning = False  # Player is respawning with invulnerability

        # Timers
        self.death_timer = 0 # When the player died
        self.invulnerability_timer = 0  # When invulnerability started
        self.flicker_counter = 0 # For visual blinking effect

        self.rotation = 0 # Current rotation angle in degrees
        self.rotation_velocity = 0
        self.timer = 0 # Shot cooldown timer

    def draw(self, screen):
        # Don't draw if player is dead
        if self.is_dead:
            return
        
        # Handle flicker effect during respawn
        if self.is_respawning:
            # Increment the flicker counter (this can also be done in update)
            self.flicker_counter +=1

            # Skip drawing every other few frames for blinking effect
            if self.flicker_counter % 6 >= 3:
                return
            
            # Draw shield effect
            pygame.draw.circle(screen, (100, 200, 255), 
                         (int(self.position.x), int(self.position.y)), 
                         self.radius + 5, 2)
            
        # Draw the player as a white triangle
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2) # 2 = line width

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            # Draw thruster flame behind the ship
            forward = pygame.Vector2(0,1).rotate(self.rotation)
            thruster_pos = self.position - forward * (self.radius + 2)

            # Triangle points for thruster
            t1 = thruster_pos - forward * 8
            t2 = thruster_pos + pygame.Vector2(0, 1).rotate(self.rotation + 160) * 3
            t3 = thruster_pos + pygame.Vector2(0, 1).rotate(self.rotation - 160) * 3

            # Draw with a flickering color for flame effect
            flame_intensity = random.randint(150, 255)
            flame_color = (flame_intensity, flame_intensity//2, 0)
            pygame.draw.polygon(screen, flame_color, [t1, t2, t3])

    def create_thrust_particles(self):
        # Get the backward direction from player rotation
        backward = pygame.Vector2(0, 1).rotate(self.rotation - 180)

        # Spawn position - behind the ship
        spawn_pos = self.position + backward * self.radius

        # Create 1-3 particles
        for _ in range(random.randint(1, 3)):
            # Random velocity based on backward direction with some spread
            angle_spread = random.uniform(-20, 20)
            particle_dir = backward.rotate(angle_spread)

            # Random speed
            speed = random.uniform(50, 150)
            velocity = particle_dir * speed

            # Random size, color, and lifetime
            size = random.uniform(2, 5)
            r = random.randint(200, 255)
            g = random.randint(100, 180)
            b = random.randint(0, 50)
            lifetime = random.uniform(0.5, 1.0)

            # Create particle
            particle = Particle(spawn_pos.x, spawn_pos.y, velocity, size, (r, g, b), lifetime)
            self.particles.append(particle)

    def triangle(self):
        # Calculate the three points of the player's triangle
        forward = pygame.Vector2(0, 1).rotate(self.rotation) # Forward unit vector based on rotation
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5 # Right perpendicular vector
        # Calculate the three vertices
        a = self.position + forward * self.radius # Nose of the ship
        b = self.position - forward * self.radius - right # Bottom-left point
        c = self.position - forward * self.radius + right # Bottom-right point
        return [a, b, c] # Return points for drawing

    def update(self, dt, keys):
        # Check if it's time to respawn
        if self.is_dead:
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.death_timer) / 1000

            if elapsed >= RESPAWN_DELAY:
                # Respawn the player
                self.is_dead = False
                self.is_respawning = True
                self.invulnerability_timer = pygame.time.get_ticks()
                self.flicker_counter = 0
                self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Center of screen
                self.velocity = pygame.Vector2(0, 0) # Reset velocity
                self.rotation = 0
            # Don't process movement while dead
            return

        # Handle invulnerability period
        if self.is_respawning:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerability_timer > RESPAWN_INVULNERABILITY_TIME:
                self.is_respawning = False

        # Add acceleration damping
        self.velocity *= (1 - PLAYER_FRICTION * dt)
        # Add rotation damping
        self.rotation_velocity *= (1 - PLAYER_ROTATION_FRICTION * dt)

        # Update position based on velocity
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

        # Screen Wrapping - if player goes off one edge 
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
            
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        
        self.rect.center = (int(self.position.x), int(self.position.y))

        if self.timer > 0:
            self.timer -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, direction=1)
            self.create_thrust_particles()
        if keys[pygame.K_s]:
            self.move(dt, direction=-1)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        updated_particles = []
        for particle in self.particles:
            if particle.update(dt):
                updated_particles.append(particle)
        self.particles = updated_particles

    def draw_particles(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def respawn(self):
        # Player was hit
        self.lives -= 1

        # Clear particles when player dies
        self.particles = []

        if self.lives < 0:
            # Game over
            return False
        
        # Start death sequence
        self.is_dead = True
        self.death_timer = pygame.time.get_ticks()
        # Not game over yet
        return True

    def rotate(self, dt):
        # Aplly rotation acceleration
        rotation_acceleration = PLAYER_ROTATION_ACCELERATION * dt
        if dt > 0: # Turning right
            self.rotation_velocity += rotation_acceleration
        else: # Turning left
            self.rotation_velocity -= rotation_acceleration

        # Cap max rotation speed
        max_rotation_speed = PLAYER_TURN_SPEED
        if abs(self.rotation_velocity) > max_rotation_speed:
            self.rotation_velocity = math.copysign(max_rotation_speed, self.rotation_velocity)
        
        # Apply rotation
        self.rotation += self.rotation_velocity * dt

    def move(self, dt, direction=1):
        # Apply thrust in the direction the player is facing
        # direction: 1 = forward, -1 = backward
        forward = pygame.Vector2(0, 1).rotate(self.rotation) # Convert from pygame coordinates

        if direction > 0:
            current_speed = self.velocity.length()
            boost_factor = 1.0
            if current_speed < PLAYER_SPEED * 0.2:
                boost_factor = 1.5

            acceleration = forward * PLAYER_ACCELERATION * dt * boost_factor
            self.velocity += acceleration
        else:
            if self.velocity.length() > 0:
                brake_strength = PLAYER_BRAKE_STRENGTH * abs(dt)
                brake_vector = -self.velocity.normalize() * brake_strength
                self.velocity += brake_vector
        
        max_speed = PLAYER_SPEED * 1.1 # Allow slight overspeed from boosts
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)
    
    def shoot(self):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.timer > 0:
            return
        else:
            velocity = direction * PLAYER_SHOOT_SPEED
            shot = Shot(self.position.x, self.position.y, velocity)
            self.timer = PLAYER_SHOOT_COOLDOWN

    def collision(self, other):
        # Calculate distance between centers
        distance = self.position.distance_to(other.position)
        # Check if distance is less than sum of radii
        return distance < (self.radius + other.radius)