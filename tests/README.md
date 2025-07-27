# HTCLI Test Suite

This directory contains comprehensive tests for the HTCLI application.

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_subnet_register.py
│   ├── test_subnet_manage.py
│   ├── test_subnet_nodes.py
│   ├── test_wallet_keys.py
│   ├── test_wallet_staking.py
│   ├── test_chain_info.py
│   └── test_chain_query.py
├── integration/             # Integration tests
│   └── test_cli_integration.py
└── fixtures/               # Test fixtures and data
```

## Running Tests

### Using the Test Runner

```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --type unit

# Run only integration tests
python run_tests.py --type integration

# Run with verbose output
python run_tests.py -v

# Run with coverage report
python run_tests.py --coverage
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_subnet_register.py

# Run tests with specific marker
pytest -m unit
pytest -m integration

# Run tests with coverage
pytest --cov=src.htcli --cov-report=html
```

## Environment Variables

The following environment variables are used for testing:

### Required for Network Tests
- `HTCLI_NETWORK_ENDPOINT`: RPC endpoint (default: `wss://hypertensor.duckdns.org`)
- `HTCLI_NETWORK_WS_ENDPOINT`: WebSocket endpoint (default: `wss://hypertensor.duckdns.org`)

### Hypertensor Network Endpoint

The test suite is configured to use the Hypertensor blockchain endpoint:
- **Endpoint**: `wss://hypertensor.duckdns.org`
- **Protocol**: WebSocket Secure (WSS)
- **Network**: Hypertensor mainnet

This endpoint is used for:
- Network connectivity tests
- Real blockchain interaction tests
- Integration tests with live network

### Optional Configuration
- `HTCLI_OUTPUT_FORMAT`: Output format (default: `table`)
- `HTCLI_OUTPUT_VERBOSE`: Verbose output (default: `false`)
- `HTCLI_OUTPUT_COLOR`: Colored output (default: `true`)
- `HTCLI_WALLET_PATH`: Wallet storage path
- `HTCLI_WALLET_DEFAULT_NAME`: Default wallet name
- `HTCLI_WALLET_ENCRYPTION_ENABLED`: Enable wallet encryption

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests focus on testing individual components in isolation:

- **Subnet Commands**: Test subnet registration, management, and node operations
- **Wallet Commands**: Test key generation, import, deletion, and staking operations
- **Chain Commands**: Test network info, account queries, and balance operations

Each test file includes:
- Success scenarios
- Error handling
- Input validation
- Help output verification
- Output format testing (JSON, CSV, table)

### Integration Tests (`tests/integration/`)

Integration tests verify that components work together:

- **CLI Integration**: Test the complete CLI application
- **End-to-End Workflows**: Test complete user workflows
- **Command Help**: Verify all commands have proper help output
- **Configuration**: Test CLI configuration options

## Test Fixtures

The `conftest.py` file provides common fixtures:

- `cli_runner`: Typer CLI runner for testing commands
- `mock_config`: Mock configuration for testing
- `mock_client`: Mock HypertensorClient for testing
- `test_wallet_dir`: Temporary wallet directory
- `sample_keypair`: Sample keypair data
- `sample_subnet_data`: Sample subnet data
- `sample_account_data`: Sample account data
- `sample_network_stats`: Sample network statistics
- `env_vars`: Environment variable setup

## Test Coverage

The test suite covers:

### Command Functionality
- ✅ All CLI commands and subcommands
- ✅ Input validation and error handling
- ✅ Success and failure scenarios
- ✅ Help output verification

### Output Formats
- ✅ Table format (default)
- ✅ JSON format
- ✅ CSV format

### Error Scenarios
- ✅ Invalid input validation
- ✅ Network errors
- ✅ Missing required arguments
- ✅ Resource not found errors

### Integration
- ✅ End-to-end workflows
- ✅ Configuration management
- ✅ Environment variable handling

## Adding New Tests

### Unit Tests

1. Create a new test file in `tests/unit/`
2. Follow the naming convention: `test_<module_name>.py`
3. Use the existing fixtures from `conftest.py`
4. Test both success and error scenarios
5. Include help output tests

Example:
```python
def test_new_command_success(self, cli_runner, mock_client):
    """Test successful command execution."""
    with patch('src.htcli.commands.module.get_client', return_value=mock_client):
        mock_client.some_method.return_value = {
            "success": True,
            "message": "Success"
        }

        result = cli_runner.invoke(app, ["command", "arg"])

        assert result.exit_code == 0
        assert "Success" in result.stdout
```

### Integration Tests

1. Add tests to `tests/integration/test_cli_integration.py`
2. Test complete workflows
3. Use the `@pytest.mark.integration` marker
4. Mock external dependencies

## Running Tests in CI/CD

The test suite is designed to run in CI/CD environments:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    python run_tests.py --coverage
    pytest --cov=src.htcli --cov-report=xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the project is installed in development mode:
   ```bash
   pip install -e .
   ```

2. **Missing Dependencies**: Install test dependencies:
   ```bash
   pip install pytest pytest-cov
   ```

3. **Network Tests**: For tests requiring network connection:
   ```bash
   pytest -m network
   ```

4. **Slow Tests**: For tests that take longer to run:
   ```bash
   pytest -m slow
   ```

### Debug Mode

Run tests with debug output:
```bash
pytest -v -s --tb=long
```

## Coverage Reports

Generate coverage reports:
```bash
# HTML report
pytest --cov=src.htcli --cov-report=html

# XML report (for CI/CD)
pytest --cov=src.htcli --cov-report=xml

# Terminal report
pytest --cov=src.htcli --cov-report=term-missing
```

The HTML report will be generated in `htmlcov/index.html`.
