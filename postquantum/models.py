from django.db import models
choices = [("pending", "pending"), ("verified", "verified")]


class PQBlock(models.Model):
    hash = models.CharField(max_length=200)
    prev_block_hash = models.CharField(max_length=200)


class PQTransaction(models.Model):
    sender_id = models.IntegerField()
    trxn_uuid = models.CharField(max_length=200)
    sender_pub_key = models.TextField()
    receiver_pub_key = models.TextField()
    amount = models.IntegerField()
    trxn_hash = models.CharField(max_length=200)
    trxn_signature = models.TextField()
    parent_block = models.ForeignKey(PQBlock, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=choices, max_length=20, default="pending")


class PQWallet(models.Model):
    name= models.CharField(max_length=100, default="John Doe")
    private_key = models.TextField()
    public_key = models.TextField()
    balance = models.IntegerField()

