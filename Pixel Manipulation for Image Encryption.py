from PIL import Image
import os

def swap_channels(pixel):
    """Swap red and blue channels in an RGB pixel."""
    r, g, b = pixel
    return (b, g, r)

def apply_xor(pixel, key):
    """Apply XOR operation to each channel of an RGB pixel with a key."""
    r, g, b = pixel
    return (r ^ key, g ^ key, b ^ key)

def process_image(image_path, mode, operation, key=None):
    """
    Process an image for encryption/decryption.
    
    Args:
        image_path: Path to input image
        mode: 'encrypt' or 'decrypt'
        operation: 'swap', 'xor', or 'both'
        key: Integer (0-255) for XOR operations
    """
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = img.load()
        width, height = img.size

        for y in range(height):
            for x in range(width):
                current = pixels[x, y]
                
                if operation in ['swap', 'both']:
                    current = swap_channels(current)
                    
                if operation in ['xor', 'both'] and key is not None:
                    current = apply_xor(current, key)
                
                pixels[x, y] = current

        # Save processed image
        base, ext = os.path.splitext(image_path)
        suffix = "_encrypted" if mode == 'encrypt' else "_decrypted"
        output_path = f"{base}{suffix}{ext}"
        img.save(output_path)
        print(f"Success! Image saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    print("Image Encryption Tool")
    print("Operations available:")
    print("1. Swap (Red/Blue channels)")
    print("2. XOR (Pixel manipulation with key)")
    print("3. Both operations")
    
    image_path = input("\nEnter image path: ").strip()
    mode = input("Choose mode (encrypt/decrypt): ").lower().strip()
    op_choice = input("Choose operation (1/2/3): ").strip()
    
    operations = {
        '1': 'swap',
        '2': 'xor',
        '3': 'both'
    }
    
    operation = operations.get(op_choice)
    if not operation:
        print("Invalid operation choice")
        return
        
    key = None
    if operation in ['xor', 'both']:
        try:
            key = int(input("Enter encryption key (0-255): "))
            if not 0 <= key <= 255:
                raise ValueError
        except ValueError:
            print("Invalid key! Must be integer between 0-255")
            return

    process_image(image_path, mode, operation, key)

if __name__ == "__main__":
    main()