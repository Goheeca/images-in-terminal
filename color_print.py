# -*- coding: utf-8 -*-

HIGH = 255*2/3
LOW = 255*1/3

def rgb2esc(fg=(255,255,255), bg=(0,0,0), low=(LOW,LOW,LOW), high=(HIGH,HIGH,HIGH), text=u'⣿'):
    def color(bands):
       color = sum(map((lambda (band, low, key): key if band > low else 0), zip(bands, low,[1,2,4])))
       high_count = sum(1 for x, h in zip(bands, high) if x > h)
       return color, high_count >= 2
    
    fg_color, fg_intensity = color(fg)
    fg_color += 90 if fg_intensity else 30
    bg_color, bg_intensity = color(bg)
    bg_color += 100 if bg_intensity else 40
    return u'\x1b['+str(fg_color)+';'+str(bg_color)+u'm'+text+u'\x1b[m'