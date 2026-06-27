#!/usr/bin/env python
"""
Setup script for AI-Powered Candidate Screening System
Handles environment setup and dependency installation
"""
import os
import sys
import subprocess
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print("✓ Python version compatible\n")


def create_virtual_environment():
    """Create Python virtual environment"""
    print_header("Setting Up Virtual Environment")
    
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"Virtual environment already exists at {venv_path}")
        response = input("Do you want to use the existing environment? (y/n): ")
        if response.lower() != 'y':
            print("Removing existing environment...")
            import shutil
            shutil.rmtree(venv_path)
    
    if not os.path.exists(venv_path):
        print(f"Creating virtual environment at {venv_path}...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("✓ Virtual environment created\n")
    else:
        print("✓ Virtual environment exists\n")
    
    return venv_path


def get_pip_command(venv_path):
    """Get the appropriate pip command for the OS"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path, "bin", "pip")


def install_dependencies(venv_path):
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    pip_cmd = get_pip_command(venv_path)
    
    print("Upgrading pip...")
    subprocess.check_call([pip_cmd, "install", "--upgrade", "pip"])
    
    print("Installing requirements from requirements.txt...")
    subprocess.check_call([pip_cmd, "install", "-r", "requirements.txt"])
    
    print("✓ All dependencies installed\n")


def create_env_file():
    """Create .env file from template"""
    print_header("Setting Up Environment Variables")
    
    if os.path.exists(".env"):
        print(".env file already exists")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Skipping .env creation\n")
            return
    
    print("Creating .env file from .env.example...")
    
    if os.path.exists(".env.example"):
        with open(".env.example", 'r') as f:
            content = f.read()
        
        with open(".env", 'w') as f:
            f.write(content)
        
        print("✓ .env file created")
        print("\n⚠️  IMPORTANT: Edit .env file and add your OpenAI API key:")
        print("   OPENAI_API_KEY=sk-your-actual-key-here\n")
    else:
        print("❌ .env.example not found\n")


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    dirs = ["sessions", "vector_db", "logs"]
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ Created {dir_name}/ directory")
    
    print()


def main():
    """Run setup"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  AI-Powered Candidate Screening System - Setup".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        check_python_version()
        venv_path = create_virtual_environment()
        install_dependencies(venv_path)
        create_env_file()
        create_directories()
        
        print_header("✓ Setup Complete!")
        
        if platform.system() == "Windows":
            activate_cmd = f"{venv_path}\\Scripts\\activate"
        else:
            activate_cmd = f"source {venv_path}/bin/activate"
        
        print("Next steps:")
        print(f"\n1. Activate virtual environment:")
        print(f"   {activate_cmd}")
        print("\n2. Edit .env file and add your OpenAI API key:")
        print("   Edit .env and set OPENAI_API_KEY=sk-...")
        print("\n3. Ingest knowledge base:")
        print("   python ingest_knowledge.py")
        print("\n4. Start the server:")
        print("   python -m uvicorn app.main:app --reload")
        print("\n5. In another terminal, start the frontend:")
        print("   cd ../frontend && npm install && npm run dev")
        print("\n6. Open browser and visit:")
        print("   http://localhost:5173")
        print("\n" + "=" * 80 + "\n")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
