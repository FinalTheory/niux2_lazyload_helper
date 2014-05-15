# -*- coding: UTF-8 -*-
"""
This pelican plugin is inspired by the plugin [better figures and images](https://github.com/getpelican/pelican-plugins/tree/master/better_figures_and_images) and is intended to be used with the theme [niu-x2-sidebar](https://github.com/mawenbao/niu-x2-sidebar).

To all the img tags in the html document, this plugin do these things:

    * add attributes:
        * width: real width of the image file, in px.
    * if `NIUX2_LAZY_LOAD` is set as True in your pelican configuration:
        * add the following attributes:
            * data-height: real height of the image file, in px.
            * data-width: real width of the image file, in px.
        * add class `lazy`.
        * move attribute `src` to attribute `data-original`.

Requirements:
pip install pillow beautifulsoup4
"""

from os import path, access, R_OK
from pelican import signals
from bs4 import BeautifulSoup
from PIL import Image
import logging
import re

logger = logging.getLogger(__name__)
_width_attr_reg = re.compile(r'[a-z]*$')

def parse_images(instance):
    if instance._content is None or not 'img' in instance._content:
        return

    content = instance._content[:]
    soup = BeautifulSoup(content)

    for img in soup('img'):
        imgPath, imgFilename = path.split(img['src'])

        if not imgPath.startswith('/static'):
            logger.debug('imgPath %s not started with /static', imgPath)
            continue
        # Build the source image filename
        imgSrc = instance.settings['PATH'] + imgPath + '/' + imgFilename
        if not (path.isfile(imgSrc) and access(imgSrc, R_OK)):
            logger.error('Error: image not found: {}'.format(imgSrc))
            continue

        # Open the source image and query dimensions
        im = Image.open(imgSrc)
        imgWidth = im.size[0]
        imgHeight = im.size[1]
        imgResized = False

        if not img.get('width'):
            img['width'] = str(imgWidth) + 'px'
        else:
            imgResized = True

        # for lazyload.js
        if instance.settings.get('NIUX2_LAZY_LOAD', False):
            if img.get('class'):
                img['class'] += 'lazy'
            else:
                img['class'] = 'lazy'
            img['data-original'] = img['src']
            del img['src']
            if imgResized:
                newImgWidth = int(_width_attr_reg.sub('', img['width']).strip())
                newImgHeight = imgHeight * newImgWidth / imgWidth
                img['data-width'] = str(newImgWidth) + 'px'
                img['data-height'] = str(newImgHeight) + 'px'
            else:
                img['data-width'] = str(imgWidth) + 'px'
                img['data-height'] = str(imgHeight) + 'px'

    instance._content = soup.decode()

def register():
    signals.content_object_init.connect(parse_images)

