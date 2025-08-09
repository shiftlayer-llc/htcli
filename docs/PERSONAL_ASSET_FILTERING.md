# Personal Asset Filtering with --mine

The Hypertensor CLI includes a powerful **universal --mine filtering system** that transforms any command to show only your personal assets instead of network-wide data.

## 🎯 **Overview**

### **The Problem**

Blockchain networks contain data from all users, making it difficult to distinguish:

- **What you own** vs. **what others own**
- **Your stakes** vs. **network-wide stakes**
- **Your subnets** vs. **all subnets on the network**

### **The Solution: Universal --mine Flag**

Add `--mine` to any command to filter results to show only **your assets**:

```bash
# 📊 NETWORK DATA (Default)
htcli subnet list              # Shows ALL subnets (including others')
htcli stake info --address ... # Shows stakes for specific address

# 👤 YOUR DATA (With --mine)
htcli --mine subnet list       # Shows ONLY subnets you own
htcli --mine stake info        # Shows stakes for ALL your addresses
```

## 🔧 **How It Works**

### **1. Automatic Key Detection**

The system automatically reads your wallet keys from `~/.htcli/wallets/`:

```bash
# First, generate or import keys
htcli wallet generate-key --name my-key
htcli wallet import-key --name imported --private-key 0x1234...

# Keys are stored securely in ~/.htcli/wallets/
ls ~/.htcli/wallets/
# my-key.json
# imported.json
```

### **2. Smart Ownership Matching**

For each command with `--mine`:

1. **Load your addresses** from stored wallet keys
2. **Query blockchain** for ownership data (subnet owners, stake holders, etc.)
3. **Filter results** to show only items where you are the owner/stakeholder
4. **Provide feedback** on filtering results

### **3. Clear User Feedback**

The system provides informative messages:

```bash
$ htcli --mine subnet list
🔍 Filtered for your 2 wallet address(es) - no matching assets found.
💡 Network has 5 total items, but none are owned by you.

$ htcli --mine stake info
🎯 Showing 3 asset(s) owned by your 2 wallet address(es).
💡 Network has 15 total items (12 owned by others).
```

## 📋 **Supported Commands**

### **✅ Commands that Support --mine**

| Category | Command | What it filters |
|----------|---------|-----------------|
| **subnet** | `list` | Shows only subnets you own |
| **subnet** | `info` | Works with your subnet IDs |
| **stake** | `info` | Shows stakes for all your addresses |
| **node** | `list` | Shows only nodes you registered |
| **node** | `status` | Works with your nodes |

### **➖ Commands where --mine doesn't apply**

- **Configuration commands** (already personal)
- **Wallet commands** (already personal by nature)
- **Chain network stats** (global data makes sense)
- **Transaction commands** (require explicit parameters)

## 💡 **Usage Examples**

### **Subnet Management**

```bash
# See all subnets on network
$ htcli subnet list
Found 5 subnets:
- Subnet 1: Owner 5G3WukHv... (someone else)
- Subnet 2: Owner 5C4mxA6R... (someone else)
- Subnet 3: Owner 5HmSbJim... (you!)

# See only YOUR subnets
$ htcli --mine subnet list
Found 1 subnet owned by you:
- Subnet 3: Owner 5HmSbJim... (my-wallet)
```

### **Stake Management**

```bash
# Check stakes for specific address
$ htcli stake info --address 5C4mxA6RzX...
Shows stakes for that one address only

# Check stakes for ALL your addresses
$ htcli --mine stake info
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Address             ┃ Subnet ID ┃ Total Stake     ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 5C4mxA6RzX...       │ 1         │ 1000.0 TENSOR   │
│ 5HmSbJimjq...       │ 2         │ 500.0 TENSOR    │
└─────────────────────┴───────────┴─────────────────┘
```

### **Node Operations**

```bash
# List all nodes in a subnet
$ htcli node list --subnet-id 1
Shows all nodes registered by anyone

# List only YOUR nodes in the subnet
$ htcli --mine node list --subnet-id 1
Shows only nodes you registered
```

## 🔒 **Security & Privacy**

### **Local Key Storage**

- Keys stored encrypted in `~/.htcli/wallets/`
- Uses Fernet encryption with password protection
- Only your local machine can access your keys

### **Privacy Protection**

- `--mine` filtering happens locally
- No additional data sent to blockchain
- Other users cannot see your filtering activity

### **Safe Defaults**

- Commands default to network-wide data (safe for exploration)
- `--mine` is explicit opt-in for personal filtering
- Clear messages distinguish between network vs. personal data

## 🎨 **User Experience Benefits**

### **1. Clarity**

- **Network View**: "Here's what exists on the blockchain"
- **Personal View**: "Here's what you own specifically"

### **2. Efficiency**

- No need to manually check ownership for each item
- Automatic filtering across multiple addresses
- Single command shows comprehensive personal portfolio

### **3. Consistency**

- Same `--mine` flag works across all categories
- Consistent feedback messages and formatting
- No separate "my" commands to remember

### **4. Scalability**

- Works with any number of wallet addresses
- Efficiently handles large networks with many assets
- Provides summaries and totals for personal assets

## 🚀 **Getting Started**

### **1. Set Up Wallet Keys**

```bash
# Generate a new key
htcli wallet generate-key --name my-main-key

# Or import existing key
htcli wallet import-key --name imported --private-key 0x1234...

# Verify keys are stored
htcli wallet list-keys
```

### **2. Test Network vs Personal Views**

```bash
# Network view
htcli subnet list
htcli stake info --address <some-address>

# Personal view
htcli --mine subnet list
htcli --mine stake info
```

### **3. Use in Workflows**

```bash
# Check your portfolio
htcli --mine subnet list    # Your subnets
htcli --mine stake info     # Your stakes
htcli --mine node list      # Your nodes

# Compare with network
htcli subnet list           # All subnets
htcli chain network         # Network stats
```

## 🔍 **Troubleshooting**

### **"No wallet keys found" Error**

```bash
❌ No wallet keys found. The --mine filter requires stored wallet keys.
💡 Generate a key first: htcli wallet generate-key --name my-key
```

**Solution:** Generate or import at least one wallet key.

### **"No matching assets found" Message**

```bash
🔍 Filtered for your 1 wallet address(es) - no matching assets found.
💡 Network has 5 total items, but none are owned by you.
```

**This is normal** - it means you don't own any assets of that type yet.

### **Keys Not Loading**

- Check `~/.htcli/wallets/` directory exists and contains `.json` files
- Verify file permissions allow reading
- Try regenerating keys if files are corrupted

## 📚 **Advanced Usage**

### **Multiple Address Management**

```bash
# Generate multiple keys for different purposes
htcli wallet generate-key --name main-wallet
htcli wallet generate-key --name staking-wallet
htcli wallet generate-key --name subnet-wallet

# --mine will check ALL your addresses automatically
htcli --mine stake info  # Shows stakes from all 3 addresses
```

### **Combining with Other Flags**

```bash
# JSON output for your assets
htcli --mine --format json stake info

# Verbose output with your filtering
htcli --mine --verbose subnet list

# Custom config with personal filtering
htcli --mine --config /path/to/config.yaml stake info
```

### **Workflow Integration**

```bash
#!/bin/bash
# Daily portfolio check script

echo "=== Your Hypertensor Portfolio ==="
echo "Subnets:"
htcli --mine subnet list

echo -e "\nStakes:"
htcli --mine stake info

echo -e "\nNodes:"
htcli --mine node list
```

The universal --mine filtering system makes the Hypertensor CLI much more user-friendly by clearly separating network-wide data from your personal assets, providing a clear and intuitive way to manage your blockchain portfolio.
