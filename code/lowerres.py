from cv2 import imread, imwrite, IMREAD_GRAYSCALE
from scipy import misc


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
    while True:
        filenameinput = input()
        if filenameinput == '!-end-!':
            break
        filenames.append(filenameinput)
    filenames = tuple(filenames)

    imagearrays = []
    for filename in filenames:
        imagearrays.append(imread(filename, IMREAD_GRAYSCALE))

    for i in range(len(imagearrays)):
        image = imagearrays[i]
        imagearrays[i] = misc.imresize(image, (round(image.shape[0] / 8), round(image.shape[1] / 8)))
    imagearrays = tuple(imagearrays)

    for i in range(len(imagearrays)):
        image = imagearrays[i]
        filename = filenames[i]
        imwrite(filename + '_down.png', image)

    print('Process completed.')


if __name__ == '__main__':
    takeinputthenrun()
