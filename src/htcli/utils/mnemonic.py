"""
Mnemonic display and clipboard utilities for htcli.
"""

import subprocess
import sys
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

console = Console()


def format_mnemonic_display(mnemonic: str, wallet_name: str, wallet_type: str = "Coldkey") -> str:
    """Format mnemonic for nice display."""
    words = mnemonic.split()
    
    # Create a formatted display with numbered words
    formatted_lines = []
    formatted_lines.append(f"🔐 {wallet_type} Recovery Phrase for '{wallet_name}'")
    formatted_lines.append("=" * 50)
    formatted_lines.append("")
    
    # Display words in rows of 4 with numbers
    for i in range(0, len(words), 4):
        row_words = words[i:i+4]
        row_line = ""
        for j, word in enumerate(row_words):
            word_num = i + j + 1
            row_line += f"{word_num:2d}. {word:<12}"
        formatted_lines.append(row_line)
    
    formatted_lines.append("")
    formatted_lines.append("⚠️  IMPORTANT: Save this phrase in a secure location!")
    formatted_lines.append("   You'll need it to recover your wallet if you lose access.")
    
    return "\n".join(formatted_lines)


def display_mnemonic_panel(mnemonic: str, wallet_name: str, wallet_type: str = "Coldkey"):
    """Display mnemonic in a beautiful panel."""
    formatted_mnemonic = format_mnemonic_display(mnemonic, wallet_name, wallet_type)
    
    panel = Panel(
        formatted_mnemonic,
        title=f"[bold red]🔐 {wallet_type} Recovery Phrase[/bold red]",
        border_style="red",
        padding=(1, 2),
        highlight=True
    )
    
    console.print(panel)
    console.print()


def create_mnemonic_table(mnemonic: str) -> Table:
    """Create a table display for mnemonic words."""
    words = mnemonic.split()
    
    table = Table(
        title="[bold red]🔐 Recovery Phrase Words[/bold red]",
        show_header=True,
        header_style="bold red",
        border_style="red"
    )
    
    # Add columns for 4 words per row
    for i in range(4):
        table.add_column(f"Word {i+1}", style="cyan", justify="left")
    
    # Add rows of 4 words each
    for i in range(0, len(words), 4):
        row_words = words[i:i+4]
        # Pad with empty strings if less than 4 words
        while len(row_words) < 4:
            row_words.append("")
        table.add_row(*row_words)
    
    return table


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard using system commands."""
    try:
        if sys.platform == "darwin":  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        elif sys.platform == "win32":  # Windows
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        else:  # Linux
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
        
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def prompt_for_mnemonic_copy(mnemonic: str, wallet_name: str) -> bool:
    """Prompt user to copy mnemonic to clipboard."""
    console.print("\n[bold yellow]💡 Quick Copy Option:[/bold yellow]")
    console.print("You can copy your recovery phrase to clipboard for easy saving.")
    
    if copy_to_clipboard(mnemonic):
        console.print("✅ Clipboard copy available!")
        
        copy_choice = Prompt.ask(
            "Copy recovery phrase to clipboard?",
            choices=["y", "n", "yes", "no"],
            default="n"
        )
        
        if copy_choice.lower() in ["y", "yes"]:
            console.print("✅ Recovery phrase copied to clipboard!")
            console.print("📋 You can now paste it in a secure location.")
            return True
        else:
            console.print("ℹ️  Recovery phrase not copied to clipboard.")
            return False
    else:
        console.print("⚠️  Clipboard not available on this system.")
        console.print("   Please manually copy the recovery phrase above.")
        return False


def display_mnemonic_with_copy_option(mnemonic: str, wallet_name: str, wallet_type: str = "Coldkey"):
    """Display mnemonic and offer clipboard copy option."""
    # Display the mnemonic in a beautiful panel
    display_mnemonic_panel(mnemonic, wallet_name, wallet_type)
    
    # Show the table format as well
    table = create_mnemonic_table(mnemonic)
    console.print(table)
    console.print()
    
    # Offer clipboard copy
    prompt_for_mnemonic_copy(mnemonic, wallet_name)
    
    # Final security reminder
    console.print("\n[bold red]🔒 Security Reminder:[/bold red]")
    console.print("• Store this recovery phrase in a secure, offline location")
    console.print("• Never share it with anyone")
    console.print("• Consider using a hardware wallet for additional security")
    console.print("• Test your recovery process in a safe environment")
    console.print()


def verify_mnemonic_backup(mnemonic: str) -> bool:
    """Verify that user has backed up their mnemonic."""
    console.print("\n[bold yellow]🔍 Backup Verification:[/bold yellow]")
    console.print("To ensure you've saved your recovery phrase, let's verify it.")
    
    # Ask user to confirm they've saved it
    saved_confirmation = Confirm.ask(
        "Have you saved your recovery phrase in a secure location?",
        default=False
    )
    
    if not saved_confirmation:
        console.print("⚠️  Please save your recovery phrase before continuing!")
        console.print("   You can scroll up to view it again.")
        return False
    
    # Optional: Ask user to verify by entering a few words
    verify_words = Confirm.ask(
        "Would you like to verify by entering a few words from your recovery phrase?",
        default=False
    )
    
    if verify_words:
        words = mnemonic.split()
        
        # Ask for 3 random words (positions 3, 7, 11 if they exist)
        test_positions = [3, 7, 11]
        test_words = []
        
        for pos in test_positions:
            if pos <= len(words):
                test_words.append((pos, words[pos-1]))
        
        if test_words:
            console.print("\n[bold cyan]Verification Test:[/bold cyan]")
            console.print("Please enter the following words from your recovery phrase:")
            
            all_correct = True
            for pos, correct_word in test_words:
                user_word = Prompt.ask(f"Word {pos}").strip().lower()
                if user_word != correct_word.lower():
                    console.print(f"❌ Incorrect. Word {pos} should be '{correct_word}'")
                    all_correct = False
                else:
                    console.print(f"✅ Correct!")
            
            if all_correct:
                console.print("\n🎉 Verification successful! Your recovery phrase is properly backed up.")
                return True
            else:
                console.print("\n⚠️  Verification failed. Please check your recovery phrase again.")
                return False
    
    console.print("\n✅ Backup confirmation received.")
    return True
