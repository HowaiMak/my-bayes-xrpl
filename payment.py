from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.account import get_balance
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait

def payment():
    print("Let's make payments... 💰")
    client = JsonRpcClient(url="https://s.altnet.rippletest.net:51234/")

    # Create wallets and fund them
    sender_wallet = generate_faucet_wallet(client=client)
    receiver_wallet = generate_faucet_wallet(client=client)

    # Fetch balances
    sender_balance = get_balance(client=client, address=sender_wallet.address)
    reciever_balance = get_balance(client=client, address=receiver_wallet.address)

    # Display sender info
    print(f"Sender Address: {sender_wallet.classic_address}")
    print(f"Sender Balance: {drops_to_xrp(str(sender_balance))} XRP")

    # Display reciever info
    print(f"Receiver Address: {receiver_wallet.classic_address}")
    print(f"Receiver Balance: {drops_to_xrp(str(reciever_balance))} XRP")

    # Prepare transaction
    payment_tx = Payment(
        account=sender_wallet.address,
        destination=receiver_wallet.address,
        amount=xrp_to_drops(10)
    )

    # Sign and submit the transaction
    payment_result = submit_and_wait(transaction=payment_tx, client=client, wallet=sender_wallet, autofill=True)
    
    # Verify the results
    if payment_result.is_successful():
        print("Payment tx succeede: ", payment_result.result['hash'])
    else:
        print("Payment tx failed: ", payment_result.result)






