HOTKEY_GUIDANCE_TEMPLATE = """
[bold cyan]🔑 Hotkey Generated Successfully[/bold cyan]

[bold]Hotkey Details:[/bold]
• Name: {name}
• Address: {address}
• Owner: {owner_name} ({owner_address})

[bold]What is a Hotkey?[/bold]
• Used for operational tasks (consensus, validation)
• Owned by your coldkey for security
• Can be kept online for frequent operations
• Cannot transfer funds directly

[bold]Usage Examples:[/bold]
• Register node: htcli node register --hotkey {address}
[yellow]💡 Security Tip:[/yellow] Keep your coldkey secure, hotkey can be rotated if compromised
"""


COLDKEY_GUIDANCE_TEMPLATE = """
[bold cyan]🔐 Coldkey Generated Successfully[/bold cyan]

[bold]Coldkey Details:[/bold]
• Name: {name}
• Address: {keypair_info.ss58_address}
• Type: {key_type}

[bold]What is a Coldkey?[/bold]
• Controls account ownership and funds
• Should be kept offline/secure
• Used for critical operations
• Can own multiple hotkeys

[bold]Usage Examples:[/bold]
• Register subnet: htcli subnet register (uses this coldkey)
• Create hotkey: htcli wallet generate-hotkey --owner {keypair_info.ss58_address}

[yellow]⚠️ Security Warning:[/yellow] Keep this coldkey secure - it controls your funds!
"""

RESTORE_GUIDANCE_TEMPLATE = """
[bold cyan]🔑 Key Imported Successfully[/bold cyan]

[bold]Imported Key Details:[/bold]
• Name: {name}
• Address: {address}
• Type: {key_type}
• Import Method: {import_method}

[bold]What was imported?[/bold]
• Your private key has been securely stored
• The key is encrypted with your password
• You can now use this key for operations

[bold]Usage Examples:[/bold]
• View key: htcli wallet list
• Use for operations: htcli subnet register
• Check status: htcli wallet status

[yellow]💡 Security Tip:[/yellow] Keep your private key and mnemonic secure and never share them!
"""


COLDKEY_RESTORE_GUIDANCE_TEMPLATE = """
[bold cyan]🔐 Coldkey Imported Successfully[/bold cyan]

[bold]Imported Coldkey Details:[/bold]
• Name: {name}
• Address: {address}
• Type: {key_type}
• Import Method: {import_method}

[bold]What was imported?[/bold]
• Your coldkey private key has been securely stored
• The key is encrypted with your password
• You can now use this coldkey for operations

[bold]What is a Coldkey?[/bold]
• Controls account ownership and funds
• Should be kept offline/secure
• Used for critical operations
• Can own multiple hotkeys

[bold]Usage Examples:[/bold]
• View key: htcli wallet list
• Register subnet: htcli subnet register
• Create hotkey: htcli wallet generate-hotkey --owner {name}
• Check status: htcli wallet status

[yellow]⚠️ Security Warning:[/yellow] Keep this coldkey secure - it controls your funds!
"""


HOTKEY_RESTORE_GUIDANCE_TEMPLATE = """
[bold cyan]🔑 Hotkey Imported Successfully[/bold cyan]

[bold]Imported Hotkey Details:[/bold]
• Name: {name}
• Address: {address}
• Type: {key_type}
• Import Method: {import_method}
• Owner: {owner_name} ({owner_address})

[bold]What was imported?[/bold]
• Your hotkey private key has been securely stored
• The key is encrypted with your password
• You can now use this hotkey for operations

[bold]What is a Hotkey?[/bold]
• Used for operational tasks (consensus, validation)
• Owned by your coldkey for security
• Can be kept online for frequent operations
• Cannot transfer funds directly

[bold]Usage Examples:[/bold]
• View key: htcli wallet list
• Register node: htcli node register --hotkey {address}
• Update hotkey: htcli wallet update-hotkey --old-hotkey {address}
• Check status: htcli wallet status

[yellow]💡 Security Tip:[/yellow] Keep your coldkey secure, hotkey can be rotated if compromised
"""


# guidance_templates.py

WALLET_STATUS_GUIDANCE_TEMPLATE = """
[bold yellow]🔑 Key Status Guide[/bold yellow]

• Your coldkey controls funds and ownership.
• Your hotkey is used for operations (staking, consensus, etc).
• Both are needed for full participation in the network.

💡 Use this command often to ensure your keys are active and ready.
"""

NO_KEYS_TEMPLATE = """
[bold red]❌ No Keys Found[/bold red]

You don't have any keys stored yet. To get started:

1. [cyan]Generate a new key:[/cyan]
   htcli wallet generate-key --name my-wallet

2. [cyan]Check your identity:[/cyan]
   htcli wallet status
"""

IDENTITY_TEMPLATE = """
[bold green]✅ Blockchain Identity Active[/bold green]

• [bold]Keys Found:[/bold] {num_keys}
• [bold]Addresses:[/bold] {num_addresses}
• [bold]Network:[/bold] Hypertensor
• [bold]Status:[/bold] Ready for operations
"""

CAPABILITIES_TEMPLATE = """
[bold blue]🚀 What You Can Do:[/bold blue]

✅ [green]Sign transactions[/green] (staking, subnet operations)
✅ [green]Own assets[/green] (subnets, nodes, stakes)
✅ [green]Filter results[/green] (use --mine flag)
✅ [green]Earn rewards[/green] (staking rewards)
✅ [green]Participate in governance[/green] (voting, proposals)
"""


WALLET_DELETE_GUIDANCE_TEMPLATE = """
[bold red]🗑️ Key Deleted Successfully[/bold red]

[bold]Deleted Key:[/bold] {name}

[bold]What happened?[/bold]
• The key has been permanently removed from your system
• The encrypted private key file has been deleted
• You can no longer use this key for operations

[bold]Important Notes:[/bold]
• If you had funds associated with this key, they are still on the blockchain
• You can recover them by importing the private key again
• Make sure you have a backup of the private key if needed

[yellow]⚠️ Warning:[/yellow] This action cannot be undone!
"""


COLDKEY_UPDATE_GUIDANCE_TEMPLATE = """
[bold green]🔐 Coldkey Updated Successfully[/bold green]

[bold]Updated Coldkey Details:[/bold]
• Old Name: {old_name}
• New Name: {new_name}
• Type: {key_type}
• Address: {ss58_address}

[bold]Changes Made:[/bold]
• Name Updated: {name_updated_status}
• Password Updated: {password_updated_status}

[bold]What this means:[/bold]
• The coldkey has been updated with your requested changes
• The private key and address remain the same
• All associated hotkeys will continue to work normally

[bold]Security Notes:[/bold]
• The private key is still stored securely on your local machine
• If you changed the password, make sure to remember the new one
• If you removed the password, the key is now stored unencrypted

[bold]Next Steps:[/bold]
• Use 'htcli wallet list' to see the updated key
• Use 'htcli wallet status' to verify the changes
• Continue using this coldkey for fund management and ownership
"""


HOTKEY_UPDATE_GUIDANCE_TEMPLATE = """
[bold green]🔑 Hotkey Updated Successfully[/bold green]

[bold]Updated Hotkey Details:[/bold]
• Old Name: {old_name}
• New Name: {new_name}
• Type: {key_type}
• Address: {ss58_address}
• Old Owner: {old_owner_address}
• New Owner: {new_owner_address}

[bold]Changes Made:[/bold]
• Name Updated: {name_updated_status}
• Password Updated: {password_updated_status}
• Owner Updated: {owner_updated_status}

[bold]What this means:[/bold]
• The hotkey has been updated with your requested changes
• The private key and address remain the same
• The hotkey will now be owned by the new coldkey (if changed)

[bold]Security Notes:[/bold]
• The private key is still stored securely on your local machine
• If you changed the password, make sure to remember the new one
• If you removed the password, the key is now stored unencrypted
• If you changed the owner, the hotkey is now controlled by a different coldkey

[bold]Next Steps:[/bold]
• Use 'htcli wallet list' to see the updated key
• Use 'htcli wallet status' to verify the changes
• Continue using this hotkey for node operations and consensus signing
"""
