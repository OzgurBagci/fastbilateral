import time
from cv2 import imread, imwrite, IMREAD_GRAYSCALE
import random as rand
from gaussiannoiser import noiser
from skimage.io import imread as skread
from skimage.io import imsave
import numpy as np


def takeinputthenrun():
    """
    :return: None
    """
    print('IMPORTANT NOTICE: You must give in at least 2 images.')
    print('Type images as full names with full path or relative path to current directory including extensions.')
    print('For same directory you can type it as "./filename.extension"')
    print('Prompt starts without any print statements in order to improve logging.')
    print('To stop giving inputs type "!-end-!", then press Enter.')

    filenames = []

    print('Overall Timer started.')
    bigstart = time.time()

    while True:
        filenameinput = input()
        if filenameinput == '!-end-!':
            break
        filenames.append(filenameinput)
    filenames = tuple(filenames)

    imagearrays = []
    for filename in filenames:
        imagearrays.append(imread(filename, IMREAD_GRAYSCALE))
    imagearrays = tuple(imagearrays)

    print('Writing gray-scale images to given image directories.')
    for i in range(len(imagearrays)):
        image = imagearrays[i]
        filename = filenames[i]
        imwrite(filename + '_grayscale.png', image)

    print('Done.')

    noisyimages, noisesigmas = noiseimages(imagearrays)

    print('Writing noisy images to given image directories.')
    for i in range(len(noisyimages)):
        noisy = noisyimages[i]
        filename = filenames[i]
        imwrite(filename + '_noisy.png', noisy)

    print('Done.')

    sknoisyimages = []
    for filename in filenames:
        sknoisyimages.append(skread(filename, as_grey=True))    # scikit-image does not play nice with OpenCV.

    print('Applying Bilateral Filter Implementations. This may take a while. Timer will print the results.')
    results = runbilaterals(noisyimages, noisesigmas, sknoisyimages)

    print('Writing the noise reduced images to given image directories.')
    for i in range(len(results[0])):
        own = results[0][i]
        cv = results[1][i]
        skim = results[2][i]
        filename = filenames[i]
        imwrite(filename + '_own.png', own)
        imwrite(filename + '_ocv.png', cv)
        imsave(filename + '_skim.png', skim)    # scikit-image does not play nice with OpenCV.
    print('Done.')

    print('Process completed.')

    bigend = time.time()
    print('Overall Timer ended in: "', bigend - bigstart, '" seconds.')


def runbilaterals(noisylist, noisesigmas, sknoisyimages, sigmarange=22):
    """
    :param imagetuple: tuple(np.array)
    :param noisylist: tuple(np.array)
    :param sigmarange: int
    :param noisestart: int
    :param noiseend: int
    :return: tuple(tuple(numpy.array))
    """

    noisesigmas = np.array(np.around(np.array(noisesigmas) / 2.87), dtype=int)

    from fastbilateralapprox import bilateral

    print('Own Implementation started.')
    start = time.time()

    bilateralown = []
    for i in range(len(noisylist)):
        noisyimage = noisylist[i]
        sigmaspatial = noisesigmas[i]
        bilateralown.append(bilateral(noisyimage, sigmaspatial, sigmarange,
                                      int(round(sigmaspatial / 2.32)), int(round(sigmarange / 2.32))))
    bilateralown = tuple(bilateralown)

    end = time.time()
    print('Own Implementation Ended in "', end - start, '" seconds.')

    from opencvbilateral import bilateral

    print('OpenCV Implementation started.')
    start = time.time()

    bilateralocv = []
    for i in range(len(noisylist)):
        noisyimage = noisylist[i]
        sigmaspatial = noisesigmas[i]
        bilateralocv.append(bilateral(noisyimage, sigmaspatial, sigmarange))
    bilateralocv = tuple(bilateralocv)

    end = time.time()
    print('OpenCV Implementation Ended in "', end - start, '" seconds.')

    from skimagebilateral import bilateral

    print('scikit-image Implementation started.')
    start = time.time()

    bilateralskim = []
    for i in range(len(sknoisyimages)):
        noisyimage = sknoisyimages[i]
        sigmaspatial = noisesigmas[i]
        bilateralskim.append(bilateral(noisyimage, sigmaspatial, sigmarange))
    bilateralskim = tuple(bilateralskim)

    end = time.time()
    print('scikit-image Implementation Ended in "', end - start, '" seconds.')

    return bilateralown, bilateralocv, bilateralskim


def noiseimages(imagetuple, noisestart=10, noiseend=25):
    """
    :param imagetuple: tuple(np.array)
    :param noisestart: int
    :param noiseend: int
    :return: tuple(tuple(np.array))
    """
    noisesigmas = rand.sample(range(noisestart, noiseend, 1), k=len(imagetuple))
    noisylist = []
    for i in range(len(imagetuple)):
        image = imagetuple[i]
        noisesigma = noisesigmas[i]
        noisylist.append(noiser(image, noisesigma))
    noisylist = tuple(noisylist)
    return noisylist, noisesigmas


if __name__ == '__main__':
    takeinputthenrun()
