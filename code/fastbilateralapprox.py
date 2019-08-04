"""
This filter is based on Fast "A Fast Approximation of the Bilateral Filter using a Signal Processing Approach"
(Paris & Durand, 2006).
For more information please follow references of The Report.

Code is highly inspired by 4 codes, 1 C++, 1 Python and 2 MatLab, available on The Internet.
For details see references of The Report.

Copyright (c) 2018 Ozgur Bagci

Contact:    {
                bagci.ozgur@metu.edu.tr
                bagciozgur@yahoo.com
                bagciozgur94@gmail.com
                bagciozgur94@hotmail.com.tr
                e2262137@ceng.metu.edu.tr
            }
"""


import numpy as np
from scipy import signal, interpolate


def bilateral(image, sigmaspatial, sigmarange, samplespatial=None, samplerange=None):
    """
    :param image: np.array
    :param sigmaspatial: int
    :param sigmarange: int
    :param samplespatial: int || None
    :param samplerange: int || None
    :return: np.array

    Note that sigma values must be integers.

    The 'image' 'np.array' must be given gray-scale. It is suggested that to use OpenCV.
    """

    height = image.shape[0]
    width = image.shape[1]

    samplespatial = sigmaspatial if (samplespatial is None) else samplespatial
    samplerange = sigmarange if (samplerange is None) else samplerange

    flatimage = image.flatten()

    edgemin = np.amin(flatimage)
    edgemax = np.amax(flatimage)
    edgedelta = edgemax - edgemin

    derivedspatial = sigmaspatial / samplespatial
    derivedrange = sigmarange / samplerange

    xypadding = round(2 * derivedspatial + 1)
    zpadding = round(2 * derivedrange + 1)

    samplewidth = int(round((width - 1) / samplespatial) + 1 + 2 * xypadding)
    sampleheight = int(round((height - 1) / samplespatial) + 1 + 2 * xypadding)
    sampledepth = int(round(edgedelta / samplerange) + 1 + 2 * zpadding)

    dataflat = np.zeros(sampleheight * samplewidth * sampledepth)

    (ygrid, xgrid) = np.meshgrid(range(width), range(height))

    dimx = np.around(xgrid / samplespatial) + xypadding
    dimy = np.around(ygrid / samplespatial) + xypadding
    dimz = np.around((image - edgemin) / samplerange) + zpadding

    flatx = dimx.flatten()
    flaty = dimy.flatten()
    flatz = dimz.flatten()

    dim = flatz + flaty * sampledepth + flatx * samplewidth * sampledepth
    dim = np.array(dim, dtype=int)

    dataflat[dim] = flatimage

    data = dataflat.reshape(sampleheight, samplewidth, sampledepth)
    weights = np.array(data, dtype=bool)

    kerneldim = derivedspatial * 2 + 1
    kerneldep = 2 * derivedrange * 2 + 1
    halfkerneldim = round(kerneldim / 2)
    halfkerneldep = round(kerneldep / 2)

    (gridx, gridy, gridz) = np.meshgrid(range(int(kerneldim)), range(int(kerneldim)), range(int(kerneldep)))
    gridx -= int(halfkerneldim)
    gridy -= int(halfkerneldim)
    gridz -= int(halfkerneldep)

    gridsqr = ((gridx * gridx + gridy * gridy) / (derivedspatial * derivedspatial)) \
        + ((gridz * gridz) / (derivedrange * derivedrange))
    kernel = np.exp(-0.5 * gridsqr)

    blurdata = signal.fftconvolve(data, kernel, mode='same')

    blurweights = signal.fftconvolve(weights, kernel, mode='same')
    blurweights = np.where(blurweights == 0, -2, blurweights)

    normalblurdata = blurdata / blurweights
    normalblurdata = np.where(blurweights < -1, 0, normalblurdata)

    (ygrid, xgrid) = np.meshgrid(range(width), range(height))

    dimx = (xgrid / samplespatial) + xypadding
    dimy = (ygrid / samplespatial) + xypadding
    dimz = (image - edgemin) / samplerange + zpadding

    return interpolate.interpn((range(normalblurdata.shape[0]), range(normalblurdata.shape[1]),
                               range(normalblurdata.shape[2])), normalblurdata, (dimx, dimy, dimz))
