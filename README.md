# Space Dodger Game with NEAT AI

This is a **space dodger** game implemented using **Pygame** for the game mechanics and **NEAT** (NeuroEvolution of Augmenting Topologies) for evolving AI agents that control the spaceship. The objective of the game is for AI-controlled spaceships to navigate falling obstacles and avoid collisions, while the neural networks controlling the spaceships evolve over multiple generations.
**You may need to change the address of the images in the main file**
### Technologies Used

1. **Pygame**:  
   Pygame is a Python library for game development that handles rendering, event management, and game loop functionality.

2. **NEAT (NeuroEvolution of Augmenting Topologies)**:  
   NEAT is used for evolving neural networks that control the AI agents (spaceships). The neural networks are trained using a genetic algorithm, where the best-performing networks reproduce to create new generations of neural networks.

### Key Concepts

#### 1. **Neural Networks and Evolution**
- The game features **neural networks** that control the behavior of each spaceship. Each spaceship's neural network receives inputs related to the game state (e.g., position of the spaceship, distance to obstacles) and produces outputs to control the spaceship's movement (left or right).
- The game uses **NEAT**, a genetic algorithm, to evolve these neural networks over multiple generations. The fitness of each spaceship (agent) is determined by how well it avoids obstacles. The more obstacles a spaceship avoids, the higher its fitness score, and the more likely it is to reproduce and pass on its network to the next generation.
  
#### 2. **Game Mechanics**
- The spaceship (player) must dodge falling obstacles. The spaceship can move left or right to avoid obstacles, and the AI controlling the spaceship evolves to improve over time.
- The AI learns by adjusting its neural network based on the score, collisions, and survival time.
  
#### 3. **Fitness Function**
- **Fitness Score**: The fitness score increases if a spaceship survives longer or avoids obstacles. It decreases when a spaceship collides with an obstacle.
  
#### 4. **High Score**
- The game keeps track of the highest score achieved in any session and saves it to a text file (`highscore.txt`), ensuring that the score persists across multiple game sessions.

### Installation and Setup

1. **Install Dependencies**  
   To run this game, you need Python 3.x installed along with the following libraries:
   - **Pygame**: For game rendering and input handling.
   - **NEAT-Python**: For evolving neural networks.

   You can install the required libraries using `pip`:
   ```bash
   pip install pygame neat-python
   ```

2. **Files**:
   - `Main.py`: Main game script that runs the game loop, initializes the game, and handles the neural network evolution using NEAT.
   - `config.txt`: Configuration file for NEAT settings. This defines parameters for evolving neural networks such as population size, mutation rates, etc.

3. **Running the Game**:
   Once the dependencies are installed and the files are set up, you can run the game using:
   ```bash
   python Main.py
   ```

### How the Game Works

#### 1. **Game Loop**:
- The main game loop continuously updates the game state, processes events (like player input), and renders the game objects (spaceships and obstacles).
  
#### 2. **NEAT AI**:
- Each spaceship is controlled by a neural network, and each neural network has inputs based on the position of the spaceship and the distance to nearby obstacles.
- The neural network outputs determine the movement of the spaceship (left or right). If a spaceship survives longer and avoids more obstacles, it gets a higher fitness score.
  
#### 3. **Obstacle Generation**:
- Obstacles are generated at regular intervals and move down the screen. The spaceship must avoid them by moving left or right.

#### 4. **Collision Detection**:
- A collision is detected when the spaceship overlaps with an obstacle. If a collision occurs, the spaceship is removed from the game and the fitness of the controlling neural network decreases.

#### 5. **High Score**:
- The highest score achieved across all game sessions is stored in `highscore.txt` for future reference.

#### 6. **NEAT Evolution**:
- The AI evolves over multiple generations. Each generation consists of multiple spaceships (each with its own neural network), and their neural networks evolve based on their performance. The best-performing networks are selected to reproduce and form the next generation.

### Game Flow:

1. **Start the Game**:
   When you run the game, the NEAT algorithm initializes a population of neural networks (spaceships). The game begins, and each spaceship is controlled by a neural network that takes inputs from the game environment.

2. **Neural Networks Control Spaceships**:
   - The neural networks take inputs such as the spaceship's position and the distance to obstacles.
   - Based on the inputs, the neural network outputs commands to move the spaceship left or right.

3. **Fitness Evaluation**:
   - The fitness of each spaceship is evaluated based on how long it survives and how many obstacles it avoids.
   - Spaceships that survive longer and avoid more obstacles are more likely to reproduce.

4. **Neural Network Evolution**:
   - After each generation, the top-performing neural networks are selected to reproduce and pass on their knowledge to the next generation. Over time, the AI improves as the neural networks become better at controlling the spaceship.

5. **Game Over**:
   - The game ends when all spaceships are eliminated (either by colliding with obstacles or being eliminated due to poor performance). The high score is updated and saved to `highscore.txt`.

### Key Functions:
1. **`main(genomes, config)`**:  
   - The core function where the game logic runs. It initializes the game environment, evolves the neural networks, and handles the game loop.

2. **`run(config)`**:  
   - This function runs the NEAT population and handles the evolutionary process of the neural networks.

3. **`collide(obj1, obj2)`**:  
   - This function checks for collisions between two game objects (spaceship and obstacle).

4. **`pause()`**:  
   - This function pauses the game when the player presses the escape key.

5. **`draw()`**:  
   - This function updates the game screen with the current positions of spaceships, obstacles, and score information.
