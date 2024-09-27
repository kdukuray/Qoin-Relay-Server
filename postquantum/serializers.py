from rest_framework.serializers import ModelSerializer
from .models import PQBlock, PQTransaction, PQWallet


class PQBlockSerializer(ModelSerializer):
    class Meta:
        model = PQBlock
        fields = "__all__"


class PQTransactionSerializer(ModelSerializer):
    class Meta:
        model = PQTransaction
        fields = "__all__"


class PQWalletSerializer(ModelSerializer):
    class Meta:
        model = PQWallet
        fields = "__all__"

