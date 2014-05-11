# -*- coding: UTF-8 -*-
"""
This pelican plugin is inspired by the plugin [better figures and images](https://github.com/getpelican/pelican-plugins/tree/master/better_figures_and_images) and is intended to be used with the theme [niu-x2-sidebar](https://github.com/mawenbao/niu-x2-sidebar).

To all the img tags in the html document, this plugin do these things:

* add class `lazy`.
* move attribute `src` to attribute `data-original`.
* add attributes:
    1. data-height: real height of the image file, in px.
    2. width and data-width: real width of the image file, in px.

Requirements

* pip install pillow beautifulsoup4
"""

from os import path, access, R_OK
from pelican import signals
from bs4 import BeautifulSoup
from PIL import Image
import logging

logger = logging.getLogger(__name__)

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

        if img.get('alt') and img['alt'] == img['src']:
            img['alt'] = ''

        if not img.get('width'):
            img['width'] = str(imgWidth) + 'px'

        # for lazyload.js
        if 'NIUX2_LAZY_LOAD' in instance.settings and instance.settings['NIUX2_LAZY_LOAD']:
            if img.get('class'):
                img['class'] += 'lazy'
            else:
                img['class'] = 'lazy'
            img['data-original'] = img['src']
            del img['src']
            img['data-width'] = str(imgWidth) + 'px'
            img['data-height'] = str(imgHeight) + 'px'

    instance._content = soup.decode()

def register():
    signals.content_object_init.connect(parse_images)

