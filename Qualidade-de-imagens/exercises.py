from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
from os import path
from itertools import product

# --------------- Questão 1 --------------- #

original_img = np.array(Image.open(path.join(path.curdir, "original_lena.jpg")).convert("L"))

# --------------- Questão 2 --------------- #

summed_img = original_img + 30
summed_img[summed_img <= 30] = 255
Image.fromarray(summed_img).save(path.join(path.curdir, "summed_lena.jpg"))

subtracted_img = original_img - 70
subtracted_img[subtracted_img >= (255 - 70)] = 0
Image.fromarray(subtracted_img).save(path.join(path.curdir, "subtracted_lena.jpg"))

multiplied_img = original_img.copy()
multiplied_img[multiplied_img > int(255 / 1.2)] = 255
multiplied_img[multiplied_img < 255] = np.array(multiplied_img[multiplied_img < 255] * 1.2, dtype="uint8")
Image.fromarray(multiplied_img).save(path.join(path.curdir, "multiplied_lena.jpg"))

divided_img = original_img // 4
Image.fromarray(divided_img).save(path.join(path.curdir, "divided_lena.jpg"))

# ------------- Questão 3 & 4 ------------- #

plt.figure()
plt.imshow(original_img, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.title("Original image")

fig, ax = plt.subplots(2, 2)
ax[0, 0].imshow(summed_img, cmap="gray", clim=(0, 255))
ax[0, 0].set_title("Summed image")
ax[0, 0].set_axis_off()
ax[0, 1].imshow(subtracted_img, cmap="gray", clim=(0, 255))
ax[0, 1].set_title("Subtracted image")
ax[0, 1].set_axis_off()
ax[1, 0].imshow(multiplied_img, cmap="gray", clim=(0, 255))
ax[1, 0].set_title("Multiplied image")
ax[1, 0].set_axis_off()
ax[1, 1].imshow(divided_img, cmap="gray", clim=(0, 255))
ax[1, 1].set_title("Divided image")
ax[1, 1].set_axis_off()
fig.tight_layout()
plt.show()

plt.figure()
plt.hist(original_img.ravel(), bins=256)
plt.title("Original image")
plt.xlabel("Grayscale value")
plt.xlabel("Pixel count")
plt.xlim(-2, 260)

fig, ax = plt.subplots(2, 2)

ax[0, 0].hist(summed_img.ravel(), bins=256)
ax[0, 0].set_title("Summed image")
ax[0, 0].set_xlabel("Grayscale value")
ax[0, 0].set_ylabel("Pixel count")
ax[0, 0].set_xlim(-5, 260)

ax[0, 1].hist(subtracted_img.ravel(), bins=256)
ax[0, 1].set_title("Subtracted image")
ax[0, 1].set_xlabel("Grayscale value")
ax[0, 1].set_ylabel("Pixel count")
ax[0, 1].set_xlim(-5, 260)

ax[1, 0].hist(multiplied_img.ravel(), bins=256)
ax[1, 0].set_title("Multiplied image")
ax[1, 0].set_xlabel("Grayscale value")
ax[1, 0].set_ylabel("Pixel count")
ax[1, 0].set_xlim(-5, 260)

ax[1, 1].hist(divided_img.ravel(), bins=256)
ax[1, 1].set_title("Divided image")
ax[1, 1].set_xlabel("Grayscale value")
ax[1, 1].set_ylabel("Pixel count")
ax[1, 1].set_xlim(-5, 260)

fig.tight_layout()
plt.show()

# --------------- Questão 5 --------------- #


def maximum_error(img_1, img_2):
    return np.max(np.abs((img_1.astype("int32") - img_2.astype("int32"))))


def mean_absolute_error(img_1, img_2):
    return np.sum(np.abs((img_1.astype("int32") - img_2.astype("int32")))) / np.prod(img_1.shape)


def mean_square_error(img_1, img_2):
    return np.sum(np.square(img_1.astype("int32") - img_2.astype("int32"))) / np.prod(img_1.shape)


def root_mean_square_error(img_1, img_2):
    return np.sqrt(mean_square_error(img_1, img_2))


def normalized_mean_square_error(img_1, img_2):
    return np.sum(np.square(img_1.astype("int32") - img_2.astype("int32"))) / np.sum(np.square(img_1.astype("int32")))


def peak_signal_to_noise_ratio(img_1, img_2):
    return 20 * np.log10(255 / root_mean_square_error(img_1, img_2))


def signal_to_noise_ratio(img_1, img_2):
    return 10 * np.log10(1 / normalized_mean_square_error(img_1, img_2))


def covariance(img_1, img_2):
    return np.sum(
        np.multiply(img_1.astype("int32") - np.mean(img_1), img_2.astype("int32") - np.mean(img_2))
    ) / np.prod(img_1.shape)


def correlation_coeficient(img_1, img_2):
    return np.sum(
        np.multiply(img_1.astype("int32") - np.mean(img_1), img_2.astype("int32") - np.mean(img_2))
    ) / np.sqrt(
        np.sum(np.square(img_1.astype("int32") - np.mean(img_1)))
        * np.sum(np.square(img_2.astype("int32") - np.mean(img_2)))
    )


def jaccard_coeficient(img_1, img_2):
    return np.sum(np.equal(img_1, img_2)) / np.prod(img_1.shape)


print("Maximum error:")
print("summed img:", maximum_error(original_img, summed_img))
print("subtracted img:", maximum_error(original_img, subtracted_img))
print("multiplied img:", maximum_error(original_img, multiplied_img))
print("divided img:", maximum_error(original_img, divided_img))
print()
print("Mean absolute error:")
print("summed img:", f"{mean_absolute_error(original_img, summed_img):.2f}")
print("subtracted img:", f"{mean_absolute_error(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{mean_absolute_error(original_img, multiplied_img):.2f}")
print("divided img:", f"{mean_absolute_error(original_img, divided_img):.2f}")
print()
print("Mean square error:")
print("summed img:", f"{mean_square_error(original_img, summed_img):.2f}")
print("subtracted img:", f"{mean_square_error(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{mean_square_error(original_img, multiplied_img):.2f}")
print("divided img:", f"{mean_square_error(original_img, divided_img):.2f}")
print()
print("Root mean square error:")
print("summed img:", f"{root_mean_square_error(original_img, summed_img):.2f}")
print("subtracted img:", f"{root_mean_square_error(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{root_mean_square_error(original_img, multiplied_img):.2f}")
print("divided img:", f"{root_mean_square_error(original_img, divided_img):.2f}")
print()
print("Normalized mean square error:")
print("summed img:", f"{normalized_mean_square_error(original_img, summed_img):.2f}")
print("subtracted img:", f"{normalized_mean_square_error(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{normalized_mean_square_error(original_img, multiplied_img):.2f}")
print("divided img:", f"{normalized_mean_square_error(original_img, divided_img):.2f}")
print()
print("Peak signal to noise ratio:")
print("summed img:", f"{peak_signal_to_noise_ratio(original_img, summed_img):.2f}")
print("subtracted img:", f"{peak_signal_to_noise_ratio(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{peak_signal_to_noise_ratio(original_img, multiplied_img):.2f}")
print("divided img:", f"{peak_signal_to_noise_ratio(original_img, divided_img):.2f}")
print()
print("Signal to noise ratio:")
print("summed img:", f"{signal_to_noise_ratio(original_img, summed_img):.2f}")
print("subtracted img:", f"{signal_to_noise_ratio(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{signal_to_noise_ratio(original_img, multiplied_img):.2f}")
print("divided img:", f"{signal_to_noise_ratio(original_img, divided_img):.2f}")
print()
print("Covariance:")
print("summed img:", f"{covariance(original_img, summed_img):.2f}")
print("subtracted img:", f"{covariance(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{covariance(original_img, multiplied_img):.2f}")
print("divided img:", f"{covariance(original_img, divided_img):.2f}")
print()
print("Correlation Coeficient:")
print("summed img:", f"{correlation_coeficient(original_img, summed_img):.2f}")
print("subtracted img:", f"{correlation_coeficient(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{correlation_coeficient(original_img, multiplied_img):.2f}")
print("divided img:", f"{correlation_coeficient(original_img, divided_img):.2f}")
print()
print("Jaccard Coeficient:")
print("summed img:", f"{jaccard_coeficient(original_img, summed_img):.2f}")
print("subtracted img:", f"{jaccard_coeficient(original_img, subtracted_img):.2f}")
print("multiplied img:", f"{jaccard_coeficient(original_img, multiplied_img):.2f}")
print("divided img:", f"{jaccard_coeficient(original_img, divided_img):.2f}")
print()

# --------------- Questão 6 --------------- #


def downscale_image(image, factor):
    downscaled_img = np.zeros((np.array(image.shape) / factor).astype("int"), dtype="uint8")

    for x in range(0, image.shape[0] - factor + 1, factor):
        for y in range(0, image.shape[1] - factor + 1, factor):
            window_buffer = [image[i, j] for i, j in product(range(x, x + factor), range(y, y + factor))]
            downscaled_img[int(x / factor), int(y / factor)] = np.sum(window_buffer) / np.square(factor)

    return downscaled_img


downscaled_img_by_2 = downscale_image(original_img, 2)
Image.fromarray(downscaled_img_by_2).save(path.join(path.curdir, "downscaled_lena_by_2.jpg"))

downscaled_img_by_4 = downscale_image(original_img, 4)
Image.fromarray(downscaled_img_by_4).save(path.join(path.curdir, "downscaled_lena_by_4.jpg"))

downscaled_img_by_8 = downscale_image(original_img, 8)
Image.fromarray(downscaled_img_by_8).save(path.join(path.curdir, "downscaled_lena_by_8.jpg"))

plt.figure()
plt.imshow(downscaled_img_by_2, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.figure()
plt.imshow(downscaled_img_by_4, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.figure()
plt.imshow(downscaled_img_by_8, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.show()

# --------------- Questão 7 --------------- #


def gaussian_noise(image, mu, sigma):
    clean_img = image.copy().astype("int16")
    noise = np.random.normal(mu, sigma, clean_img.shape).astype("int16")
    noised_img = clean_img + noise
    noised_img[noised_img < 0] = 0
    noised_img[noised_img > 255] = 255
    return noised_img.astype("uint8")


noised_img = gaussian_noise(original_img, 0, 10)
Image.fromarray(noised_img).save(path.join(path.curdir, "noised_lena.jpg"))

plt.figure()
plt.imshow(original_img, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.figure()
plt.imshow(noised_img, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.show()

# --------------- Questão 8 --------------- #


def entropy(image):
    _, frequency = np.unique(image, return_counts=True)
    frequency_density = frequency / image.size
    return -np.sum([p * np.log2(p) for p in frequency_density])


print(f"Entropia (imagem original): {entropy(original_img):.3f}")
print(f"Entropia (imagem com ruido): {entropy(noised_img):.3f}")
print()

# --------------- Questão 9 --------------- #

modified_img = np.array(Image.open(path.join(path.curdir, "modified_lena.jpg")).convert("L"))

difference = np.abs(original_img.astype("int16") - modified_img.astype("int16")).astype("uint8")

binary_difference = difference.copy()
binary_difference[binary_difference > 0] = 255
Image.fromarray(binary_difference).save(path.join(path.curdir, "binary_difference_lena.jpg"))

plt.figure()
plt.imshow(binary_difference, cmap="gray", clim=(0, 255))
plt.axis("off")
plt.show()

# --------------- Questão 10 -------------- #


def find_neighbors(image, index, neighboring_method):
    neighbors = set()
    raw_neighbors = {
        "4": [(0, 1), (1, 0), (0, -1), (-1, 0)],
        "8": [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)],
    }
    for neighbor in raw_neighbors[neighboring_method]:
        calculated_neighbor = tuple(np.array(index) + neighbor)
        try:
            if all(coord >= 0 for coord in calculated_neighbor) and image[calculated_neighbor] == 255:
                neighbors.add(calculated_neighbor)
        except Exception:
            pass

    return neighbors


def find_components(binary_image, neighboring_method):
    visited_pixels = set()
    pixels_stack = list()
    to_be_visited_pixels = set()
    components = list()
    for index, value in np.ndenumerate(binary_image):
        if value != 255 or index in visited_pixels:
            continue

        pixels_stack.append(index)
        component = []

        while len(pixels_stack) > 0:
            pixel_index = pixels_stack.pop()
            component.append(pixel_index)
            visited_pixels.add(pixel_index)
            to_be_visited_pixels.discard(pixel_index)

            pixel_neighbors = find_neighbors(binary_image, pixel_index, neighboring_method)
            pixels_stack.extend(
                [
                    neighbor
                    for neighbor in pixel_neighbors
                    if neighbor not in to_be_visited_pixels and neighbor not in visited_pixels
                ]
            )
            to_be_visited_pixels |= pixel_neighbors

        components.append(component)

    return components


components_4 = find_components(binary_difference, "4")
print("vizinhança-4:", len(components_4))
components_8 = find_components(binary_difference, "8")
print("vizinhança-8:", len(components_8))


binary_difference_clipped = binary_difference[270:297, 335:361]

components_4_clipped = find_components(binary_difference_clipped, "4")
components_8_clipped = find_components(binary_difference_clipped, "8")

fig, ax = plt.subplots(1, 2)
ax[0].imshow(binary_difference_clipped, cmap="gray", clim=(0, 255))
for component in components_4_clipped:
    ax[0].plot([pixel[1] for pixel in component], [pixel[0] for pixel in component], "o", alpha=0.5)
ax[0].set_title("neighborhood-4 example")

ax[1].imshow(binary_difference_clipped, cmap="gray", clim=(0, 255))
for component in components_8_clipped:
    ax[1].plot([pixel[1] for pixel in component], [pixel[0] for pixel in component], "o", alpha=0.5)
ax[1].set_title("neighborhood-8 example")


plt.show()
