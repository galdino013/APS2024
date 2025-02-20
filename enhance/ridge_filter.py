import numpy as np
import scipy


def ridge_filter(im, orient, freq, kx, ky):
    angleInc = 3
    im = im.astype(float)
    rows, cols = im.shape
    newim = np.zeros((rows, cols))

    freq_1d = np.reshape(freq, (1, rows * cols))
    ind = np.where(freq_1d > 0)

    ind = np.array(ind)
    ind = ind[1, :]

    # Round the array of frequencies to the nearest 0.01 to reduce the
    # number of distinct frequencies we have to deal with.

    non_zero_elems_in_freq = freq_1d[0][ind]
    non_zero_elems_in_freq = np.double(
        np.round((non_zero_elems_in_freq * 100))) / 100

    unfreq = np.unique(non_zero_elems_in_freq)

    # Generate filters corresponding to these distinct frequencies and
    # orientations in 'angleInc' increments.

    sigmax = 1 / unfreq[0] * kx
    sigmay = 1 / unfreq[0] * ky

    sze = np.round(3 * np.max([sigmax, sigmay]))

    x = np.linspace(-int(sze), int(sze), (2 * int(sze) + 1))
    y = np.linspace(-int(sze), int(sze), (2 * int(sze) + 1))
    X, Y = np.meshgrid(x, y)

    reffilter = np.exp(-(((np.power(x, 2)) / (sigmax * sigmax) + (np.power(y, 2)) / (sigmay * sigmay)))
                       ) * np.cos(2 * np.pi * unfreq[0] * x)  # this is the original gabor filter

    if len(normim.shape) == 1:
        normim = normim.reshape(1, -1)  # Converte para uma matriz 2D com uma linha e várias colunas

    if len(reffilter.shape) == 2:
        filt_rows, filt_cols = reffilter.shape
    else:
    # Garantir que filt_rows e filt_cols sejam definidos
        filt_rows, filt_cols = 1, len(reffilter)
        print("reffilter não tem duas dimensões, atribuindo valores padrão")


    gabor_filter = np.array(
        np.zeros(
            (int(
                180 /
                angleInc),
                int(filt_rows),
                int(filt_cols))))

    for o in range(0, int(180 / angleInc)):

        # Generate rotated versions of the filter.  Note orientation
        # image provides orientation *along* the ridges, hence +90
        # degrees, and imrotate requires angles +ve anticlockwise, hence
        # the minus sign.

        rot_filt = scipy.ndimage.rotate(
            reffilter, -(o * angleInc + 90), reshape=False)
        gabor_filter[o] = rot_filt

    # Find indices of matrix points greater than maxsze from the image
    # boundary

    maxsze = int(sze)

    temp = freq > 0
    validr, validc = np.where(temp)

    temp1 = validr > maxsze
    temp2 = validr < rows - maxsze
    temp3 = validc > maxsze
    temp4 = validc < cols - maxsze

    final_temp = temp1 & temp2 & temp3 & temp4

    finalind = np.where(final_temp)

    # Convert orientation matrix values from radians to an index value
    # that corresponds to round(degrees/angleInc)

    maxorientindex = np.round(180 / angleInc)
    orientindex = np.round(orient / np.pi * 180 / angleInc)

    # do the filtering

    for i in range(0, rows):
        for j in range(0, cols):
            if(orientindex[i][j] < 1):
                orientindex[i][j] = orientindex[i][j] + maxorientindex
            if(orientindex[i][j] > maxorientindex):
                orientindex[i][j] = orientindex[i][j] - maxorientindex
    finalind_rows, finalind_cols = np.shape(finalind)
    sze = int(sze)
    for k in range(0, finalind_cols):
        r = validr[finalind[0][k]]
        c = validc[finalind[0][k]]

        img_block = im[r - sze:r + sze + 1][:, c - sze:c + sze + 1]

        newim[r][c] = np.sum(
            img_block * gabor_filter[int(orientindex[r][c]) - 1])

    return(newim)
