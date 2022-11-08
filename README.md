# Edge Financial Transactions Simulator

This is a simple simulation of customer transactions from edge devices (like credit card readers or POS systems) for Mezmo Pipeline Workshop.

## Requirements
* Docker

## Build the Docker image
```cmd
docker build -t transaction-device-sim .
```

## Define environment varialbes prior
* `KEY`: Pipeline key to use
* `NUMBER_DEVICES`: Number of devices to simulate

Ex:
```cmd
export KEY="s_YOUR_KEY"
export NUMBER_DEVICES=25
```

## Run
```cmd
docker run -e KEY=${KEY} -e NUMBER_DEVICES=${NUMBER_DEVICES} -it transaction-device-sim
```
