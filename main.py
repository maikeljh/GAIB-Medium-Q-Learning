# Michael Jonathan Halim 13521124
# Medium - Q-Learning

# Import libraries
import numpy as np
import tkinter as tk
import time
from PIL import Image, ImageTk

# Output Intro
print("Permainan Q-Learning")
print("By Michael Jonathan Halim | 13521124")

# Initialize board
board_length = 10
board = np.zeros(board_length)

# Initialize constants
learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.1
epochs = 5000

# Function to choose action
def choose_action(state):
    # Random choice if random number below exploration probability (Exploration)
    if np.random.uniform(0, 1) < exploration_prob:
        return np.random.choice([0, 1])
    else:
        # Choose best action on state
        return np.argmax(Q[state, :])

# Function to update Q Table
def update_Q(state, action, reward, next_state):
    Q[state, action] = Q[state, action] + learning_rate * (reward + discount_factor * np.max(Q[next_state, :]) - Q[state, action])

# Function to resize images to fit the rectangle size
def resize_image(image_path, width, height):
    # Open image
    image = Image.open(image_path)

    # Resize image
    resized_image = image.resize((width, height), Image.LANCZOS)

    # Create image tkinter element
    return ImageTk.PhotoImage(resized_image)

# Update the animate_path function to start from state 2
def animate_path():
    # Create root
    root = tk.Tk()
    root.title("Optimum Path")

    # Calculate the window position to center it on the screen
    window_width = board_length * 50
    window_height = 50
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create canvas
    canvas = tk.Canvas(root, width=board_length * 50, height=50)
    canvas.pack()

    # Load images
    hole_image = resize_image("./assets/hole.jpg", 50, 50)
    apple_image = resize_image("./assets/apple.jpg", 50, 50)
    player_image = resize_image("./assets/player.png", 50, 50)

    # Draw the game board
    def draw_game_board():
        for i in range(board_length):
            # Calculate coordinates for images and box numbers
            x0, y0 = i * 50, 0
            x1, y1 = x0 + 49, y0 + 50

            if i == 0:
                # Draw hole image at position 0
                canvas.create_image(x0 + 25, y0 + 25, image=hole_image)
            elif i == 9:
                # Draw apple image at position 9
                canvas.create_image(x0 + 25, y0 + 25, image=apple_image)
            else:
                # Draw box number
                color = "white"
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                canvas.create_text(x0 + 25, y0 + 25, text=str(i), font=("Helvetica", 12, "bold"))

    # Animate the player's movement
    def animate():
        # Draw game board
        draw_game_board()

        # Create player image
        player = canvas.create_image(75, 25, image=player_image)

        # Animation
        for i, state in enumerate(optimum_path):
            # Calculate coordinates
            x = int(state) * 50 + 25
            y = 25

            # Update player image position
            canvas.coords(player, x, y)
            canvas.update()

            # Animation delay
            time.sleep(0.5)

            # Show finish animation
            if i == len(optimum_path) - 1:
                canvas.create_rectangle(x - 25, y - 25, x + 25, y + 25, fill="green")
                canvas.update()
                time.sleep(1.0)

        # Exit the application after the animation ends
        root.after(1000, root.quit)

    # Animation
    animate()

# Function to play game
def play_game():
    # Initialize variables
    state = 2
    total_reward = 0

    # Loop play game while total reward doesn't meet condition
    while True:
        # Choose action
        action = choose_action(state)
        
        # Update next state
        if action == 0:
            next_state = state - 1
        else:
            next_state = state + 1

        # Check if next state out of range
        next_state = max(0, min(board_length - 1, next_state))

        # Initialize variable to check teleport
        teleport = False

        # Check if player gets apple or falls into hole
        if next_state == 0:
            reward = -100
            teleport = True
        elif next_state == 9:
            reward = 100
            teleport = True
        else:
            reward = -1

        # Update total reward
        total_reward += reward

        # Update Q Table
        update_Q(state, action, reward, next_state)

        # Update state
        state = next_state

        # Check if total reward meets condition or not
        if total_reward >= 500 or total_reward <= -200:
            break

        # Check if teleport
        if teleport:
            state = 3

    return total_reward

# Function to find optimum path
def find_optimum_path():
    # Initialize variables
    optimum_path = [2]
    state = 2
    total_reward = 0

    # Iterate Q Table until game finished
    while True:
        # Choose action
        action = np.argmax(Q[state, :])

        # Update next state
        if action == 0:
            next_state = state - 1
        else:
            next_state = state + 1

        # Check if next state out of range
        next_state = max(0, min(board_length - 1, next_state))

        # Initialize variable to check teleport
        teleport = False

        # Check if player gets apple or falls into hole
        if next_state == 0:
            reward = -100
            teleport = True
        elif next_state == 9:
            reward = 100
            teleport = True
        else:
            reward = -1

        # Update total reward
        total_reward += reward

        # Update state
        state = next_state
        optimum_path.append(state)

        # Check if total reward meets condition or not
        if total_reward >= 500 or total_reward <= -200:
            break

        # Check if teleport
        if teleport:
            state = 3
            optimum_path.append(state)
    
    return optimum_path

# Initialize Q Table
Q = np.zeros((board_length, 2))

# Output Learning Result
print()
print("Hasil pembelajaran:")

# Iterate learning process
for epoch in range(epochs):
    # Play game
    total_reward = play_game()

    # Output current total reward
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}, Total Reward: {total_reward}")

# Output Q Table
print("\nTabel Q akhir:")
print(Q)

# Find optimum path
optimum_path = find_optimum_path()

# Animate the path using Tkinter
animate_path()