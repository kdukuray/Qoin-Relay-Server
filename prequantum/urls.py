from django.urls import path
from . import views

urlpatterns = [
    path("blocks/all/", views.get_blocks, name="all-blocks"),
    path("blocks/after/<block_id>/", views.get_blocks_after, name="blocks-after"),
    path("wallets/after/<wallet_id>/", views.get_wallets_after, name="wallets-after"),
    path("wallets/new/", views.new_wallet, name="new-wallet"),
    path("wallets/balance/<sender_id>/", views.get_wallet_balance, name="get-wallet-balance"),
    path("wallets/<private_key>/", views.get_wallet_id, name="get-wallet-id"),
    path("blocks/<block_id>/transactions/", views.get_block_transactions, name="block-transactions"),
    path("blocks/new/", views.new_block, name="new-block"),
    path("transactions/new/", views.new_transaction, name="new-transaction"),
    path("transactions/pending/", views.get_pending_transactions, name="get-pending-transactions"),
]
