import xml.etree.ElementTree as ET
import sys
import os
import re
import cairosvg

def process_svg(input_svg):
    """ Converts an SVG file to PNG in the same folder, appending ' PROOF' to the filename. """

    if not os.path.exists(input_svg):
        print(f"Error: File '{input_svg}' not found.")
        return

    # Get the directory and filename
    folder, filename = os.path.split(input_svg)
    name, _ = os.path.splitext(filename)  # Remove .svg extension

    # Create the output PNG name
    output_png = os.path.join(folder, f"{name} PROOF.png")

    try:
        # Parse the SVG file
        tree = ET.parse(input_svg)
        root = tree.getroot()

        # Function to convert stroke-width values to points (pt)
        def convert_to_pt(value):
            match = re.match(r"([0-9.]+)([a-zA-Z%]*)", value)
            if match:
                num, unit = match.groups()
                num = float(num)
                if unit == "mm":
                    return num * 2.83465  # Convert mm to pt
                elif unit == "px":
                    return num * 0.75  # Convert px to pt
                elif unit in ["pt", ""]:
                    return num
            return 0.5  # Default stroke width in pt

        # Find all elements that could have a stroke
        for elem in root.iter():
            if elem.tag == "{http://www.w3.org/2000/svg}text":
                continue

            style = elem.get("style", "").strip()
            stroke_value = elem.get("stroke", "").strip().lower()
            stroke_width_value = elem.get("stroke-width", "").strip().lower()

            new_style = []
            has_stroke = False

            for rule in style.split(";"):
                rule = rule.strip()
                if rule.startswith("stroke:"):
                    has_stroke = True
                    new_style.append(rule)
                elif rule.startswith("stroke-width"):
                    width_val = rule.split(":")[1].strip()
                    new_width = convert_to_pt(width_val)
                    new_style.append(f"stroke-width:{new_width}pt")
                else:
                    new_style.append(rule)

            if stroke_value and not stroke_width_value:
                new_style.append("stroke-width:0.5pt")

            if not has_stroke:
                new_style.append("stroke:black")
                new_style.append("stroke-width:0.5pt")

            if new_style:
                elem.set("style", ";".join(filter(None, new_style)))

        # Determine canvas size using width/height or fallback to viewBox
        width = root.get("width")
        height = root.get("height")

        if not width or not height:
            viewBox = root.get("viewBox")
            if viewBox:
                _, _, w, h = viewBox.strip().split()
                width = w
                height = h
            else:
                width = "1000"
                height = "1000"

        # Convert to PNG without inserting a <rect>
        cairosvg.svg2png(
            bytestring=ET.tostring(root),
            write_to=output_png,
            dpi=150,
            background_color="white"
        )

        print(f"Success: PNG saved as {output_png}")

    except Exception as e:
        print(f"Error: {e}")

# Run the function if called from command line
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: convert_svg.py <path-to-svg-file>")
    else:
        process_svg(sys.argv[1])
