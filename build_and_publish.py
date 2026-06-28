#!/usr/bin/env python3
"""
Build and publish script for GeoMoz package
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        print(f"SUCCESS")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output:\n{e.stdout}")
        if e.stderr:
            print(f"Error output:\n{e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts"""
    print("\nCleaning previous build artifacts...")

    # Remove build directories
    for dir_name in ['build', 'dist', '*.egg-info']:
        for path in Path('.').glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed: {path}")
            elif path.is_file():
                path.unlink()
                print(f"   Removed: {path}")

    # Remove cache
    cache_dirs = [
        Path('.pytest_cache'),
        Path('.coverage'),
        Path('__pycache__'),
        Path('geomoz/__pycache__'),
        Path('geomoz/utils/__pycache__')
    ]

    for cache_dir in cache_dirs:
        if cache_dir.exists():
            if cache_dir.is_dir():
                shutil.rmtree(cache_dir)
                print(f"   Removed cache: {cache_dir}")

def build_package():
    """Build the package"""
    print("\nBuilding package...")

    # Build source distribution
    if not run_command("python3 -m build", "Building source distribution"):
        return False

    # Build wheel
    if not run_command("python3 -m build", "Building wheel"):
        return False

    return True

def check_package():
    """Check the built package"""
    print("\nChecking built package...")

    # Check if files exist
    dist_files = list(Path('dist').glob('*'))
    if not dist_files:
        print("No distribution files found")
        return False

    print(f"Found distribution files:")
    for file in dist_files:
        size = file.stat().st_size
        print(f"   {file.name} ({size:,} bytes)")

    return True

def install_test():
    """Test installation in a clean environment"""
    print("\nTesting installation...")

    # Create test virtual environment
    if not run_command("python3 -m venv test_env", "Creating test virtual environment"):
        return False

    # Activate and install
    if not run_command("test_env/bin/pip install dist/*.whl", "Installing package in test environment"):
        return False

    # Test import
    if not run_command("test_env/bin/python -c 'import geomoz; print(\"Import successful\")'", "Testing import"):
        return False

    # Test basic functionality
    test_script = '''
import geomoz
try:
    provinces = geomoz.read_province()
    print(f"Successfully loaded {len(provinces)} provinces")

    from geomoz.utils.data import get_cache_info
    cache_info = get_cache_info()
    print(f"Cache info accessible: {cache_info['cache_dir']}")

    print("All tests passed!")
except Exception as e:
    print(f"Test failed: {e}")
    exit(1)
'''

    success, result = run_command(
        f"test_env/bin/python -c '{test_script}'",
        "Testing basic functionality"
    )

    if not success:
        return False

    # Cleanup test environment
    if Path('test_env').exists():
        shutil.rmtree('test_env')
        print("   Cleaned test environment")

    return True

def publish_to_testpypi():
    """Publish to Test PyPI"""
    print("\nPublishing to Test PyPI...")

    # Check if twine is installed
    try:
        subprocess.run(['twine', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("twine not found. Installing...")
        if not run_command("pip install twine", "Installing twine"):
            return False

    # Publish to test PyPI
    if not run_command("twine upload --repository testpypi dist/*", "Publishing to Test PyPI"):
        return False

    print("Published to Test PyPI!")
    print("Install with: pip install --index-url https://test.pypi.org/simple/ geomoz")
    return True

def publish_to_pypi():
    """Publish to PyPI"""
    print("\nPublishing to PyPI...")

    # Check if twine is installed
    try:
        subprocess.run(['twine', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("twine not found. Installing...")
        if not run_command("pip install twine", "Installing twine"):
            return False

    # Publish to PyPI
    if not run_command("twine upload dist/*", "Publishing to PyPI"):
        return False

    print("Published to PyPI!")
    print("Install with: pip install geomoz")
    return True

def main():
    """Main function"""
    print("GeoMoz Build and Publish Script")
    print("=" * 60)

    # Parse arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        print("Usage: python build_and_publish.py [build|test|testpypi|pypi|all]")
        print("  build    - Build the package only")
        print("  test     - Build and test the package")
        print("  testpypi - Build, test and publish to Test PyPI")
        print("  pypi     - Build, test and publish to PyPI")
        print("  all      - Build, test and publish to PyPI")
        return

    # Clean first
    clean_build()

    if command == "build":
        success = build_package() and check_package()

    elif command == "test":
        success = build_package() and check_package() and install_test()

    elif command == "testpypi":
        success = build_package() and check_package() and install_test() and publish_to_testpypi()

    elif command == "pypi":
        success = build_package() and check_package() and install_test() and publish_to_pypi()

    elif command == "all":
        success = build_package() and check_package() and install_test() and publish_to_pypi()

    else:
        print(f"Unknown command: {command}")
        return

    # Final result
    print(f"\n{'='*60}")
    if success:
        print("SUCCESS! GeoMoz package ready for distribution!")
    else:
        print("FAILED! Check the errors above.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
