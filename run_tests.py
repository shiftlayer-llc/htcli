#!/usr/bin/env python3
"""
Test runner for htcli project.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=False):
    """Run tests with specified options."""
    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=src.htcli", "--cov-report=term-missing", "--cov-report=html"])

    if test_type == "unit":
        cmd.append("tests/unit/")
    elif test_type == "integration":
        cmd.append("tests/integration/")
    elif test_type == "all":
        cmd.append("tests/")
    else:
        print(f"Unknown test type: {test_type}")
        return False

    print(f"Running {test_type} tests...")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode == 0


def main():
    """Main test runner function."""
    import argparse

    parser = argparse.ArgumentParser(description="Run htcli tests")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "all"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report"
    )

    args = parser.parse_args()

    # Set environment variables for testing
    os.environ.setdefault("HTCLI_NETWORK_ENDPOINT", "wss://hypertensor.duckdns.org")
    os.environ.setdefault("HTCLI_NETWORK_WS_ENDPOINT", "wss://hypertensor.duckdns.org")
    os.environ.setdefault("HTCLI_OUTPUT_FORMAT", "table")
    os.environ.setdefault("HTCLI_OUTPUT_VERBOSE", "false")
    os.environ.setdefault("HTCLI_OUTPUT_COLOR", "true")

    success = run_tests(args.type, args.verbose, args.coverage)

    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
