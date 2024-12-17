# Market Direction API Integration

This open-source project demonstrates how to integrate with the Market Direction API endpoint to retrieve the market direction indicator (Bull or Bear) based on trading data. The project serves as a reference implementation for developers looking to integrate the Bull/Bear market indicator into their applications.

# Table of Contents
1. [Getting Started](#getting-started)
2. [Docker](#docker)
3. [Endpoint Specification](#endpoint-specification)
4. [How It Works](#how-it-works)

## Overview

The `get_market_direction` function in this project retrieves market direction indicators for trading pairs like `BTC/USD` and `SOL/USD` based on intraday trading data. The data is sent to the Market Direction API, which uses the trading data to generate a market direction (Bull or Bear). The response from the API is then parsed and processed to display the market direction for each trading pair.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.


## Getting Started
1. **Clone the repository**
  ```bash
  git clone https://github.com/MarketRaker/marketraker-direction-sdk
  ```
2. **Set up the Python environment**  
  Ensure you have **Python 3.13** installed. It is recommended to use a virtual environment for dependency management:
  - Create a virtual environment:
    ```bash
    python -m venv venv
    ```
  - Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3. **Install dependancies**
  Execute the following command in the terminal:
  ```bash
  pip install -r requirements.txt
  ```
4. **Configure environmental variables (`.env`)**
  - Enter your **Application ID** and **Signing ID**. These can be found at the official MarketRaker website.  
    Route: My Profile -> Set Up Integration -> API URL -> MarketRaker API

5. **Run the FastAPI Server**
  ```bash
  uvicorn app.main:app --reload --host 127.0.0.1 --port 5005
  ```

### Docker

This repository provides a **Dockerfile** to easily deploy the **MarketRaker Market Direction Integration** backend. The Dockerfile ensures that the backend service is containerized and can be run consistently in any environment with Docker support.

## Docker Setup Instructions

Follow the steps below to build and run the **MarketRaker Market Direction Integration** backend inside a Docker container.

### Prerequisites

Ensure that you have the following tools installed on your system:

- **Docker**: You can download Docker from the [official website](https://www.docker.com/get-started).
- **Configure Environment Variables**: Before building the Docker image, ensure that you have a `.env` file in the root of the repository with the appropriate environment variables for your trading bot and API keys. The `.env` file should contain sensitive information such as API keys for Binance and Bybit.

### Setup
- **Build the Docker Image**:
  Run the following command to build the Docker image from the `Dockerfile`:
  ```bash
  docker build -t trading-bot-example-code .
  ```
  This will:
  - Set up a Python 3.13 slim container.
  - Install dependencies from `requirements.txt`.
  - Copy the `.env` file and application code to the container.
  - Expose port `5005` (default backend port).

- **Run the Docker Container**:
  Once the image is built, you can run the container with the following command:
  ```bash
  docker run -d -p 5005:5005 trading-bot-example-code
  ```
  This will:
  - Run the container in the background (-d).
  - Forward the backend's port 5005 to your local machine's port 5005 (-p 5005:5005).

Your FastAPI backend will now be accessible at http://localhost:5005.

**Note:**  
For testing, Postman can interact with your FastAPI server on localhost, but because localhost is not a public IP address, it cannot be registered as a webhook URL on the MarketRaker website. MarketRaker needs a publicly accessible endpoint to send indicators to your application.  
To make your application accessible publicly, you would need to deploy it to a server with a public IP address (e.g., on a cloud service like AWS, Azure, or Heroku)

### MarketRaker Endpoint Specification:

- **Method:** POST
- **URL:** `/v1/trading_pairs/market_direction`
- **Credit Cost:** 1 credit per request

## How It Works

### 1. Request Authentication

The function constructs a request URL to interact with the `/v1/trading_pairs/market_direction` endpoint of the Market Direction API. For authentication, it adds a timestamp and a signature to the request headers. The signature is generated using the application's signing key, ensuring the integrity and security of the request.

### 2. Preparing Trading Data

The function retrieves intraday trading data from CSV files. In this example the following files are used:

- `BTC_USD_Intraday_Data.csv`
- `SOL_USD_Intraday_Data.csv`

The data is extracted and organized into a dictionary, formatted according to the API requirements, and is ready to be sent in the request.

The CSV files must contain at least 20 data points, with the following columns:

- `open_price`
- `high`
- `low`
- `close`
- `volume`

Example CSV format:
```csv
"id","currency","open_time","open_price","high","low","close","volume"
1,"BTC/USD","2023-08-19 17:00:00","26253.3","26253.31","26072.29","26086.9","1368.5996"
2,"BTC/USD","2023-08-19 18:00:00","26086.9","26138","26026.96","26126.44","972.9137"
...
```

## 3. Sending the Request

Once the trading data is prepared and the authentication headers are set, the request is sent to the Market Direction API via the `POST` method.  
This example can be executed using a `GET` request on `localhost:5005/marketraker/generate_market_indicator` .  
The request contains:

- **X-Signature**: A signature created using the timestamp and application ID, which authenticates the request and ensures its integrity.
- **X-Signature-Timestamp**: The timestamp when the request is made, used for validating the request's freshness.
- **X-Application-Id**: Your unique application ID provided by MarketRaker.
- **Content-Type**: Specifies that the request body is formatted as JSON.

These headers are crucial for ensuring secure communication with the API and validating the authenticity of the request.

## 4. Handling the Response

After the request is sent, the function processes the response from the API:

- **Success**: If the request is successful and contains records, the market direction for each trading pair is printed. The possible market directions are:
  - **Bull**: Indicates a bullish market.
  - **Bear**: Indicates a bearish market.

- **Error**: If the request fails or returns an error, the error message is printed to help troubleshoot the issue.

### Example Output

```plaintext
BTC/USD - Market Direction: Bull
SOL/USD - Market Direction: Bear