import torch
import torch.optim as optim
from tqdm import tqdm  # Import tqdm for the progress bar
from local_data import LocalData
from cnn_models import vgg16

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def calculate_accuracy(outputs, labels, threshold=0.5):
    preds = (outputs > threshold).float()
    correct = (preds == labels).float().sum()
    accuracy = correct / labels.size(0)
    return accuracy

def train_local_model(model, train_loader, val_loader, num_epochs=10):
    criterion = torch.nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        running_accuracy = 0.0
        total_train = 0
        threshold = 0.5

        for images, labels in train_loader:
            optimizer.zero_grad()
            images, labels = images.to(device), labels.to(device)
            outputs = model(images).squeeze(1)

            # Calculate loss
            loss = criterion(outputs, labels.float())
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            running_accuracy += calculate_accuracy(outputs, labels, threshold)
            total_train += 1


        # Validation phase
        model.eval()
        val_loss = 0.0
        val_accuracy = 0.0
        total_val = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images).squeeze(1)
                loss = criterion(outputs, labels.float())
                val_loss += loss.item()
                val_accuracy += calculate_accuracy(outputs, labels, threshold)
                total_val += 1

        avg_val_loss = val_loss / total_val
        avg_val_accuracy = val_accuracy / total_val
        print (f"Epoch {epoch + 1}/{num_epochs}:\ntrain_loss: {running_loss / total_train}, train_accuracy: {running_accuracy / total_train}\nValidation Loss: {avg_val_loss:.4f}, Validation Accuracy: {avg_val_accuracy:.4f}")
    
    return model, avg_val_loss, avg_val_accuracy
