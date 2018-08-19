#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

def colorEscapeAnother(r,g,b, low, high):
    avg = (r+g+b)/3
    th = 128
    color = 0
    if r > th:
  	color += 1
    if g > th:
        color += 2
    if b > th:
        color += 4
    if avg > high:
	color += 8
    return color

def num2esc(n):
    if n >= 8:
        return u'\x1b['+str(30+n-8)+'1m'
    else:
        return u'\x1b['+str(30+n)+'m'

def getTerminalSize():
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        import fcntl
        import termios
        import struct
        cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


A = 1/3.0
B = 1/3.0

def image2term(image, threshold=128, ratio=None, invert=False):
    if image.startswith('http://') or image.startswith('https://'):
        desc = StringIO(urllib2.urlopen(image).read())
    else:
        desc = open(image)

    img = Image.open(desc)

    w, h = img.size
    if ratio:
        w = int(w * ratio)
        h = int(h * ratio)
        img = img.resize((w, h), Image.ANTIALIAS)
    else:
        tw = getTerminalSize()[0]
        tw *= 2
        if tw < w:
            ratio = tw / float(w)
            w = tw
            h = int(h * ratio)
            img = img.resize((w, h), Image.ANTIALIAS)
    can = Canvas()
    x = y = 0

    i = img.convert('L')

    try:
         i_converted = i.tobytes()
    except AttributeError:
         i_converted = i.tostring()

    for pix in i_converted:
        if invert:
            if ord(pix) > threshold:
                can.set(x, y)
        else:
            if ord(pix) < threshold:
                can.set(x, y)
        x += 1
        if x >= w:
            y += 1
            x = 0

    img = img.resize((w/2, h/4), Image.ANTIALIAS)
    w, h = img.size
    (rimg, gimg, bimg) = img.split()
    x = y = 0
    nums_rows = []
    #s = ''
    z = []
    for (r, g, b) in zip(rimg.tobytes(), gimg.tobytes(), bimg.tobytes()):
        c = colorEscapeAnother(ord(r),ord(g),ord(b), A*threshold, 255*(1-B)+B*threshold)
        z.append(c)
        #s += num2esc(c)+'@\x1b[m'
        x += 1
        if x >= w:
            nums_rows.append(z)
            z = []
            y += 1
            x = 0
            #s += '\n'
    nums_rows.append(z)
    #print(s)

    return (can.rows(), nums_rows)


def argparser():
    import argparse
    from sys import stdout
    argp = argparse.ArgumentParser(description='drawille - image to terminal example script')
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
    argp.add_argument('-t', '--threshold'
                     ,help      = 'Color threshold'
                     ,default   = 128
                     ,action    = 'store'
                     ,type      = int
                     ,metavar   = 'N'
                     )
    argp.add_argument('-i', '--invert'
                     ,help      = 'Invert colors'
                     ,default   = False
                     ,action    = 'store_true'
                     )
    argp.add_argument('image'
                     ,metavar   = 'FILE'
                     ,help      = 'Image file path/url'
                     )
    return vars(argp.parse_args())


def __main__():
    args = argparser()
    (dot_rows, coloring) = image2term(args['image'], args['threshold'], args['ratio'], args['invert'])
    colored = u''
    for (dot_row, color_row) in zip(dot_rows, coloring):
        for (dot, color) in zip(dot_row, color_row):
            args['output'].write(num2esc(color)+dot+u'\x1b[m')
        args['output'].write('\n')
    #args['output'].write(dots)
    args['output'].write('\x1b[m')
    args['output'].write('\n')


if __name__ == '__main__':
    __main__()
