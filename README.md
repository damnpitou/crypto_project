# Dot Cryptography App

A modern GUI application for encoding and decoding messages using colored dot patterns. This application allows you to encrypt text messages into a visual representation where each character is represented by a unique pattern of colored dots.

![Dot Cryptography App](https://github.com/username/dot-cryptography/assets/screenshot.png) *(Add your own screenshot here)*

## Features

- **Message Encryption**: Convert text into colored dot patterns
- **Message Decryption**: Convert dot patterns back to readable text
- **Modern UI**: Clean, dark-themed interface using customtkinter
- **File Operations**: Load and save encrypted images
- **Real-time Status Updates**: View operation status in the footer bar

## Installation

### Prerequisites

- Python 3.8 or higher
- PIL (Pillow)
- customtkinter

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/username/dot-cryptography.git
   cd dot-cryptography
   ```

2. Install required packages:
   ```bash
   pip install pillow customtkinter
   ```

3. Run the application:
   ```bash
   python crypto_app.py
   ```

## Usage

### Encrypting a Message

1. Enter your message in the text box on the left panel
2. Click "Encrypt Message"
3. The encrypted image will appear in the main panel
4. Use "Save Image" to save the encrypted image to a file

### Decrypting a Message

1. Load an encrypted image using "Load Image" or encrypt a message first
2. Click "Decrypt Image"
3. The decrypted message will appear in the text box at the bottom

## How It Works

The encryption system uses a grid of colored dots to represent each character:

- Each character is encoded as a 3×3 grid of colored dots
- The application uses 6 colors: Black, White, Gray, Green, Blue, and Red
- Some positions in the grid may be empty (using the background color)
- Each character has a unique pattern, making the code decipherable

The algorithm converts each character to its corresponding dot pattern and arranges these patterns in rows to form the complete encrypted message.

## File Structure

- `crypto_app.py` - Main application with GUI
- `crypting.py` - Core encryption functionality
- `decrypting.py` - Core decryption functionality
- `README.md` - Project documentation

## Technical Details

### Color Palette

- **BLACK**: (0, 0, 0)
- **WHITE**: (255, 255, 255)
- **GRAY**: (128, 128, 128)
- **GREEN**: (0, 255, 0)
- **BLUE**: (0, 0, 255)
- **RED**: (255, 0, 0)
- **Background**: (200, 200, 200)

### Grid Specifications

- **DOT_SIZE**: 10 pixels
- **GRID_WIDTH**: 3 dots
- **GRID_HEIGHT**: 3 dots
- **GRID_SPACING**: 5 pixels between dots
- **CHAR_SPACING**: 20 pixels between character grids
- **ROW_SPACING**: 10 pixels between rows

## Advanced Features

- **Fuzzy Color Matching**: The decryption algorithm can handle slight color variations due to image compression or editing
- **Pattern Recognition**: Uses pattern matching to identify characters even when exact matches aren't found
- **Error Handling**: Gracefully handles invalid characters and file operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components

---

*Note: This README template can be customized with your own information and screenshots.*
