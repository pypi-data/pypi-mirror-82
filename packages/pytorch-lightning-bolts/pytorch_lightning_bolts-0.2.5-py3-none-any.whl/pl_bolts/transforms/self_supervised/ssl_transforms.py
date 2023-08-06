from warnings import warn

import numpy as np
import torch.nn.functional as F

try:
    from PIL import Image
except ImportError:
    warn('You want to use `Pillow` which is not installed yet,'  # pragma: no-cover
         ' install it with `pip install Pillow`.')
    _PIL_AVAILABLE = False
else:
    _PIL_AVAILABLE = True


class RandomTranslateWithReflect:
    '''
    Translate image randomly
    Translate vertically and horizontally by n pixels where
    n is integer drawn uniformly independently for each axis
    from [-max_translation, max_translation].
    Fill the uncovered blank area with reflect padding.
    '''

    def __init__(self, max_translation):
        self.max_translation = max_translation

    def __call__(self, old_image):
        if not _PIL_AVAILABLE:
            raise ImportError('You want to use `Pillow` which is not installed yet,'
                              ' install it with `pip install Pillow`.')
        xtranslation, ytranslation = np.random.randint(-self.max_translation,
                                                       self.max_translation + 1,
                                                       size=2)
        xpad, ypad = abs(xtranslation), abs(ytranslation)
        xsize, ysize = old_image.size

        flipped_lr = old_image.transpose(Image.FLIP_LEFT_RIGHT)
        flipped_tb = old_image.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_both = old_image.transpose(Image.ROTATE_180)

        new_image = Image.new("RGB", (xsize + 2 * xpad, ysize + 2 * ypad))

        new_image.paste(old_image, (xpad, ypad))

        new_image.paste(flipped_lr, (xpad + xsize - 1, ypad))
        new_image.paste(flipped_lr, (xpad - xsize + 1, ypad))

        new_image.paste(flipped_tb, (xpad, ypad + ysize - 1))
        new_image.paste(flipped_tb, (xpad, ypad - ysize + 1))

        new_image.paste(flipped_both, (xpad - xsize + 1, ypad - ysize + 1))
        new_image.paste(flipped_both, (xpad + xsize - 1, ypad - ysize + 1))
        new_image.paste(flipped_both, (xpad - xsize + 1, ypad + ysize - 1))
        new_image.paste(flipped_both, (xpad + xsize - 1, ypad + ysize - 1))

        new_image = new_image.crop((xpad - xtranslation,
                                    ypad - ytranslation,
                                    xpad + xsize - xtranslation,
                                    ypad + ysize - ytranslation))
        return new_image


class Patchify(object):

    def __init__(self, patch_size, overlap_size):
        self.patch_size = patch_size
        self.overlap_size = self.patch_size - overlap_size

    def __call__(self, x):
        x = x.unsqueeze(0)
        b, c, h, w = x.size()

        # patch up the images
        # (b, c, h, w) -> (b, c*patch_size, L)
        x = F.unfold(x, kernel_size=self.patch_size, stride=self.overlap_size)

        # (b, c*patch_size, L) -> (b, nb_patches, width, height)
        x = x.transpose(2, 1).contiguous().view(b, -1, self.patch_size, self.patch_size)

        # reshape to have (b x patches, c, h, w)
        x = x.view(-1, c, self.patch_size, self.patch_size)

        x = x.squeeze(0)

        return x
