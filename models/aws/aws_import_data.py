from aws_client import aws_client
from PIL import Image
import numpy as np
import io

s3_client = aws_client()
class Data:
    def __init__ (self, image_size, label, num_instances):
        self.bucket_name = 'gashissdb-dataset'
        self.image_size = image_size
        self.label = label
        self.keys = []
        self.data = []
        self.target = None
        self.get_data(num_instances)
        self.download_images()
        
    
    def get_data (self, num_instances = 30):
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate (Bucket = self.bucket_name, Prefix = f'{self.image_size}/{self.label}')
        count = 0
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    self.keys.append (obj['Key'])
                    count+=1 
                    if count > num_instances:
                        return
                    
    def download_images (self):
        for key in self.keys:
            s3_object = s3_client.get_object (Bucket = self.bucket_name, Key = key)
            image_data = s3_object['Body'].read()
            image = Image.open (io.BytesIO(image_data)).convert('RGB')
            image_array = np.array (image)[:, :, :-1]
            # Add the third color channel, the 1st channel was taken
            image_array = np.dstack((image_array, image_array[:, :, 0])) 
            self.data.append (image_array)
        
        self.data = np.array (self.data)
        
        if self.label == 'Normal':
            self.target = np.zeros (self.data.shape[0]).astype ('int')
        else:
            self.target = np.ones (self.data.shape[0]).astype ('int')

    