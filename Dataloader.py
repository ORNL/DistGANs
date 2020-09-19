# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:22:47 2020

@authors: Andrey Prokpenko (e-mail: prokopenkoav@ornl.gov)
        : Debangshu Mukherjee (e-mail: mukherjeed@ornl.gov)
        : Massimiliano Lupo Pasini (e-mail: lupopasinim@ornl.gov)
        : Nouamane Laanait (e-mail: laanaitn@ornl.gov)
        : Simona Perotto (e-mail: simona.perotto@polimi.it)
        : Vitaliy Starchenko  (e-mail: starchenkov@ornl.gov)
        : Vittorio Gabbi (e-mail: vittorio.gabbi@mail.polimi.it) 
"""


from torchvision import transforms, datasets
import os


def mnist_data(rand_rotation=False, max_degree=90):
    if rand_rotation == True:
        compose = transforms.Compose(
            [
                transforms.Resize(64),
                transforms.RandomRotation(max_degree),
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,)),
            ]
        )

    else:
        compose = transforms.Compose(
            [
                transforms.Resize(64),
                transforms.ToTensor(),
                transforms.Normalize((0.5,), (0.5,)),
            ]
        )
    out_dir = '{}/dataset'.format(os.getcwd())
    return datasets.MNIST(
        root=out_dir, train=True, transform=compose, download=True
    )


def cifar10_data():
    compose = transforms.Compose(
        [
            transforms.Resize(64),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    out_dir = '{}/dataset'.format(os.getcwd())
    return datasets.CIFAR10(
        root=out_dir, train=True, transform=compose, download=True
    )


def cifar100_data():
    compose = transforms.Compose(
        [
            transforms.Resize(64),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    out_dir = '{}/dataset'.format(os.getcwd())
    return datasets.CIFAR100(
        root=out_dir, train=True, transform=compose, download=True
    )


PREPROCESS = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        ),
    ]
)
