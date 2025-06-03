# Register a new subnet

```htcli subnet register --wallet.name test```

```python
Connecting to main (wss://hypertensor.duckdns.org)
Estimated transaction fee: 0.000107 tokens
✅ Sufficient balance. Your balance will be approximately 9999999999999.999893 tokens after the transaction.
Do you want to proceed with the registration? [y/N]: y
Extrinsic Hash: 0xef0fcd43030313b619e46422d66d74674cb05fa2fd38b9f5dad178547774a171
Block Hash: 0x2f56595364bc3467773fad25c6fab2300bcb3bc7d58b5a4f13d59a0c3034d5ef
✅ Subnet registered successfully!
```


```poetry run htcli subnet info --rpc_network test --wallet.name test --subnet_id 0 ```

```poetry run htcli subnet activate --rpc_network test --wallet.name test1 --subnet_id 3 ```

```poetry run htcli subnet list```

```htcli subnet remove --wallet.name test --subnet_id 2```