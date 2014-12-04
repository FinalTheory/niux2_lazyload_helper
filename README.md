# niu-x2 lazy load helper

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

**NOTE THAT**, you have to wirte your a function called `MY_IMG_URL2PATH_FUNC`, which can convert value of the image src attribute to the image's absolute path. e.g.

    import os
    def my_img_url_2_path(url):
        '''convert //static.atime.me/images/a/b.jpg to /path/to/a/b.jpg'
        if not url.startswith('//static.atime.me'):
            print("ignore " + url)
            return ''
        return os.path.abspath(os.path.join('content', 'static', url[1 + url.index('/', 2):]))
    MY_IMG_URL2PATH_FUNC = my_img_url_2_path
    
## Requirements

    pip install pillow beautifulsoup4

