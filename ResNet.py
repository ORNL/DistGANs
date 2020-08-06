from ResBlock import ResBlock2d, ResBlock2d32Pix, FastResBlock2dDownsample
from ResNet_utils import Lambda, NormalizeLayer, Conv2dEx, LinearEx
from torch import nn
from abc import ABC, abstractmethod

FMAP_G = 64
FMAP_D = 64
FMAP_G_INIT_32_FCTR = 1
FMAP_G_INIT_64_FCTR = 4
RES_FEATURE_SPACE = 4
FMAP_SAMPLES = 3
RES_INIT = 4


class GAN(nn.Module, ABC):
    """Base GAN for all non-progressive architectures."""

    def __init__(self, res, n_classes):
        super(GAN, self).__init__()
        self._res = res
        self.n_classes = n_classes

    def most_parameters(self, recurse=True, excluded_params: list = []):
        """torch.nn.Module.parameters() generator method but with the option to exclude specified parameters."""
        for name, params in self.named_parameters(recurse=recurse):
            if name not in excluded_params:
                yield params

    @property
    def res(self):
        return self._res

    @res.setter
    def res(self, new_res):
        message = f'GAN().res cannot be changed, as {self.__class__.__name__} only permits one resolution: {self._res}.'
        raise AttributeError(message)

    @abstractmethod
    def forward(self, x):
        raise NotImplementedError(
            'Can only call `forward` on valid subclasses.'
        )


class Generator64PixResnet(GAN):
    """ResNet GAN Generator for 64-pixel samples with optional class-conditioning (Mirza & Osindero, 2014).
  """

    def __init__(
        self,
        len_latent=128,
        fmap=FMAP_G,
        upsampler=nn.Upsample(scale_factor=2, mode='nearest'),
        blur_type=None,
        nl=nn.ReLU(),
        num_classes=0,
        equalized_lr=False,
    ):
        super(Generator64PixResnet, self).__init__(64)

        self.len_latent = len_latent
        self.num_classes = num_classes

        self.equalized_lr = equalized_lr

        _fmap_init_64 = len_latent * FMAP_G_INIT_64_FCTR
        self.generator_model = nn.Sequential(
            Lambda(lambda x: x.view(-1, len_latent + num_classes)),
            LinearEx(
                nin_feat=len_latent + num_classes,
                nout_feat=_fmap_init_64 * RES_INIT ** 2,
                init='Xavier',
                equalized_lr=equalized_lr,
            ),
            Lambda(lambda x: x.view(-1, _fmap_init_64, RES_INIT, RES_INIT)),
            ResBlock2d(
                ni=_fmap_init_64,
                nf=8 * fmap,
                ks=3,
                norm_type='BatchNorm',
                upsampler=upsampler,
                init='He',
                nl=nl,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            ResBlock2d(
                ni=8 * fmap,
                nf=4 * fmap,
                ks=3,
                norm_type='BatchNorm',
                upsampler=upsampler,
                init='He',
                nl=nl,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            ResBlock2d(
                ni=4 * fmap,
                nf=2 * fmap,
                ks=3,
                norm_type='BatchNorm',
                upsampler=upsampler,
                init='He',
                nl=nl,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            ResBlock2d(
                ni=2 * fmap,
                nf=1 * fmap,
                ks=3,
                norm_type='BatchNorm',
                upsampler=upsampler,
                init='He',
                nl=nl,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            NormalizeLayer('BatchNorm', ni=1 * fmap),
            nl,
            Conv2dEx(
                ni=1 * fmap,
                nf=FMAP_SAMPLES,
                ks=3,
                stride=1,
                padding=1,
                init='He',
                equalized_lr=equalized_lr,
            ),
            nn.Tanh(),
        )

    def forward(self, x):
        return self.generator_model(x)

    def to(self, device):
        super(Generator64PixResnet, self).to(device)
        self.device = device


class Discriminator64PixResnet(GAN):
    """ResNet GAN Discriminator for 64-pixel samples with optional class-conditioning (Mirza & Osindero, 2014).
  """

    def __init__(
        self,
        fmap=FMAP_D,
        pooler=nn.AvgPool2d(kernel_size=2, stride=2),
        blur_type=None,
        nl=nn.ReLU(),
        num_classes=0,
        equalized_lr=False,
    ):
        super(Discriminator64PixResnet, self).__init__(64)

        self.num_classes = num_classes
        self.equalized_lr = equalized_lr

        self.view1 = Lambda(
            lambda x: x.view(
                -1, FMAP_SAMPLES + num_classes, self.res, self.res
            )
        )
        self.conv1 = Conv2dEx(
            ni=FMAP_SAMPLES + num_classes,
            nf=1 * fmap,
            ks=3,
            stride=1,
            padding=1,
            init='Xavier',
            equalized_lr=equalized_lr,
        )
        self.resblocks = nn.Sequential(
            ResBlock2d(
                ni=1 * fmap,
                nf=2 * fmap,
                ks=3,
                norm_type='LayerNorm',
                pooler=pooler,
                init='He',
                nl=nl,
                res=self.res // 1,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            ResBlock2d(
                ni=2 * fmap,
                nf=4 * fmap,
                ks=3,
                norm_type='LayerNorm',
                pooler=pooler,
                init='He',
                nl=nl,
                res=self.res // 2,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            ResBlock2d(
                ni=4 * fmap,
                nf=8 * fmap,
                ks=3,
                norm_type='LayerNorm',
                pooler=pooler,
                init='He',
                nl=nl,
                res=self.res // 4,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            ResBlock2d(
                ni=8 * fmap,
                nf=8 * fmap,
                ks=3,
                norm_type='LayerNorm',
                pooler=pooler,
                init='He',
                nl=nl,
                res=self.res // 8,
                equalized_lr=equalized_lr,
                blur_type=blur_type,
            ),
            Lambda(
                lambda x: x.view(-1, RES_FEATURE_SPACE ** 2 * 8 * fmap)
            )  # final feature space
            # NormalizeLayer( 'LayerNorm', ni = fmap, res = 1 )
        )
        self.linear1 = LinearEx(
            nin_feat=RES_FEATURE_SPACE ** 2 * 8 * fmap,
            nout_feat=1,
            init='Xavier',
            equalized_lr=equalized_lr,
        )

    def forward(self, x):
        return (self.linear1(self.resblocks(self.conv1(self.view1(x))))).view(
            -1
        )

    def to(self, device):
        super(Discriminator64PixResnet, self).to(device)
        self.device = device
