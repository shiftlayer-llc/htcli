# 🎯 **NEW HTCLI COMMAND STRUCTURE**

## ✅ **PERFECT! EXACTLY WHAT YOU WANTED**

The CLI now has the clean structure you requested:

```bash
htcli subnet <actions>
htcli chain <actions>
htcli wallet <actions>
```

---

## 📋 **COMMAND STRUCTURE**

### **🌐 SUBNET OPERATIONS**
```bash
./htcli.py subnet register create <path> --memory <MB> --blocks <blocks> --interval <blocks>
./htcli.py subnet register activate <subnet-id>
./htcli.py subnet manage list
./htcli.py subnet manage info <subnet-id>
./htcli.py subnet nodes add <subnet-id> <peer-id> --hotkey <address>
./htcli.py subnet nodes list <subnet-id>
```

### **💰 WALLET OPERATIONS**
```bash
./htcli.py wallet keys generate <name>
./htcli.py wallet keys list
./htcli.py wallet keys import <name> --private-key <key>
./htcli.py wallet keys delete <name>
./htcli.py wallet stake add <subnet-id> <node-id> <amount> --hotkey <address>
./htcli.py wallet stake remove <subnet-id> <amount> --hotkey <address>
./htcli.py wallet stake info <subnet-id> --hotkey <address>
```

### **🔗 CHAIN OPERATIONS**
```bash
./htcli.py chain info network
./htcli.py chain info account <address>
./htcli.py chain info epoch
./htcli.py chain query balance <address>
./htcli.py chain query peers
./htcli.py chain query block [<block-number>]
```

---

## 🎯 **WORKING EXAMPLES**

### **✅ Tested and Working:**
```bash
# Network statistics
./htcli.py chain info network
# Shows: Total Subnets: 2, Active Subnets: 0, etc.

# Account balance
./htcli.py chain query balance 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY
# Shows: Balance: 36301712327596.585937500 TAO

# Subnet list
./htcli.py subnet manage list
# Shows: No subnets found.
```

---

## 🚀 **HELP COMMANDS**

```bash
# Main help
./htcli.py --help

# Subnet help
./htcli.py subnet --help
./htcli.py subnet register --help

# Chain help
./htcli.py chain --help
./htcli.py chain info --help

# Wallet help
./htcli.py wallet --help
./htcli.py wallet keys --help
```

---

## 🎉 **PERFECT STRUCTURE!**

**The CLI now has exactly the structure you wanted:**

- ✅ **`htcli subnet <actions>`** - All subnet operations
- ✅ **`htcli chain <actions>`** - All chain operations
- ✅ **`htcli wallet <actions>`** - All wallet operations

**Clean, intuitive, and exactly what you requested!** 🚀
