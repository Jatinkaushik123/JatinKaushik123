import os
import re
import json
import base64
from PIL import Image

def get_base64_font(font_path):
    with open(font_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# Test fonts
space_grotesk_b64 = get_base64_font("fonts/space-grotesk-bold.woff2")
jetbrains_mono_b64 = get_base64_font("fonts/jetbrains-mono-semibold.woff2")

print(f"Space Grotesk b64 len: {len(space_grotesk_b64)}")
print(f"JetBrains Mono b64 len: {len(jetbrains_mono_b64)}")

# Test images
id_b64 = get_base64_image("assets/id.png")
pointing_b64 = get_base64_image("assets/right_pointing.png")

print(f"id.png b64 len: {len(id_b64)}")
print(f"right_pointing.png b64 len: {len(pointing_b64)}")

# Extract icon paths
icons = {}
for fname in os.listdir("assets/icons"):
    if fname.endswith(".svg"):
        name = fname[:-4]
        with open(os.path.join("assets/icons", fname), "r", encoding="utf-8") as f:
            content = f.read()
        paths = re.findall(r'd="([^"]+)"', content)
        if paths:
            icons[name] = paths
        else:
            print("No path found in", fname)

with open("assets/icons/extracted_icons.json", "w", encoding="utf-8") as f:
    json.dump(icons, f, indent=2)

print("Icons successfully extracted:", list(icons.keys()))
