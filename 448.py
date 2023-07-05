import os
import tensorflow as tf

def resize_image(image_path, target_size=(224, 224)):
    image_string = tf.io.read_file(image_path)
    image_decoded = tf.image.decode_jpeg(image_string, channels=1)  # use decode_jpeg for JPEG images
    image_resized = tf.image.resize(image_decoded, target_size)
    return image_resized

# Specify your directories
image_directory = 'output_grayscale'  # Replace with your root image directory
output_directory = 'output_224'  # Replace with your root output directory

# Iterate over all subdirectories in the directory
for subdir, dirs, files in os.walk(image_directory):
    for filename in files:
        if filename.endswith('.jpeg'):  # Use this for JPEG images
            image_path = os.path.join(subdir, filename)

            # Prepare output path
            relative_path = os.path.relpath(subdir, image_directory)
            output_subdir = os.path.join(output_directory, relative_path)
            
            # Create necessary subdirectories in output path
            os.makedirs(output_subdir, exist_ok=True)

            # Prepare the output file path
            output_path = os.path.join(output_subdir, filename)
            
            # Resize the image
            resized_image = resize_image(image_path)
            
            # Convert the tensor to uint8 for saving
            resized_image = tf.cast(resized_image, tf.uint8)
            
            # Encode the image to JPEG and write to file
            encoded_image = tf.image.encode_jpeg(resized_image)
            tf.io.write_file(output_path, encoded_image)
        
print("All images have been resized and saved to the new directory.")
