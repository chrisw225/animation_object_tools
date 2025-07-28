# Build Instructions for Animation & Object Tools Extension

This document explains how to build the extension for submission to the Blender Extensions Platform.

## Prerequisites

1. **Blender 3.0+** installed and accessible from command line
2. **Python 3.7+** (for the build script)
3. All extension files in the current directory

## Required Files

Make sure you have these files in your directory:
- `blender_manifest.toml`
- `animation_object_tools.py`
- `README.md`
- `test_nla_strip_randomizer.py`

## Building the Extension

### Option 1: Using the Build Script (Recommended)

#### Windows
```cmd
python build_extension.py
```
or
```cmd
build.bat
```

#### Linux/macOS
```bash
python3 build_extension.py
```
or
```bash
./build.sh
```

### Option 2: Manual Build

If the build script doesn't work, you can build manually:

```bash
blender --command extension build
```

### Option 3: Using Blender GUI

1. Open Blender
2. Go to **Edit > Preferences > Extensions**
3. Click **Build Extension**
4. Select the directory containing your extension files

## What the Build Process Does

1. **Validates** the `blender_manifest.toml` file
2. **Checks** that all required files exist
3. **Builds** the extension using Blender's official command-line tool
4. **Creates** a `.zip` file ready for submission

## Expected Output

After a successful build, you should see:
- A `.zip` file in the current directory (e.g., `animation_object_tools-1.4.0.zip`)
- Success messages in the console

## Troubleshooting

### "Blender not found"
- Make sure Blender is installed
- Add Blender to your system PATH
- Or specify the full path to the Blender executable

### "blender_manifest.toml not found"
- Make sure you're running the script from the directory containing the extension files
- Check that the manifest file exists and has the correct name

### "Build failed"
- Check the error messages for specific issues
- Verify all required fields are present in the manifest
- Make sure all required files exist

## Testing the Extension

Before submitting, test the extension:

1. Open Blender
2. Go to **Edit > Preferences > Add-ons**
3. Click **Install** and select the generated `.zip` file
4. Enable the addon
5. Test all functionality in the 3D View sidebar

## Submission

Once the extension is built and tested:

1. Go to https://extensions.blender.org/submit/
2. Upload the generated `.zip` file
3. Fill in any additional required information
4. Submit for review

## File Structure

```
extension-directory/
├── blender_manifest.toml      # Extension metadata
├── animation_object_tools.py  # Main addon file
├── README.md                 # Documentation
├── test_nla_strip_randomizer.py  # Test script
├── build_extension.py        # Build script
├── build.bat                 # Windows build script
├── build.sh                  # Unix build script
└── BUILD_INSTRUCTIONS.md     # This file
```

## Support

If you encounter issues:
1. Check the Blender Extensions documentation
2. Verify all files are present and correctly named
3. Test with a simple extension first
4. Check Blender's system console for error messages 