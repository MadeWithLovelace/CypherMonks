import os
import transaction as trx
from sys import exit
from os.path import isdir, isfile

def swap(tmp, wallet_skey_path, wallet_addr, script_addr, swap_amt, datum_hash, plutus_script, owner_addr, policy_id, token_name, collateral):

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
        utxo_out = trx.asset_change(tmp, script_currencies, wallet_addr) # UTxO to swap NFT out of contract
        utxo_out += trx.asset_change(tmp, currencies, wallet_addr) # Account for token change
        utxo_out += ['--tx-out', owner_addr+'+'+str(swap_amt)] # UTxO to swap ADA to NFT owner for the swap
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
    COLLATERAL = 2000000 # Should be min of 2000000 lovelace in a separate UTxO
    
    print("\n--- NOTE: Proceed Only If You Are Swapping Out ADA in Exchange for the NFT at the NFT Swap Smart Contract  ---\n")
    print("\n---       Be sure to have at least 1 UTxO in the wallet with 2 ADA for collateral, this is returned to you ---\n")
    # Get input from user
    SWAP_ADDR = input("\nYour Cardano Address to Swap From (eg addr1...) \n    My Address:>")
    SWAP_SKEY_PATH = input("\nPath to Your Signing Key File for This Address (eg /home/user/node/wallet/payment.skey) \n    Path to skey File:>")
    OWNER_ADDR = input("\nNFT Owner's Provided Cardano Address (eg addr1...) \n    NFT Owner Address:>")
    PLUTUS_SCRIPT_PATH = input("\nPath to Plutus SmartContract File (eg /home/user/node/wallet/scripts/smartcontract.plutus) \n    Path to SmartContract File:>")
    SCRIPT_ADDR = input("\nSmartContract Cardano Address (eg addr1...) \n    SmartContract Address:>")
    POLICY_ID = input("\nPolicy ID of NFT You're Swapping For (eg 3cb979ba9d8d618acc88fb716e97782469f04727d5ba8b428a9a9258) \n    NFT Policy ID:>")
    TOKEN_NAME = input("\nName/Ticker of NFT You're Swapping For (eg CypherMonkZero) \n    NFT Name:>")
    SWAP_AMT = input("\nAmount of Lovelace to Swap for the NFT (multiply ada by 1000000, eg for 10ADA, enter: 10000000) \n    Lovelace to Swap:>")
    
    print("\n-----------------------------\n| Please Verify Your Input! |\n-----------------------------\n")
    print("\nMy Address >> ",SWAP_ADDR)
    print("\nMy Address skey File Path >> ",SWAP_SKEY_PATH)
    print("\nNFT Owner Address >> ",OWNER_ADDR)
    print("\nSmartContract File Path >> ",PLUTUS_SCRIPT_PATH)
    print("\nSmartContract Address >> ",SCRIPT_ADDR)
    print("\nNFT Policy ID >> ",POLICY_ID)
    print("\nNFT Name >> ",TOKEN_NAME)
    print("\nLovelace to Swap >> ",SWAP_AMT)
    
    VALUES_CORRECT = input("\n\nIs the information above correct? (yes or no): ")
    
    if VALUES_CORRECT == ("yes"):
        print("\n\nContinuing . . . \n")
    elif VALUES_CORRECT == ("no"):
        print("\n\nQuitting, please run again to try again!\n\n")
        exit(0)
    
    # Calculate the "fingerprint"
    FINGERPRINT = trx.get_token_identifier(POLICY_ID, TOKEN_NAME) # Not real fingerprint but works
    DATUM_HASH  = trx.get_hash_value('"{}"'.format(FINGERPRINT)).replace('\n', '')
    
    print('DATUM Hash: ', DATUM_HASH)
    
    swap(TMP, SWAP_SKEY_PATH, SWAP_ADDR, SCRIPT_ADDR, SWAP_AMT, DATUM_HASH, PLUTUS_SCRIPT_PATH, OWNER_ADDR, POLICY_ID, TOKEN_NAME, COLLATERAL)
