import omni.ui as ui
from pathlib import Path

icons_path = Path(__file__).parent.parent.parent.parent.parent / "icons"


sdg_style = {
    "HStack": {
        "margin": 3
    },
    "Button.Image::create": {"image_url": f"{icons_path}/plus.svg", "color": 0xFF00B976},
    "Button.Image::properties": {"image_url": f"{icons_path}/cog.svg", "color": 0xFF989898},
    "Line": {
        "margin": 3
    },
    "Label": {
        "margin_width": 5
    }
}