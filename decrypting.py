# decrypt_dot_grid.py
from PIL import Image
import os

# ── Settings (must match your encryption script) ──────────────────────────────
DOT_SIZE     = 10
GRID_WIDTH   = 3
GRID_HEIGHT  = 3
GRID_SPACING = 5
CHAR_SPACING = 20
ROW_SPACING  = 10

# Background color used when creating the image
BG_COLOR = (200, 200, 200)

# Define the same patterns you used for encryption
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

# Build reverse lookup: pattern‐tuple → character
PATTERN_TO_CHAR = { tuple(v): k for k, v in DOT_PATTERNS.items() }


def extract_dot_grid(img, x, y):
    """
    Sample the center of each DOT_SIZE×DOT_SIZE cell.
    If it equals BG_COLOR, treat it as None; otherwise record the RGB tuple.
    """
    pat = []
    for ry in range(GRID_HEIGHT):
        for rx in range(GRID_WIDTH):
            dot_x = x + rx * (DOT_SIZE + GRID_SPACING)
            dot_y = y + ry * (DOT_SIZE + GRID_SPACING)
            cx = dot_x + DOT_SIZE // 2
            cy = dot_y + DOT_SIZE // 2
            pixel = img.getpixel((cx, cy))
            if pixel == BG_COLOR:
                pat.append(None)
            else:
                pat.append(pixel)
    return tuple(pat)


def decrypt_image(path="encrypted_message.png"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    img = Image.open(path).convert("RGB")
    W, H = img.size

    grid_w = GRID_WIDTH  * (DOT_SIZE + GRID_SPACING) - GRID_SPACING
    grid_h = GRID_HEIGHT * (DOT_SIZE + GRID_SPACING) - GRID_SPACING

    # how many chars fit per row/column
    cols = (W + CHAR_SPACING) // (grid_w + CHAR_SPACING)
    rows = (H + ROW_SPACING) // (grid_h + ROW_SPACING)

    result = []
    for ry in range(rows):
        for cx in range(cols):
            x = cx * (grid_w + CHAR_SPACING)
            y = ry * (grid_h + ROW_SPACING)
            if x + grid_w > W or y + grid_h > H:
                continue
            pat = extract_dot_grid(img, x, y)
            result.append(PATTERN_TO_CHAR.get(pat, '?'))

    # join and lowercase
    return "".join(result).lower()


if __name__ == "__main__":
    try:
        message = decrypt_image("encrypted_message.png")
        print("Decrypted Message:\n", message)
    except FileNotFoundError as e:
        print(e)

