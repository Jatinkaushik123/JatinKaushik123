import xml.etree.ElementTree as ET
import glob
import re

svg_files = glob.glob('assets/*.svg')
print(f"Found {len(svg_files)} SVGs to verify.")

for path in sorted(svg_files):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. XML parse
    try:
        root = ET.fromstring(content)
        vb = root.attrib.get('viewBox', 'NONE')
        w = root.attrib.get('width', 'NONE')
        h = root.attrib.get('height', 'NONE')
        print(f"[PASS] {path}: Valid XML. viewBox={vb}, width={w}, height={h}")
    except Exception as e:
        print(f"[FAIL] {path}: XML Parse Error: {e}")
        continue

    # 2. Check for external network requests
    # Search for http:// or https:// outside of standard XML namespaces
    urls = re.findall(r'(https?://[^\s"\'<>]+)', content)
    external_urls = [u for u in urls if not (u.startswith('http://www.w3.org/') or u.startswith('https://www.w3.org/'))]
    if external_urls:
        print(f"  WARNING: Found external URLs in {path}: {external_urls}")
    else:
        print(f"  [PASS] {path}: ZERO external network requests. Completely self-contained.")

    # 3. Check for disallowed foreignObject or script tags
    if '<foreignObject' in content or '<script' in content:
        print(f"  [FAIL] {path}: Disallowed foreignObject or script found!")
    else:
        print(f"  [PASS] {path}: No foreignObject or script tags.")
