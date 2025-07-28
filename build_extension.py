#!/usr/bin/env python3
"""
Build script for Animation & Object Tools extension
This script uses the official Blender command-line tool to build the extension
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def find_blender_executable():
    """Find the Blender executable"""
    # Common Blender installation paths
    possible_paths = [
        "blender",  # If in PATH
        "/usr/bin/blender",  # Linux
        "/Applications/Blender.app/Contents/MacOS/Blender",  # macOS
        "C:/Program Files/Blender Foundation/Blender*/blender.exe",  # Windows
    ]
    
    # Check if blender is in PATH
    try:
        result = subprocess.run(["blender", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return "blender"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Check other possible paths
    for path in possible_paths:
        if "*" in path:
            # Handle wildcards (Windows)
            import glob
            matches = glob.glob(path)
            if matches:
                return matches[0]
        elif os.path.exists(path):
            return path
    
    return None

def build_extension_with_blender():
    """Build the extension using Blender's command-line tool"""
    
    blender_exe = find_blender_executable()
    if not blender_exe:
        print("❌ Blender executable not found!")
        print("Please make sure Blender is installed and accessible from command line.")
        print("\nYou can also run the command manually:")
        print("blender --command extension build")
        return False
    
    print(f"🔍 Found Blender: {blender_exe}")
    
    # Check if we're in the right directory
    if not os.path.exists("blender_manifest.toml"):
        print("❌ blender_manifest.toml not found in current directory")
        print("Please run this script from the directory containing the extension files.")
        return False
    
    # Build the extension
    print("\n🚀 Building extension with Blender...")
    try:
        cmd = [blender_exe, "--command", "extension", "build"]
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Extension built successfully!")
            print("\n📋 Build output:")
            print(result.stdout)
            
            # Look for the generated zip file
            zip_files = list(Path(".").glob("*.zip"))
            if zip_files:
                print(f"\n📦 Generated extension: {zip_files[0].name}")
                print(f"📏 File size: {zip_files[0].stat().st_size} bytes")
            else:
                print("\n⚠️  No zip file found in current directory")
            
            return True
        else:
            print("❌ Build failed!")
            print("\n📋 Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build timed out")
        return False
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def validate_manifest():
    """Validate the manifest file"""
    print("\n🔍 Validating manifest...")
    
    if not os.path.exists("blender_manifest.toml"):
        print("❌ blender_manifest.toml not found")
        return False
    
    try:
        import tomllib
        with open("blender_manifest.toml", "rb") as f:
            manifest = tomllib.load(f)
        
        # Check required fields
        required_fields = [
            "blender_version_min", "id", "license", "maintainer", 
            "name", "schema_version", "tagline", "type", "version"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in manifest:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print("✅ Manifest validation passed")
        print(f"  - Extension ID: {manifest['id']}")
        print(f"  - Name: {manifest['name']}")
        print(f"  - Version: {manifest['version']}")
        print(f"  - Blender Version: {manifest['blender_version_min']} - {manifest.get('blender_version_max', 'latest')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating manifest: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        "blender_manifest.toml",
        "__init__.py",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    return True

def main():
    """Main build process"""
    print("🚀 Animation & Object Tools Extension Builder")
    print("Using official Blender command-line tool")
    print("=" * 60)
    
    # Check files
    if not check_files():
        return False
    
    # Validate manifest
    if not validate_manifest():
        return False
    
    # Build extension
    if not build_extension_with_blender():
        return False
    
    print("\n🎉 Extension build completed successfully!")
    print("\n📤 Next steps:")
    print("1. Test the extension in Blender")
    print("2. Upload to https://extensions.blender.org/submit/")
    print("3. Wait for review and approval")
    
    return True

if __name__ == "__main__":
    main() 