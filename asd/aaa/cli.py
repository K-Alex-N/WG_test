#!/usr/bin/env python3
"""Command-line interface for the WG Test project."""

import argparse
import sys
from pathlib import Path

from config import DB_NAME, TEMP_DB_NAME
from db.create_db import create_db, verify_db_schema
from db.seed_db import seed_db
from db.tmp_db import create_tmp_db, drop_tmp_db, temp_db_exists
from db.logger import logger


def create_database_command(args) -> None:
    """Create the main database."""
    try:
        logger.info("Creating main database...")
        create_db(DB_NAME)
        if verify_db_schema(DB_NAME):
            logger.info("Database created and verified successfully")
        else:
            logger.error("Database creation failed verification")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        sys.exit(1)


def seed_database_command(args) -> None:
    """Seed the database with data."""
    try:
        logger.info("Seeding database...")
        seed_db(DB_NAME)
        logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
        sys.exit(1)


def create_temp_database_command(args) -> None:
    """Create temporary database for testing."""
    try:
        logger.info("Creating temporary database...")
        create_tmp_db()
        logger.info("Temporary database created successfully")
    except Exception as e:
        logger.error(f"Failed to create temporary database: {e}")
        sys.exit(1)


def cleanup_command(args) -> None:
    """Clean up temporary files."""
    try:
        logger.info("Cleaning up temporary files...")
        drop_tmp_db()
        logger.info("Cleanup completed successfully")
    except Exception as e:
        logger.error(f"Failed to cleanup: {e}")
        sys.exit(1)


def status_command(args) -> None:
    """Show project status."""
    print("=== WG Test Project Status ===")
    print(f"Main database: {DB_NAME} - {'EXISTS' if Path(DB_NAME).exists() else 'NOT FOUND'}")
    print(f"Temp database: {TEMP_DB_NAME} - {'EXISTS' if temp_db_exists() else 'NOT FOUND'}")
    
    if Path(DB_NAME).exists():
        try:
            if verify_db_schema(DB_NAME):
                print("Database schema: VALID")
            else:
                print("Database schema: INVALID")
        except Exception as e:
            print(f"Database schema: ERROR - {e}")


def run_tests_command(args) -> None:
    """Run the test suite."""
    import subprocess
    
    try:
        logger.info("Running tests...")
        cmd = [sys.executable, "-m", "pytest"]
        
        if args.verbose:
            cmd.append("-v")
        
        if args.coverage:
            cmd.extend(["--cov=db", "--cov-report=html"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        sys.exit(result.returncode)
        
    except Exception as e:
        logger.error(f"Failed to run tests: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="WG Test Project - Database testing and management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create-db          # Create the main database
  %(prog)s seed-db            # Seed the database with data
  %(prog)s create-temp-db     # Create temporary database for testing
  %(prog)s run-tests -v       # Run tests with verbose output
  %(prog)s status             # Show project status
  %(prog)s cleanup            # Clean up temporary files
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create database command
    create_parser = subparsers.add_parser("create-db", help="Create the main database")
    create_parser.set_defaults(func=create_database_command)
    
    # Seed database command
    seed_parser = subparsers.add_parser("seed-db", help="Seed the database with data")
    seed_parser.set_defaults(func=seed_database_command)
    
    # Create temp database command
    temp_parser = subparsers.add_parser("create-temp-db", help="Create temporary database")
    temp_parser.set_defaults(func=create_temp_database_command)
    
    # Run tests command
    test_parser = subparsers.add_parser("run-tests", help="Run the test suite")
    test_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    test_parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    test_parser.set_defaults(func=run_tests_command)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show project status")
    status_parser.set_defaults(func=status_command)
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up temporary files")
    cleanup_parser.set_defaults(func=cleanup_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the selected command
    args.func(args)


if __name__ == "__main__":
    main()
