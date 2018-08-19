def threshold(histogram):
    total = sum(histogram)
    sumB = 0
    wB = 0
    maximum = 0.0
    sum1 = 0
    level = 0
    for pos, val in enumerate(histogram, 0):
        sum1 += pos * val
    for i in range(256):
    	wB += histogram[i]
        wF = total - wB
        if wB == 0 or wF == 0:
            continue
        sumB += i * histogram[i]
        mF = (sum1 - sumB) / wF;
        between = wB * wF * ((sumB / wB) - mF) * ((sumB / wB) - mF);
        if between >= maximum:
            level = i
            maximum = between
    return level