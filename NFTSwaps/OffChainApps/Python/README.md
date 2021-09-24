# About Python Scripts

These python scripts are for "off-chain" use to interact with CypherMonk NFT swap smart contracts. There are 3 script files: swapIN.py, swapOUT.py, and transaction.py. Both swapIN.py and swapOUT.py depend on transaction.py for performing various cardano-cli functions in building the transactions. The swapIN.py script is intended for use by the owner of the NFT to be swapped, in this case CypherMonks would use swapIN.py to "deposit" the NFT into the smart contract for the swap.  The swapOUT.py script is then used by the person who is swapping ADA for that NFT, after swapIN.py has been successfully run and the NFT is sitting at the contract's Cardano address.  


## Requirements

- Cardano Full Node
Because everything runs via cardano-cli, it is a requirement that to run these Python scripts the user (whether running swapIN or swapOUT) must run on a system with an up-to-date Cardano full node, with cardano-cli available of course.

- Wallet Signing Key File
The ".skey" file of the user's "swap wallet" they intend to use for the swap must also be present on the system where they are running the Python script, as cardano-cli will need this file to sign the transaction.

- SmartContract Script File
The ".plutus" file (eg cyphermonkzero.plutus) will need to be on the same system where they are running the Python script.


## What swapIN.py Does

The swapIN.py script is used to "begin" the swap of the NFT, and is run by the NFT owner. This script facilitates building and sending a transaction on the NFT owner's machine via cardano-cli, which sends the NFT to be swapped into the smart contract address on the blockchain, ready to be swapped out when the conditions of the smart contract are satisfied.

The transaction built will do the following:
- Send the NFT specified into the smart contract address, along with 2 ADA
- Any change in the owner's wallet is sent back to the owner of course


## What swapOUT.py Does

The swapOUT.py script facilitates building and sending a transaction on the user's machine via cardano-cli, which performs the swap of sending the ADA from the user to the NFT owner and the NFT from the smart contract out to the user.

The transaction built will do the following: 
- The agreed-upon ADA in lovelace is sent to the NFT owner
- The NFT (and 2 ADA in it's UTxO) is sent out of the smart contract, to the user
- Any change in the user's wallet is sent back to the user of course


## Additional Notes for Both Scripts

Before running either script, in addition to having the required ADA for the swap in their wallet, the user also needs to create a new UTxO at their wallet which will be used for the swap, of 2 ADA. This can be done by simply sending 2 ADA to their own wallet address (the wallet to be used for the swap). This is used as "collateral", which is a requirement in running smart contracts on Cardano and in short, guarantees that if the script is somehow faulty in a way that the cardano-cli cannot detect and fails validation, the user will pay 2 ADA as a fee for the failed transaction. However, when a smart contract has been created correctly and is verifiable as such, and has been tested on testnet (as we do here for all CypherMonks smart contracts), this is virtually impossible and the collateral is just to satisfy the requirements of the transaction.

It's advisable to swap from a wallet without a lot of native tokens or NFTs, in other words using a wallet with simply ADA would be best practice to ensure there are no unknown errors preventing the swap from completing.

The scripts rely upon cardano-cli to perform all blockchain tasks, such as building the transactions, reading wallets, signing and submitting transactions.  All these tasks are done by cardano-cli, the Python script just facilitates the commands being built, the math and hashing involved, and issuing the constructed cardano-cli commands to the system. Cardano-cli is what is actually performing all the tasks, including reading wallet values, utilizing the signing key, etc.  The Python script never "knows" this sensitive information besides the folder locations to "paste" into the cardano-cli command, and so acts as a sort of "macro" for the user. All the required commands can be entered by hand if you understand how to construct them.

