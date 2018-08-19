from PIL import Image
from StringIO import StringIO
import urllib2

def load(image):
    if image.startswith('http://') or image.startswith('https://'):
        desc = StringIO(urllib2.urlopen(image).read())
    else:
        desc = open(image)
    return Image.open(desc)