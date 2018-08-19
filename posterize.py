from PIL import Image
from PIL import ImageChops
import otsu

def posterize(img, low_thresholds, high_thresholds):
    bands = img.split()
    low_bands = map((lambda (band, threshold): band.point(lambda val: 128 if val > threshold else 0)), zip(bands, low_thresholds))
    high_bands = map((lambda (band, threshold): band.point(lambda val: 128 if val > threshold else 0)), zip(bands, high_thresholds))
    #bands = map(lambda band: band.convert('1'), bands)
    #map(lambda band: band.show(), bands)
    low_img = Image.merge('RGB', low_bands)
    high_img = Image.merge('RGB', high_bands)
    return ImageChops.add(low_img, high_img)

def thresholds(img):
    bands = img.split()
    low_band_thresholds = map(lambda band: otsu.threshold(band.histogram()), bands)
    low_bands = map((lambda (band, threshold): band.point(lambda val: 128 if val > threshold else 0)), zip(bands, low_band_thresholds))
    high_band_thresholds = map(lambda (band, band_mask): otsu.threshold(band.histogram(band_mask)), zip(bands, low_bands))
    return low_band_thresholds, high_band_thresholds
