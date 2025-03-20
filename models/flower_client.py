import flwr as fl
import torch
from train_client import train_local_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, train_loader, val_loader):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.val_loss = None
        self.val_accuracy = None

    def get_parameters(self, config=None):  # Added config to the method signature
        # Extract model parameters
        params = [val.cpu().numpy() for val in self.model.state_dict().values()]
        return params

    def set_parameters(self, parameters):
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.model.load_state_dict(state_dict, strict=False)

    def fit(self, parameters, config=None):
        # Set model parameters from the server
        self.set_parameters(parameters)

        # Train the model locally (includes validation)
        self.model, self.val_loss, self.val_accuracy = train_local_model(
            self.model, self.train_loader, self.val_loader
        )

        # Return updated model parameters
        return self.get_parameters(), len(self.train_loader.dataset), {}

    def evaluate(self, parameters, config=None):
        # Set model parameters from the server
        self.set_parameters(parameters)

        # Return the validation metrics obtained during the fit() call
        if self.val_loss is not None and self.val_accuracy is not None:
            return float(self.val_loss), len(self.val_loader.dataset), {"accuracy": float(self.val_accuracy)}
        else:
            # If fit wasn't run before evaluate
            return 0.0, len(self.val_loader.dataset), {"accuracy": 0.0}
