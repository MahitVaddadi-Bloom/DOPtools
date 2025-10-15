#!/usr/bin/env python3
"""
Test script for DOPtools package installation and basic functionality.
"""

def test_imports():
    """Test basic imports."""
    print("Testing basic imports...")
    
    try:
        import doptools
        print("✓ Successfully imported doptools")
    except ImportError as e:
        print(f"✗ Failed to import doptools: {e}")
        return False
    
    try:
        from doptools.chem import *
        print("✓ Successfully imported doptools.chem")
    except ImportError as e:
        print(f"✗ Failed to import doptools.chem: {e}")
        return False
    
    try:
        from doptools.optimizer import *
        print("✓ Successfully imported doptools.optimizer")
    except ImportError as e:
        print(f"✗ Failed to import doptools.optimizer: {e}")
        return False
    
    try:
        from doptools.cli import *
        print("✓ Successfully imported doptools.cli")
    except ImportError as e:
        print(f"✗ Failed to import doptools.cli: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality if possible."""
    print("\nTesting basic functionality...")
    
    try:
        from doptools.chem.chem_features import ChythonCircus
        print("✓ ChythonCircus class available")
        
        # Test instantiation
        circus = ChythonCircus(lower=0, upper=2)
        print("✓ ChythonCircus instantiation successful")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_cli_commands():
    """Test that CLI commands are installed."""
    print("\nTesting CLI command availability...")
    import shutil
    
    commands = [
        'launch_preparer',
        'launch_optimizer', 
        'plotter',
        'rebuilder'
    ]
    
    available_commands = []
    for cmd in commands:
        if shutil.which(cmd):
            print(f"✓ {cmd} command available")
            available_commands.append(cmd)
        else:
            print(f"✗ {cmd} command not found in PATH")
    
    return len(available_commands) > 0

def main():
    """Run all tests."""
    print("DOPtools Installation Test")
    print("=" * 30)
    
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("CLI Commands", test_cli_commands),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 30)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DOPtools is working correctly.")
        return True
    else:
        print(f"⚠️ {total - passed} test(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)