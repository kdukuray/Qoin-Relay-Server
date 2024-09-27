from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Block, Transaction, Wallet
from . import serializers
from rest_framework import status
from .helperstructs import TransactionStruct, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import hashlib
from .serializers import TransactionSerializer, WalletSerializer
from .helperfunctions import string_to_b64, binary_to_b64


@api_view(["GET"])
def get_blocks(request):
    """Retrieves all the blocks in the database"""
    blocks = Block.objects.all()
    serialized_blocks = serializers.BlockSerializer(blocks, many=True)
    return Response(serialized_blocks.data, status=status.HTTP_200_OK)


# The following function may be a security vulnerability.
# We should come up with methods to circumvent having to use such a function
@api_view(["GET"])
def get_wallet_id(request, private_key):
    """Retrieves the wallet ID associated with the given retrieved private key"""
    wallet = Wallet.objects.get(private_key=private_key)
    wallet_id = wallet.pk
    payload = {"wallet_id": wallet_id}
    return Response(payload, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_blocks_after(requests, block_id):
    """Retrieves all the blocks after the block with the given ID"""
    blocks = Block.objects.filter(pk__gt=block_id)
    serialized_blocks = serializers.BlockSerializer(blocks, many=True)
    return Response(serialized_blocks.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_block_transactions(request, block_id):
    """Retrives all the transactions associated with a given block"""
    parent_block = Block.objects.get(pk=block_id)
    transactions = Transaction.objects.filter(parent_block=parent_block)
    serialized_transactions = serializers.TransactionSerializer(transactions, many=True)
    return Response(serialized_transactions.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def new_transaction(request):
    """Adds a transaction to the pool of pending transactions"""
    ntd = request.data
    new_transaction_obj = Transaction(sender_id=ntd.get("sender_id"), trxn_uuid=ntd.get("trxn_uuid"),
                                      sender_pub_key=ntd.get("sender_pub_key"), amount=ntd.get("amount"),
                                      receiver_pub_key=ntd.get("receiver_pub_key"), trxn_hash=ntd.get("trxn_hash"),
                                      trxn_signature=ntd.get("trxn_signature"))
    # Make sure receiving address exists
    try:


        receiver_pub_key = string_to_b64(ntd.get("receiver_pub_key").replace("\\n", "\n"))
        receiver_wallet = Wallet.objects.get(public_key=receiver_pub_key)
    except Exception as e:
        print(e)
        return Response({"result": "The specified wallet does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    new_transaction_obj.save()
    return Response({"result": "Transaction added to pending transactions"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_wallet_balance(request, sender_id):
    """Returns the balance of a wallet given its ID"""
    wallet = Wallet.objects.get(pk=sender_id)
    resp = {"wallet_balance": wallet.balance}
    return Response(resp, status=status.HTTP_200_OK)


@api_view(["GET"])
def new_wallet(request, name):
    """Creates a new wallet"""
    # Generate private key & public key pair
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Convert both keys into strings
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_str = pem_private_key.decode('utf-8')
    private_key = private_key_str

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_str = pem_public_key.decode('utf-8')
    public_key = public_key_str

    # Convert  private and public key pair into Bas64 for storage
    private_key_in_b64 = string_to_b64(private_key)
    public_key_in_b64 = string_to_b64(public_key)

    # Create & save new wallet with private and public key pair
    wallet_to_create = Wallet(name=name, private_key=private_key_in_b64, public_key=public_key_in_b64, balance=1000)
    wallet_to_create.save()
    payload = {"wallet_id": wallet_to_create.pk, "private_key": private_key, "public_key": public_key,
               "private_key_in_b64": private_key_in_b64, "public_key_in_b64": public_key_in_b64}
    return Response(payload, status=status.HTTP_200_OK)


@api_view(["POST"])
def new_block(request):
    """Verifies new blocks and adds them to the database"""
    # Get the new block's data
    new_block_data = request.data
    # By default, we assume that all the transactions data in the block is valid
    all_transaction_are_valid = True
    new_block_hash = ""
    # Retrieve the previous block's hash
    previous_block_hash = Block.objects.all().last().hash
    # For each transaction, create a TransactionStruct object
    transaction_structs = [TransactionStruct(tr.get("sender_id"), tr.get("trxn_uuid"), tr.get("sender_pub_key"),
                                             tr.get("receiver_pub_key"), tr.get("amount"), tr.get("trxn_hash"),
                                             tr.get("trxn_signature"))
                           for tr in new_block_data.get("transactions")]
    # Check that all the transactions in the block are valid
    for tr in transaction_structs:
        # If any of the transactions isn't valid, set all_transaction_are_valid to False
        if not(tr.verify_transaction()):
            all_transaction_are_valid = False

    # If the transactions are valid, hash their uuids, get the previous block hash,
    # append it to the uuid string, and hash it produce the new block's hash
    if all_transaction_are_valid:
        all_transactions_hashes_as_str = "".join([trxn.trxn_hash for trxn in transaction_structs])
        new_block_hash_ingest = all_transactions_hashes_as_str + previous_block_hash
        new_block_hash = hashlib.sha256((bytes(new_block_hash_ingest, 'utf-8'))).hexdigest()

    # if the new block hash that we generated matches the new block hash sent with the block, add it to the database
    if new_block_data.get("hash") == new_block_hash:
        block_to_add = Block(hash=new_block_hash, prev_block_hash=previous_block_hash)
        block_to_add.save()

        # Now that the block has been creates, create the associated transactions for the block
        for trxn in transaction_structs:
            transaction_to_add = Transaction(sender_id=trxn.sender_id, trxn_uuid=trxn.trxn_uuid,
                                             sender_pub_key=trxn.sender_pub_key, receiver_pub_key=trxn.receiver_pub_key,
                                             amount=trxn.amount, trxn_hash=trxn.trxn_hash,
                                             trxn_signature=trxn.trxn_signature, parent_block=block_to_add,
                                             status="verified")

            transaction_to_delete = Transaction.objects.get(trxn_uuid=transaction_to_add.trxn_uuid)
            transaction_to_delete.delete()
            transaction_to_add.save()

            # For each transaction, debit the transaction sender
            sender_wallet = Wallet.objects.get(id=trxn.sender_id)
            sender_wallet.balance -= trxn.amount
            sender_wallet.save()

            # For each transaction, credit the transaction receiver
            receiver_pub_key = string_to_b64(trxn.receiver_pub_key.replace("\\n", "\n"))
            receiver_wallet = Wallet.objects.get(public_key=receiver_pub_key)
            receiver_wallet.balance += trxn.amount
            receiver_wallet.save()

        # Because the block is valid, reward the block's miner for expending compute to mine the block
        miner = Wallet.objects.get(pk=new_block_data.get("miner_id"))
        miner.balance = miner.balance + 100
        miner.save()

    return Response({"test": "test"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_pending_transactions(request):
    """Retrieves 10 transactions in the current pending transactions pool"""
    pending_transactions = Transaction.objects.filter(status="pending")[:10]
    serialized_pending_transactions = TransactionSerializer(pending_transactions, many=True)
    return Response(serialized_pending_transactions.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_wallets_after(request, wallet_id):
    """Retrives the wallets with an ID greater than the given ID"""
    wallets = Wallet.objects.filter(pk__gt=wallet_id)
    serialized_wallets = WalletSerializer(wallets, many=True)
    payload = {"new_wallets": [wallet for wallet in serialized_wallets.data]}
    return Response(payload, status=status.HTTP_200_OK)

