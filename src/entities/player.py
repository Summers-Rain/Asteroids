import pygame
from src.utilities.circleshape import CircleShape
from src.constants import *
from src.entities.bullet import Shot

class Player(CircleShape, pygame.sprite.Sprite):
    containers = None # Will be set to a sprite group later for automatic management

    def __init__(self, x, y):
        # Initialize both parent classes
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self, self.containers)

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

    def triangle(self):
        # Calculate the three points of the player's triangle
        forward = pygame.Vector2(0, 1).rotate(self.rotation) # Forward unit vector based on rotation
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5 # Right perpendicular vector
        # Calculate the three vertices
        a = self.position + forward * self.radius # Nose of the ship
        b = self.position - forward * self.radius - right # Bottom-left point
        c = self.position - forward * self.radius + right # Bottom-right point
        return [a, b, c] # Return points for drawing

    def update(self, dt):
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
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def respawn(self):
        # Player was hit
        self.lives -= 1

        if self.lives < 0:
            # Game over
            return False
        
        # Start death sequence
        self.is_dead = True
        self.death_timer = pygame.time.get_ticks()
        # Not game over yet
        return True

    def rotate(self, dt):
        # Rotate the player based on direction (1 = right, -1 = left)
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        # Apply thrust in the direction the player is facing
        # direction: 1 = forward, -1 = backward
        forward = pygame.Vector2(0, 1).rotate(self.rotation) # Convert from pygame coordinates
        self.position += forward * PLAYER_SPEED * dt
    
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