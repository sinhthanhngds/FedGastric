import flwr as fl

strategy = fl.server.strategy.FedAvg()

# Start the server
if __name__ == "__main__":
    fl.server.start_server(
        server_address="localhost:8080",  
        config=fl.server.ServerConfig(num_rounds=5),  
        strategy=strategy,
    )

    #global_weights = strategy.get_parameters()['weights']
    #torch.save(global_weights, "global_model.pth")

