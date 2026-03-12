from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.account import get_balance
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait
from xrpl.models.transactions import AccountSet, AccountSetAsfFlag
from xrpl.utils import str_to_hex
from xrpl.models.transactions import TrustSet
from xrpl.models.amounts import IssuedCurrencyAmount

def get_xrpl_currency_hex(name: str) -> str:
    """Converts a string to a 40-char XRPL hex currency code."""
    if len(name) == 3:
        return name # Standard 3-char codes don't need hex
    
    # Convert to hex and pad to 40 characters
    hex_code = name.encode("ascii").hex().upper()
    return hex_code.ljust(40, "0")

def tokens():
    print("Let's manage tokens... 📊")
    client = JsonRpcClient(url="https://s.altnet.rippletest.net:51234/")

    # Create wallets and fund them
    issuer_wallet = generate_faucet_wallet(client=client)
    holder_wallet = generate_faucet_wallet(client=client)

    # Fetch balances
    issuer_balance = get_balance(client=client, address=issuer_wallet.address)
    holder_balance = get_balance(client=client, address=holder_wallet.address)

    # Display issuer info
    print(f"Issuer Address: {issuer_wallet.classic_address}")
    print(f"Issuer Balance: {drops_to_xrp(str(issuer_balance))} XRP")

    # Display holder info
    print(f"Holder Address: {holder_wallet.classic_address}")
    print(f"Holder Balance: {drops_to_xrp(str(holder_balance))} XRP")

    account_set_tx = AccountSet(
        account = issuer_wallet.address,
        set_flag=AccountSetAsfFlag.ASF_DEFAULT_RIPPLE
    )

    account_set_result = submit_and_wait(transaction=account_set_tx, client=client, wallet=issuer_wallet)

    # Verify the results
    if account_set_result.is_successful():
        print("Account Set tx succeede: ", account_set_result.result['hash'])
    else:
        print("Account Set tx failed: ", account_set_result.result)

    # Create new token
    currency_hex = get_xrpl_currency_hex("BAYES")

    # Define token rules
    trust_tx = TrustSet(
        account=holder_wallet.address,
        limit_amount=IssuedCurrencyAmount(
            currency=currency_hex,
            issuer=issuer_wallet.address,
            value="1000"
        )
    )
    
    # Trustline submit
    trust_result = submit_and_wait(transaction=trust_tx, client=client, wallet=holder_wallet, autofill=True)

    # Verify the results
    if trust_result.is_successful():
        print("Trustline tx succeede: ", trust_result.result['hash'])
    else:
        print("Trustline tx failed: ", trust_result.result)


