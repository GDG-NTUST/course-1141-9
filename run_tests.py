#!/usr/bin/env python
"""Script to run tests with various configurations."""

import logging
import subprocess
import sys

logger = logging.getLogger(__name__)


def run_command(cmd: list[str]) -> int:
    """Run a command and return its exit code."""
    logger.debug('\n%s', '=' * 60)
    logger.debug('Running: %s', ' '.join(cmd))
    logger.debug('%s\n', '=' * 60)
    result = subprocess.run(cmd, check=False)  # noqa: S603
    return result.returncode


def main():
    """Run different test configurations based on command line argument."""
    if len(sys.argv) < 2:
        logger.debug('Usage: python run_tests.py [all|fast|coverage|specific]')
        logger.debug('\nOptions:')
        logger.debug('  all       - Run all tests with detailed output')
        logger.debug('  fast      - Run tests without coverage')
        logger.debug('  coverage  - Run tests with HTML coverage report')
        logger.debug(
            '  specific  - Run specific test file (provide path as next arg)',
        )
        sys.exit(1)

    mode = sys.argv[1]

    if mode == 'all':
        return run_command(
            ['pytest', '-v', '--cov=nano_banana', '--cov-report=term-missing'],
        )

    if mode == 'fast':
        return run_command(['pytest', '-v'])

    if mode == 'coverage':
        exit_code = run_command(
            [
                'pytest',
                '--cov=nano_banana',
                '--cov-report=html',
                '--cov-report=term',
            ],
        )
        if exit_code == 0:
            logger.debug('\n✅ Coverage report generated in htmlcov/index.html')
        return exit_code

    if mode == 'specific':
        if len(sys.argv) < 3:
            logger.debug('Error: Please provide test file path')
            logger.debug(
                'Example: python run_tests.py specific tests/core/test_config.py',
            )
            sys.exit(1)
        test_path = sys.argv[2]
        return run_command(['pytest', '-v', test_path])

    logger.debug('Unknown mode: %s', mode)
    logger.debug("Use 'all', 'fast', 'coverage', or 'specific'")
    sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
