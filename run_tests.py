"""
Comprehensive test runner for HTCLI.
"""

import pytest
import sys
import os

def run_all_tests():
    """Run all tests in the project."""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Run all tests
    pytest.main([
        'tests/',
        '-v',
        '--tb=short',
        '--strict-markers',
        '--disable-warnings'
    ])

def run_unit_tests():
    """Run only unit tests."""
    pytest.main([
        'tests/unit/',
        '-v',
        '--tb=short',
        '--strict-markers',
        '--disable-warnings',
        '-m', 'unit'
    ])

def run_integration_tests():
    """Run only integration tests."""
    pytest.main([
        'tests/integration/',
        '-v',
        '--tb=short',
        '--strict-markers',
        '--disable-warnings',
        '-m', 'integration'
    ])

def run_specific_test_category(category):
    """Run tests for a specific category."""
    pytest.main([
        'tests/',
        '-v',
        '--tb=short',
        '--strict-markers',
        '--disable-warnings',
        '-m', category
    ])

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='HTCLI Test Runner')
    parser.add_argument('--category', choices=['all', 'unit', 'integration', 'password', 'staking', 'subnet', 'node', 'flow'], 
                       default='all', help='Test category to run')
    
    args = parser.parse_args()
    
    if args.category == 'all':
        run_all_tests()
    elif args.category == 'unit':
        run_unit_tests()
    elif args.category == 'integration':
        run_integration_tests()
    else:
        run_specific_test_category(args.category)
