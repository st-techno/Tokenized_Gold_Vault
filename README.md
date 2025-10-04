#  Copyright @ ST Technologies

## Program Code Logic:

vault_api.py: Flask backend with live Chainlink price feed integration for gold using AggregatorV3Interface ABI.

GoldVault.sol: Solidity contract using Chainlink Oracle directly for gold price data, ERC-4626/7943 compliant.

VaultDashboard.jsx and App.jsx: Modular React frontend that interacts with the backend, providing vault deposit/withdrawal and price interface.

Each file follows production naming and structure best practices, with Chainlink details correctly integrated for robust, real-time gold pricing in both backend and contract layers.
