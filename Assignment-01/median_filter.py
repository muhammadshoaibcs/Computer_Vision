from PIL import Image
import os

# ---------------------------------------------------------
# Find the folder containing this Python file
# ---------------------------------------------------------

current_folder = os.path.dirname(os.path.abspath(__file__))

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


# ---------------------------------------------------------
# Manual sorting function
# ---------------------------------------------------------

def bubble_sort(values):

    n = len(values)

    for i in range(n):

        for j in range(0, n - i - 1):

            if values[j] > values[j + 1]:

                temporary = values[j]

                values[j] = values[j + 1]

                values[j + 1] = temporary


    return values


def median_filter(image, padding_type):

    width, height = image.size

    input_pixels = image.load()

    output_image = Image.new("L", (width, height))
    output_pixels = output_image.load()


    for y in range(height):

        for x in range(width):

            values = []


            # Collect the 9 neighborhood values
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

                    values.append(value)


            # Sort values manually
            values = bubble_sort(values)


            # For 9 values, middle value is index 4
            median = values[4]

            output_pixels[x, y] = median


    return output_image


input_images = [
    ("gaussian_noise.png", "gaussian"),
    ("salt_pepper_noise.png", "salt_pepper")
]


for filename, name in input_images:

    image = Image.open(
        os.path.join(current_folder, filename)
    ).convert("L")


    zero_result = median_filter(image, "zero")

    zero_result.save(
        os.path.join(
            current_folder,
            name + "_median_zero.png"
        )
    )


    border_result = median_filter(image, "border")

    border_result.save(
        os.path.join(
            current_folder,
            name + "_median_border.png"
        )
    )


print("Median filtering completed successfully.")