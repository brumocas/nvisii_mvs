import os
from PIL import Image

def add_background_to_images(background_path, input_dir, output_dir, position=(0, 0)):
    # Load the background image
    background = Image.open(background_path)

    # Walk through the input directory and subdirectories
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Construct the full file path for each image
            file_path = os.path.join(root, file)

            # Check if the file is an image (add more formats if needed)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                print(f"Processing: {file_path}")
                
                # Load the foreground image
                foreground = Image.open(file_path)

                # Resize foreground to 200x200 pixels (adjust as needed)
                foreground = foreground.resize((200, 200), Image.ANTIALIAS)

                # Create a copy of the background image
                background_copy = background.copy()

                # Paste the foreground onto the background at the specified position
                background_copy.paste(foreground, position, foreground.convert("RGBA"))  # Use RGBA for transparency
                
                # Get the relative path from input_dir to maintain subfolder structure
                relative_path = os.path.relpath(root, input_dir)
                output_subfolder = os.path.join(output_dir, relative_path)

                # Create the output subfolder if it doesn't exist
                os.makedirs(output_subfolder, exist_ok=True)

                # Construct output file path and save the image
                output_file_path = os.path.join(output_subfolder, f"bg_{file}")
                background_copy.save(output_file_path)
                print(f"Saved: {output_file_path}")

if __name__ == "__main__":
    # Path to the background image
    background_image_path = "background.jpg"  # Change to your background image path

    # Input directory containing images (and subdirectories)
    input_directory = "input_images"  # Change to your input directory

    # Output directory to save processed images
    output_directory = "output_images"  # Change to your output directory

    # Position to paste the foreground image on the background
    position = (50, 50)  # Adjust as necessary

    # Call the function to process images
    add_background_to_images(background_image_path, input_directory, output_directory, position)
