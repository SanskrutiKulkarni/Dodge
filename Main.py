import pygame
import os
import os.path
import sys
import time
import random
import neat
pygame.init()


#Some variables below

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
VEL = 7
WIDTH, HEIGHT = 750, 750
GEN = 0

# These are images i have for the player and for the obstacles
Sprite_Image = pygame.image.load("Dodger_game/Player_Ship.png")
Obstacle_Image = pygame.image.load("Dodger_game/obstacle.png")

# this part is supposed to be opening and reading the file i want adn to create it if it doesnt exist


# Just some font
FONT = pygame.font.SysFont("comicsans", 30)

# This is for the window 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")
 
# I created a class here for the player 
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Sprite_Image 
        self.mask = pygame.mask.from_surface(self.sprite) # this assigns the image to the player
    
    def move_left(self, vel): #obstacles can only move left in the x direction
        self.x += vel

    def move_right(self, vel): #obstacles can only move right in the x direction
        self.x -= vel
    
    def draw(self, win): #This function is to draw the player on to the screen
        win.blit(self.sprite, (self.x, self.y))
        
    def get_width(self):
        return self.sprite.get_width()

    def get_height(self):
        return self.sprite.get_height()

def quit():
    pygame.quit()
    sys.exit()


class Obstacles: #This class is for the obstacles similar to the player
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Obstacle_Image 
        self.mask = pygame.mask.from_surface(self.sprite)

    def move(self, vel): #obstacles can only move in the y direction
        self.y += vel

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def get_width(self): #This is to get the width of the player
        return self.sprite.get_width()
    
    def get_height(self):
        return self.sprite.get_height()


def collide(obj1, obj2): #This is a function to be used when checking if two objects collide with each other
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #If two masks overlap then the collision is true


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        # You can add other pause-related functionality here, such as displaying a pause menu or message
        pygame.display.update()


def main(genomes, config):
    global GEN
    GEN += 1
    run = True
    FPS = 60
    Score = 0
    file_path = "highscore.txt"
    HighScore = 0 # Set a default value for HighScore
    
    Nets = []
    ge = []
    obstacles = [] # This creates a list for the obstacles
    Ships = []
    #Ship = Player(300, 650)
    

    for _, g in genomes:
        Net = neat.nn.FeedForwardNetwork.create(g, config)
        Nets.append(Net)
        Ship = Player(300, 650)
        Ships.append(Ship)
        g.fitness = 0
        ge.append(g)

    if os.path.isfile(file_path): # Check if the file exists
        with open(file_path, "r") as file:
            contents = file.read().strip() # Remove any leading/trailing white spaces

            if contents.isdigit(): # Check if the contents are digits only
                HighScore = int(contents)
            else:
                print("Error: The contents of the file are not valid integers.")
                # Handle the error as needed
    else:
        print(f"The file '{file_path}' does not exist. Using default value for HighScore.")
        
    # This is the player we spawn them in this location
    clock = pygame.time.Clock()
    lost_font = pygame.font.SysFont("comicsans", 60)
 
    def draw(): # Here we start drawing everything on to the screen 
        WIN.fill(BLACK) 
        Score_label = FONT.render(f"SCORE: {Score}", 1, (255, 255, 255)) # This gets the score 
        gen_label = FONT.render(f"GEN: {GEN}", 1, (255, 255, 255)) # This gets the gen
        High_score_label = FONT.render(f"HIGH SCORE: {HighScore}", 1, (255, 255, 255))# This gets the Highscore 

        WIN.blit(Score_label, (10, 10)) # This puts the score value on the screen and the one below does the Highscore
        WIN.blit(gen_label, (300, 10))
        WIN.blit(High_score_label, (WIDTH - High_score_label.get_width() - 10, 10))
        
        for obstacle in obstacles: # This draws the obstacle 
            obstacle.draw(WIN)

        for Ship in Ships:
            Ship.draw(WIN) # This draws the player

        pygame.display.update()
    
    obstacle_timer = 0  # variable to track time elapsed since last obstacle added
    

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # set run variable to False to exit loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()  # pause the game if user presses ESC key

        # add new obstacle if enough time has elapsed
        obstacle_timer += clock.get_time() / 1000  # convert milliseconds to seconds
        if obstacle_timer > 1 and len(obstacles) < 5:  # spawn new obstacle every 1 second if there are less than 5 obstacles
            obstacle = Obstacles(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
            obstacles.append(obstacle)
            obstacle_timer = 0  # reset timer
            

        for Ship, Net, g in zip(Ships, Nets, ge):
            num_obstacles = min(len(obstacles), 5)

            input_values = [
                Ship.x,
                Ship.y,
                *[abs(Ship.y - obstacles[i].y) if i < len(obstacles) else -1 for i in range(num_obstacles)],
                *[abs(Ship.x - obstacles[i].x) if i < len(obstacles) else -1 for i in range(num_obstacles)],
                *[-1 for _ in range(12 - (2 + 2 * num_obstacles))]
            ]

            output = Net.activate(tuple(input_values))

            if output[0] < 0.5 and Ship.x - Ship.get_width() > 0:
                Ship.x -= 5  # Move left
            elif output[1] > 0.5 and Ship.x + (2*Ship.get_width()) < WIDTH:
                Ship.x += 5  # Move right
            # Add an else condition to handle the case where no movement is chosen based on output[2]
            else:
                pass

        for obstacle in obstacles:
            obstacle.move(VEL)
            if obstacle.y + obstacle.sprite.get_height() > HEIGHT:  # check if obstacle goes out of bounds
                obstacles.remove(obstacle)  # remove obstacle from list
                g.fitness += 1  # increase fitness for passing obstacle
                Score += 1  # increase score
            for Ship, g in zip(Ships, ge):
                if collide(obstacle, Ship):  # check for collision between obstacle and player
                    g.fitness -= 1  # decrease fitness for collision
                    Nets.pop(Ships.index(Ship))  # remove net from list
                    ge.pop(Ships.index(Ship))  # remove genome from list
                    Ships.pop(Ships.index(Ship))  # remove player from list


        if Score > HighScore: # Update HighScore if current score is higher
            HighScore = Score
            # Save HighScore to file
            with open(file_path, "w") as file:
                file.write(str(HighScore))

        draw()


        if len(Ships) == 0:  # check if all players are dead
            run = False  # exit loop if all players are dead

    

def run(config):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    #P = neat.Checkpointer.restore_checkpoint('neat-checkpoint-27')
    P = neat.Population(config)
    P.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    P.add_reporter(stats)
    #P.add_reporter(neat.Checkpointer(1))

    winner = P.run(main, 50)
    
if __name__ == '__main__':
    local_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    config_path = os.path.join(os.path.dirname(__file__), "config.txt")


    run(config_path)

    