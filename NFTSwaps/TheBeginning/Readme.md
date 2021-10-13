# Finalization of "The Beginning" 
October 12, 2021 our auction ended for NFT The Beginning and we later finalized the purchase with our winning bidder utilizing a Cardano smart contract (plutus script). We've added the script source code here in an effort to keep all CypherMonks transactions completely open source, verifiable, and transparent.

In interacting with the smart contract we used our Smart Contract Gateway application, the source of which will be available in the MadeWithLovelace organization under its own repository.

## Auction Details
The Beginning was auctioned on our official site of cyphermonks.com beginning 6th of Oct 2021 and ending at 6 PM UTC on 12th Oct, 2021. The winning bidder was whitelisted in the Smart Contract Gateway and was given the Gateway address of addr1v8l5z0anxxnyjvzpf0c8uugx5pyg27w4x2t4t53untq27jg8qmf93 - after this address had been validated on the blockchain using our internal NFT "CMLoading", which we use to validate an address is indeed an official CypherMonks address.  Shortly after, the buyer sent the winning bid amount of 105 ADA to the Gateway address and the Gateway completed the sale by sending the appropriate transaction to the Smart Contract, releasing the NFT The Beginning to the buyer.

To be released the Smart Contract validator required two conditions: Amount of ADA = final auction price of 105 ADA; Recipient of ADA = our Gateway address. When the buyer sent the ADA To our Gateway, the Gateway is able to then satisfy those conditions and provide the required Datum to the Smart Contract transaction, thereby unlocking the NFT and finalizing the sale.
