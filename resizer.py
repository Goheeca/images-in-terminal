from PIL import Image

def resize(img, ratio, multiplier=(1,1)):
    x, y = multiplier
    w, h = img.size
    w = int(int(w * ratio) * x)
    h = int(int(h * ratio) * y)
    return img.resize((w, h), Image.ANTIALIAS)

def fit_in_ratio((orig_w, orig_h), (box_w, box_h)):
    ratio_w = box_w / float(orig_w)
    ratio_h = box_h / float(orig_h)
    return min(ratio_w, ratio_h)
    