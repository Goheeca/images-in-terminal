from PIL import Image, ImageChops
import otsu

def posterize(img, low_thresholds, high_thresholds):
    bands = img.split()
    band_thresholds = map(lambda band: otsu.threshold(band.histogram()), bands)
    low_bands = map((lambda (band, threshold): band.point(lambda val: 128 if val > threshold else 0)), zip(bands, low_thresholds))
    band_thresholds = map(lambda (band, band_mask): otsu.threshold(band.histogram(band_mask)), zip(bands, low_bands))
    high_bands = map((lambda (band, threshold): band.point(lambda val: 128 if val > threshold else 0)), zip(bands, high_thresholds))
#    bands = map(lambda band: band.convert('1'), bands)
#    map(lambda band: band.show(), bands)
    low_img = Image.merge('RGB', low_bands)
    high_img = Image.merge('RGB', high_bands)
    return ImageChops.add(low_img, high_img)

def thresholds(img):
    bands = img.split()
    mid = map(lambda band: otsu.threshold(band.histogram()), bands)
    mid_bands = map((lambda (band, threshold): band.point(lambda val: 255 if val > threshold else 0)), zip(bands, mid))
    high = map(lambda (band, band_mask): otsu.threshold(band.histogram(band_mask)), zip(bands, mid_bands))
    mid_bands = map(lambda band: band.point(lambda val: not val), mid_bands)
    low = map(lambda (band, band_mask): otsu.threshold(band.histogram(band_mask)), zip(bands, mid_bands))
    return low, mid, high
