#!/usr/bin/env python3
"""
Quick Start Script for Personal Expense Tracker
This script helps you get started quickly with the expense tracker application.
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
        return False

def generate_sample_data():
    """Generate sample data if user wants it"""
    response = input("🎯 Would you like to generate sample data for demonstration? (y/n): ").lower()
    if response in ['y', 'yes']:
        try:
            from sample_data import create_sample_data
            create_sample_data()
            return True
        except Exception as e:
            print(f"❌ Failed to generate sample data: {e}")
            return False
    return True

def run_app():
    """Run the Streamlit application"""
    print("🚀 Starting Personal Expense Tracker...")
    print("📱 The app will open in your default browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Thanks for using Personal Expense Tracker!")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main function to orchestrate the startup process"""
    print("💰 Personal Expense Tracker - Quick Start")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("📦 Installing missing dependencies...")
        if not install_dependencies():
            return
    
    # Generate sample data
    generate_sample_data()
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main() 