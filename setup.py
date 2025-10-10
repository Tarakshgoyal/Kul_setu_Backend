#!/usr/bin/env python3
"""
Environment setup script for Kul Setu backend
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Successfully installed all requirements!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_files():
    """Check if required files exist"""
    required_files = ["tree.csv", "app.py", "requirements.txt"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found!")
    return True

def main():
    """Main setup function"""
    print("🔧 Setting up Kul Setu backend environment...")
    
    # Check required files
    if not check_files():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    print("\n🎉 Environment setup completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python deploy.py' to initialize the database")
    print("2. Run 'python app.py' to start the backend server")
    
    return True

if __name__ == "__main__":
    main()