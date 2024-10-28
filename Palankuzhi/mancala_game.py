import pygame
import sys
import math
from palankuzhi import Palankuzhi  # Assuming your class is in palankuzhi_module.py
from alphabeta import ai_move_AlphaBeta
from minimax import ai_move_minimax
from heuristic import ai_move_heuristic

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 700  # 7 columns * 100 px each
SCREEN_HEIGHT = 300  # Increased height to give space for coin count

CIRCLE_RADIUS = 40

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("7x2 Palankuzhi Board with Circles")

# Font for rendering the number of coins and player counts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 25)

# Initialize Palankuzhi game
palankuzhi_game = Palankuzhi()

# Store circle positions
circles = []

# Game mode variables
game_mode = None  # 'multiplayer' or 'ai'
ai_difficulty = None  # 'minimax', 'alphabeta', 'heuristic'
game_over = False
winner = None  # Track the winner

# Function to draw the grid with circles and current board numbers
def draw_board():
    screen.fill(WHITE)
    global circles
    circles = []  # Clear circle positions before drawing

    # Loop through rows and columns
    for row in range(2):
        for col in range(7):
            # Calculate the position of each circle (centered in each grid cell)
            x = col * 100 + 50  # Horizontal position
            y = row * 100 + 100  # Vertical position, moved down by 100 pixels
            
            # Draw the circle
            pygame.draw.circle(screen, RED, (x, y), CIRCLE_RADIUS, 5)
            
            # Render the number of coins in each hole and place it inside the circle
            number_text = font.render(str(palankuzhi_game.board[row][col]), True, BLACK)
            text_rect = number_text.get_rect(center=(x, y))  # Center the number in the circle
            screen.blit(number_text, text_rect)

            # Store the circle's position and row/col info for click detection
            circles.append((x, y, row, col))

# Function to display the coin count of both players
def display_coin_count():
    # Render text for Player 1 and Player 2
    player1_text = small_font.render(f'Player 1 Coins: {palankuzhi_game.player_coins[0]}', True, BLACK)
    player2_text = small_font.render(f'Player 2 Coins: {palankuzhi_game.player_coins[1]}', True, BLACK)

    # Blit (draw) the text on the screen, aligned to the top-right corner
    screen.blit(player1_text, (SCREEN_WIDTH - player1_text.get_width() - 20, 10))  # Higher up
    screen.blit(player2_text, (SCREEN_WIDTH - player2_text.get_width() - 20, 30))  # Slightly below Player 1

# Function to detect if a circle is clicked and perform game logic
def check_circle_click(mouse_pos, current_player):
    mouse_x, mouse_y = mouse_pos

    for circle in circles:
        x, y, row, col = circle
        distance = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)  # Calculate distance from mouse to circle center

        # Check if the mouse click is inside the circle
        if distance <= CIRCLE_RADIUS:
            # Restrict Player 1 to row 0 and Player 2 to row 1
            if (current_player == 0 and row == 0) or (current_player == 1 and row == 1):
                if palankuzhi_game.valid_move(row, col):
                    # Perform move for the current player
                    palankuzhi_game.move_coins(current_player, row, col)

                    # Check for win condition
                    has_won, win_player = palankuzhi_game.check_for_win()
                    if has_won:
                        global game_over, winner
                        game_over = True
                        winner = win_player
                        return True

                    return True
    return False

# Function to display the home menu
def display_home_menu():
    screen.fill(WHITE)
    title_text = font.render("Palankuzhi Game", True, BLACK)
    multiplayer_text = small_font.render("1. Multiplayer", True, BLACK)
    ai_text = small_font.render("2. Play against AI", True, BLACK)
    
    # Draw texts
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(multiplayer_text, (SCREEN_WIDTH // 2 - multiplayer_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(ai_text, (SCREEN_WIDTH // 2 - ai_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    pygame.display.flip()

# Function to display AI difficulty options
def display_ai_menu():
    screen.fill(WHITE)
    title_text = small_font.render("Choose AI Difficulty", True, BLACK)
    minimax_text = small_font.render("1. Minimax", True, BLACK)
    alphabeta_text = small_font.render("2. Alpha-Beta Pruning", True, BLACK)
    heuristic_text = small_font.render("3. Heuristic", True, BLACK)

    # Draw texts
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(minimax_text, (SCREEN_WIDTH // 2 - minimax_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(alphabeta_text, (SCREEN_WIDTH // 2 - alphabeta_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(heuristic_text, (SCREEN_WIDTH // 2 - heuristic_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    pygame.display.flip()

# Function to display the game over screen
def display_game_over():
    screen.fill(WHITE)
    game_over_text = font.render(f"Player {winner + 1} Wins!", True, BLACK)
    p1_coins = small_font.render(f"Player 1 Coins : {palankuzhi_game.player_coins[0]}", True, BLACK)
    p2_coins = small_font.render(f"Player 2 Coins : {palankuzhi_game.player_coins[1]}", True, BLACK)
    home_text = small_font.render("Click to return to home", True, BLACK)

    # Draw texts
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(p1_coins, (SCREEN_WIDTH // 2 - p1_coins.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(p2_coins, (SCREEN_WIDTH // 2 - p2_coins.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(home_text, (SCREEN_WIDTH // 2 - home_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

# Function to trigger AI move based on the selected difficulty
def perform_ai_move(ai_player):
    #global palankuzhi_game
    if ai_difficulty == 'minimax':
        #palankuzhi_game = minimax.Palankuzhi()
        move = ai_move_minimax(palankuzhi_game, ai_player)
    elif ai_difficulty == 'alphabeta':
        #palankuzhi_game = alphabera.Palankuzhi()
        move = ai_move_AlphaBeta(palankuzhi_game, ai_player)
    elif ai_difficulty == 'heuristic':
        #palankuzhi_game = heuristic.Palankuzhi()
        move = ai_move_heuristic(palankuzhi_game, ai_player)

    if move is not None:
        palankuzhi_game.move_coins(ai_player, ai_player, move)
        return True
    return False

# Main loop
running = True
current_player = 0  # Track current player (0 for Player 1, 1 for Player 2)
menu_active = True  # Home menu is initially active
ai_menu_active = False  # AI difficulty menu inactive initially
game_over = False  # Track game over state
ai_player = None  # Track the AI player

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active:
                # Check for menu option selection
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if multiplayer option is clicked
                if SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100:
                    if SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2:
                        game_mode = 'multiplayer'
                        menu_active = False  # Exit home menu to start the game
                    elif SCREEN_HEIGHT // 2 + 20 < mouse_y < SCREEN_HEIGHT // 2 + 40:
                        game_mode = 'ai'
                        menu_active = False  # Exit home menu to AI difficulty menu
                        ai_menu_active = True  # Activate AI difficulty menu

            elif ai_menu_active:
                # Handle AI difficulty selection
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if minimax, alpha-beta, or heuristic option is clicked
                if SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100:
                    if SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2:
                        ai_difficulty = 'minimax'
                    elif SCREEN_HEIGHT // 2 + 20 < mouse_y < SCREEN_HEIGHT // 2 + 40:
                        ai_difficulty = 'alphabeta'
                    elif SCREEN_HEIGHT // 2 + 60 < mouse_y < SCREEN_HEIGHT // 2 + 80:
                        ai_difficulty = 'heuristic'

                    # Start the game with AI
                    ai_menu_active = False  # Exit AI menu to start the game
                    ai_player = 1  # Assign AI as Player 2
                    current_player = 0  # Start with Player 1's turn

            elif game_over:
                # Restart game from home menu if clicked after game over
                game_over = False
                menu_active = True
                palankuzhi_game = Palankuzhi()

            else:
                # Only handle click if it's a human's turn
                if (game_mode == 'multiplayer') or (game_mode == 'ai' and current_player == 0):
                    if check_circle_click(pygame.mouse.get_pos(), current_player):
                        current_player = (current_player + 1) % 2  # Switch turns

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if menu_active:
        display_home_menu()

    elif ai_menu_active:
        display_ai_menu()

    elif game_over:
        display_game_over()

    else:
        draw_board()
        display_coin_count()

        # Handle AI turn if it's AI's turn in the AI mode
        if game_mode == 'ai' and current_player == 1:
            if perform_ai_move(ai_player):
                current_player = 0  # After AI's move, switch to player

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
