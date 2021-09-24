# CypherMonks - NFT Swaps

This is where we will share the Cardano smart contract source and compiled code for CypherMonk NFT swaps for transparency, verification and education. Note: The code within this repository is not guaranteed in any way and if you clone or use any code within this repository you do so at your own risk.

## About the Folders and Files

### OnChainSmartContracts
Each compiled smart contract (aka Cardano Plutus script) and accompanying source code is in a subfolder of OnChainSmartContracts matching the name of the NFT. The compiled smart contract for the NFT swap is within this NFT-named folder, along with a folder called SmartContractSourceCode, which contains the Haskell source code, app, cabal.project, and .cabal files and folders for verification and review.

### OffChainApplications

This folder contains supporting applications or scripts to be used "off-chain" to interact with On-Chain NFT-swap smart contracts. Each NFT folder contains a README.md file that lists the applications which can be used for that particular smart contract.

## Using Applications

At this time we simply have two Python scripts, originally adapted from [logicalmechanism](https://github.com/logicalmechanism/Token-Sale-Plutus-Contract). These have been modified, updated, and tested carefully but should still be considered "Use at your own risk" and the source code should be verified before using. 

We will be adding additional applications, as well as compiled binaries for both the Python scripts and any future applications, but the source code will always be open and available.

To use an application with a smart contract, you'll simply need the smart contract itself (the .plutus script file) and the application for the purpose. For example, if you are a buyer, you'll need the appropriate smart contract .plutus file and for using Python, both the buyNFT.py and transaction.py files. You would want these two Python files in the same folder as each other, and the smart contract can be anywhere so long as it's on the same device and you know the path to it.
