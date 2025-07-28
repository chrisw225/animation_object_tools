#!/bin/bash

echo "Building Animation & Object Tools Extension..."
echo

# Check if blender is available
if ! command -v blender &> /dev/null; then
    echo "Error: Blender not found in PATH"
    echo "Please make sure Blender is installed and accessible from command line"
    echo
    echo "You can also run manually:"
    echo "blender --command extension build"
    exit 1
fi

echo "Found Blender, building extension..."
echo

# Build the extension
blender --command extension build

if [ $? -eq 0 ]; then
    echo
    echo "✅ Extension built successfully!"
    echo
    echo "📤 Next steps:"
    echo "1. Test the extension in Blender"
    echo "2. Upload to https://extensions.blender.org/submit/"
    echo "3. Wait for review and approval"
else
    echo
    echo "❌ Build failed!"
    echo "Check the error messages above."
fi 