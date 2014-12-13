from urllib2 import urlopen, HTTPError
from hashlib import sha384
from os.path import isfile, splitext, exists, join
from os import makedirs

try:
    from PIL import Image, ImageEnhance
except ImportError:
    raise RuntimeError('Image module of PIL needs to be installed')


class ImageUtilis(object):
    """
    Image Usefull utilitis for crolling and adding watermak to protect your images and ...

    Author: Hamid FzM
    Email: hamidfzm@gmail.com

    Usages:
    Add watermark to your image, you can use this functions in your jinja templates
        Samples:
        1:
            WatermarkImage(image_address, mark_address, 'tile', 0.5)
        2:
            WatermarkImage(image_address, mark_address, 'scale', 1.0)
        3:
            WatermarkImage(image_address, mark_address, (100, 100), 0.5)

        Use cache_url to download images to your server and cache theme. Remember to address MEDIA_FOLDER in you config file.
        Function will return file name in your server and you can use it whereever you want.

        Sample:
        file-name = cache_url('http://online-behavior.com/sites/default/files/imagecache/Content/articles/sampled-data-analytics.jpg')

    """
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
            self.cache = None
        else:
            self.app = None

    def init_app(self, app):
        self.app = app

        if not self.app.config.get('MEDIA_FOLDER', None):
            raise RuntimeError('You\'re using the flask-thumbnail app '
                               'without having set the required MEDIA_FOLDER setting.')

        self.cache = join(self.app.config['MEDIA_FOLDER'], 'image_cache')
        app.config.setdefault('MEDIA_URL', '/')


        app.jinja_env.globals['CacheUrlImage'] = self.cache_url
        app.jinja_env.globals['WatermarkImage'] = self.make_watermark

    def cache_url(self, url):
        """
        Cache images from url
        """
	if not url:
	    return None

        fdir = self.cache
        name = sha384(url).hexdigest() + splitext(url)[1]
        fname = join(fdir, name)

        if not isfile(fname):
            if not exists(fdir):
                makedirs(fdir)
            try:
                img = urlopen(url)
                output = open(fname, 'wb+')
                output.write(img.read())
                output.close()
            except HTTPError:
                pass
        return fname

    @staticmethod
    def reduce_opacity(im, opacity):
        """Returns an image with reduced opacity."""
        assert 0 <= opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im

    def make_watermark(self, im, mark, position, opacity=1):
        """Adds a watermark to an image."""
        if opacity < 1:
            mark = self.reduce_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        if position == 'tile':
            for y in range(0, im.size[1], mark.size[1]):
                for x in range(0, im.size[0], mark.size[0]):
                    layer.paste(mark, (x, y))
        elif position == 'scale':
            # scale, but preserve the aspect ratio
            ratio = min(
                float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
            w = int(mark.size[0] * ratio)
            h = int(mark.size[1] * ratio)
            mark = mark.resize((w, h))
            layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
        else:
            layer.paste(mark, position)
        # composite the watermark with the layer
        return Image.composite(layer, im, layer)

    """
    Add watermark to your image
    Samples:
    1:
        watermark(image_address, mark_address, 'tile', 0.5)
    2:
        watermark(image_address, mark_address, 'scale', 1.0)
    3:
        watermark(image_address, mark_address, (100, 100), 0.5)
    """
    def watermark(self, image_address, mark_address, *args, **kwargs):
        im = Image.open(image_address)
        mark = Image.open(mark_address)
        self.make_watermark(im, mark, *args, **kwargs).save(image_address)
