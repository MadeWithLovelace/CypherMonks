import os
import transaction as trx
from sys import exit
from os.path import isdir, isfile

def buy(tmp, buyer_addr, wallet_skey_path, wallet_addr, script_addr, cost, datum_hash, plutus_script, seller_addr, policy_id, token_name, collateral):

    # Ensure the tmp folder exists    
    if isdir(tmp) is False:
        print('The directory:', tmp, 'does not exists')
        exit(0)

    # Clean the folder
    trx.delete_contents(tmp)
    trx.protocol(tmp)
    trx.utxo(wallet_addr, tmp, 'utxo.json')
    
    # Check if wallet address is correct
    if isfile(tmp+'utxo.json') is False:
        print('The file:', tmp+'utxo.json', 'does not exists')
        exit(0)
    utxo_in, utxo_col, currencies, flag, _ = trx.txin(tmp, 'utxo.json', collateral)
    
    # Check for collateral
    if flag is True:
        trx.utxo(script_addr, tmp, 'utxo_script.json')
        if isfile(tmp+'utxo_script.json') is False:
            print('The file:', tmp+'utxo_script.json', 'does not exists')
            exit(0)
        _, _, script_currencies, _, data_list = trx.txin(tmp, 'utxo_script.json', collateral, True, datum_hash)
        contract_utxo_in = utxo_in
        for key in data_list:
            # A single UTXO with a single datum can be spent
            if data_list[key] == datum_hash:
                contract_utxo_in += ['--tx-in', key]
                break
        _, final_tip, block = trx.tip(tmp)
        print('\nThe current block:', block)
        utxo_out = trx.asset_change(tmp, script_currencies, buyer_addr) # UTxO to Send NFT to the Buyer
        utxo_out += trx.asset_change(tmp, currencies, wallet_addr) # Account for token change TODO: Double check fee calc error
        utxo_out += ['--tx-out', seller_addr+'+'+str(cost)] # UTxO to Send Payment to Seller
        print('\nUTxO: ', utxo_out)
        additional_data = [
            '--tx-out-datum-hash', datum_hash,
            '--tx-in-datum-value', '"{}"'.format(trx.get_token_identifier(policy_id, token_name)),
            '--tx-in-redeemer-value', '""',
            '--tx-in-script-file', plutus_script
        ]
        print('\nCheck DATUM: ', additional_data)
        trx.build(tmp, wallet_addr, final_tip, contract_utxo_in, utxo_col, utxo_out, additional_data)

        # User Confirms if Data is Correct
        answer = -1
        while answer not in [0, 1]:
            try:
                answer = int(input("Proceed by entering 1 or exit with 0\n"))
            except ValueError:
                pass
        if answer == 0:
            print('The transaction information is incorrect.')
            exit(0)
        
        # Ensure the tmp folder exists
        if isfile(wallet_skey_path) is False:
            print('The file:', wallet_skey_path, 'does not exists')
            exit(0)
        
        signers = [
            '--signing-key-file',
            wallet_skey_path
        ]
        trx.sign(tmp, signers)
        trx.submit(tmp)
    else:
        print("The wallet did not account for collateral. Please create a UTxO of 2 ADA (2000000 lovelace) before trying again.")
        exit(0)

if __name__ == "__main__":
    # Setup Temp Directory (try to)
    scptroot = os.path.realpath(os.path.dirname(__file__))
    tmpname = "tmp"
    tmppath = os.path.join(scptroot, tmpname)
    TMP = os.path.join(tmppath, '')
    try:
        os.mkdir(tmpname)
    except OSError:
        pass
        
    
    
    # Collateral for script transaction
    COLLATERAL = 2000000 # Should be min of 2000000 lovelace in a separate UTxO in buyer's wallet
    
    # Setup vars for smart contract transaction
    API_ID = 'BLOCKFROST_API_ID'
    SELLER_ADDR = "addr_test1nnnnn_seller_addr"
    BRIDGE_ADDR = "addr_test1nnnnnnn_bridge_addr"
    BRIDGE_SKEY_PATH = "/home/user/wallets/bridge.skey"
    PLUTUS_SCRIPT_PATH = "/home/user/scripts/nft_swap.plutus"
    PLUTUS_SCRIPT_ADDR = "addr_test1nnnnnn_plutus_addr"
    ASSET_POLICY_ID = "nft_policy_ID"
    ASSET_NAME = "nft_name"
    PRICE = 10000000 # Price in lovelace
    BUYER_ADDR = "addr_test1nnnnn_buyer_addr"
    
    # Calculate the "fingerprint"
    FINGERPRINT = trx.get_token_identifier(ASSET_POLICY_ID, ASSET_NAME)
    DATUM_HASH  = trx.get_hash_value(SELLER_ADDR)
    
    # Check for payment, initiate Smart Contract on success
    result = trx.check_for_payment(TMP, API_ID, BRIDGE_ADDR, PRICE, BUYER_ADDR)
    
    if result:
        buy(TMP, BUYER_ADDR, BRIDGE_SKEY_PATH, BRIDGE_ADDR, PLUTUS_SCRIPT_ADDR, PRICE, DATUM_HASH, PLUTUS_SCRIPT_PATH, SELLER_ADDR, ASSET_POLICY_ID, ASSET_NAME, COLLATERAL)
