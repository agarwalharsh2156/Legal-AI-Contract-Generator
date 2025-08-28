"""
Application Launcher for Legal AI Contract Generator
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    
    required_packages = [
        'streamlit',
        'google-generativeai', 
        'python-dotenv',
        'pathlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_api_key():
    """Check if API key is configured"""
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("🔑 API Key not found!")
        print("\n📋 Setup Instructions:")
        print("1. Get your free API key from: https://aistudio.google.com/")
        print("2. Create a .env file in this directory")
        print("3. Add: GEMINI_API_KEY=your_api_key_here")
        print("4. Run this script again")
        return False
    
    if not api_key.startswith(('AIza', 'sk-')):
        print("⚠️ API key format looks incorrect")
        print("Google Gemini keys typically start with 'AIza'")
        return False
    
    print("✅ API key found and configured")
    return True

def create_project_structure():
    """Create necessary project directories"""
    
    directories = [
        "templates",
        "generated_contracts", 
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Project structure created")

def run_streamlit_app():
    """Launch the Streamlit application"""
    
    print("🚀 Starting Legal AI Contract Generator...")
    print("📱 The app will open in your browser automatically")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--theme.base", "light",
            "--theme.primaryColor", "#1f77b4"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {str(e)}")

def main():
    """Main launcher function"""
    
    print("=" * 60)
    print("⚖️  LEGAL AI CONTRACT GENERATOR")
    print("=" * 60)
    
    # Check system
    print(f"🖥️  System: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print()
    
    # Check requirements
    print("📦 Checking requirements...")
    if not check_requirements():
        return 1
    print("✅ All requirements satisfied")
    
    # Check API configuration
    print("\n🔑 Checking API configuration...")
    if not check_api_key():
        return 1
    
    # Create project structure
    print("\n📁 Setting up project structure...")
    create_project_structure()
    
    # Launch application
    print("\n🚀 Launching application...")
    run_streamlit_app()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
