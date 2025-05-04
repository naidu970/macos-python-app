README: Convert SVG to PNG macOS .app Build

This folder contains everything needed to build a macOS .app from the included Python script using PyInstaller, and set it up to work as a Finder Quick Action.

Included:
- createPNG.py — the Python script (takes an SVG, creates a PNG with “ PROOF” in the name)
- sampleSVG.svg — for testing the .app
- icon.icns — optional custom icon for the .app

What I need you to do:
1. Use PyInstaller to build a `.app` from `createPNG.py`:
   pyinstaller --onefile --windowed --icon=icon.icns createPNG.py

2. Move the resulting `.app` to /Applications (or another known path)

3. Create an Automator Quick Action with:
   - Input: files or folders in Finder
   - Action: Run Shell Script
   - Script:

     for f in "$@"
     do
         open -a "/Applications/convertSVGtoPNG.app" "$f"
     done

     (If you use a different name for the `.app`, be sure to update the path accordingly.)

4. Save the Quick Action as "Create PNG"

5. Test it by:
   - Right-clicking sampleSVG.svg
   - Selecting Quick Actions → Create PNG
   - Confirm a PNG file is created next to the SVG

6. Export the Quick Action as a .workflow file

7. Send back:
   - The .app (zipped)
   - The .workflow file (zipped)

Thank you!
