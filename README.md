# AI Solution in Python for Solving the 2048 Game

**A Python script that creates and plays the classic "2048" game itself for maximum high scores during 20 rounds (max 1000 moves each).**

**Author:** Aleksi Bovellan

**Technologies:** Python 3, Numpy, Math

**Algorithms:** Expectimax Algorithm with Heuristics

**Python Extensions:** None (uses standard libraries)

---

![screenshot](https://github.com/user-attachments/assets/9e0fbc98-8f6a-4f50-ae69-b9b5fc576897)

---

## Main Usage

To run the AI-powered 2048 game simulation, simply execute the main script:

python3 2048_ai.py

The script will automatically start simulating the game using the AI. It will display the game board after each move and provide a summary of the results at the end.

---

## Included Files

- `2048_ai.py` - The main game script with AI implementation
- `README.md` - This file containing instructions and project details

---

## Special Attention for Apple Mac Computers

For an optimal experience, Mac users can utilize the Terminal application instead of code editors. Follow these steps to create a virtual environment:

python3 -m venv myenv

source myenv/bin/activate

Since the script only uses standard Python libraries, no additional installations are required. When you're done experimenting, exit the virtual environment by typing `deactivate`. To reactivate it later, use `source myenv/bin/activate`.

---

## Pre-installation Requirements for All Users

No external packages are required. Ensure you have **Python 3** installed on your system.

Optional: if you want to use 'numba' for GPU performance benefits on CUDA, type: pip install numba

---

## How It Works

The AI utilizes several heuristics and the Expectimax algorithm to make decisions during the game.

### Heuristics Used in Decision-Making

- **Empty Tile Heuristic:** Aims to maximize the number of empty tiles, providing more opportunities for tile merging.
- **Smoothness Heuristic:** Encourages the arrangement of tiles so that adjacent tiles have similar values, facilitating future merges.
- **Monotonicity Heuristic:** Promotes keeping the tiles in a specific order (either increasing or decreasing), which helps in creating higher-value tiles.
- **Max Tile Heuristic:** Favors moves that keep the highest-value tile on the board, pushing towards achieving larger tiles like 2048 or higher.

### Expectimax Algorithm

- **Player and Chance Nodes:** The algorithm considers both the player's moves and the randomness of new tiles (2 or 4) appearing on the board.
- **Search Depth:** The depth of the search tree is adjustable (default is 3), providing a balance between foresight and computational efficiency.
- **Decision Making:** At each move, the AI evaluates possible moves using the heuristics and chooses the one with the highest expected score.

### Game Simulation

- The game is simulated multiple times (default is 20 runs).
- After each run, the script reports the highest tile achieved.
- At the end, it summarizes the results and highlights the highest tile reached across all simulations.

---

## Code Logic and Structure

### `__main__`

- **Purpose:** Entry point of the program.
- **Functionality:** Initiates the game simulation loop for the specified number of runs.
- **Outcome:** After each game, displays the maximum tile reached and, at the end, reports the highest tile achieved across all games.

### `play_game` Function

- **Manages Game Flow:**
  - Initializes a blank 4x4 grid.
  - Adds random tiles (2 or 4) to start the game.
- **AI Decision Making:**
  - Uses the Expectimax algorithm to select the best move.
  - Continues the game until no more moves are possible.
- **Result:**
  - Returns the highest tile achieved in that game.

### `expectimax` Function

- **Purpose:** Core of the AI decision-making process.
- **Mechanism:**
  - Explores possible future moves up to a certain depth.
  - Evaluates board states using the combined heuristics.
  - Determines the move with the maximum expected utility.

### Heuristic Functions

- **`empty_tile_heuristic`:** Encourages maintaining empty spaces on the board.
- **`smoothness_heuristic`:** Rewards arrangements where adjacent tiles have similar values.
- **`monotonicity_heuristic`:** Favors keeping the tile values in order, either increasing or decreasing.
- **`max_tile_heuristic`:** Focuses on achieving and maintaining high-value tiles.

These heuristics guide the AI to make strategic decisions that increase the likelihood of achieving higher tiles during the game.

---

## CPU/GPU Compatibility

The script is designed to run efficiently on both Macs and PCs without requiring GPU support. It relies solely on standard Python libraries and does not need any specialized hardware. However, if you're using a MacBook (such as an M1 Air), the system may automatically utilize its GPU to enhance performance.

---

## Customization

- **Adjusting Simulation Runs:**
  - You can change the number of game simulations by modifying the `num_runs` variable in the script.
- **Changing Search Depth:**
  - The AI's lookahead depth can be adjusted by changing the `max_depth` parameter in the `play_game` function. Be aware that increasing the depth may impact runtime performance.
- **Tweaking Heuristic Weights:**
  - The weights of the heuristics in the `combined_heuristic` function can be modified to experiment with different AI behaviors.

---

## Conclusion

This project demonstrates an AI approach to solving the 2048 game using Python. By combining several heuristics with the Expectimax algorithm, the AI makes strategic decisions to maximize the tile values on the board. The script is user-friendly and requires minimal setup, making it accessible for experimentation and further development.

---
