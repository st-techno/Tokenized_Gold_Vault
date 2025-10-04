// src/components/VaultDashboard.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function VaultDashboard() {
  const [price, setPrice] = useState(0);
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('/price').then(res => setPrice(res.data.gold_price));
  }, []);

  const handleDeposit = async () => {
    const res = await axios.post('/deposit', { address: 'USER_ADDRESS', amount });
    setMessage(`Deposit tx: ${res.data.tx_hash}`);
  };

  const handleWithdraw = async () => {
    const res = await axios.post('/withdraw', { address: 'USER_ADDRESS', shares: amount });
    setMessage(`Withdraw tx: ${res.data.tx_hash}`);
  };

  return (
    <div>
      <h2>Gold Vault Dashboard</h2>
      <p>Current Gold Price: {price}</p>
      <input
        value={amount}
        onChange={e => setAmount(e.target.value)}
        placeholder="Amount"
      />
      <button onClick={handleDeposit}>Deposit</button>
      <button onClick={handleWithdraw}>Withdraw</button>
      <p>{message}</p>
    </div>
  );
}

export default VaultDashboard;
