import cairosvg
from PIL import Image, ImageTk, ImageOps
from pathlib import Path
import io, re

def svg_to_coloured_photo(svg_file: Path, colour: str, size_xy, mirror=False) -> ImageTk.PhotoImage:
    """Return a PhotoImage of the SVG filled with *colour* (stroke stays)."""
    txt = svg_file.read_text(encoding="utf-8")
    txt = re.sub(r'fill\s*:\s*#[0-9a-fA-F]{3,6}', f'fill:{colour}', txt)
    txt = re.sub(r'fill="[^"]+"',                 f'fill="{colour}"', txt, flags=re.I)
    png = cairosvg.svg2png(bytestring=txt.encode(),
                           output_width=size_xy[0], output_height=size_xy[1])
    pil_img = Image.open(io.BytesIO(png)).convert("RGBA")

    if mirror:
        pil_img = ImageOps.mirror(pil_img)

    return ImageTk.PhotoImage(pil_img)

def svg_to_photo(svg_path, width=None, height=None):

    svg_path = str(svg_path)
    png_bytes = cairosvg.svg2png(url=svg_path, output_width=width, output_height=height)
    image = Image.open(io.BytesIO(png_bytes))

    return ImageTk.PhotoImage(image)

def load_svg_img(self, path, size_xy, colour='', mirror=False):
    if colour != '':
        img = svg_to_coloured_photo(path, colour, size_xy, mirror)
    else:
        img = svg_to_photo(path, size_xy[0], size_xy[1])
    self.img_refs.append(img)
    return img