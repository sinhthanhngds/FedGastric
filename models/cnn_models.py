import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset, random_split
import numpy as np
from torchvision import models

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def resnet18 (weights='DEFAULT'):
    resnet18 = models.resnet18 (weights = weights).to(device)
    
    for param in resnet18.parameters():
        param.requires_grad = False
    resnet18.fc = nn.Sequential (
    nn.Linear(in_features = 512, out_features = 256, bias = True),
    nn.Dropout(p = 0.5),
    nn.Linear(in_features = 256, out_features = 1, bias = True),
    nn.Sigmoid()
    )
    
    for param in resnet18.fc.parameters():
        param.requires_grad = True
    
    return resnet18

def vgg16(weights = 'DEFAULT'):
    model = models.vgg16(weights='IMAGENET1K_V1')

# Freeze the parameters of the base model
    for param in model.features.parameters():
        param.requires_grad = False
    
# Modify the classifier part for binary classification
    model.classifier[6] = nn.Sequential(
        nn.Linear(model.classifier[6].in_features, 512),
        nn.ReLU(),
        nn.Dropout(p=0.5),
        nn.Linear(512, 1),
        nn.Sigmoid()
    )

    return model

    
def vgg19 (weights=None):
    vgg19 = models.vgg19 (weights=weights).to(device)
    
    for param in vgg19.parameters():
        param.requires_grad = False
        
    vgg19.classifier = nn.Sequential (
        nn.Linear(25088, 4096),        
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.5),
        nn.Linear(4096, 4096),       
        nn.ReLU(inplace=True),
        nn.Dropout(p=0.5),
        nn.Linear(4096, 1),
        nn.Sigmoid()          
    )
    for param in vgg19.classifier.parameters():
        param.requires_grad = True
    
    return vgg19