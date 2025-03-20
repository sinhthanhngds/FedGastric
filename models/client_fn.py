import flwr as fl
import argparse

from cnn_models import resnet18, vgg16
from flower_client import FlowerClient
from local_data import LocalData

# Parse command line argument to get client ID
parser = argparse.ArgumentParser(description="Flower Client")
parser.add_argument("--cid", type=str, help="Client ID")
args = parser.parse_args()

# Function to select dataset based on client ID
def get_dataset_for_client(cid: str):
    if cid == "0":
        return LocalData('clinic_0').dataset()
    elif cid == "1":
        return LocalData('clinic_1').dataset()
    elif cid == "2":
        return LocalData('clinic_2').dataset()
    elif cid == "3":
        return LocalData('clinic_3').dataset()
    else:
        raise ValueError(f"Unknown client id: {cid}")

#client function
def client_fn(cid: str):
    print(f"Loading dataset for client {cid}")
    train_loader, val_loader = get_dataset_for_client(cid)

    # Create the model and Flower client
    model = resnet18(weights='DEFAULT')
    client = FlowerClient(model, train_loader, val_loader)
    return client.to_client()

# Start the client with the provided CID
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Flower Client")
    parser.add_argument("--cid", type=str, required=True, help="Client ID")
    args = parser.parse_args()

    # Start the client using the new start_client() method
    fl.client.start_client(
        server_address="localhost:8080", 
        client=client_fn(args.cid)  # Make sure to call the client_fn with the CID
    )

