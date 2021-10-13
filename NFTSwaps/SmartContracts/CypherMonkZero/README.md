# CypherMonkZero NFT
## NFT #1

CypherMonkZero is the first NFT in the CypherMonks series and is an exclusive NFT, meaning it is the only NFT within it's Policy ID. More info is found at [CypherMonks.com/zero](https://cyphermonks.com/zero)

## About the SmartContract

This NFT swap smart contract allows two parties to trustlessly perform a swap of ADA for an NFT. We adapted the source code from [logicalmechanism](https://github.com/logicalmechanism/Token-Sale-Plutus-Contract)'s token sale repository, along with adapting and modifying the Python scripts from the same repo. 

The smart contract works in the following way:
- The NFT owner who looks to swap their NFT for ADA, modifies the smart contract source code to include their Cardano wallet's public key hash and the amount of ADA they are looking to swap for. There are two clearly marked sections in the SwapNFT.hs file to do this. They then compile the smart contract by running `cabal build` and after, `cabal run swapnft` which will spit out a ".plutus" file in the same directory.
- They then send the NFT to smart contract address, with a datum hashed "fingerprint" of the NFT policy ID + name. The swapIN.py script facilitates this, run from a computer with their wallet signing key file and cardano-cli
- They will lastly share their wallet address (the same they obtained their public key hash from), smart contract address, and the smart contract .plutus file (the script) with the person who wants to swap ADA for the NFT. 
- This person will send the agreed upon ADA to the NFT owner's wallet address in a special transaction which also includes a tx-out targeting the smart contract for the NFT they are receiving.
- The smart contract validates this transaction by verifying their tx-out for the NFT also includes a tx-out for the NFT owner at the agreed upon ADA amount, and if so, it validates and both parties receive their swapped assets in that transaction!

## Off-Chain Applications

Following are the applications which support interacting with this smart contract:
- [PythonScripts](https://github.com/MadeWithLovelace/CypherMonks/tree/main/NFTSwaps/OffChainApps/Python): swapIN.py (NFT owner deposits the NFT for a swap), swapOUT.py (other party swaps preset amount of ADA for the NFT) (dependencies: transaction.py)

## Update on Swap

We completed this swap directly (OTC) with the winner of CypherMonk Zero, however this smartcontract is fully tested as working in conjunction with the above mentioned Python scripts.
