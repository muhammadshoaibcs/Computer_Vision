from PIL import Image
import os

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


def weighted_mean_filter(image, padding_type):

    width, height = image.size

    input_pixels = image.load()

    output_image = Image.new("L", (width, height))
    output_pixels = output_image.load()


    # Weighted mask
    kernel = [
        [1, 1, 1],
        [1, 2, 1],
        [1, 1, 1]
    ]

    total_weight = 10


    for y in range(height):

        for x in range(width):

            weighted_sum = 0


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

                    weighted_sum = weighted_sum + pixel * weight


            result = weighted_sum / total_weight

            output_pixels[x, y] = int(result)


    return output_image


input_images = [
    ("gaussian_noise.png", "gaussian"),
    ("salt_pepper_noise.png", "salt_pepper")
]


for filename, name in input_images:

    image = Image.open(
        os.path.join(images_folder, filename)
    ).convert("L")


    zero_result = weighted_mean_filter(image, "zero")

    zero_result.save(
        os.path.join(
            images_folder,
            name + "_weighted_mean_zero.png"
        )
    )


    border_result = weighted_mean_filter(image, "border")

    border_result.save(
        os.path.join(
            images_folder,
            name + "_weighted_mean_border.png"
        )
    )


print("Weighted mean filtering completed successfully.")