import os
import cv2
import numpy as np

def add_background_to_images(background_path, input_dir, output_dir, position=(0, 0)):
    # Load the background image using OpenCV
    background = cv2.imread(background_path)

    # Walk through the input directory and subdirectories
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Construct the full file path for each image
            file_path = os.path.join(root, file)

            # Check if the file is an image (add more formats if needed)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                print(f"Processing: {file_path}")
                
                # Load the foreground image
                foreground = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel if available
                
                # Resize the foreground image to 200x200 pixels
                foreground_resized = cv2.resize(foreground, (400, 400), interpolation=cv2.INTER_LANCZOS4)

                # Get the dimensions of the foreground image
                fg_height, fg_width = foreground_resized.shape[:2]

                # Crop the background image to the size of the foreground image
                background_cropped = background[:fg_height, :fg_width]

                # Create a copy of the cropped background image
                background_copy = background_cropped.copy()

                # Extract alpha channel from the foreground if it exists
                if foreground_resized.shape[2] == 4:  # Check if there is an alpha channel
                    alpha_channel = foreground_resized[:, :, 3]  # Extract alpha
                    alpha_mask = alpha_channel / 255.0  # Normalize alpha mask
                    alpha_inv = 1.0 - alpha_mask  # Inverse alpha mask

                    # Place the foreground on the cropped background
                    for c in range(0, 3):
                        background_copy[position[1]:position[1]+fg_height, position[0]:position[0]+fg_width, c] = (
                            alpha_mask * foreground_resized[:, :, c] + 
                            alpha_inv * background_copy[position[1]:position[1]+fg_height, position[0]:position[0]+fg_width, c]
                        )
                else:
                    # If no alpha channel, just overlay the image at the specified position
                    background_copy[position[1]:position[1]+fg_height, position[0]:position[0]+fg_width] = foreground_resized

                # Get the relative path from input_dir to maintain subfolder structure
                relative_path = os.path.relpath(root, input_dir)
                output_subfolder = os.path.join(output_dir, relative_path)

                # Create the output subfolder if it doesn't exist
                os.makedirs(output_subfolder, exist_ok=True)

                # Construct output file path and save the image
                output_file_path = os.path.join(output_subfolder, f"bg_{file}")
                cv2.imwrite(output_file_path, background_copy)
                print(f"Saved: {output_file_path}")

if __name__ == "__main__":
    # Path to the background image
    background_image_path = "back1.jpg"  # Change to your background image path

    # Input directory containing images (and subdirectories)
    input_directory = "images_5"  # Change to your input directory

    # Output directory to save processed images
    output_directory = "images_5_computed"  # Change to your output directory

    # Position to paste the foreground image on the background
    position = (0, 0)  # Adjust as necessary

    # Call the function to process images
    add_background_to_images(background_image_path, input_directory, output_directory, position)
