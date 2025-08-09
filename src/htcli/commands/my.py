"""
User-specific "My Assets" commands for the Hypertensor CLI.
Shows only assets owned by the user's wallet addresses.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
from ..utils.crypto import list_keys
from ..utils.formatting import (
    print_success, print_error, print_info, format_balance
)
from ..dependencies import get_client

app = typer.Typer(name="my", help="View your personal assets and ownership")
console = Console()


def get_user_addresses():
    """Get all wallet addresses for the current user."""
    try:
        keys = list_keys()
        if not keys:
            return []
        return [(key.get('name', 'Unknown'), key.get('address', '')) for key in keys if key.get('address')]
    except Exception as e:
        print_error(f"Failed to get wallet addresses: {e}")
        return []


@app.command()
def subnets(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Show only subnets that you own."""
    client = get_client()
    
    # Get user addresses
    user_addresses = get_user_addresses()
    if not user_addresses:
        print_error("❌ No wallet addresses found. Generate a key first:")
        print_info("   htcli wallet generate-key --name my-key")
        raise typer.Exit(1)
    
    print_info(f"🔍 Checking ownership for {len(user_addresses)} wallet address(es)...")
    
    # Check subnet ownership
    owned_subnets = []
    
    try:
        # Check each subnet to see if user owns it
        for subnet_id in range(1, 20):  # Check first 20 subnet IDs
            try:
                subnet_response = client.subnet.get_subnet_data(subnet_id)
                if subnet_response.success:
                    subnet_data = subnet_response.data
                    owner = subnet_data.get('owner', '')
                    
                    # Check if this user owns the subnet
                    user_owns = any(owner == addr for _, addr in user_addresses)
                    
                    if user_owns:
                        # Find which key owns it
                        owner_key = next((name for name, addr in user_addresses if addr == owner), 'Unknown')
                        
                        owned_subnets.append({
                            'subnet_id': subnet_id,
                            'name': subnet_data.get('name', f'Subnet-{subnet_id}'),
                            'state': subnet_data.get('state', 'Unknown'),
                            'owner_key': owner_key,
                            'owner_address': owner,
                            'total_nodes': subnet_data.get('total_nodes', 0),
                            'total_active_nodes': subnet_data.get('total_active_nodes', 0),
                            'delegate_stake_balance': subnet_data.get('total_delegate_stake_balance', 0),
                            'data_completeness': subnet_data.get('data_completeness', 'unknown')
                        })
            except:
                # Skip subnets that don't exist or error
                continue
        
        if format_type == "json":
            import json
            console.print(json.dumps(owned_subnets, indent=2))
        else:
            if owned_subnets:
                table = Table(title=f"🏗️ Your Owned Subnets ({len(owned_subnets)} found)")
                table.add_column("Subnet ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("State", style="yellow")
                table.add_column("Owner Key", style="magenta")
                table.add_column("Nodes", style="blue")
                table.add_column("Delegate Stake", style="red")
                
                for subnet in owned_subnets:
                    table.add_row(
                        str(subnet['subnet_id']),
                        subnet['name'],
                        subnet['state'],
                        subnet['owner_key'],
                        f"{subnet['total_active_nodes']}/{subnet['total_nodes']}",
                        format_balance(subnet['delegate_stake_balance'])
                    )
                
                console.print(table)
                print_success(f"✅ Found {len(owned_subnets)} subnet(s) owned by you")
            else:
                console.print(Panel(
                    "[yellow]No subnets found that you own.[/yellow]\n\n"
                    "[bold]To register a subnet:[/bold]\n"
                    "htcli subnet register --path my-subnet --memory 2048 --blocks 1000 --interval 100\n\n"
                    "[bold]Your wallet addresses:[/bold]\n" + 
                    "\n".join([f"• {name}: {addr[:20]}..." for name, addr in user_addresses]),
                    title="🏗️ Your Subnets",
                    border_style="yellow"
                ))
        
    except Exception as e:
        print_error(f"Failed to check subnet ownership: {str(e)}")
        raise typer.Exit(1)


@app.command() 
def stakes(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Show all your staking positions across all subnets."""
    client = get_client()
    
    # Get user addresses
    user_addresses = get_user_addresses()
    if not user_addresses:
        print_error("❌ No wallet addresses found. Generate a key first:")
        print_info("   htcli wallet generate-key --name my-key")
        raise typer.Exit(1)
    
    print_info(f"🔍 Checking stakes for {len(user_addresses)} wallet address(es)...")
    
    all_stakes = []
    
    try:
        # Check each address for stakes in all subnets
        for key_name, address in user_addresses:
            for subnet_id in range(1, 10):  # Check first 10 subnets
                try:
                    stake_response = client.staking.get_account_subnet_stake(address, subnet_id)
                    if stake_response.success and stake_response.data:
                        stake_data = stake_response.data
                        total_stake = stake_data.get('total_stake', 0)
                        
                        if total_stake > 0:
                            all_stakes.append({
                                'key_name': key_name,
                                'address': address,
                                'subnet_id': subnet_id,
                                'total_stake': total_stake,
                                'rewards': stake_data.get('rewards', 0),
                                'unbonding': stake_data.get('unbonding', 0)
                            })
                except:
                    # Skip non-existent stakes
                    continue
        
        if format_type == "json":
            import json
            console.print(json.dumps(all_stakes, indent=2))
        else:
            if all_stakes:
                table = Table(title=f"📈 Your Stake Positions ({len(all_stakes)} found)")
                table.add_column("Key Name", style="magenta")
                table.add_column("Subnet ID", style="cyan") 
                table.add_column("Staked Amount", style="green")
                table.add_column("Rewards", style="yellow")
                table.add_column("Unbonding", style="red")
                
                total_staked = 0
                total_rewards = 0
                
                for stake in all_stakes:
                    table.add_row(
                        stake['key_name'],
                        str(stake['subnet_id']),
                        format_balance(stake['total_stake']),
                        format_balance(stake['rewards']),
                        format_balance(stake['unbonding'])
                    )
                    total_staked += stake['total_stake']
                    total_rewards += stake['rewards']
                
                console.print(table)
                
                # Summary panel
                summary = Panel(
                    f"[bold green]Total Staked:[/bold green] {format_balance(total_staked)}\n"
                    f"[bold yellow]Total Rewards:[/bold yellow] {format_balance(total_rewards)}\n"
                    f"[bold cyan]Active Positions:[/bold cyan] {len(all_stakes)}",
                    title="📊 Staking Summary",
                    border_style="green"
                )
                console.print(summary)
                
            else:
                console.print(Panel(
                    "[yellow]No active stakes found for your addresses.[/yellow]\n\n"
                    "[bold]To start staking:[/bold]\n"
                    "htcli stake add --subnet-id 1 --node-id 1 --hotkey <address> --amount 1000000000000000000\n\n"
                    "[bold]Your wallet addresses:[/bold]\n" + 
                    "\n".join([f"• {name}: {addr[:20]}..." for name, addr in user_addresses]),
                    title="📈 Your Stakes",
                    border_style="yellow"
                ))
        
    except Exception as e:
        print_error(f"Failed to check stake positions: {str(e)}")
        raise typer.Exit(1)


@app.command()
def balances(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Show balances for all your wallet addresses."""
    client = get_client()
    
    # Get user addresses
    user_addresses = get_user_addresses()
    if not user_addresses:
        print_error("❌ No wallet addresses found. Generate a key first:")
        print_info("   htcli wallet generate-key --name my-key")
        raise typer.Exit(1)
    
    print_info(f"💰 Checking balances for {len(user_addresses)} wallet address(es)...")
    
    balances = []
    
    try:
        for key_name, address in user_addresses:
            try:
                balance_response = client.chain.get_balance(address)
                if balance_response.success:
                    balance_data = balance_response.data
                    balances.append({
                        'key_name': key_name,
                        'address': address,
                        'free': balance_data.get('free', 0),
                        'reserved': balance_data.get('reserved', 0),
                        'total': balance_data.get('total', 0)
                    })
                else:
                    balances.append({
                        'key_name': key_name,
                        'address': address,
                        'free': 0,
                        'reserved': 0,
                        'total': 0,
                        'error': 'Failed to query'
                    })
            except Exception as e:
                balances.append({
                    'key_name': key_name,
                    'address': address,
                    'free': 0,
                    'reserved': 0,
                    'total': 0,
                    'error': str(e)
                })
        
        if format_type == "json":
            import json
            console.print(json.dumps(balances, indent=2))
        else:
            table = Table(title=f"💰 Your Wallet Balances ({len(balances)} addresses)")
            table.add_column("Key Name", style="magenta")
            table.add_column("Address", style="cyan")
            table.add_column("Free Balance", style="green")
            table.add_column("Reserved", style="yellow")
            table.add_column("Total Balance", style="bold green")
            
            total_free = 0
            total_reserved = 0
            total_balance = 0
            
            for balance in balances:
                if 'error' in balance:
                    table.add_row(
                        balance['key_name'],
                        balance['address'][:20] + "...",
                        "[red]Error[/red]",
                        "[red]Error[/red]",
                        "[red]Error[/red]"
                    )
                else:
                    table.add_row(
                        balance['key_name'],
                        balance['address'][:20] + "...",
                        format_balance(balance['free']),
                        format_balance(balance['reserved']),
                        format_balance(balance['total'])
                    )
                    total_free += balance['free']
                    total_reserved += balance['reserved']
                    total_balance += balance['total']
            
            console.print(table)
            
            # Summary
            summary = Panel(
                f"[bold green]Total Free:[/bold green] {format_balance(total_free)}\n"
                f"[bold yellow]Total Reserved:[/bold yellow] {format_balance(total_reserved)}\n"
                f"[bold cyan]Grand Total:[/bold cyan] {format_balance(total_balance)}",
                title="📊 Balance Summary",
                border_style="green"
            )
            console.print(summary)
        
    except Exception as e:
        print_error(f"Failed to check balances: {str(e)}")
        raise typer.Exit(1)


@app.command()
def overview(
    format_type: str = typer.Option("table", "--format", "-f", help="Output format (table/json)")
):
    """Show a complete overview of all your assets."""
    console.print(Panel(
        "[bold cyan]Your Personal Asset Overview[/bold cyan]\n\n"
        "This command will show a comprehensive view of all your assets:\n"
        "• Owned subnets\n"
        "• Active stake positions\n" 
        "• Wallet balances\n"
        "• Node registrations",
        title="🎯 Personal Asset Overview",
        border_style="cyan"
    ))
    
    # Get user addresses first
    user_addresses = get_user_addresses()
    if not user_addresses:
        print_error("❌ No wallet addresses found. Generate a key first:")
        print_info("   htcli wallet generate-key --name my-key")
        raise typer.Exit(1)
    
    print_info(f"📊 Analyzing assets for {len(user_addresses)} wallet address(es)...")
    
    # Show addresses
    console.print("\n[bold]🔑 Your Wallet Addresses:[/bold]")
    for i, (name, address) in enumerate(user_addresses, 1):
        console.print(f"  {i}. [magenta]{name}[/magenta]: {address}")
    
    # Call other commands
    console.print("\n" + "="*60)
    console.print("[bold cyan]Your Owned Subnets:[/bold cyan]")
    try:
        # This will call the subnets command above
        ctx = typer.Context(subnets)
        ctx.invoke(subnets, format_type="table")
    except:
        print_info("No subnets found or error occurred")
    
    console.print("\n" + "="*60)
    console.print("[bold cyan]Your Stake Positions:[/bold cyan]")
    try:
        ctx = typer.Context(stakes)
        ctx.invoke(stakes, format_type="table")
    except:
        print_info("No stakes found or error occurred")
    
    console.print("\n" + "="*60)
    console.print("[bold cyan]Your Wallet Balances:[/bold cyan]")
    try:
        ctx = typer.Context(balances)
        ctx.invoke(balances, format_type="table")
    except:
        print_info("Balance check failed or error occurred")
