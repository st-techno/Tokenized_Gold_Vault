#  Copyright @ ST Technologies

# Tokenized Vault Smart Contract Solidity ERC-4626 + ERC-7943

Python Backend Overview
The backend acts as a service integrating smart contract interaction via Web3.py, Chainlink oracle feeds for gold valuation, risk logic, and endpoints for frontend communication.

## Key Components:

Smart contract integration for deposits, withdrawals, minting, rebalancing (ERC-4626/7943 methods)

Chainlink price adapter for gold token pricing

Dynamic rebalancing and risk trigger logic

Logging and backtesting utilities

## Program Code Logic:

vault_api.py: Flask backend with live Chainlink price feed integration for gold using AggregatorV3Interface ABI.

GoldVault.sol: Solidity contract using Chainlink Oracle directly for gold price data, ERC-4626/7943 compliant.

VaultDashboard.jsx and App.jsx: Modular React frontend that interacts with the backend, providing vault deposit/withdrawal and price interface.

Each file follows production naming and structure best practices, with Chainlink details correctly integrated for robust, real-time gold pricing in both backend and contract layers.
