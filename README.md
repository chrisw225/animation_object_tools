# Animation & Object Tools

A comprehensive Blender addon that provides tools for NLA strip manipulation, parent transform fixes, and object replacement functionality.

## Features

### 🎬 **NLA Strip Offset & Random Scale**
- **Absolute Positioning**: Set NLA strips to absolute frame positions (not relative to current values)
- **Offset Methods**: 
  - **Random**: Random offset within a specified range
  - **3D Cursor Distance**: Offset based on distance from 3D cursor
- **Random Scale**: Apply random playback speed to strips (0.9-1.1 by default)
- **Preserve Duration**: Maintains strip duration while adjusting position

### 🔧 **Parent Transform Fix**
- Fixes parent-child transform relationships
- Preserves world transforms while correcting local transforms
- Handles complex parent hierarchies safely

### 🎯 **Object Replacement**
- Replace selected objects with instances of the active object
- Preserves original transforms and positions
- Creates linked duplicates for efficient memory usage

## Installation

### From Blender Extensions Platform (Recommended)
1. Open Blender 4.2.0 or later
2. Go to **Edit > Preferences > Extensions**
3. Search for "Animation & Object Tools"
4. Click **Install** and enable the addon

### Manual Installation
1. Download the `animation_object_tools-1.4.0.zip` file
2. Open Blender 4.2.0 or later
3. Go to **Edit > Preferences > Add-ons**
4. Click **Install** and select the zip file
5. Enable the addon by checking the box

## Usage

### NLA Strip Tools
1. **Select objects** with NLA animation data
2. **Open the Tool Tab** in the 3D View sidebar
3. **Configure settings**:
   - **Offset Method**: Choose "Random" or "3D Cursor"
   - **Base Start Frame**: Set the base frame position
   - **Scale Range**: Adjust min/max scale values
4. **Click "Apply Offset & Random Scale"**

### Parent Transform Fix
1. **Select objects** with parent relationships
2. **Click "Fix Parent Transforms"** in the Tool Tab
3. **Check the console** for results

### Object Replacement
1. **Select the template object** (this will be the source)
2. **Select target objects** to replace
3. **Click "Replace with Instance"** in the Tool Tab

## UI Location

The addon appears in the **3D View > Sidebar > Tool Tab** as "Animation & Object Tools".

## Settings

### Offset Settings
- **Offset Method**: Random or 3D Cursor distance
- **Base Start Frame**: Absolute frame position for all strips
- **Max Random Offset**: Maximum random offset (frames)
- **Offset Multiplier**: Frames per unit distance from cursor

### Scale Settings
- **Scale Min**: Minimum random scale value (default: 0.9)
- **Scale Max**: Maximum random scale value (default: 1.1)

## Requirements

- **Blender 4.2.0+**
- **Objects with NLA animation data** (for strip tools)
- **Parent-child relationships** (for transform fix)

## File Structure

```
animation_object_tools/
├── __init__.py                    # Main addon file
├── blender_manifest.toml          # Extension metadata
├── README.md                      # This documentation
├── test_nla_strip_randomizer.py  # Test script
├── build_extension.py             # Build script
├── build.bat                      # Windows build script
├── build.sh                       # Unix build script
└── BUILD_INSTRUCTIONS.md          # Build instructions
```

## Development

### Building the Extension
```bash
# Using the build script
python build_extension.py

# Or manually
blender --command extension build
```

### Testing
1. Install the extension in Blender
2. Run the test script: `test_nla_strip_randomizer.py`
3. Verify all functionality works as expected

## Troubleshooting

### "No objects with animation data selected"
- Make sure selected objects have NLA tracks
- Check that objects have animation data

### "No active object selected" (Object Replacement)
- Select the template object first
- Make sure it's the active object

### "No parent" (Transform Fix)
- Only objects with parents will be processed
- Objects without parents are skipped safely

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the troubleshooting section
- Review the console output for error messages
- Test with a simple scene first

## Version History

- **1.4.0**: Added object replacement functionality
- **1.3.0**: Added parent transform fix
- **1.2.0**: Added offset method menu and improved defaults
- **1.1.0**: Implemented absolute positioning
- **1.0.0**: Initial release with NLA strip offset and random scale 