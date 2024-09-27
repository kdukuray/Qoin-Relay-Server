from rest_framework.serializers import ModelSerializer
from .models import Block, Transaction, Wallet


class BlockSerializer(ModelSerializer):
    class Meta:
        model = Block
        fields = "__all__"


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"

