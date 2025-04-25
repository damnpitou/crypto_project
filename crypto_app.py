import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
import os
import io
import base64
import math

# ---- Constants ----
# Colors (RGB)
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
GRID_HEIGHT = 3
GRID_SPACING = 5
CHAR_SPACING = 20
ROW_SPACING = 10

# Background color
BG_COLOR = (200, 200, 200)

# Define patterns for letters
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

# Build reverse lookup: pattern-tuple → character
PATTERN_TO_CHAR = {tuple(v): k for k, v in DOT_PATTERNS.items()}

# ---- Helper Functions ----
def color_distance(color1, color2):
    """Calculate Euclidean distance between two RGB colors"""
    if color1 is None or color2 is None:
        return 0 if color1 == color2 else 999
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def find_closest_color(pixel, bg_color):
    """Find the closest matching color from the predefined colors or None for bg"""
    if pixel is None:
        return None
        
    # If it's close to the background color, consider it None
    if color_distance(pixel, bg_color) < 30:  # Threshold for background
        return None
        
    # Find the closest color from our defined palette
    closest = None
    min_dist = float('inf')
    for color in COLORS:
        dist = color_distance(pixel, color)
        if dist < min_dist:
            min_dist = dist
            closest = color
    return closest

def match_pattern(extracted_pattern, patterns_dict):
    """Find the best match for an extracted pattern from the patterns dictionary"""
    best_match = None
    best_score = float('inf')
    
    for pattern, char in patterns_dict.items():
        score = 0
        for i, (p1, p2) in enumerate(zip(extracted_pattern, pattern)):
            score += color_distance(p1, p2)
        
        if score < best_score:
            best_score = score
            best_match = char
            
    return best_match

# ---- Functions ----
def draw_dot_grid(draw, x, y, pattern):
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
            
            # Ensure coordinates are within image bounds
            if cx >= img.width or cy >= img.height:
                pat.append(None)
                continue
                
            pixel = img.getpixel((cx, cy))
            closest_color = find_closest_color(pixel, BG_COLOR)
            pat.append(closest_color)
    return tuple(pat)

def decrypt_image(path="encrypted_message.png"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    img = Image.open(path).convert("RGB")
    W, H = img.size

    grid_w = GRID_WIDTH * (DOT_SIZE + GRID_SPACING) - GRID_SPACING
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
                
            extracted_pattern = extract_dot_grid(img, x, y)
            
            # First try direct match (for speed)
            char = PATTERN_TO_CHAR.get(extracted_pattern)
            
            # If no direct match, use pattern matching
            if char is None:
                # Create dictionary of all patterns with characters as values
                pattern_dict = {pattern: char for char, pattern in DOT_PATTERNS.items()}
                char = match_pattern(extracted_pattern, pattern_dict)
            
            result.append(char if char is not None else '?')

    # join and lowercase
    return "".join(result).lower()

class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Dot Cryptography")
        self.geometry("1100x800")
        
        # Set appearance mode and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(2, weight=0)  # Footer
        
        # Create header
        self.create_header()
        
        # Create content
        self.create_content()
        
        # Create footer
        self.create_footer()
        
        # Initialize variables
        self.current_image = None
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame, 
            text="Dot Cryptography", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)
        
    def create_content(self):
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=0)  # Input panel
        content_frame.grid_columnconfigure(1, weight=1)  # Display panel
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Create input panel
        self.create_input_panel(content_frame)
        
        # Create display panel
        self.create_display_panel(content_frame)
        
    def create_input_panel(self, parent):
        input_panel = ctk.CTkFrame(parent)
        input_panel.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="ns")
        
        # Message input
        input_label = ctk.CTkLabel(
            input_panel, 
            text="Enter Message:", 
            font=ctk.CTkFont(size=16)
        )
        input_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.message_entry = ctk.CTkTextbox(
            input_panel, 
            width=300, 
            height=150,
            font=ctk.CTkFont(size=14)
        )
        self.message_entry.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Action buttons
        encrypt_button = ctk.CTkButton(
            input_panel, 
            text="Encrypt Message", 
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.encrypt_message
        )
        encrypt_button.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        decrypt_button = ctk.CTkButton(
            input_panel, 
            text="Decrypt Image", 
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.decrypt_current_image
        )
        decrypt_button.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        load_button = ctk.CTkButton(
            input_panel, 
            text="Load Image", 
            font=ctk.CTkFont(size=14),
            command=self.load_image
        )
        load_button.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        save_button = ctk.CTkButton(
            input_panel, 
            text="Save Image", 
            font=ctk.CTkFont(size=14),
            command=self.save_image
        )
        save_button.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        
    def create_display_panel(self, parent):
        display_panel = ctk.CTkFrame(parent)
        display_panel.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        display_panel.grid_columnconfigure(0, weight=1)
        display_panel.grid_rowconfigure(0, weight=1)  # Image
        display_panel.grid_rowconfigure(1, weight=0)  # Decrypted text
        
        # Image display
        self.image_frame = ctk.CTkFrame(display_panel)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="No image generated yet")
        self.image_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        # Decrypted text display
        decrypted_frame = ctk.CTkFrame(display_panel)
        decrypted_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        decrypted_frame.grid_columnconfigure(0, weight=1)
        
        decrypted_label = ctk.CTkLabel(
            decrypted_frame, 
            text="Decrypted Message:", 
            font=ctk.CTkFont(size=16)
        )
        decrypted_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.decrypted_text = ctk.CTkTextbox(
            decrypted_frame, 
            height=100, 
            font=ctk.CTkFont(size=14)
        )
        self.decrypted_text.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="ew")
        
    def create_footer(self):
        footer_frame = ctk.CTkFrame(self)
        footer_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        status_label = ctk.CTkLabel(
            footer_frame, 
            text="Ready", 
            font=ctk.CTkFont(size=12)
        )
        status_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.status_label = status_label
        
    def encrypt_message(self):
        message = self.message_entry.get("1.0", "end-1c")
        if not message:
            self.update_status("Please enter a message to encrypt")
            return
            
        # Calculate image dimensions
        chars_per_row = 8
        num_chars = len(message)
        num_rows = (num_chars + chars_per_row - 1) // chars_per_row
        grid_pixel_width = GRID_WIDTH * (DOT_SIZE + GRID_SPACING) - GRID_SPACING
        grid_pixel_height = GRID_HEIGHT * (DOT_SIZE + GRID_SPACING) - GRID_SPACING
        image_width = chars_per_row * (grid_pixel_width + CHAR_SPACING) - CHAR_SPACING
        image_height = num_rows * (grid_pixel_height + ROW_SPACING) - ROW_SPACING

        # Create image
        image = Image.new("RGB", (image_width, image_height), color=BG_COLOR)
        draw = ImageDraw.Draw(image)

        # Draw message
        for i, char in enumerate(message.upper()):
            if char not in DOT_PATTERNS:
                continue
            row = i // chars_per_row
            col = i % chars_per_row
            x = col * (grid_pixel_width + CHAR_SPACING)
            y = row * (grid_pixel_height + ROW_SPACING)
            draw_dot_grid(draw, x, y, DOT_PATTERNS[char])

        # Save temporary and display
        image.save("encrypted_message.png")
        self.current_image = image
        self.display_image(image)
        self.update_status(f"Message encrypted: {num_chars} characters")
        
        # Clear decrypted text
        self.decrypted_text.delete("1.0", "end")
    
    def decrypt_current_image(self):
        if self.current_image is None:
            self.update_status("No image to decrypt. Please encrypt a message or load an image first.")
            return
        
        try:
            # Save the current image if it's not already saved
            if not os.path.exists("encrypted_message.png"):
                self.current_image.save("encrypted_message.png")
                
            # Decrypt the image
            decrypted_text = decrypt_image("encrypted_message.png")
            
            # Display the decrypted text
            self.decrypted_text.delete("1.0", "end")
            self.decrypted_text.insert("1.0", decrypted_text)
            self.update_status("Image decrypted successfully")
        except Exception as e:
            self.update_status(f"Error decrypting image: {str(e)}")
    
    def load_image(self):
        try:
            import tkinter.filedialog as filedialog
            file_path = filedialog.askopenfilename(
                title="Select Encrypted Image",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            image = Image.open(file_path).convert("RGB")
            self.current_image = image
            self.display_image(image)
            self.update_status(f"Image loaded from {file_path}")
            
            # Clear decrypted text
            self.decrypted_text.delete("1.0", "end")
        except Exception as e:
            self.update_status(f"Error loading image: {str(e)}")
    
    def save_image(self):
        if self.current_image is None:
            self.update_status("No image to save. Please encrypt a message first.")
            return
            
        try:
            import tkinter.filedialog as filedialog
            file_path = filedialog.asksaveasfilename(
                title="Save Encrypted Image",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            self.current_image.save(file_path)
            self.update_status(f"Image saved to {file_path}")
        except Exception as e:
            self.update_status(f"Error saving image: {str(e)}")
    
    def display_image(self, image):
        # Calculate the available space in the image frame
        self.image_frame.update()
        max_width = self.image_frame.winfo_width() - 40
        max_height = self.image_frame.winfo_height() - 40
        
        if max_width <= 0 or max_height <= 0:
            # Widget not fully initialized yet, use default values
            max_width = 700
            max_height = 500
        
        # Resize the image to fit the available space while preserving aspect ratio
        width, height = image.size
        ratio = min(max_width/width, max_height/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # Resize and convert to CTkImage
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        ctk_image = ctk.CTkImage(
            light_image=resized_image,
            dark_image=resized_image,
            size=(new_width, new_height)
        )
        
        # Update the image label
        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image  # Keep a reference
    
    def update_status(self, message):
        self.status_label.configure(text=message)
        print(message)

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()
