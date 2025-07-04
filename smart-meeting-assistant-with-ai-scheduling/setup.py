#!/usr/bin/env python3
"""
Setup script for Smart Meeting Assistant with AI Scheduling
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def create_venv():
    """Create virtual environment"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    # Determine the correct pip path
    if sys.platform == "win32":
        pip_path = Path("venv/Scripts/pip.exe")
        python_path = Path("venv/Scripts/python.exe")
    else:
        pip_path = Path("venv/bin/pip")
        python_path = Path("venv/bin/python")
    
    # Install requirements
    result = subprocess.run([
        str(pip_path), "install", "-r", "requirements.txt"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Dependencies installed successfully")
    else:
        print(f"✗ Error installing dependencies: {result.stderr}")
        return False
    
    return True

def verify_installation():
    """Verify the installation works"""
    print("Verifying installation...")
    
    # Check if data file exists
    data_file = Path("data/sample_content.json")
    if not data_file.exists():
        print("✗ Sample data file not found")
        return False
    
    print("✓ Sample data file found")
    
    # Test import
    if sys.platform == "win32":
        python_path = Path("venv/Scripts/python.exe")
    else:
        python_path = Path("venv/bin/python")
    
    test_import = subprocess.run([
        str(python_path), "-c", 
        "import sys; sys.path.append('src'); from server import meeting_assistant; print('✓ Server imports successfully')"
    ], capture_output=True, text=True)
    
    if test_import.returncode == 0:
        print(test_import.stdout.strip())
        return True
    else:
        print(f"✗ Import test failed: {test_import.stderr}")
        return False

def show_usage():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("🎉 Smart Meeting Assistant Setup Complete!")
    print("="*60)
    print("\nTo run the server:")
    
    if sys.platform == "win32":
        print("  1. Activate virtual environment: venv\\Scripts\\activate")
    else:
        print("  1. Activate virtual environment: source venv/bin/activate")
    
    print("  2. Run server: python src/server.py")
    print("\nTo integrate with Claude Desktop:")
    print("  1. Copy claude_desktop_config.json content to your Claude Desktop config")
    print("  2. Update the path to point to this directory")
    print("  3. Restart Claude Desktop")
    print("\nFor more information, see README.md")

def main():
    """Main setup function"""
    print("Smart Meeting Assistant Setup")
    print("="*30)
    
    # Check if we're in the correct directory
    if not Path("requirements.txt").exists():
        print("✗ Please run this script from the project root directory")
        sys.exit(1)
    
    # Create virtual environment
    create_venv()
    
    # Install dependencies
    if not install_dependencies():
        print("✗ Setup failed during dependency installation")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("✗ Setup failed during verification")
        sys.exit(1)
    
    # Show usage instructions
    show_usage()

if __name__ == "__main__":
    main() 