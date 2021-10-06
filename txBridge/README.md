# SmartContract Bridge
This is a "bridge" of sorts between an "average user" and a Smart Contract. It allows for a user to simply pay an agreed-upon amount to an agreed-upon Cardano address and the "bridge" scripts will interact with the Smart Contract on the user's behalf. 

This is admittedly a "quick and dirty" technique for bridging interaction between a user and a smart contract, wherein the user does not need to build any specific type of transaction or include datum, etc. They can send an amount to an address and engage the smart contract.

The script being built allows a node operator/smart contract developer to watch an address for a specific type of transaction (amount, amount+address, amount+whitelisted addresses). By watching for these transaction types, the node/smartcontract operator can then engage the smartcontract with the appropriate inputs, outputs, datum, redeemer, etc necessary, from the address the user sent to.

## Use Cases
For simple NFT sales and transfers, for native token distribution (with or without a smart contract), etc.

## Notes
Still in infancy and not complete yet.
