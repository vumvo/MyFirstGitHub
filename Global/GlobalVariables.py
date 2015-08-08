import os
import time
import random
from lib import General

USER = os.environ['USERNAME']
CURRENT_TIME = time.asctime()
UNIQUESTRING = time.time()

if time.localtime()[3] > 12:
    AFTERNOON = True
else:
    AFTERNOON = False
    
import math as _math

def _get_area(diameter):
    radius = diameter /2.0
    area = _math.pi * radius * radius
    return area
AREA1 = _get_area(1)
AREA2 = _get_area(2)

FF_PROFILE = General.get_absolute_path('Browser/ff_profile')
