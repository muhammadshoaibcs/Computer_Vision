from PIL import Image
import os

# ---------------------------------------------------------
# Find the folder containing this Python file
# ---------------------------------------------------------

src_folder = os.path.dirname(os.path.abspath(__file__))
assignment_folder = os.path.dirname(src_folder)
images_folder = os.path.join(assignment_folder, "images")
# current_folder = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# Function to get a pixel with padding
# ---------------------------------------------------------

def get_pixel(pixels, x, y, width, height, padding_type):

    if padding_type == "zero":

        if x < 0 or x >= width or y < 0 or y >= height:
            return 0

        return pixels[x, y]


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


def maximum_filter(image, padding_type):

    width, height = image.size

    input_pixels = image.load()

    output_image = Image.new("L", (width, height))
    output_pixels = output_image.load()


    for y in range(height):

        for x in range(width):

            # Lowest possible grayscale value
            maximum_value = 0


            for j in range(-1, 2):

                for i in range(-1, 2):

                    value = get_pixel(
                        input_pixels,
                        x + i,
                        y + j,
                        width,
                        height,
                        padding_type
                    )


                    if value > maximum_value:
                        maximum_value = value


            output_pixels[x, y] = maximum_value


    return output_image


input_images = [
    ("gaussian_noise.png", "gaussian"),
    ("salt_pepper_noise.png", "salt_pepper")
]


for filename, name in input_images:

    image = Image.open(
        os.path.join(images_folder, filename)
    ).convert("L")


    zero_result = maximum_filter(image, "zero")

    zero_result.save(
        os.path.join(
            images_folder,
            name + "_maximum_zero.png"
        )
    )


    border_result = maximum_filter(image, "border")

    border_result.save(
        os.path.join(
            images_folder,
            name + "_maximum_border.png"
        )
    )


print("Maximum filtering completed successfully.")