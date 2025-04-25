from PIL import Image, ImageDraw
import io
import base64

# Define colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLORS = [BLACK, WHITE, GRAY, GREEN, BLUE, RED]

# Dot grid settings
DOT_SIZE = 10
GRID_WIDTH = 3
GRID_HEIGHT = 3  # 3x3 grid, but we'll mimic 3x2 patterns
GRID_SPACING = 5  # Space between dots in a grid
CHAR_SPACING = 20  # Space between character grids
ROW_SPACING = 10  # Space between rows

# Define a 3x3 grid pattern for each letter (A-Z) and space
# Original patterns are 3x2 (6 dots); extend to 3x3 (9 dots) with None for unused positions
# Use uppercase keys to match the MESSAGE.upper() conversion
DOT_PATTERNS = {
    'T': [WHITE, GRAY, WHITE, None, BLACK, WHITE, BLACK, BLACK, None],
    'H': [WHITE, GRAY, WHITE, BLACK, BLACK, WHITE, BLACK, None, None],
    'I': [None, BLACK, None, WHITE, BLACK, None, WHITE, BLUE, WHITE],
    'S': [None, BLUE, None, WHITE, WHITE, WHITE, None, BLACK, BLACK],
    'M': [WHITE, WHITE, WHITE, BLACK, WHITE, BLACK, BLUE, WHITE, None],
    'E': [WHITE, GREEN, None, None, BLACK, None, WHITE, WHITE, WHITE],
    'W': [WHITE, WHITE, None, WHITE, BLACK, BLACK, WHITE, BLACK, None],
    'U': [BLACK, WHITE, WHITE, GREEN, WHITE, WHITE, WHITE, GRAY, WHITE],
    'O': [BLACK, BLACK, BLACK, None, WHITE, WHITE, None, GRAY, None],
    'C': [None, BLACK, None, GREEN, GRAY, None, BLACK, BLACK, BLACK],
    'F': [WHITE, WHITE, WHITE, WHITE, BLUE, BLACK, None, None, BLACK],
    'R': [WHITE, BLUE, WHITE, WHITE, WHITE, BLACK, BLACK, None, BLACK],
    'A': [WHITE, WHITE, None, None, GRAY, WHITE, None, WHITE, WHITE],
    'L': [WHITE, WHITE, WHITE, None, RED, WHITE, None, BLACK, BLACK],
    'P': [WHITE, WHITE, WHITE, BLACK, None, WHITE, BLACK, BLACK, BLACK],
    'B': [None, BLACK, None, BLACK, BLUE, BLACK, BLACK, WHITE, None],
    'N': [WHITE, GRAY, WHITE, BLACK, WHITE, None, None, BLACK, BLACK],
    # Add remaining letters (D, G, J, K, Q, V, X, Y, Z) and space to complete the dictionary
    'D': [GRAY, WHITE, BLACK, None, RED, BLACK, BLUE, None, None],
    'G': [GRAY, BLACK, WHITE, None, GREEN, RED, BLUE, None, None],
    'J': [BLACK, GRAY, WHITE, None, RED, BLUE, GREEN, None, None],
    'K': [WHITE, GRAY, BLACK, None, BLUE, RED, GREEN, None, None],
    'Q': [GRAY, WHITE, BLACK, None, GREEN, RED, BLUE, None, None],
    'V': [BLACK, GRAY, WHITE, None, BLUE, GREEN, RED, None, None],
    'X': [WHITE, BLACK, GRAY, None, RED, BLUE, GREEN, None, None],
    'Y': [GRAY, BLACK, WHITE, None, BLUE, RED, GREEN, None, None],
    'Z': [WHITE, GRAY, BLACK, None, RED, GREEN, BLUE, None, None],
    ' ': [None, None, None, None, None, None, None, None, None]
}

# Message to encrypt
MESSAGE = "this time we used dot codes for each alphabet character. a little harder perhaps. well done if you were able to solve it"

# Calculate image dimensions
chars_per_row = 8  # Match the image layout (8 chars per row)
num_chars = len(MESSAGE)
num_rows = (num_chars + chars_per_row - 1) // chars_per_row
grid_pixel_width = GRID_WIDTH * (DOT_SIZE + GRID_SPACING) - GRID_SPACING
grid_pixel_height = GRID_HEIGHT * (DOT_SIZE + GRID_SPACING) - GRID_SPACING
image_width = chars_per_row * (grid_pixel_width + CHAR_SPACING) - CHAR_SPACING
image_height = num_rows * (grid_pixel_height + ROW_SPACING) - ROW_SPACING

# Create a new image with a background color
image = Image.new("RGB", (image_width, image_height), color=(200, 200, 200))
draw = ImageDraw.Draw(image)

def draw_dot_grid(x, y, pattern):
    """Draw a 3x3 grid of colored dots at position (x, y), skipping None values."""
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = pattern[row * GRID_WIDTH + col]
            if color is None:
                continue  # Skip drawing if color is None (mimics unused dots)
            dot_x = x + col * (DOT_SIZE + GRID_SPACING)
            dot_y = y + row * (DOT_SIZE + GRID_SPACING)
            # Draw a circle (dot) at the calculated position
            draw.ellipse(
                [dot_x, dot_y, dot_x + DOT_SIZE, dot_y + DOT_SIZE],
                fill=color
            )

# Render the encrypted message as dot grids
for i, char in enumerate(MESSAGE.upper()):
    if char not in DOT_PATTERNS:
        continue  # Skip unsupported characters (e.g., punctuation)
    row = i // chars_per_row
    col = i % chars_per_row
    x = col * (grid_pixel_width + CHAR_SPACING)
    y = row * (grid_pixel_height + ROW_SPACING)
    draw_dot_grid(x, y, DOT_PATTERNS[char])

# Save the image to a file in the same folder as the script
image.save("encrypted_message.png")
print("Image saved as 'encrypted_message.png' in the current directory.")

