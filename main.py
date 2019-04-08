#!/usr/bin/env python
# -*- coding: utf-8 -*-

import image
import term
import resizer
import posterizer
import color_print
import otsu
import math
from PIL import ImageEnhance
from drawille import Canvas

ANTI_FONT_DISTORTION = (2,1)

def bound_addition(a, b, low = 0, high = 255):
    p2p = high - low   
    x = -math.log(float(p2p) / (a - low) - 1)
    x += b
    return p2p / (1 + math.exp(-x)) + low

def argparser():
    import argparse
    from sys import stdout
    argp = argparse.ArgumentParser(description='Image to terminal')
    argp.add_argument('-o', '--output'
                     ,help      = 'Output file - default is STDOUT'
                     ,metavar   = 'FILE'
                     ,default   = stdout
                     ,type      = argparse.FileType('w')
                     )
    argp.add_argument('-r', '--ratio'
                     ,help      = 'Image resize ratio'
                     ,default   = None
                     ,action    = 'store'
                     ,type      = float
                     ,metavar   = 'N'
                     )
    argp.add_argument('-c', '--color'
                     ,help      = 'Threshold multiplier'
                     ,default   = None
                     ,action    = 'store'
                     ,type      = float
                     ,metavar   = 'N'
                     )
    argp.add_argument('-s', '--shape'
                     ,help      = 'Contour threshold multiplier'
                     ,default   = None
                     ,action    = 'store'
                     ,type      = float
                     ,metavar   = 'N'
                     )
    argp.add_argument('-n', '--contrast'
                     ,help      = 'Contrast adjustment'
                     ,default   = None
                     ,action    = 'store'
                     ,type      = float
                     ,metavar   = 'N'
                     )
    argp.add_argument('image'
                     ,metavar   = 'FILE'
                     ,help      = 'Image file path/url'
                     )
    return vars(argp.parse_args())


def __main__():
    args = argparser()
    out = args['output']

    orig_img = image.load(args['image']).convert('RGB')
    if args['contrast'] != None:
        orig_img = ImageEnhance.Contrast(orig_img).enhance(args['contrast'])
    orig_img = resizer.resize(orig_img, 1, ANTI_FONT_DISTORTION)
    fit_ratio = resizer.fit_in_ratio(orig_img.size, term.size())
    if args['ratio']:
        fit_ratio *= args['ratio']

    img = resizer.resize(orig_img, fit_ratio, (1, 1))
    lows, mids, highs = posterizer.thresholds(img)
    if args['color'] != None:
	lows = map(lambda val: bound_addition(val, args['color']), lows)
	mids = map(lambda val: bound_addition(val, args['color']), mids)
	highs = map(lambda val: bound_addition(val, args['color']), highs)
    colors = posterizer.posterize(img, mids, highs)

#    img.show()
    shapes = resizer.resize(orig_img, fit_ratio, (2, 4))
#    shapes.show()
    shapes = shapes.convert('L')
    threshold = otsu.threshold(shapes.histogram())
#    mask = shapes.point(lambda val: 255 if val <= threshold else 0).convert('1')
#    threshold = otsu.threshold(shapes.histogram(mask))
    if args['shape'] != None:
	threshold = bound_addition(threshold, args['shape'])
    shapes = shapes.point(lambda val: 255 if val > threshold else 0).convert('1')
#    shapes.show()
    dots = Canvas()
    w, h = shapes.size
    for index, pixel in enumerate(list(shapes.getdata()),0):
        if pixel:
	    dots.set(index % w, index // w)
#    out.write(dots.frame(0,0,w,h))
#    out.write('\n')
    
    w, h = colors.size
    for index, pixel in enumerate(list(colors.getdata()),0):
        x = (index % w) * 2
        y = (index // w) * 4
        miniframe = unicode(dots.frame(x,y,x+2,y+4), 'utf-8')
	miniframe = miniframe if len(miniframe) else u'\u2800'
        out.write(color_print.rgb2esc(pixel, [0,0,0], lows, highs, miniframe))
	if not (1+index) % w:
	    out.write('\n')
        

if __name__ == '__main__':
    __main__()