# ---------------------------------------------------------
# Computer Vision Assignment
# Add Gaussian Noise and Salt-and-Pepper Noise to an Image
# ---------------------------------------------------------

from PIL import Image
import random
import math
import os

# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------

# Current src folder
src_folder = os.path.dirname(os.path.abspath(__file__))

# Assignment-01 folder
assignment_folder = os.path.dirname(src_folder)

# Images folder
images_folder = os.path.join(assignment_folder, "images")

# ---------------------------------------------------------
# STEP 1: Open the original image
# ---------------------------------------------------------

# "L" means grayscale image.
# Pixel values will be between 0 and 255.
image_path = os.path.join(images_folder, "original.png")
image = Image.open(image_path).convert("L")

# Get image width and height.
width, height = image.size

print("Image width :", width)
print("Image height:", height)


# ---------------------------------------------------------
# STEP 2: Create empty images for our noisy results
# ---------------------------------------------------------

# These images have the same size as the original image.
gaussian_image = Image.new("L", (width, height))
salt_pepper_image = Image.new("L", (width, height))


# ---------------------------------------------------------
# STEP 3: Get access to individual pixels
# ---------------------------------------------------------

original_pixels = image.load()
gaussian_pixels = gaussian_image.load()
salt_pepper_pixels = salt_pepper_image.load()


# ---------------------------------------------------------
# FUNCTION 1: Generate one Gaussian random noise value
# ---------------------------------------------------------

def generate_gaussian_noise(mean, standard_deviation):

    # Generate two random numbers between 0 and 1.
    u1 = random.random()
    u2 = random.random()

    # Box-Muller formula.
    #
    # This converts uniform random numbers into Gaussian (normally distributed) random numbers.
    #
    # z = sqrt(-2 ln(u1)) * cos(2 pi u2)

    z = math.sqrt(-2.0 * math.log(u1)) * \
        math.cos(2.0 * math.pi * u2)

    # Convert the standard Gaussian value into the mean and standard deviation we want.
    noise = mean + standard_deviation * z

    return noise


# ---------------------------------------------------------
# STEP 4: ADD GAUSSIAN NOISE
# ---------------------------------------------------------

# Mean = 0 means that the noise is centered around zero.
gaussian_mean = 0

# Standard deviation controls noise strength.
# Increase this value for stronger noise.
gaussian_sigma = 20


# Visit every pixel in the image.
for y in range(height):

    for x in range(width):

        # Read original pixel value.
        original_value = original_pixels[x, y]

        # Generate one random Gaussian noise value.
        noise = generate_gaussian_noise(
            gaussian_mean,
            gaussian_sigma
        )

        # Add noise to original pixel.
        noisy_value = original_value + noise

        # Pixel values must remain between 0 and 255.
        if noisy_value < 0:
            noisy_value = 0

        if noisy_value > 255:
            noisy_value = 255

        # Convert decimal result into integer.
        noisy_value = int(noisy_value)

        # Store new pixel value.
        gaussian_pixels[x, y] = noisy_value


# ---------------------------------------------------------
# STEP 5: ADD SALT-AND-PEPPER NOISE
# ---------------------------------------------------------

# Probability determines how much noise is added.
#
# 0.05 means approximately 5% of pixels will be changed.
noise_probability = 0.05


for y in range(height):

    for x in range(width):

        # Read original pixel.
        original_value = original_pixels[x, y]

        # Generate random number:
        #
        # 0.0 <= random_number < 1.0
        random_number = random.random()

        # Half of noisy pixels become PEPPER.
        if random_number < noise_probability / 2:

            # Pepper = black.
            salt_pepper_pixels[x, y] = 0

        # Other half become SALT.
        elif random_number < noise_probability:

            # Salt = white.
            salt_pepper_pixels[x, y] = 255

        else:

            # Pixel remains unchanged.
            salt_pepper_pixels[x, y] = original_value


# ---------------------------------------------------------
# STEP 6: SAVE OUTPUT IMAGES
# ---------------------------------------------------------
gaussian_image.save(
    os.path.join(images_folder, "gaussian_noise.png")
)

salt_pepper_image.save(
    os.path.join(images_folder, "salt_pepper_noise.png")
)

# ---------------------------------------------------------
# STEP 7: Display completion message
# ---------------------------------------------------------

print("Noise successfully added.")
print("Created: gaussian_noise.png")
print("Created: salt_pepper_noise.png")