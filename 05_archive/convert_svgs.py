import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def convert_svg_to_png(svg_path, png_path):
    print(f"Converting {svg_path} to {png_path}")
    try:
        drawing = svg2rlg(svg_path)
        if drawing is None:
            print(f"Error: svglib could not read {svg_path}")
            return
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        print("Success")
    except Exception as e:
        print(f"Failed to convert: {e}")

def main():
    figs = ["fig1_aire_trace_architecture", "fig2_provenance_recovery", "fig3_prospective_prefix"]
    for f in figs:
        svg_path = f"figures/ieee/{f}.svg"
        png_path = f"figures/ieee/{f}.png"
        if os.path.exists(svg_path):
            convert_svg_to_png(svg_path, png_path)
        else:
            print(f"Not found: {svg_path}")

if __name__ == "__main__":
    main()
