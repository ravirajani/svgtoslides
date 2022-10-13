import xml.etree.ElementTree as ET
import subprocess, platform, sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import path
from pathlib import Path

is_win = (platform.system() == "Windows")

####################################################################
####                  Default configuration                     ####
####################################################################
DEFAULT_INKSCAPE_WIN = "C:/Program Files/Inkscape/bin/inkscape.com"
DEFAULT_INKSCAPE_LIN = "/usr/bin/inkscape"
DEFAULT_SVG_NAMESPACE = "http://www.w3.org/2000/svg"
DEFAULT_SVG_LAYER_TAGNAME = "g"

####################################################################
####################################################################
parser = ArgumentParser(description=f"""
The input SVG file should have structure:

<?xml version="1.0" encoding="UTF-8" ... ?>
<svg xmlns="{DEFAULT_SVG_NAMESPACE}" ... >
    ...
    <{DEFAULT_SVG_LAYER_TAGNAME} ... > ... </{DEFAULT_SVG_LAYER_TAGNAME}>
    <{DEFAULT_SVG_LAYER_TAGNAME} ... > ... </{DEFAULT_SVG_LAYER_TAGNAME}>
    ...
</svg>

where each <{DEFAULT_SVG_LAYER_TAGNAME}> denotes a layer, and the order runs
from top to bottom. (The tag name and namespace are configurable.)

If the number of layers is n, the following output files are generated:
file1.svg,   ...   , file{{n-1}}.svg
file1.pdf,   ...   , file{{n-1}}.pdf,     file{{n}}.pdf
file1.pdf_tex, ... , file{{n-1}}.pdf_tex, file{{n}}.pdf_tex

where file{{i}}.svg contains the bottom i layers of file.svg
""", formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('filepath', metavar='file.svg', type=Path)
parser.add_argument('--output-dir', type=Path, default=Path('.'))
parser.add_argument('--inkscape-bin',  type=Path,
    default=Path(DEFAULT_INKSCAPE_WIN if is_win else DEFAULT_INKSCAPE_LIN),
    help="The path to the Inkscape command line program")
parser.add_argument('--svg-namespace', default=DEFAULT_SVG_NAMESPACE)
parser.add_argument('--svg-layer-tagname', default=DEFAULT_SVG_LAYER_TAGNAME,
    help="The tagname for the layer elements directly beneath the svg root")
args = parser.parse_args()

inkscape = str(args.inkscape_bin)
if not args.inkscape_bin.exists():
    sys.exit(f"Inkscape binary '{inkscape}' not found!")

filepath = args.filepath
_, tail = path.split(filepath)
pre_ext = path.splitext(tail)    # e.g. [ 'file', '.svg' ]
filename_pre = pre_ext[0] 
filename_ext = pre_ext[1]

output_dir = args.output_dir

def create_pdftex_from_svg(svg_filename, pdf_filename):
    """Makes a call to Inkscape to create a PDF
    and a Latex file.
    If pdf_filename is 'file.pdf', then the output files
    are called 'file.pdf' and 'file.pdf_tex'
    """
    output_file = str(output_dir / pdf_filename)
    inkscape_cmd = [
        inkscape,
        '--export-filename=' + output_file,
        '--export-latex',
        svg_filename ]
    print(subprocess.list2cmdline(inkscape_cmd))
    print(f"Writing '{output_file}', '{output_file}_tex'", 
        end='... ', flush=True)
    p = subprocess.run(inkscape_cmd)
    if p.returncode == 0:
        print("Done")

tree = ET.parse(filepath)
root = tree.getroot()
els = root.findall('svg:' + args.svg_layer_tagname, 
    { 'svg': args.svg_namespace })
n = len(els)

create_pdftex_from_svg(str(filepath), filename_pre + str(n) + '.pdf')

for i in range(n-1, 0, -1):
    el = els[i]
    root.remove(el)
    newfile_pre = filename_pre + str(i) 
    newpath_svg = output_dir / (newfile_pre + filename_ext)
    newfile_svg = str(newpath_svg)
    newfile_pdf = newfile_pre + '.pdf'
    print(f"Writing '{newfile_svg}'", end='... ', flush=True)
    tree.write(newpath_svg)
    print("Done")
    create_pdftex_from_svg(newfile_svg, newfile_pdf)
