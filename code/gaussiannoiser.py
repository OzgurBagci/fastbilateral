import numpy as np


def noiser(image, sigma):
    """
    :param sourcePath: np.array
    :param sigma: float
    :return: np.array

    The 'image' 'np.array' must be given gray-scale. It is suggested that to use OpenCV.
    """

    im = image + np.random.normal(0, sigma, (image.shape[0], image.shape[1])).reshape(image.shape[0], image.shape[1])
    return np.array(im, dtype=np.float32)
