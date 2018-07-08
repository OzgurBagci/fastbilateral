from skimage.restoration import denoise_bilateral as bilateralfilter


def bilateral(image, sigmaspatial, sigmarange):
    """
    :param image: np.array
    :param sigmaspatial: float || int
    :param sigmarange: float || int
    :return: np.array

    The 'image' 'np.array' must be given gray-scale. It is suggested that to use scikit-image.
    """

    return bilateralfilter(image, win_size=10, sigma_color=sigmarange,
                           sigma_spatial=sigmaspatial, bins=1000, multichannel=False)
