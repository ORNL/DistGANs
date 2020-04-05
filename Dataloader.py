# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:22:47 2020

@author: claud
"""
# DATA LOADER MNIST
import torch
from torch import nn, optim
from torch.autograd.variable import Variable
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
#from utils import Logger

def mnist_data():
    compose = transform = transforms.Compose([transforms.ToTensor(),
                                              transforms.Normalize((0.5,), (0.5,))
                                              ])
    out_dir = './dataset'
    return datasets.MNIST(root=out_dir, train=True, transform=compose, download=True)

def cifar10_data():
    compose = transform = transforms.Compose([transforms.ToTensor(), 
                                              transforms.Normalize((0.5,), (0.5,))
                                              ])
    out_dir = './dataset'
    return datasets.CIFAR10(root=out_dir, train=True, transform=compose, download=True)