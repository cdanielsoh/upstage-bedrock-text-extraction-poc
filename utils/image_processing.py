from PIL import Image
import os


def crop_image_with_overlap(input_path, output_folder, crop_height, overlap):
    """
    Crops an image vertically with overlap and saves the cropped images.

    :param input_path: The path to the input image.
    :param output_folder: The path to the output folder.
    :param crop_height: The height of the crop.
    :param overlap: The height of the overlap.
    """
    with Image.open(input_path) as img:
        width, height = img.size

        # Handle case where image height is smaller than crop height
        if height <= crop_height:
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_folder, filename)
            img.save(output_path)  # Save the original image as is
            return

        # Extract filename and extension correctly
        filename = os.path.splitext(os.path.basename(input_path))[0]
        extension = os.path.splitext(input_path)[1]

        start = 0
        count = 0
        while start < height:
            end = min(start + crop_height, height)
            cropped_img = img.crop((0, start, width, end))
            output_path = os.path.join(output_folder, f"{filename}_cropped_{count}{extension}")
            cropped_img.save(output_path, optimize=True)
            cropped_img.close()

            if end == height:  # Break if we've reached the end of the image
                break

            start = end - overlap
            count += 1


def create_output_directory_structure(input_base_dir, output_base_dir):
    """
    Creates matching directory structure in output directory.

    :param input_base_dir: The input base directory.
    :param output_base_dir: The output base directory.
    """
    for root, dirs, files in os.walk(input_base_dir):
        relative_path = os.path.relpath(root, input_base_dir)
        output_dir = os.path.join(output_base_dir, relative_path)
        os.makedirs(output_dir, exist_ok=True)


def process_images_in_directory(input_base_dir, output_base_dir, crop_height=5000, overlap=100):
    """
    Processes all images in the input directory structure.

    :param input_base_dir: The input base directory.
    :param output_base_dir: The output base directory.
    :param crop_height: The height of the crop.
    :param overlap: The height of the overlap.
    """
    create_output_directory_structure(input_base_dir, output_base_dir)

    for root, dirs, files in os.walk(input_base_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(root, file)
                print(f"Processing {input_path}")
                relative_path = os.path.relpath(root, input_base_dir)
                output_dir = os.path.join(output_base_dir, relative_path)
                crop_image_with_overlap(input_path, output_dir, crop_height, overlap)
