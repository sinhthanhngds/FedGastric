from models.aws_import_data import Data
import numpy as np
from PIL import Image
import torch
from torchvision.transforms import transforms
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Data_Loader:
    def __init__ (self, normal = 500, abnormal = 500,  image_size = 120):
        self.abnormal = Data (image_size, 'Abnormal', abnormal)
        self.normal = Data (image_size, 'Normal', normal)
        self.X = np.concatenate ([self.normal.data, self.abnormal.data])
        self.y = np.concatenate ([self.normal.target, self.abnormal.target])

        self.transform = transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(58),
            transforms.ToTensor(),
            transforms.Normalize (mean = [0.485, 0.456, 0.406],
                                  std = [0.229, 0.224, 0.225])
        ])
    def preprocessing (self):

        processed_images = []
        for img in self.X:
            img = Image.fromarray((img / 255).astype(np.uint8))
            img = self.transform(img)
            processed_images.append (img)

        return torch.stack(processed_images)
    

    def dataloader (self):
        batch_size = 32
        images_tensor = self.preprocessing()
        labels_tensor = torch.tensor (self.y, dtype = torch.float32).unsqueeze(1)
    
        X_train, X_val, y_train, y_val = train_test_split (images_tensor, labels_tensor, test_size = 0.2)
        train_dataset = TensorDataset (X_train, y_train)
        val_dataset = TensorDataset (X_val, y_val)
    
        train_loader = DataLoader (train_dataset, batch_size = batch_size, shuffle = True)
        val_loader = DataLoader (val_dataset, batch_size = batch_size, shuffle = False)
    
        return train_loader, val_loader
    