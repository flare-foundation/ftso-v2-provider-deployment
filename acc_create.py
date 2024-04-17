from mnemonic import Mnemonic
from bip44 import Wallet
from eth_keys import keys


def create_accounts(num_accounts):
    # Generate a new mnemonic phrase
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=256)

    # Create a wallet from the mnemonic phrase
    wallet = Wallet(mnemonic_phrase)
    accounts = []

    for i in range(num_accounts):
        # Derive accounts from the same mnemonic
        account = wallet.derive_account("eth", account=i)
        private_key_bytes = account[0]
        private_key = keys.PrivateKey(private_key_bytes)

        # Use eth_keys library to get the correct address
        address = private_key.public_key.to_checksum_address()

        accounts.append({
            'private_key': private_key.to_hex(),
            'address': address
        })
    return mnemonic_phrase, accounts


# Create 5 accounts
mnemonic_phrase, accounts = create_accounts(5)

# Print the mnemonic phrase
print("Mnemonic Phrase:", mnemonic_phrase)

# Print account information
for index, account in enumerate(accounts):
    print(f"Account {index + 1}: Address = {account['address']}, Private Key = {account['private_key']}")
