# Cardano Transaction Bridge
This little set of scripts will allow a user to simply send ADA to an agreed-upon address, in an agreed-upon amount of ADA, and the python script will automatically interact with the Smart Contract like a sort of bridge, so the user doesn't need to build a specialized tx.

## Use Cases
The most expected use-case is NFT swap, wherein a "buyer" can swap ADA for an NFT from a "seller". The seller hosts the smart contract and python script herein, on a live node that has the cardano-cli installed. This allows the seller to setup a cron or sched task to run the bridge.py script in intervals, watching for the payment in the agreed amount, from the address of the buyer, any address, or a whitelist of addresses.  The whitelist has a True/False switch, to remove an address from the whitelist once used...in case the use of native token (non-NFT) swaps in limits is needed.

The "bridge" address is a wallet maintained by the seller on their node, when the bridge script "sees" the transaction being watched for, it will initiate the smart contract via the built in swap function and assuming all variables are set correctly.  This way a buyer only needs to trust the seller and send the ADA to the address the bridge script monitors.
