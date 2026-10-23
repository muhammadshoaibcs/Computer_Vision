from PIL import Image
import os
import csv


# ---------------------------------------------------------
# STEP 1: SET PROJECT PATHS
# ---------------------------------------------------------

# Folder where this Python file is stored
src_folder = os.path.dirname(os.path.abspath(__file__))

# Parent Assignment-01 folder
assignment_folder = os.path.dirname(src_folder)

# Folder containing all images
images_folder = os.path.join(assignment_folder, "images")


# ---------------------------------------------------------
# STEP 2: MANUAL MSE FUNCTION
# ---------------------------------------------------------

def calculate_mse(original_image, processed_image):

    # Get dimensions of both images
    original_width, original_height = original_image.size
    processed_width, processed_height = processed_image.size

    # Both images must have exactly the same dimensions
    if original_width != processed_width or \
       original_height != processed_height:

        print("Error: Image sizes are different.")
        return None


    # Access individual pixels
    original_pixels = original_image.load()
    processed_pixels = processed_image.load()


    # This variable will store the total squared error
    squared_error_sum = 0.0


    # Visit every pixel
    for y in range(original_height):

        for x in range(original_width):

            # Original true pixel value
            original_value = original_pixels[x, y]

            # Corresponding processed pixel value
            processed_value = processed_pixels[x, y]


            # STEP A: Calculate difference
            difference = processed_value - original_value


            # STEP B: Square the difference
            squared_difference = difference * difference


            # STEP C: Add to total error
            squared_error_sum = (
                squared_error_sum + squared_difference
            )


    # STEP D: Calculate total number of pixels
    total_pixels = original_width * original_height


    # STEP E: Calculate average squared error
    mse = squared_error_sum / total_pixels


    return mse


# ---------------------------------------------------------
# STEP 3: OPEN ORIGINAL CLEAN IMAGE
# ---------------------------------------------------------

original_path = os.path.join(
    images_folder,
    "original.png"
)

original_image = Image.open(
    original_path
).convert("L")


# ---------------------------------------------------------
# STEP 4: LIST IMAGES TO EVALUATE
# ---------------------------------------------------------

test_images = [

    # Original noisy images
    ("Gaussian Noise",
     "gaussian_noise.png"),

    ("Salt-Pepper Noise",
     "salt_pepper_noise.png"),


    # MEAN FILTER
    ("Gaussian - Mean - Zero Padding",
     "gaussian_mean_zero_padding.png"),

    ("Gaussian - Mean - Border Padding",
     "gaussian_mean_border_padding.png"),

    ("Salt-Pepper - Mean - Zero Padding",
     "salt_pepper_mean_zero_padding.png"),

    ("Salt-Pepper - Mean - Border Padding",
     "salt_pepper_mean_border_padding.png"),


    # WEIGHTED MEAN FILTER
    ("Gaussian - Weighted Mean - Zero Padding",
     "gaussian_weighted_mean_zero.png"),

    ("Gaussian - Weighted Mean - Border Padding",
     "gaussian_weighted_mean_border.png"),

    ("Salt-Pepper - Weighted Mean - Zero Padding",
     "salt_pepper_weighted_mean_zero.png"),

    ("Salt-Pepper - Weighted Mean - Border Padding",
     "salt_pepper_weighted_mean_border.png"),


    # MEDIAN FILTER
    ("Gaussian - Median - Zero Padding",
     "gaussian_median_zero.png"),

    ("Gaussian - Median - Border Padding",
     "gaussian_median_border.png"),

    ("Salt-Pepper - Median - Zero Padding",
     "salt_pepper_median_zero.png"),

    ("Salt-Pepper - Median - Border Padding",
     "salt_pepper_median_border.png"),


    # MINIMUM FILTER
    ("Gaussian - Minimum - Zero Padding",
     "gaussian_minimum_zero.png"),

    ("Gaussian - Minimum - Border Padding",
     "gaussian_minimum_border.png"),

    ("Salt-Pepper - Minimum - Zero Padding",
     "salt_pepper_minimum_zero.png"),

    ("Salt-Pepper - Minimum - Border Padding",
     "salt_pepper_minimum_border.png"),


    # MAXIMUM FILTER
    ("Gaussian - Maximum - Zero Padding",
     "gaussian_maximum_zero.png"),

    ("Gaussian - Maximum - Border Padding",
     "gaussian_maximum_border.png"),

    ("Salt-Pepper - Maximum - Zero Padding",
     "salt_pepper_maximum_zero.png"),

    ("Salt-Pepper - Maximum - Border Padding",
     "salt_pepper_maximum_border.png"),


    # GAUSSIAN FILTER
    ("Gaussian Noise - Gaussian Filter - Zero Padding",
     "gaussian_gaussian_filter_zero.png"),

    ("Gaussian Noise - Gaussian Filter - Border Padding",
     "gaussian_gaussian_filter_border.png"),

    ("Salt-Pepper - Gaussian Filter - Zero Padding",
     "salt_pepper_gaussian_filter_zero.png"),

    ("Salt-Pepper - Gaussian Filter - Border Padding",
     "salt_pepper_gaussian_filter_border.png")
]


# ---------------------------------------------------------
# STEP 5: CALCULATE MSE FOR EVERY IMAGE
# ---------------------------------------------------------

results = []


print("")
print("------------------------------------------")
print("       MSE EVALUATION RESULTS")
print("------------------------------------------")
print("")


for description, filename in test_images:

    image_path = os.path.join(
        images_folder,
        filename
    )


    # Check if file actually exists
    if os.path.exists(image_path):

        processed_image = Image.open(
            image_path
        ).convert("L")


        mse_value = calculate_mse(
            original_image,
            processed_image
        )


        if mse_value is not None:

            results.append(
                (description, filename, mse_value)
            )

            print(
                description,
                "=",
                round(mse_value, 4)
            )

    else:

        print(
            "File not found:",
            filename
        )


# ---------------------------------------------------------
# STEP 6: SORT FROM LOWEST MSE TO HIGHEST
# ---------------------------------------------------------

# Manual simple sorting
for i in range(len(results)):

    for j in range(
        0,
        len(results) - i - 1
    ):

        if results[j][2] > results[j + 1][2]:

            temporary = results[j]

            results[j] = results[j + 1]

            results[j + 1] = temporary


# ---------------------------------------------------------
# STEP 7: DISPLAY RANKING
# ---------------------------------------------------------

print("")
print("------------------------------------------")
print("       RANKED BY LOWEST MSE")
print("------------------------------------------")
print("")


rank = 1

for description, filename, mse_value in results:

    print(
        rank,
        ".",
        description,
        "=",
        round(mse_value, 4)
    )

    rank = rank + 1


# ---------------------------------------------------------
# STEP 8: SAVE RESULTS TO CSV
# ---------------------------------------------------------

csv_path = os.path.join(
    assignment_folder,
    "mse_results.csv"
)


with open(csv_path, "w", newline="") as csv_file:

    writer = csv.writer(csv_file)

    # Column headings
    writer.writerow([
        "Filter / Image",
        "Filename",
        "MSE"
    ])


    for description, filename, mse_value in results:

        writer.writerow([
            description,
            filename,
            round(mse_value, 4)
        ])


print("")
print("MSE calculation completed.")
print("Results saved to:")
print(csv_path)