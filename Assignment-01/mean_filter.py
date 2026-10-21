from PIL import Image
import os


# ---------------------------------------------------------
# STEP 1: Find the folder containing this Python file
# ---------------------------------------------------------

current_folder = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------
# STEP 2: Function to get a pixel with padding
# ---------------------------------------------------------

def get_pixel(pixels, x, y, width, height, padding_type):

    # ZERO PADDING
    # If pixel is outside image, return 0.
    if padding_type == "zero":

        if x < 0 or x >= width or y < 0 or y >= height:
            return 0

        return pixels[x, y]


    # BORDER / REPLICATE PADDING
    # Copy nearest border pixel.
    if padding_type == "border":

        if x < 0:
            x = 0

        if x >= width:
            x = width - 1

        if y < 0:
            y = 0

        if y >= height:
            y = height - 1

        return pixels[x, y]


# ---------------------------------------------------------
# STEP 3: Mean filter function
# ---------------------------------------------------------

def mean_filter(image, padding_type):

    width, height = image.size

    input_pixels = image.load()

    output_image = Image.new("L", (width, height))
    output_pixels = output_image.load()


    # Visit every pixel
    for y in range(height):

        for x in range(width):

            total = 0

            # 3 x 3 neighborhood
            for j in range(-1, 2):

                for i in range(-1, 2):

                    pixel_value = get_pixel(
                        input_pixels,
                        x + i,
                        y + j,
                        width,
                        height,
                        padding_type
                    )

                    total = total + pixel_value


            # There are 9 pixels in a 3 x 3 mask
            average = total / 9

            output_pixels[x, y] = int(average)


    return output_image


# ---------------------------------------------------------
# STEP 4: Process both noisy images
# ---------------------------------------------------------

input_images = [
    ("gaussian_noise.png", "gaussian"),
    ("salt_pepper_noise.png", "salt_pepper")
]


for filename, name in input_images:

    image_path = os.path.join(current_folder, filename)

    image = Image.open(image_path).convert("L")


    # Apply mean filter using zero padding
    zero_result = mean_filter(image, "zero")

    zero_result.save(
        os.path.join(
            current_folder,
            name + "_mean_zero_padding.png"
        )
    )


    # Apply mean filter using border padding
    border_result = mean_filter(image, "border")

    border_result.save(
        os.path.join(
            current_folder,
            name + "_mean_border_padding.png"
        )
    )


print("Mean filtering completed successfully.")