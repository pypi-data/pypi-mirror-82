from warnings import warn

from pl_bolts.transforms.self_supervised import RandomTranslateWithReflect

try:
    from torchvision import transforms
except ImportError:
    warn('You want to use `torchvision` which is not installed yet,'  # pragma: no-cover
         ' install it with `pip install torchvision`.')
    _TORCHVISION_AVAILABLE = False
else:
    _TORCHVISION_AVAILABLE = True


class AMDIMTrainTransformsCIFAR10:
    def __init__(self):
        """
        Transforms applied to AMDIM

        Transforms::

            img_jitter,
            col_jitter,
            rnd_gray,
            transforms.ToTensor(),
            normalize

        Example::

            x = torch.rand(5, 3, 32, 32)

            transform = AMDIMTrainTransformsCIFAR10()
            (view1, view2) = transform(x)

        """
        if not _TORCHVISION_AVAILABLE:
            raise ImportError('You want to use `transforms` from `torchvision` which is not installed yet.')

        # flipping image along vertical axis
        self.flip_lr = transforms.RandomHorizontalFlip(p=0.5)

        # image augmentation functions
        normalize = transforms.Normalize(mean=[x / 255.0 for x in [125.3, 123.0, 113.9]],
                                         std=[x / 255.0 for x in [63.0, 62.1, 66.7]])
        col_jitter = transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.4, 0.2)], p=0.8)
        img_jitter = transforms.RandomApply([RandomTranslateWithReflect(4)], p=0.8)
        rnd_gray = transforms.RandomGrayscale(p=0.25)

        self.transforms = transforms.Compose([
            img_jitter,
            col_jitter,
            rnd_gray,
            transforms.ToTensor(),
            normalize
        ])

    def __call__(self, inp):
        inp = self.flip_lr(inp)
        out1 = self.transforms(inp)
        out2 = self.transforms(inp)
        return out1, out2


class AMDIMEvalTransformsCIFAR10:
    def __init__(self):
        """
        Transforms applied to AMDIM

        Transforms::

            transforms.ToTensor(),
            normalize

        Example::

            x = torch.rand(5, 3, 32, 32)

            transform = AMDIMEvalTransformsCIFAR10()
            (view1, view2) = transform(x)
        """
        if not _TORCHVISION_AVAILABLE:
            raise ImportError('You want to use `transforms` from `torchvision` which is not installed yet.')

        # flipping image along vertical axis
        self.flip_lr = transforms.RandomHorizontalFlip(p=0.5)
        normalize = transforms.Normalize(mean=[x / 255.0 for x in [125.3, 123.0, 113.9]],
                                         std=[x / 255.0 for x in [63.0, 62.1, 66.7]])

        # transform for testing
        self.transforms = transforms.Compose([
            transforms.ToTensor(),
            normalize
        ])

    def __call__(self, inp):
        inp = self.flip_lr(inp)
        out1 = self.transforms(inp)
        return out1


class AMDIMTrainTransformsSTL10:
    def __init__(self, height=64):
        """
        Transforms applied to AMDIM

        Transforms::

            img_jitter,
            col_jitter,
            rnd_gray,
            transforms.ToTensor(),
            normalize

        Example::

            x = torch.rand(5, 3, 64, 64)

            transform = AMDIMTrainTransformsSTL10()
            (view1, view2) = transform(x)
        """
        if not _TORCHVISION_AVAILABLE:
            raise ImportError('You want to use `transforms` from `torchvision` which is not installed yet.')

        # flipping image along vertical axis
        self.flip_lr = transforms.RandomHorizontalFlip(p=0.5)
        normalize = transforms.Normalize(mean=(0.43, 0.42, 0.39), std=(0.27, 0.26, 0.27))
        # image augmentation functions
        col_jitter = transforms.RandomApply([
            transforms.ColorJitter(0.4, 0.4, 0.4, 0.2)], p=0.8)
        rnd_gray = transforms.RandomGrayscale(p=0.25)
        rand_crop = transforms.RandomResizedCrop(height, scale=(0.3, 1.0), ratio=(0.7, 1.4), interpolation=3)

        self.transforms = transforms.Compose([
            rand_crop,
            col_jitter,
            rnd_gray,
            transforms.ToTensor(),
            normalize
        ])

    def __call__(self, inp):
        inp = self.flip_lr(inp)
        out1 = self.transforms(inp)
        out2 = self.transforms(inp)
        return out1, out2


class AMDIMEvalTransformsSTL10(object):
    def __init__(self, height=64):
        """
        Transforms applied to AMDIM

        Transforms::

            transforms.Resize(height + 6, interpolation=3),
            transforms.CenterCrop(height),
            transforms.ToTensor(),
            normalize

        Example::

            x = torch.rand(5, 3, 64, 64)

            transform = AMDIMTrainTransformsSTL10()
            view1 = transform(x)
        """
        if not _TORCHVISION_AVAILABLE:
            raise ImportError('You want to use `transforms` from `torchvision` which is not installed yet.')

        # flipping image along vertical axis
        self.flip_lr = transforms.RandomHorizontalFlip(p=0.5)
        normalize = transforms.Normalize(mean=(0.43, 0.42, 0.39), std=(0.27, 0.26, 0.27))
        transforms.RandomResizedCrop(height, scale=(0.3, 1.0), ratio=(0.7, 1.4), interpolation=3)

        self.transforms = transforms.Compose(
            [
                transforms.Resize(height + 6, interpolation=3),
                transforms.CenterCrop(height),
                transforms.ToTensor(),
                normalize
            ])

    def __call__(self, inp):
        inp = self.flip_lr(inp)
        out1 = self.transforms(inp)
        return out1


class AMDIMTrainTransformsImageNet128(object):
    def __init__(self, height=128):
        """
        Transforms applied to AMDIM

        Transforms::

            img_jitter,
            col_jitter,
            rnd_gray,
            transforms.ToTensor(),
            normalize

        Example::

            x = torch.rand(5, 3, 128, 128)

            transform = AMDIMTrainTransformsSTL10()
            (view1, view2) = transform(x)
        """
        if not _TORCHVISION_AVAILABLE:
            raise ImportError('You want to use `transforms` from `torchvision` which is not installed yet.')

        # image augmentation functions
        self.flip_lr = transforms.RandomHorizontalFlip(p=0.5)
        rand_crop = transforms.RandomResizedCrop(height, scale=(0.3, 1.0), ratio=(0.7, 1.4), interpolation=3)
        col_jitter = transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.4, 0.1)], p=0.8)
        rnd_gray = transforms.RandomGrayscale(p=0.25)
        post_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        self.transforms = transforms.Compose([
            rand_crop,
            col_jitter,
            rnd_gray,
            post_transform
        ])

    def __call__(self, inp):
        inp = self.flip_lr(inp)
        out1 = self.transforms(inp)
        out2 = self.transforms(inp)
        return out1, out2


class AMDIMEvalTransformsImageNet128(object):
    def __init__(self, height=128):
        """
        Transforms applied to AMDIM

        Transforms::

            transforms.Resize(height + 6, interpolation=3),
            transforms.CenterCrop(height),
            transforms.ToTensor(),
            normalize

        Example::

            x = torch.rand(5, 3, 128, 128)

            transform = AMDIMEvalTransformsImageNet128()
            view1 = transform(x)
        """
        if not _TORCHVISION_AVAILABLE:
            raise ImportError('You want to use `transforms` from `torchvision` which is not installed yet.')

        # image augmentation functions
        self.flip_lr = transforms.RandomHorizontalFlip(p=0.5)
        post_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        self.transforms = transforms.Compose([
            transforms.Resize(height + 18, interpolation=3),
            transforms.CenterCrop(height),
            post_transform
        ])

    def __call__(self, inp):
        inp = self.flip_lr(inp)
        out1 = self.transforms(inp)
        return out1
