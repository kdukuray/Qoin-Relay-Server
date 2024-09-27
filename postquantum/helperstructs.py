from pqcrypto.sign.dilithium4 import verify
from .helperfunctions import *
from .models import PQWallet


class TransactionStruct:
    """Transaction Struct to help perform transaction operations"""
    def __init__(self, sender_id, trxn_uuid, sender_pub_key, receiver_pub_key, amount, trxn_hash, trnx_signature):
        self.sender_id = sender_id
        self.trxn_uuid = trxn_uuid
        self.sender_pub_key = sender_pub_key
        self.receiver_pub_key = receiver_pub_key
        self.amount = amount
        self.trxn_hash = trxn_hash
        self.trxn_signature = trnx_signature

    def verify_transaction(self) -> bool:
        """Verifies that a transaction is valid"""
        # Assumes that the transaction is valid by default
        transaction_is_valid: bool = True

        # Verifies that the transaction amount is valid
        if self.amount < 0:
            transaction_is_valid = False
            print("Invalid Transaction Amount!")

        # Verifies that the transactions signature is valid
        # if the transaction is in valid, an exception will be thrown
        transaction_is_valid = verify(b64_to_binary(self.sender_pub_key),
                                      bytes(self.trxn_hash, 'utf-8'),
                                      b64_to_binary(self.trxn_signature))
        # try:
        #     serialization.load_pem_public_key(self.sender_pub_key.encode("utf-8")) \
        #         .verify(b64_to_binary(self.trnx_signature), bytes(self.trxn_hash, "utf-8"))
        # except:
        #     transaction_is_valid = False

        # Verifies that the sender's wallet exists and has the necessary funds
        try:
            user_wallet_balance = PQWallet.objects.get(pk=self.sender_id).balance
            if self.amount > user_wallet_balance:
                transaction_is_valid = False
        except:
            transaction_is_valid = False

        return transaction_is_valid

# This function is meant for debugging purposes
    def print(self):
        """Prints the transactions details"""
        print(f"""
        Sender Id: {self.sender_id}
        Transaction UUID: {self.trxn_uuid},
        Sender Public Key: {self.sender_pub_key},
        Receiver Public Key: {self.receiver_pub_key},
        Transaction Amount: {self.amount},
        Transaction Hash: {self.trxn_hash},
        Transaction Signature: {self.trxn_signature}
""")



