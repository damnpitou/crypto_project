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
    'T': [ (255,255,255), (128,128,128), (255,255,255),
           None,            (  0,  0,  0), (255,255,255),
           (  0,  0,  0), (  0,  0,  0), None ],
    'H': [ (255,255,255), (128,128,128), (255,255,255),
           (  0,  0,  0), (  0,  0,  0), (255,255,255),
           (  0,  0,  0), None,            None ],
    'I': [ None,            (  0,  0,  0), None,
           (255,255,255), (  0,  0,  0), None,
           (255,255,255), (  0,  0,255), (255,255,255) ],
    'S': [ None,            (  0,  0,255), None,
           (255,255,255), (255,255,255), (255,255,255),
           None,            (  0,  0,  0), (  0,  0,  0) ],
    'M': [ (255,255,255), (255,255,255), (255,255,255),
           (  0,  0,  0), (255,255,255), (  0,  0,  0),
           (  0,  0,255), (255,255,255), None ],
    'E': [ (255,255,255), (  0,255,  0), None,
           None,            (  0,  0,  0), None,
           (255,255,255), (255,255,255), (255,255,255) ],
    'W': [ (255,255,255), (255,255,255), None,
           (255,255,255), (  0,  0,  0), (  0,  0,  0),
           (255,255,255), (  0,  0,  0), None ],
    'U': [ (  0,  0,  0), (255,255,255), (255,255,255),
           (  0,255,  0), (255,255,255), (255,255,255),
           (255,255,255), (128,128,128), (255,255,255) ],
    'O': [ (  0,  0,  0), (  0,  0,  0), (  0,  0,  0),
           None,            (255,255,255), (255,255,255),
           None,            (128,128,128), None ],
    'C': [ None,            (  0,  0,  0), None,
           (  0,255,  0), (128,128,128), None,
           (  0,  0,  0), (  0,  0,  0), (  0,  0,  0) ],
    'F': [ (255,255,255), (255,255,255), (255,255,255),
           (255,255,255), (  0,  0,255), (  0,  0,  0),
           None,            None,            (  0,  0,  0) ],
    'R': [ (255,255,255), (  0,  0,255), (255,255,255),
           (255,255,255), (255,255,255), (  0,  0,  0),
           (  0,  0,  0), None,            (  0,  0,  0) ],
    'A': [ (255,255,255), (255,255,255), None,
           None,            (128,128,128), (255,255,255),
           None,            (255,255,255), (255,255,255) ],
    'L': [ (255,255,255), (255,255,255), (255,255,255),
           None,            (255,  0,  0), (255,255,255),
           None,            (  0,  0,  0), (  0,  0,  0) ],
    'P': [ (255,255,255), (255,255,255), (255,255,255),
           (  0,  0,  0), None,            (255,255,255),
           (  0,  0,  0), (  0,  0,  0), (  0,  0,  0) ],
    'B': [ None,            (  0,  0,  0), None,
           (  0,  0,  0), (  0,  0,255), (  0,  0,  0),
           (  0,  0,  0), (255,255,255), None ],
    'N': [ (255,255,255), (128,128,128), (255,255,255),
           (  0,  0,  0), (255,255,255), None,
           None,            (  0,  0,  0), (  0,  0,  0) ],
    'D': [ (128,128,128), (255,255,255), (  0,  0,  0),
           None,            (255,  0,  0), (  0,  0,  0),
           (  0,  0,255), None,            None ],
    'G': [ (128,128,128), (  0,  0,  0), (255,255,255),
           None,            (  0,255,  0), (255,  0,  0),
           (  0,  0,255), None,            None ],
    'J': [ (  0,  0,  0), (128,128,128), (255,255,255),
           None,            (255,  0,  0), (  0,  0,255),
           (  0,255,  0), None,            None ],
    'K': [ (255,255,255), (128,128,128), (  0,  0,  0),
           None,            (  0,  0,255), (255,  0,  0),
           (  0,255,  0), None,            None ],
    'Q': [ (128,128,128), (255,255,255), (  0,  0,  0),
           None,            (  0,255,  0), (255,  0,  0),
           (  0,  0,255), None,            None ],
    'V': [ (  0,  0,  0), (128,128,128), (255,255,255),
           None,            (  0,  0,255), (  0,255,  0),
           (255,  0,  0), None,            None ],
    'X': [ (255,255,255), (  0,  0,  0), (128,128,128),
           None,            (255,  0,  0), (  0,  0,255),
           (  0,255,  0), None,            None ],
    'Y': [ (128,128,128), (  0,  0,  0), (255,255,255),
           None,            (  0,  0,255), (255,  0,  0),
           (  0,255,  0), None,            None ],
    'Z': [ (255,255,255), (128,128,128), (  0,  0,  0),
           None,            (255,  0,  0), (  0,255,  0),
           (  0,  0,255), None,            None ],
    ' ': [ None ] * 9
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

