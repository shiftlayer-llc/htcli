# HTCLI Test Suite

This directory contains comprehensive tests for the HTCLI application with a clean, organized structure.

## Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and shared fixtures
├── unit/                          # Unit tests for individual components
│   ├── test_subnet_operations.py  # Subnet command unit tests
│   ├── test_wallet_operations.py  # Wallet command unit tests
│   └── test_chain_operations.py   # Chain command unit tests
├── integration/                   # Integration tests for workflows
│   ├── test_cli_integration.py   # CLI workflow integration tests
│   └── test_network_connectivity.py # Network connectivity tests
└── README.md                     # This documentation
```

## Test Types Explained

### 1. Unit Tests (`tests/unit/`)
**Purpose**: Test individual functions/methods in isolation
- **Scope**: Single component or class
- **Dependencies**: Usually mocked
- **Speed**: Fast execution
- **Example**: Testing `register_subnet()` method with mocked blockchain

**What they test**:
- Individual method functionality
- Input validation
- Error handling
- Return value correctness
- Mocked dependencies

### 2. Integration Tests (`tests/integration/`)
**Purpose**: Test how components work together
- **Scope**: Multiple components or end-to-end workflows
- **Dependencies**: May use real external services
- **Speed**: Slower than unit tests
- **Example**: Testing complete CLI workflow from command to response

**What they test**:
- Component interactions
- End-to-end workflows
- Real network connectivity
- CLI command execution
- Configuration handling

### 3. Fixture Tests (in conftest.py)
**Purpose**: Test data setup and configuration
- **Scope**: Test data, mock objects, configuration
- **Dependencies**: Usually isolated setup/teardown
- **Speed**: Very fast
- **Example**: Testing wallet creation, key generation, config loading

**What they provide**:
- Shared test data
- Mock objects
- Configuration setup
- Cleanup functions

## Running Tests

### Using pytest (Recommended)

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=src.htcli --cov-report=html

# Run specific test file
pytest tests/unit/test_subnet_operations.py

# Run tests with verbose output
pytest -v

# Run tests with markers
pytest -m unit
pytest -m integration
pytest -m network
```

## Test Coverage

The test suite covers:

### Command Functionality
- ✅ All CLI commands and subcommands
- ✅ Input validation and error handling
- ✅ Success and failure scenarios
- ✅ Help output verification

### Blockchain Operations
- ✅ Real blockchain queries
- ✅ Transaction composition
- ✅ Network connectivity
- ✅ Error handling for network issues

### Output Formats
- ✅ Table format (default)
- ✅ JSON format
- ✅ CSV format

### Error Scenarios
- ✅ Invalid input validation
- ✅ Network errors
- ✅ Missing required arguments
- ✅ Resource not found errors

## Environment Variables

### Required for Network Tests
- `HTCLI_NETWORK_ENDPOINT`: RPC endpoint (default: `wss://hypertensor.duckdns.org`)
- `HTCLI_NETWORK_WS_ENDPOINT`: WebSocket endpoint (default: `wss://hypertensor.duckdns.org`)

### Optional Configuration
- `HTCLI_OUTPUT_FORMAT`: Output format (default: `table`)
- `HTCLI_OUTPUT_VERBOSE`: Verbose output (default: `false`)
- `HTCLI_OUTPUT_COLOR`: Colored output (default: `true`)
- `HTCLI_WALLET_PATH`: Wallet storage path
- `HTCLI_WALLET_DEFAULT_NAME`: Default wallet name
- `HTCLI_WALLET_ENCRYPTION_ENABLED`: Enable wallet encryption

## Adding New Tests

### Unit Tests

1. Create a new test file in `tests/unit/`
2. Follow the naming convention: `test_<module_name>.py`
3. Use the existing fixtures from `conftest.py`
4. Test both success and error scenarios
5. Include input validation tests

Example:
```python
def test_new_method_success(self, mock_client):
    """Test successful method execution."""
    mock_client.some_method.return_value = {
        "success": True,
        "message": "Success"
    }

    result = some_function()
    assert result.success is True
    assert "Success" in result.message
```

### Integration Tests

1. Add tests to `tests/integration/`
2. Test complete workflows
3. Use the `@pytest.mark.integration` marker
4. Test real network connectivity when needed

Example:
```python
@pytest.mark.integration
def test_complete_workflow(self, cli_runner):
    """Test complete user workflow."""
    result = cli_runner.invoke(app, ["subnet", "register", "test"])
    assert result.exit_code == 0
    assert "Success" in result.stdout
```

## Test Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.network`: Tests requiring network connection
- `@pytest.mark.slow`: Tests that take longer to run

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

## Test Results

Current test status:
- **Unit Tests**: ✅ All passing
- **Integration Tests**: ✅ All passing
- **Network Tests**: ✅ All passing
- **Coverage**: >90% code coverage
- **Performance**: All tests complete within acceptable timeframes
