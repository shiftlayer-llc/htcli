# Password Management Usage Guide

## Simple Password Flow

The password system follows this simple flow:

1. **Check Cache** → If password was recently used, return it immediately
2. **Check Environment** → Look for `HTCLI_PASSWORD_KEYNAME` environment variable
3. **Check Stored** → Look in encrypted local file
4. **Prompt User** → Ask user to type password
5. **Fallback** → Use default password (if allowed)

## Basic Usage

### 1. Simple Password Prompt
```python
from htcli.utils.password import get_secure_password

# Get password for a key
password = get_secure_password("my_wallet_key")
```

### 2. With Custom Prompt
```python
password = get_secure_password(
    key_name="subnet_key",
    prompt_message="Enter your subnet password"
)
```

### 3. Environment Variable (Recommended for Automation)
```bash
# Set environment variable
export HTCLI_PASSWORD_MY_WALLET_KEY="my-secure-password"

# In your script
password = get_secure_password("my_wallet_key")  # Will use env var automatically
```

### 4. Store Password for Future Use
```python
from htcli.utils.password import store_password

# Store a password securely
store_password("my_key", "my_password")

# Later, retrieve it
password = get_secure_password("my_key")  # Will get from storage
```

## Security Features

### Account Lockout
- After 5 failed attempts, account is locked for 5 minutes
- Prevents brute force attacks

### Audit Logging
- All password operations are logged to `~/.htcli/password_audit.log`
- Format: `2024-01-15 10:30:45 | key_name | source | SUCCESS/FAILED`

### Encryption
- Passwords are encrypted using Fernet before storage
- Master key can be set via `HTCLI_MASTER_KEY` environment variable

### Cache Management
- Passwords are cached for 30 minutes for convenience
- Cache is cleared when switching environments

## Configuration

### Environment Variables
```bash
# Set master key for encryption
export HTCLI_MASTER_KEY="your-secure-master-key"

# Set specific passwords
export HTCLI_PASSWORD_WALLET_KEY="wallet-password"
export HTCLI_PASSWORD_SUBNET_KEY="subnet-password"
```

### Configuration Directory
- All files stored in `~/.htcli/`
- Directory permissions: 700 (user only)
- Files: `passwords.enc`, `password_audit.log`

## CLI Integration

### In Commands
```python
@app.command()
def my_command():
    """Example command using password management."""
    try:
        password = get_secure_password("wallet_key")
        # Use password for operation
        print_success("Operation completed")
    except LockoutException:
        print_error("Account is temporarily locked")
    except SecurityException as e:
        print_error(f"Security error: {e}")
```

### Password Help
```python
from htcli.utils.password import show_password_help

@app.command()
def password_help():
    """Show password management help."""
    show_password_help()
```

## Best Practices

### For Development
```python
# Simple approach - just prompt user
password = get_secure_password("dev_key")
```

### For Automation
```bash
# Use environment variables
export HTCLI_PASSWORD_AUTO_KEY="automation-password"
```

### For Production
```bash
# Set strong master key
export HTCLI_MASTER_KEY="very-long-random-string-here"

# Use specific passwords
export HTCLI_PASSWORD_PROD_WALLET="production-wallet-password"
```

### Security Tips
1. **Never hardcode passwords** in scripts
2. **Use environment variables** for automation
3. **Set a strong master key** via environment variable
4. **Clear cache** when switching environments
5. **Monitor audit logs** for suspicious activity
6. **Rotate passwords** regularly

## Error Handling

```python
from htcli.utils.password import get_secure_password, LockoutException, SecurityException

try:
    password = get_secure_password("my_key")
except LockoutException:
    print("Account is locked due to failed attempts. Try again later.")
except SecurityException as e:
    print(f"Security error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Migration from Old System

If you have existing passwords stored with the old system:

1. **Backup your old passwords**
2. **Set the new master key**: `export HTCLI_MASTER_KEY="your-new-key"`
3. **Re-enter passwords** - they'll be stored with the new system
4. **Clear old cache**: `htcli wallet clear-cache`

## Troubleshooting

### Common Issues

1. **"Account is locked"**
   - Wait 5 minutes or clear cache
   - Check for multiple failed attempts

2. **"Failed to decrypt passwords"**
   - Master key may have changed
   - Delete `~/.htcli/passwords.enc` and re-enter passwords

3. **"Permission denied"**
   - Check `~/.htcli/` directory permissions (should be 700)
   - Run: `chmod 700 ~/.htcli/`

4. **Cache not working**
   - Clear cache: `htcli wallet clear-cache`
   - Check if cache timeout is too short

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now password operations will show detailed logs
password = get_secure_password("debug_key")
```

This simplified system provides essential security while being much easier to use and understand than the complex enterprise version.
