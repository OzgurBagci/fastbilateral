from cv2 import bilateralFilter as bilateralfilter


def bilateral(image, sigmaspatial, sigmarange):
    """
    :param image: np.array
    :param sigmaspatial: float || int
    :param sigmarange: float || int
    :return: np.array

    The 'image' 'np.array' must be given gray-scale. It is suggested that to use OpenCV.
    """

    return bilateralfilter(image, 75, sigmarange, sigmaspatial)
