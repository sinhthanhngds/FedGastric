from PIL import Image
import numpy as np
from torchvision import datasets, transforms
from torchvision.transforms import transforms
from torch.utils.data import random_split, DataLoader, Subset


class LocalData:
    def __init__ (self, clinic_id):
        self.clinic_id = clinic_id
        self.path = f'../120_dataset/{clinic_id}/'
        
    def dataset (self):
        transform = transforms.Compose([
        transforms.Resize((128, 128)),  # Resize images to a fixed size (optional)
        transforms.ToTensor(),          # Convert images to PyTorch tensors
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]) 
        ])

# Load the dataset from the train folder
        train_dataset = datasets.ImageFolder(root=f'{self.path}', transform=transform)
        subset_indices = list(range(8100,8400))    #remove for final code
        train_dataset = Subset (train_dataset, subset_indices) #remove for final code

        train_size = int(0.8*len(train_dataset))
        val_size = len(train_dataset)-train_size

        train_subset, val_subset = random_split(train_dataset, [train_size, val_size])
        train_loader = DataLoader(train_subset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_subset, batch_size=32, shuffle=False)

        print (f'loading {self.clinic_id}')
        return train_loader, val_loader