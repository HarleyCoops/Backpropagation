#!/usr/bin/env python3
"""
Environment Test Script for Backpropagation Museum Project
Tests key components and dependencies
"""

import sys
import importlib
import requests
import time
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        return False

def test_dependencies():
    """Test if required packages are installed"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'numpy', 'matplotlib', 'torch', 'openai', 
        'fastapi', 'uvicorn', 'aiohttp', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✓ All core dependencies available")
        return True

def test_files():
    """Test if required files exist"""
    print("\n📁 Testing project files...")
    
    required_files = [
        'requirements.txt', 'mcp_server.py', 'config.env',
        'BP.tex', 'BP_review.md', 'setup.ps1'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_mcp_server():
    """Test MCP server startup (basic)"""
    print("\n🚀 Testing MCP server startup...")
    
    try:
        # Import the server module
        import mcp_server
        print("✓ MCP server module imports successfully")
        
        # Test server instantiation
        server = mcp_server.BackpropagationMCPServer()
        print("✓ MCP server can be instantiated")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server test failed: {str(e)}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\n⚙️  Testing environment configuration...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        # Try to load config
        load_dotenv("config.env")
        
        config_vars = [
            'MCP_SERVER_HOST', 'MCP_SERVER_PORT', 
            'ENABLE_INTERNET_ACCESS', 'DEFAULT_LEARNING_RATE'
        ]
        
        for var in config_vars:
            value = os.getenv(var)
            if value:
                print(f"✓ {var} = {value}")
            else:
                print(f"⚠️  {var} - Not set (using defaults)")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment config test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧠 Backpropagation Museum Environment Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Project Files", test_files),
        ("Environment Config", test_environment_config),
        ("Dependencies", test_dependencies),
        ("MCP Server", test_mcp_server),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            time.sleep(0.5)  # Brief pause between tests
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Environment is ready! Run './setup.ps1' to complete setup.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("💡 Try running: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
 