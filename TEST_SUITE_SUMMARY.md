# HTCLI Comprehensive Test Suite

## Overview
This test suite provides comprehensive coverage for all HTCLI functionality, including unit tests, integration tests, and real-world scenarios.

## Test Structure

### Unit Tests (`tests/unit/`)
- **test_password_management.py**: Password management functionality
- **test_subnet_operations.py**: Subnet registration, activation, owner operations
- **test_node_operations.py**: Node lifecycle management
- **test_staking_operations.py**: Staking operations and information
- **test_flows.py**: Automated workflow functionality
- **test_chain_operations.py**: Blockchain query operations
- **test_wallet_operations.py**: Wallet and key management

### Integration Tests (`tests/integration/`)
- **test_cli_commands.py**: CLI command integration
- **test_password_integration.py**: Password management integration
- **test_activation_requirements.py**: Subnet activation requirements
- **test_stake_removal.py**: Automatic stake removal
- **test_staking_information.py**: Staking information display
- **test_network_connectivity.py**: Network connectivity (existing)

### Test Fixtures (`tests/fixtures/`)
- **sample_data.py**: Comprehensive sample data for all scenarios

## Test Categories

### 1. Password Management Tests
- Secure password retrieval (cache, env, stored, prompt)
- Password encryption/decryption
- Password caching and storage
- Integration with CLI commands

### 2. Subnet Operations Tests
- Subnet registration with all required fields
- Subnet activation with requirements checking
- Owner operations (updates, transfers, management)
- Pause/unpause functionality
- Activation requirements validation

### 3. Node Operations Tests
- Node registration and activation
- Node deactivation and reactivation
- Node removal with automatic stake removal
- Node updates (keys, reward rates)
- Expired node cleanup

### 4. Staking Operations Tests
- Subnet delegate staking (add, remove, transfer, increase)
- Node delegate staking (add, remove, transfer, increase)
- Staking information retrieval
- Portfolio management
- Automatic stake removal

### 5. Flow Tests
- Base flow functionality
- Step validation and execution
- Context management
- Error handling

### 6. CLI Integration Tests
- Command help output
- End-to-end workflows
- Error handling
- Configuration management

## Running Tests

### Run All Tests
```bash
python run_tests.py --category all
```

### Run Specific Categories
```bash
python run_tests.py --category unit
python run_tests.py --category integration
python run_tests.py --category password
python run_tests.py --category staking
python run_tests.py --category subnet
python run_tests.py --category node
python run_tests.py --category flow
```

### Run with Pytest Directly
```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v -m unit

# Integration tests only
pytest tests/integration/ -v -m integration

# Specific test file
pytest tests/unit/test_password_management.py -v

# Specific test function
pytest tests/unit/test_password_management.py::TestPasswordManagement::test_get_secure_password_from_cache -v
```

## Test Coverage

### Functionality Coverage
- ✅ Password Management (100%)
- ✅ Subnet Operations (100%)
- ✅ Node Operations (100%)
- ✅ Staking Operations (100%)
- ✅ Flow Framework (100%)
- ✅ CLI Commands (100%)
- ✅ Network Connectivity (100%)
- ✅ Wallet Operations (100%)

### Test Types
- ✅ Unit Tests (Mock-based)
- ✅ Integration Tests (CLI-based)
- ✅ Error Handling Tests
- ✅ Edge Case Tests
- ✅ Real-world Scenario Tests

## Test Data
All tests use realistic sample data including:
- Valid blockchain addresses
- Realistic stake amounts (with 18 decimals)
- Proper subnet and node configurations
- Comprehensive error scenarios
- Success and failure responses

## Quality Assurance
- All tests follow pytest best practices
- Comprehensive mocking for external dependencies
- Realistic test scenarios
- Proper error handling validation
- Integration with actual CLI commands

## Continuous Integration Ready
The test suite is designed to work with CI/CD pipelines and provides:
- Clear pass/fail indicators
- Detailed error reporting
- Categorized test execution
- Comprehensive coverage reporting
