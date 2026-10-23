from PIL import Image
import os
import math

src_folder = os.path.dirname(os.path.abspath(__file__))
assignment_folder = os.path.dirname(src_folder)
images_folder = os.path.join(assignment_folder, "images")
#current_folder = os.path.dirname(os.path.abspath(__file__))


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
# Create 3 x 3 Gaussian kernel manually
# ---------------------------------------------------------

def create_gaussian_kernel(sigma):

    kernel = []

    total = 0.0


    for y in range(-1, 2):

        row = []

        for x in range(-1, 2):

            exponent = -(x * x + y * y) / (2 * sigma * sigma)

            value = math.exp(exponent)

            row.append(value)

            total = total + value


        kernel.append(row)


    # Normalize kernel so total weight becomes 1
    for y in range(3):

        for x in range(3):

            kernel[y][x] = kernel[y][x] / total


    return kernel


def gaussian_filter(image, padding_type, sigma):

    width, height = image.size

    input_pixels = image.load()

    output_image = Image.new("L", (width, height))
    output_pixels = output_image.load()


    kernel = create_gaussian_kernel(sigma)


    for y in range(height):

        for x in range(width):

            result = 0.0


            for j in range(-1, 2):

                for i in range(-1, 2):

                    pixel = get_pixel(
                        input_pixels,
                        x + i,
                        y + j,
                        width,
                        height,
                        padding_type
                    )

                    weight = kernel[j + 1][i + 1]

                    result = result + pixel * weight


            # Make sure result remains valid
            if result < 0:
                result = 0

            if result > 255:
                result = 255


            output_pixels[x, y] = int(result)


    return output_image


# Standard deviation
sigma = 1.0


input_images = [
    ("gaussian_noise.png", "gaussian"),
    ("salt_pepper_noise.png", "salt_pepper")
]


for filename, name in input_images:

    image = Image.open(
        os.path.join(images_folder, filename)
    ).convert("L")


    zero_result = gaussian_filter(
        image,
        "zero",
        sigma
    )

    zero_result.save(
        os.path.join(
            images_folder,
            name + "_gaussian_filter_zero.png"
        )
    )


    border_result = gaussian_filter(
        image,
        "border",
        sigma
    )

    border_result.save(
        os.path.join(
            images_folder,
            name + "_gaussian_filter_border.png"
        )
    )


print("Gaussian filtering completed successfully.")