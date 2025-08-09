# TENSOR Token Precision Guide

## Overview

The TENSOR token uses **18 decimal places** for precision, which is the standard for most modern blockchain tokens (similar to Ethereum's ERC-20 tokens). This guide explains how the precision is implemented throughout the Hypertensor CLI.

## Precision Implementation

### Constants

```python
# TENSOR token precision constant
TENSOR_DECIMALS = 18
```

### Key Functions

#### `format_balance(amount: int, decimals: int = TENSOR_DECIMALS) -> str`

Formats TENSOR amounts with proper 18-decimal precision.

**Example:**

```python
# 1 TENSOR in smallest unit
amount = 1000000000000000000000  # 18 zeros
formatted = format_balance(amount)  # "1.0 TENSOR"

# 0.5 TENSOR in smallest unit
amount = 500000000000000000000   # 17 zeros
formatted = format_balance(amount)  # "0.5 TENSOR"
```

#### `tensor_to_smallest_unit(tensor_amount: float) -> int`

Converts TENSOR amount to smallest unit (18 decimals).

**Example:**

```python
tensor_amount = 1.5
smallest_unit = tensor_to_smallest_unit(tensor_amount)  # 1500000000000000000000
```

#### `smallest_unit_to_tensor(smallest_unit: int) -> float`

Converts smallest unit to TENSOR amount (18 decimals).

**Example:**

```python
smallest_unit = 1500000000000000000000
tensor_amount = smallest_unit_to_tensor(smallest_unit)  # 1.5
```

#### `validate_tensor_amount(amount: float) -> bool`

Validates TENSOR amount has proper precision (max 18 decimal places).

## Usage Examples

### Staking Operations

```python
# Add 1.5 TENSOR stake
stake_amount = tensor_to_smallest_unit(1.5)  # 1500000000000000000000
request = StakeAddRequest(
    subnet_id=1,
    node_id=1,
    hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
    stake_to_be_added=stake_amount
)
```

### Balance Display

```python
# Display balance with proper formatting
balance_smallest_unit = 31662054793350007812500
formatted_balance = format_balance(balance_smallest_unit)  # "31.6621 TENSOR"
```

### Validation

```python
# Validate TENSOR amount
amount = 1.5
if validate_tensor_amount(amount):
    # Amount is valid
    smallest_unit = tensor_to_smallest_unit(amount)
else:
    # Amount has too many decimal places
    print("Invalid TENSOR amount precision")
```

## Test Data Updates

All test files have been updated to use 18-digit precision:

### Before (9 decimals)

```python
stake_amount = 1000000000000  # 1 TENSOR (9 decimals)
```

### After (18 decimals)

```python
stake_amount = 1000000000000000000000  # 1 TENSOR (18 decimals)
```

## Common Values

| TENSOR Amount | Smallest Unit (18 decimals) |
|---------------|----------------------------|
| 0.1 TENSOR    | 100000000000000000000     |
| 0.5 TENSOR    | 500000000000000000000     |
| 1.0 TENSOR    | 1000000000000000000000    |
| 1.5 TENSOR    | 1500000000000000000000    |
| 2.0 TENSOR    | 2000000000000000000000    |
| 5.0 TENSOR    | 5000000000000000000000    |
| 10.0 TENSOR   | 10000000000000000000000   |

## Validation Rules

1. **Maximum Precision**: TENSOR amounts cannot have more than 18 decimal places
2. **Positive Values**: All stake amounts must be positive
3. **Balance**: Account balances can be zero or positive
4. **Formatting**: All displayed amounts use 18-decimal precision

## Error Handling

The CLI includes comprehensive error handling for precision issues:

- **Invalid Precision**: Amounts with more than 18 decimal places are rejected
- **Negative Values**: Negative stake amounts are rejected
- **Format Errors**: Invalid number formats are caught and reported

## Migration Notes

If you're migrating from a system using different precision:

1. **Multiply by 10^9**: If coming from 9-decimal system
2. **Update Test Data**: All test values updated to 18 decimals
3. **Validate Inputs**: Use `validate_tensor_amount()` for user inputs
4. **Format Outputs**: Use `format_balance()` for all displays

## Best Practices

1. **Always use the utility functions** for conversions
2. **Validate user inputs** before processing
3. **Use the TENSOR_DECIMALS constant** for consistency
4. **Test with realistic amounts** (not just whole numbers)
5. **Handle edge cases** (zero amounts, very small amounts)
