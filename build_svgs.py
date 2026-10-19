import os
import json
import base64

def get_base64_font(font_path):
    with open(font_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

print("Loading fonts...")
space_grotesk_b64 = get_base64_font("fonts/space-grotesk-bold.woff2")
jetbrains_mono_b64 = get_base64_font("fonts/jetbrains-mono-semibold.woff2")

print("Loading icons...")
with open("assets/icons/extracted_icons.json", "r", encoding="utf-8") as f:
    icons = json.load(f)

print("Loading images...")
id_b64 = get_base64_image("assets/id.png")
pointing_b64 = get_base64_image("assets/right_pointing.png")

# Common font styles with fallback
def get_font_css(prefix):
    return f"""
    @font-face {{
      font-family: '{prefix}-Display';
      src: url('data:font/woff2;base64,{space_grotesk_b64}') format('woff2');
      font-weight: 700;
      font-style: normal;
    }}
    @font-face {{
      font-family: '{prefix}-Mono';
      src: url('data:font/woff2;base64,{jetbrains_mono_b64}') format('woff2');
      font-weight: 600;
      font-style: normal;
    }}
    .{prefix}-font-display {{
      font-family: '{prefix}-Display', 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    .{prefix}-font-mono {{
      font-family: '{prefix}-Mono', 'JetBrains Mono', 'SF Mono', Consolas, 'Courier New', monospace;
    }}
    """

# -------------------------------------------------------------
# 1. assets/hero.svg
# -------------------------------------------------------------
def build_hero_svg():
    prefix = "hero"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 450" width="100%" height="100%">
  <defs>
    <style>
      {get_font_css(prefix)}
      
      /* Base animations */
      @keyframes heroFadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
      }}
      @keyframes heroSlideUp {{
        from {{ transform: translateY(40px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
      }}
      @keyframes heroNameReveal {{
        0% {{ transform: translateY(68px); }}
        100% {{ transform: translateY(0); }}
      }}
      @keyframes heroCursorBlink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
      @keyframes heroPulseGlow {{
        0%, 100% {{ opacity: 0.25; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(1.04); }}
      }}
      @keyframes heroFloatPortrait {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-7px); }}
      }}

      /* Cycling 4 roles (12s total: 3s each) */
      @keyframes roleCycle1 {{
        0%, 22% {{ opacity: 1; transform: translateY(0); }}
        25%, 97% {{ opacity: 0; transform: translateY(-8px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes roleCycle2 {{
        0%, 22% {{ opacity: 0; transform: translateY(8px); }}
        25%, 47% {{ opacity: 1; transform: translateY(0); }}
        50%, 100% {{ opacity: 0; transform: translateY(-8px); }}
      }}
      @keyframes roleCycle3 {{
        0%, 47% {{ opacity: 0; transform: translateY(8px); }}
        50%, 72% {{ opacity: 1; transform: translateY(0); }}
        75%, 100% {{ opacity: 0; transform: translateY(-8px); }}
      }}
      @keyframes roleCycle4 {{
        0%, 72% {{ opacity: 0; transform: translateY(8px); }}
        75%, 97% {{ opacity: 1; transform: translateY(0); }}
        100% {{ opacity: 0; transform: translateY(8px); }}
      }}

      .hero-greeting {{
        animation: heroSlideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
      }}
      .hero-name-group {{
        animation: heroNameReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.25s both;
      }}
      .hero-cursor {{
        animation: heroCursorBlink 0.8s infinite;
      }}
      .hero-role-1 {{ animation: roleCycle1 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}
      .hero-role-2 {{ animation: roleCycle2 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}
      .hero-role-3 {{ animation: roleCycle3 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}
      .hero-role-4 {{ animation: roleCycle4 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}

      .hero-portrait-anim {{
        animation: heroFloatPortrait 5s ease-in-out infinite;
      }}
      .hero-badge-glow {{
        animation: heroPulseGlow 3s ease-in-out infinite;
      }}

      @media (prefers-reduced-motion: reduce) {{
        .hero-greeting, .hero-name-group, .hero-cursor,
        .hero-role-1, .hero-role-2, .hero-role-3, .hero-role-4,
        .hero-portrait-anim, .hero-badge-glow {{
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
        }}
        .hero-role-2, .hero-role-3, .hero-role-4 {{
          display: none;
        }}
      }}
    </style>

    <!-- Hairline Gradients -->
    <linearGradient id="{prefix}-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.8"/>
      <stop offset="45%" stop-color="#247bff" stop-opacity="0.2"/>
      <stop offset="70%" stop-color="#ff354f" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.8"/>
    </linearGradient>

    <linearGradient id="{prefix}-role-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff354f" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0.9"/>
    </linearGradient>

    <linearGradient id="{prefix}-text-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>

    <radialGradient id="{prefix}-blue-glow" cx="15%" cy="20%" r="55%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="{prefix}-crimson-glow" cx="85%" cy="85%" r="55%">
      <stop offset="0%" stop-color="#ff354f" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="{prefix}-portrait-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.35"/>
      <stop offset="60%" stop-color="#ff354f" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#070b16" stop-opacity="0"/>
    </radialGradient>

    <!-- Dot Pattern -->
    <pattern id="{prefix}-dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.5" fill="#38bdf8" fill-opacity="0.02"/>
    </pattern>

    <!-- Name Mask Reveal -->
    <clipPath id="{prefix}-name-clip">
      <rect x="42" y="85" width="510" height="72"/>
    </clipPath>

    <!-- Portrait Clip for Card Frame -->
    <clipPath id="{prefix}-portrait-frame">
      <rect x="525" y="38" width="275" height="374" rx="20"/>
    </clipPath>
  </defs>

  <!-- Background Base -->
  <rect width="840" height="450" rx="16" fill="#070b16"/>
  <rect width="840" height="450" rx="16" fill="url(#{prefix}-blue-glow)"/>
  <rect width="840" height="450" rx="16" fill="url(#{prefix}-crimson-glow)"/>
  <rect width="840" height="450" rx="16" fill="url(#{prefix}-dots)"/>
  <rect width="838" height="448" x="1" y="1" rx="15" fill="none" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

  <!-- Left Content Column -->
  <!-- Top Terminal Badge -->
  <g class="hero-greeting" transform="translate(42, 42)">
    <rect width="280" height="28" rx="14" fill="#0c1527" stroke="#1e2d4d" stroke-width="1"/>
    <circle cx="16" cy="14" r="4" fill="#10b981"/>
    <text x="28" y="18" fill="#94a3b8" font-size="11" class="{prefix}-font-mono" letter-spacing="1">SYSTEM: ONLINE // NCR-IN</text>
  </g>

  <!-- Greeting Typed Prompt -->
  <g class="hero-greeting" transform="translate(42, 90)">
    <text x="0" y="0" fill="#247bff" font-size="14" class="{prefix}-font-mono" font-weight="600" letter-spacing="1.5">&gt; HELLO, WORLD! I AM</text>
    <rect x="175" y="-12" width="8" height="15" fill="#247bff" class="hero-cursor"/>
  </g>

  <!-- Rising-Mask Name Reveal -->
  <g clip-path="url(#{prefix}-name-clip)">
    <g class="hero-name-group">
      <text x="42" y="142" fill="url(#{prefix}-text-grad)" font-size="48" font-weight="700" class="{prefix}-font-display" letter-spacing="1.5">JATIN KAUSHIK</text>
    </g>
  </g>

  <!-- Cycling Roles Section -->
  <g transform="translate(42, 178)">
    <!-- Role Container Capsule -->
    <rect width="360" height="38" rx="8" fill="#0c1426" stroke="url(#{prefix}-role-border)" stroke-width="1.2"/>
    
    <!-- Prefix Tag -->
    <rect x="1" y="1" width="70" height="36" rx="7" fill="#ff354f" fill-opacity="0.14"/>
    <text x="14" y="24" fill="#ff354f" font-size="11" class="{prefix}-font-mono" font-weight="700" letter-spacing="1.5">ROLE</text>
    <text x="75" y="24" fill="#384968" font-size="13" class="{prefix}-font-mono">//</text>

    <!-- Role 1: B.Tech Student -->
    <g class="hero-role-1">
      <text x="96" y="24" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">B.Tech Student</text>
    </g>

    <!-- Role 2: ACM BMU Tech Lead -->
    <g class="hero-role-2">
      <text x="96" y="24" fill="#38bdf8" font-size="14" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">ACM BMU Tech Lead</text>
    </g>

    <!-- Role 3: Full-Stack Explorer -->
    <g class="hero-role-3">
      <text x="96" y="24" fill="#f43f5e" font-size="14" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">Full-Stack Explorer</text>
    </g>

    <!-- Role 4: Problem Solver -->
    <g class="hero-role-4">
      <text x="96" y="24" fill="#a855f7" font-size="14" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">Problem Solver</text>
    </g>
  </g>

  <!-- One-Line Pitch -->
  <g transform="translate(42, 246)">
    <text x="0" y="0" fill="#94a3b8" font-size="14.5" class="{prefix}-font-mono" line-height="1.5">
      <tspan x="0" dy="0">Engineering student building scalable full-stack web</tspan>
      <tspan x="0" dy="23">solutions and data-driven systems.</tspan>
    </text>
  </g>

  <!-- Location & Company / Education Row -->
  <g transform="translate(42, 320)">
    <!-- Location Chip -->
    <g transform="translate(0, 0)">
      <rect width="185" height="42" rx="10" fill="#0b1324" stroke="#1d2c49" stroke-width="1"/>
      <!-- Map Pin Icon -->
      <path transform="translate(14, 11) scale(0.85)" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="#247bff"/>
      <text x="42" y="19" fill="#64748b" font-size="9.5" class="{prefix}-font-mono" letter-spacing="1">LOCATION</text>
      <text x="42" y="32" fill="#e2e8f0" font-size="12" class="{prefix}-font-display" font-weight="700">Delhi NCR, India</text>
    </g>

    <!-- University Chip -->
    <g transform="translate(197, 0)">
      <rect width="275" height="42" rx="10" fill="#0b1324" stroke="#1d2c49" stroke-width="1"/>
      <!-- Mortarboard Icon -->
      <path transform="translate(14, 11) scale(0.85)" d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3z M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z" fill="#ff354f"/>
      <text x="42" y="19" fill="#64748b" font-size="9.5" class="{prefix}-font-mono" letter-spacing="1">INSTITUTION &amp; ROLE</text>
      <text x="42" y="32" fill="#e2e8f0" font-size="12" class="{prefix}-font-display" font-weight="700">BML Munjal University</text>
    </g>
  </g>

  <!-- Bottom Mini Tech Indicator -->
  <g transform="translate(42, 396)">
    <text x="0" y="0" fill="#475569" font-size="11" class="{prefix}-font-mono">STACK HIGHLIGHTS // REACT • NODE • PYTHON • C++ • DSA • GIT</text>
  </g>

  <!-- Right Column: Portrait Card -->
  <!-- Ambient Glow Behind Portrait -->
  <ellipse cx="660" cy="225" rx="160" ry="170" fill="url(#{prefix}-portrait-glow)" class="hero-badge-glow"/>

  <!-- Portrait Frame Card -->
  <g transform="translate(525, 38)">
    <!-- Base Card Container -->
    <rect width="275" height="374" rx="20" fill="#09101f" stroke="url(#{prefix}-card-border)" stroke-width="1.5"/>
    
    <!-- Top Card Bar -->
    <rect width="275" height="32" rx="20" fill="#0d182e"/>
    <rect y="20" width="275" height="12" fill="#0d182e"/>
    <circle cx="20" cy="16" r="4.5" fill="#ff354f"/>
    <circle cx="34" cy="16" r="4.5" fill="#f59e0b"/>
    <circle cx="48" cy="16" r="4.5" fill="#10b981"/>
    <text x="255" y="20" fill="#475569" font-size="10" text-anchor="end" class="{prefix}-font-mono">ID: JK-BMU</text>

    <!-- Embedded Portrait image with exact alpha -->
    <g clip-path="url(#{prefix}-portrait-frame)">
      <g class="hero-portrait-anim">
        <!-- Exact id.png (1086x1448) positioned and scaled cleanly -->
        <image href="{id_b64}" x="-10" y="36" width="295" height="393" preserveAspectRatio="xMidYMid slice"/>
      </g>
    </g>

    <!-- Gradient Edge Overlay at Card Bottom to blend frame -->
    <linearGradient id="{prefix}-portrait-bottom-fade" x1="0" y1="0" x2="0" y2="100%">
      <stop offset="0%" stop-color="#09101f" stop-opacity="0"/>
      <stop offset="65%" stop-color="#09101f" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#09101f" stop-opacity="0.95"/>
    </linearGradient>
    <rect x="0" y="280" width="275" height="94" rx="20" fill="url(#{prefix}-portrait-bottom-fade)"/>

    <!-- Verified Badge Overlay -->
    <g transform="translate(18, 324)">
      <rect width="239" height="36" rx="8" fill="#0b1426" stroke="#247bff" stroke-width="1" stroke-opacity="0.8"/>
      <!-- Checkmark Hexagon -->
      <polygon points="18,10 26,14 26,24 18,28 10,24 10,14" fill="#247bff"/>
      <path d="M14 19l3 3 5-5" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="36" y="17" fill="#60a5fa" font-size="9" class="{prefix}-font-mono" letter-spacing="1">VERIFIED QUALIFIER</text>
      <text x="36" y="28" fill="#f1f5f9" font-size="10.5" class="{prefix}-font-display" font-weight="700">Odoo '26 • SIH Team Lead</text>
    </g>
  </g>
</svg>"""
    with open("assets/hero.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Built assets/hero.svg successfully!")


# -------------------------------------------------------------
# 2. assets/about-life.svg
# -------------------------------------------------------------
def build_about_svg():
    prefix = "about"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 410" width="100%" height="100%">
  <defs>
    <style>
      {get_font_css(prefix)}

      /* 12-second Carousel Cycle (4s each slide) */
      @keyframes aboutSlide1 {{
        0%, 30% {{ opacity: 1; transform: translateY(0); }}
        33%, 97% {{ opacity: 0; transform: translateY(12px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes aboutSlide2 {{
        0%, 30% {{ opacity: 0; transform: translateY(-12px); }}
        33.3%, 63.3% {{ opacity: 1; transform: translateY(0); }}
        66.6%, 100% {{ opacity: 0; transform: translateY(12px); }}
      }}
      @keyframes aboutSlide3 {{
        0%, 63.3% {{ opacity: 0; transform: translateY(-12px); }}
        66.6%, 96.6% {{ opacity: 1; transform: translateY(0); }}
        100% {{ opacity: 0; transform: translateY(12px); }}
      }}

      /* Segment Progress Bars: 12s loop */
      @keyframes aboutProgress1 {{
        0% {{ width: 0px; }}
        33.3% {{ width: 104px; }}
        98% {{ width: 104px; }}
        100% {{ width: 0px; }}
      }}
      @keyframes aboutProgress2 {{
        0%, 33.3% {{ width: 0px; }}
        66.6% {{ width: 104px; }}
        98% {{ width: 104px; }}
        100% {{ width: 0px; }}
      }}
      @keyframes aboutProgress3 {{
        0%, 66.6% {{ width: 0px; }}
        98% {{ width: 104px; }}
        100% {{ width: 0px; }}
      }}

      .about-carousel-1 {{ animation: aboutSlide1 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}
      .about-carousel-2 {{ animation: aboutSlide2 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}
      .about-carousel-3 {{ animation: aboutSlide3 12s infinite cubic-bezier(0.4, 0, 0.2, 1); }}

      .about-bar-1 {{ animation: aboutProgress1 12s infinite linear; }}
      .about-bar-2 {{ animation: aboutProgress2 12s infinite linear; }}
      .about-bar-3 {{ animation: aboutProgress3 12s infinite linear; }}

      @media (prefers-reduced-motion: reduce) {{
        .about-carousel-1, .about-carousel-2, .about-carousel-3,
        .about-bar-1, .about-bar-2, .about-bar-3 {{
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
        }}
        .about-carousel-2, .about-carousel-3 {{
          display: none;
        }}
        .about-bar-1, .about-bar-2, .about-bar-3 {{
          width: 104px !important;
        }}
      }}
    </style>

    <linearGradient id="{prefix}-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.7"/>
      <stop offset="50%" stop-color="#247bff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.7"/>
    </linearGradient>

    <linearGradient id="{prefix}-bar-fill" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#247bff"/>
      <stop offset="100%" stop-color="#ff354f"/>
    </linearGradient>

    <pattern id="{prefix}-dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.5" fill="#38bdf8" fill-opacity="0.02"/>
    </pattern>

    <clipPath id="{prefix}-carousel-window">
      <rect x="0" y="0" width="370" height="250"/>
    </clipPath>
  </defs>

  <!-- Background Base -->
  <rect width="840" height="410" rx="16" fill="#070b16"/>
  <rect width="840" height="410" rx="16" fill="url(#{prefix}-dots)"/>
  <rect width="838" height="408" x="1" y="1" rx="15" fill="none" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

  <!-- Section Header -->
  <g transform="translate(42, 40)">
    <text x="0" y="0" fill="#ff354f" font-size="12" class="{prefix}-font-mono" font-weight="700" letter-spacing="1.5">// 01. PROFILE &amp; TRAJECTORY</text>
    <text x="0" y="24" fill="#f8fafc" font-size="22" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">ENGINEERING CAPABILITIES &amp; LIFE FOCUS</text>
  </g>

  <!-- Left Column: Core Capabilities (width: 380px) -->
  <g transform="translate(42, 95)">
    <!-- Capability 1 -->
    <g transform="translate(0, 0)">
      <rect width="365" height="80" rx="12" fill="#0a1224" stroke="#1d2a45" stroke-width="1"/>
      <circle cx="28" cy="28" r="14" fill="#247bff" fill-opacity="0.15"/>
      <!-- Layers / Stack Icon -->
      <path transform="translate(19, 19) scale(0.75)" d="M12 2L2 7l10 5 10-5-10-5z M2 17l10 5 10-5M2 12l10 5 10-5" fill="none" stroke="#247bff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="52" y="24" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">Full-Stack Architecture</text>
      <text x="52" y="42" fill="#38bdf8" font-size="10.5" class="{prefix}-font-mono">React · Vite · Node.js · Express · MongoDB</text>
      <text x="52" y="62" fill="#94a3b8" font-size="11.5" class="{prefix}-font-mono">Scalable microservices, REST APIs &amp; responsive UI.</text>
    </g>

    <!-- Capability 2 -->
    <g transform="translate(0, 92)">
      <rect width="365" height="80" rx="12" fill="#0a1224" stroke="#1d2a45" stroke-width="1"/>
      <circle cx="28" cy="28" r="14" fill="#ff354f" fill-opacity="0.15"/>
      <!-- CPU / DSA Icon -->
      <path transform="translate(19, 19) scale(0.75)" d="M4 4h16v16H4z M9 9h6v6H9z M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 15h3M1 9h3M1 15h3" fill="none" stroke="#ff354f" stroke-width="2" stroke-linecap="round"/>
      <text x="52" y="24" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">Algorithmic Problem Solving</text>
      <text x="52" y="42" fill="#f43f5e" font-size="10.5" class="{prefix}-font-mono">Python · C · Java · Data Structures</text>
      <text x="52" y="62" fill="#94a3b8" font-size="11.5" class="{prefix}-font-mono">Algorithm optimization, logic purity &amp; complexity control.</text>
    </g>

    <!-- Capability 3 -->
    <g transform="translate(0, 184)">
      <rect width="365" height="80" rx="12" fill="#0a1224" stroke="#1d2a45" stroke-width="1"/>
      <circle cx="28" cy="28" r="14" fill="#10b981" fill-opacity="0.15"/>
      <!-- Network / Community Icon -->
      <path transform="translate(19, 19) scale(0.75)" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2 M9 11a4 4 0 100-8 4 4 0 000 8zm14 10v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="52" y="24" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">Technical Leadership</text>
      <text x="52" y="42" fill="#34d399" font-size="10.5" class="{prefix}-font-mono">ACM BMU Tech Lead · Git · Mentorship</text>
      <text x="52" y="62" fill="#94a3b8" font-size="11.5" class="{prefix}-font-mono">Spearheading dev squads, bootcamps &amp; hackathon sprints.</text>
    </g>
  </g>

  <!-- Right Column: 3-Slide Carousel Card (width: 375px) -->
  <g transform="translate(425, 95)">
    <!-- Container Card -->
    <rect width="372" height="264" rx="14" fill="#091122" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

    <!-- Progress Bars Header Area -->
    <g transform="translate(18, 16)">
      <!-- Segment 1 Base -->
      <rect x="0" y="0" width="106" height="4" rx="2" fill="#1a253d"/>
      <rect x="0" y="0" width="0" height="4" rx="2" fill="url(#{prefix}-bar-fill)" class="about-bar-1"/>

      <!-- Segment 2 Base -->
      <rect x="114" y="0" width="106" height="4" rx="2" fill="#1a253d"/>
      <rect x="114" y="0" width="0" height="4" rx="2" fill="url(#{prefix}-bar-fill)" class="about-bar-2"/>

      <!-- Segment 3 Base -->
      <rect x="228" y="0" width="106" height="4" rx="2" fill="#1a253d"/>
      <rect x="228" y="0" width="0" height="4" rx="2" fill="url(#{prefix}-bar-fill)" class="about-bar-3"/>
    </g>

    <!-- Carousel Slides Container -->
    <g transform="translate(18, 32)">
      <!-- SLIDE 1: Hackathons (0s - 4s) -->
      <g class="about-carousel-1">
        <!-- Tag -->
        <g transform="translate(0, 8)">
          <rect width="165" height="22" rx="11" fill="#ff354f" fill-opacity="0.15"/>
          <text x="10" y="15" fill="#ff354f" font-size="10" class="{prefix}-font-mono" font-weight="700">01 // HACKATHONS</text>
        </g>
        <text x="0" y="56" fill="#f8fafc" font-size="18" class="{prefix}-font-display" font-weight="700">Competitive Prototyping</text>
        <text x="0" y="78" fill="#38bdf8" font-size="12" class="{prefix}-font-mono" font-weight="600">★ Odoo Qualifier '26 • SIH Team Lead</text>
        
        <rect x="0" y="92" width="336" height="1" fill="#1e293b"/>
        
        <text x="0" y="116" fill="#94a3b8" font-size="12" class="{prefix}-font-mono">
          <tspan x="0" dy="0">Taking complex problem statements from 0 to 1</tspan>
          <tspan x="0" dy="20">under high-velocity 36-hour sprint environments.</tspan>
          <tspan x="0" dy="20">Architected Modular Inventory for Odoo and led</tspan>
          <tspan x="0" dy="20">AI Anomaly Audit pipeline for SIH 2026.</tspan>
        </text>

        <rect x="0" y="185" width="130" height="24" rx="6" fill="#162035"/>
        <text x="12" y="201" fill="#64748b" font-size="10" class="{prefix}-font-mono">STATUS: ACTIVE SPRINT</text>
      </g>

      <!-- SLIDE 2: Tech Communities (4s - 8s) -->
      <g class="about-carousel-2">
        <!-- Tag -->
        <g transform="translate(0, 8)">
          <rect width="185" height="22" rx="11" fill="#247bff" fill-opacity="0.15"/>
          <text x="10" y="15" fill="#38bdf8" font-size="10" class="{prefix}-font-mono" font-weight="700">02 // TECH COMMUNITIES</text>
        </g>
        <text x="0" y="56" fill="#f8fafc" font-size="18" class="{prefix}-font-display" font-weight="700">ACM BMU Tech Lead</text>
        <text x="0" y="78" fill="#38bdf8" font-size="12" class="{prefix}-font-mono" font-weight="600">★ Chapter Leadership &amp; Mentorship</text>
        
        <rect x="0" y="92" width="336" height="1" fill="#1e293b"/>
        
        <text x="0" y="116" fill="#94a3b8" font-size="12" class="{prefix}-font-mono">
          <tspan x="0" dy="0">Spearheading campus developer culture, organizing</tspan>
          <tspan x="0" dy="20">hands-on web development bootcamps, algorithmic</tspan>
          <tspan x="0" dy="20">problem solving rounds, and mentoring student</tspan>
          <tspan x="0" dy="20">engineers across stacks.</tspan>
        </text>

        <rect x="0" y="185" width="145" height="24" rx="6" fill="#162035"/>
        <text x="12" y="201" fill="#64748b" font-size="10" class="{prefix}-font-mono">COMMUNITY: ACM BMU</text>
      </g>

      <!-- SLIDE 3: Exploring New Frameworks (8s - 12s) -->
      <g class="about-carousel-3">
        <!-- Tag -->
        <g transform="translate(0, 8)">
          <rect width="210" height="22" rx="11" fill="#10b981" fill-opacity="0.15"/>
          <text x="10" y="15" fill="#34d399" font-size="10" class="{prefix}-font-mono" font-weight="700">03 // NEW FRAMEWORKS</text>
        </g>
        <text x="0" y="56" fill="#f8fafc" font-size="18" class="{prefix}-font-display" font-weight="700">Exploration &amp; Toolchains</text>
        <text x="0" y="78" fill="#34d399" font-size="12" class="{prefix}-font-mono" font-weight="600">★ Modern Runtimes &amp; AI Pipelines</text>
        
        <rect x="0" y="92" width="336" height="1" fill="#1e293b"/>
        
        <text x="0" y="116" fill="#94a3b8" font-size="12" class="{prefix}-font-mono">
          <tspan x="0" dy="0">Continuously experimenting with modern Vite</tspan>
          <tspan x="0" dy="20">toolchains, high-performance web standards,</tspan>
          <tspan x="0" dy="20">data analytics engines (MausamCrop), and machine</tspan>
          <tspan x="0" dy="20">learning anomaly audit pipelines.</tspan>
        </text>

        <rect x="0" y="185" width="140" height="24" rx="6" fill="#162035"/>
        <text x="12" y="201" fill="#64748b" font-size="10" class="{prefix}-font-mono">MINDSET: ZERO TO ONE</text>
      </g>
    </g>
  </g>
</svg>"""
    with open("assets/about-life.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Built assets/about-life.svg successfully!")


# -------------------------------------------------------------
# 3. assets/stack.svg
# -------------------------------------------------------------
def build_stack_svg():
    prefix = "stack"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 480" width="100%" height="100%">
  <defs>
    <style>
      {get_font_css(prefix)}

      /* Orbital rotation / gentle sway */
      @keyframes stackOrb1 {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}
      @keyframes stackPulseCore {{
        0%, 100% {{ r: 24px; opacity: 0.8; }}
        50% {{ r: 28px; opacity: 1; }}
      }}
      @keyframes stackFloatBadge {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-4px); }}
      }}

      .stack-core-pulse {{ animation: stackPulseCore 3s ease-in-out infinite; }}
      .stack-float {{ animation: stackFloatBadge 4s ease-in-out infinite; }}

      @media (prefers-reduced-motion: reduce) {{
        .stack-core-pulse, .stack-float {{
          animation: none !important;
        }}
      }}
    </style>

    <linearGradient id="{prefix}-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#247bff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.8"/>
    </linearGradient>

    <linearGradient id="{prefix}-core-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff354f"/>
      <stop offset="100%" stop-color="#247bff"/>
    </linearGradient>

    <radialGradient id="{prefix}-core-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#ff354f" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#070b16" stop-opacity="0"/>
    </radialGradient>

    <pattern id="{prefix}-dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.5" fill="#38bdf8" fill-opacity="0.02"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="840" height="480" rx="16" fill="#070b16"/>
  <rect width="840" height="480" rx="16" fill="url(#{prefix}-dots)"/>
  <rect width="838" height="478" x="1" y="1" rx="15" fill="none" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

  <!-- Section Header -->
  <g transform="translate(42, 38)">
    <text x="0" y="0" fill="#247bff" font-size="12" class="{prefix}-font-mono" font-weight="700" letter-spacing="1.5">// 02. TECHNOLOGY MATRIX</text>
    <text x="0" y="24" fill="#f8fafc" font-size="22" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">THREE-TIER ORBITAL TECH STACK</text>
  </g>

  <!-- Center Core & 3 Tilted Elliptical Orbits (Center at cx=420, cy=200) -->
  <g transform="translate(0, 0)">
    <!-- Radial Glow Behind Orbits -->
    <ellipse cx="420" cy="205" rx="240" ry="110" fill="url(#{prefix}-core-glow)"/>

    <!-- Tilted Elliptical Orbits (Tilted -12deg) -->
    <!-- Orbit 3: Outer (Languages & Tools) rx=350, ry=110 -->
    <g transform="rotate(-12, 420, 205)">
      <ellipse cx="420" cy="205" rx="350" ry="110" fill="none" stroke="#247bff" stroke-width="1.2" stroke-dasharray="6 8" stroke-opacity="0.35"/>
      <text x="760" y="200" fill="#334155" font-size="9" class="{prefix}-font-mono">ORBIT 03 // CORE &amp; TOOLS</text>
    </g>

    <!-- Orbit 2: Middle (Backend & DB) rx=250, ry=78 -->
    <g transform="rotate(-12, 420, 205)">
      <ellipse cx="420" cy="205" rx="250" ry="78" fill="none" stroke="#ff354f" stroke-width="1.2" stroke-dasharray="5 7" stroke-opacity="0.4"/>
      <text x="660" y="195" fill="#334155" font-size="9" class="{prefix}-font-mono">ORBIT 02 // BACKEND</text>
    </g>

    <!-- Orbit 1: Inner (Frontend) rx=150, ry=48 -->
    <g transform="rotate(-12, 420, 205)">
      <ellipse cx="420" cy="205" rx="150" ry="48" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4 6" stroke-opacity="0.55"/>
      <text x="560" y="190" fill="#334155" font-size="9" class="{prefix}-font-mono">ORBIT 01 // FRONTEND</text>
    </g>

    <!-- Center Nucleus (JK Full-Stack Core) -->
    <g transform="translate(420, 205)">
      <circle cx="0" cy="0" r="28" fill="url(#{prefix}-core-glow)"/>
      <circle cx="0" cy="0" r="22" fill="#0b1325" stroke="url(#{prefix}-core-grad)" stroke-width="2"/>
      <text x="0" y="4" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="700" class="{prefix}-font-display" letter-spacing="1">JK</text>
      <text x="0" y="14" text-anchor="middle" fill="#38bdf8" font-size="7" font-weight="700" class="{prefix}-font-mono">CORE</text>
    </g>

    <!-- Correctly Labelled Tech Icons on Orbits -->
    
    <!-- INNER ORBIT (Frontend): React, Vite -->
    <!-- React (Orbit 1, left) -->
    <g transform="translate(290, 165)" class="stack-float">
      <rect x="-38" y="-18" width="76" height="36" rx="18" fill="#0b1428" stroke="#61dafb" stroke-width="1.2"/>
      <g transform="translate(-28, -10) scale(0.85)">
        <path d="{icons['react'][0]}" fill="#61dafb"/>
      </g>
      <text x="2" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">React</text>
    </g>

    <!-- Vite (Orbit 1, right) -->
    <g transform="translate(545, 235)" class="stack-float">
      <rect x="-36" y="-18" width="72" height="36" rx="18" fill="#0b1428" stroke="#bd34fe" stroke-width="1.2"/>
      <g transform="translate(-26, -10) scale(0.85)">
        <path d="{icons['vite'][0]}" fill="#bd34fe"/>
      </g>
      <text x="2" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">Vite</text>
    </g>


    <!-- MIDDLE ORBIT (Backend & DB): Node.js, Express, MongoDB -->
    <!-- Node.js (Orbit 2, top-center) -->
    <g transform="translate(390, 105)" class="stack-float">
      <rect x="-44" y="-18" width="88" height="36" rx="18" fill="#0b1428" stroke="#5fa04e" stroke-width="1.2"/>
      <g transform="translate(-34, -10) scale(0.85)">
        <path d="{icons['nodejs'][0]}" fill="#5fa04e"/>
      </g>
      <text x="-4" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">Node.js</text>
    </g>

    <!-- Express (Orbit 2, left-bottom) -->
    <g transform="translate(200, 245)" class="stack-float">
      <rect x="-42" y="-18" width="84" height="36" rx="18" fill="#0b1428" stroke="#cbd5e1" stroke-width="1.2"/>
      <g transform="translate(-32, -10) scale(0.85)">
        <path d="{icons['express'][0]}" fill="#f8fafc"/>
      </g>
      <text x="-3" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">Express</text>
    </g>

    <!-- MongoDB (Orbit 2, right-middle) -->
    <g transform="translate(640, 160)" class="stack-float">
      <rect x="-46" y="-18" width="92" height="36" rx="18" fill="#0b1428" stroke="#47a248" stroke-width="1.2"/>
      <g transform="translate(-36, -10) scale(0.85)">
        <path d="{icons['mongodb'][0]}" fill="#47a248"/>
      </g>
      <text x="-6" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">MongoDB</text>
    </g>


    <!-- OUTER ORBIT (Languages & Tooling): Python, C, Java, Git -->
    <!-- Python (Orbit 3, top-left) -->
    <g transform="translate(190, 120)" class="stack-float">
      <rect x="-42" y="-18" width="84" height="36" rx="18" fill="#0b1428" stroke="#3776ab" stroke-width="1.2"/>
      <g transform="translate(-32, -10) scale(0.85)">
        <path d="{icons['python'][0]}" fill="#3776ab"/>
      </g>
      <text x="-2" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">Python</text>
    </g>

    <!-- C Language (Orbit 3, bottom-left) -->
    <g transform="translate(95, 215)" class="stack-float">
      <rect x="-30" y="-18" width="60" height="36" rx="18" fill="#0b1428" stroke="#a8b9cc" stroke-width="1.2"/>
      <g transform="translate(-20, -10) scale(0.85)">
        <path d="{icons['c'][0]}" fill="#a8b9cc"/>
      </g>
      <text x="3" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">C</text>
    </g>

    <!-- Java (Orbit 3, bottom-right) -->
    <g transform="translate(470, 305)" class="stack-float">
      <rect x="-36" y="-18" width="72" height="36" rx="18" fill="#0b1428" stroke="#e76f00" stroke-width="1.2"/>
      <g transform="translate(-26, -10) scale(0.85)">
        <path d="{icons['java'][0]}" fill="#e76f00"/>
      </g>
      <text x="2" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">Java</text>
    </g>

    <!-- Git (Orbit 3, far-right) -->
    <g transform="translate(735, 230)" class="stack-float">
      <rect x="-34" y="-18" width="68" height="36" rx="18" fill="#0b1428" stroke="#f05032" stroke-width="1.2"/>
      <g transform="translate(-24, -10) scale(0.85)">
        <path d="{icons['git'][0]}" fill="#f05032"/>
      </g>
      <text x="2" y="5" fill="#f8fafc" font-size="11.5" font-weight="700" class="{prefix}-font-display">Git</text>
    </g>
  </g>

  <!-- Grouped Stack Chips (Bottom Section at y=365) -->
  <g transform="translate(42, 365)">
    <!-- Group 1: Frontend (width: 175) -->
    <g transform="translate(0, 0)">
      <rect width="175" height="85" rx="10" fill="#091122" stroke="#1e2c49" stroke-width="1"/>
      <rect x="1" y="1" width="173" height="24" rx="9" fill="#247bff" fill-opacity="0.12"/>
      <text x="12" y="17" fill="#38bdf8" font-size="10" class="{prefix}-font-mono" font-weight="700">FRONTEND ARCHITECTURE</text>
      <!-- Chips -->
      <g transform="translate(12, 35)">
        <rect width="66" height="26" rx="6" fill="#111c33" stroke="#61dafb" stroke-width="0.8"/>
        <text x="10" y="17" fill="#f8fafc" font-size="11" class="{prefix}-font-display">React</text>
      </g>
      <g transform="translate(86, 35)">
        <rect width="60" height="26" rx="6" fill="#111c33" stroke="#bd34fe" stroke-width="0.8"/>
        <text x="12" y="17" fill="#f8fafc" font-size="11" class="{prefix}-font-display">Vite</text>
      </g>
    </g>

    <!-- Group 2: Backend & DB (width: 200) -->
    <g transform="translate(187, 0)">
      <rect width="200" height="85" rx="10" fill="#091122" stroke="#1e2c49" stroke-width="1"/>
      <rect x="1" y="1" width="198" height="24" rx="9" fill="#ff354f" fill-opacity="0.12"/>
      <text x="12" y="17" fill="#ff354f" font-size="10" class="{prefix}-font-mono" font-weight="700">BACKEND &amp; DATABASE</text>
      <!-- Chips -->
      <g transform="translate(10, 35)">
        <rect width="56" height="26" rx="6" fill="#111c33" stroke="#5fa04e" stroke-width="0.8"/>
        <text x="6" y="17" fill="#f8fafc" font-size="10" class="{prefix}-font-display">Node</text>
      </g>
      <g transform="translate(72, 35)">
        <rect width="56" height="26" rx="6" fill="#111c33" stroke="#cbd5e1" stroke-width="0.8"/>
        <text x="5" y="17" fill="#f8fafc" font-size="10" class="{prefix}-font-display">Express</text>
      </g>
      <g transform="translate(134, 35)">
        <rect width="56" height="26" rx="6" fill="#111c33" stroke="#47a248" stroke-width="0.8"/>
        <text x="5" y="17" fill="#f8fafc" font-size="10" class="{prefix}-font-display">Mongo</text>
      </g>
    </g>

    <!-- Group 3: Core Languages (width: 195) -->
    <g transform="translate(399, 0)">
      <rect width="195" height="85" rx="10" fill="#091122" stroke="#1e2c49" stroke-width="1"/>
      <rect x="1" y="1" width="193" height="24" rx="9" fill="#247bff" fill-opacity="0.12"/>
      <text x="12" y="17" fill="#38bdf8" font-size="10" class="{prefix}-font-mono" font-weight="700">LANGUAGES &amp; DSA</text>
      <!-- Chips -->
      <g transform="translate(10, 35)">
        <rect width="58" height="26" rx="6" fill="#111c33" stroke="#3776ab" stroke-width="0.8"/>
        <text x="8" y="17" fill="#f8fafc" font-size="10.5" class="{prefix}-font-display">Python</text>
      </g>
      <g transform="translate(74, 35)">
        <rect width="46" height="26" rx="6" fill="#111c33" stroke="#a8b9cc" stroke-width="0.8"/>
        <text x="14" y="17" fill="#f8fafc" font-size="10.5" class="{prefix}-font-display">C</text>
      </g>
      <g transform="translate(126, 35)">
        <rect width="58" height="26" rx="6" fill="#111c33" stroke="#e76f00" stroke-width="0.8"/>
        <text x="12" y="17" fill="#f8fafc" font-size="10.5" class="{prefix}-font-display">Java</text>
      </g>
    </g>

    <!-- Group 4: Tooling (width: 150) -->
    <g transform="translate(606, 0)">
      <rect width="150" height="85" rx="10" fill="#091122" stroke="#1e2c49" stroke-width="1"/>
      <rect x="1" y="1" width="148" height="24" rx="9" fill="#ff354f" fill-opacity="0.12"/>
      <text x="12" y="17" fill="#ff354f" font-size="10" class="{prefix}-font-mono" font-weight="700">VCS &amp; WORKFLOW</text>
      <!-- Chips -->
      <g transform="translate(12, 35)">
        <rect width="60" height="26" rx="6" fill="#111c33" stroke="#f05032" stroke-width="0.8"/>
        <text x="17" y="17" fill="#f8fafc" font-size="11" class="{prefix}-font-display">Git</text>
      </g>
      <g transform="translate(78, 35)">
        <rect width="60" height="26" rx="6" fill="#111c33" stroke="#247bff" stroke-width="0.8"/>
        <text x="10" y="17" fill="#38bdf8" font-size="10" class="{prefix}-font-mono">GitHub</text>
      </g>
    </g>
  </g>
</svg>"""
    with open("assets/stack.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Built assets/stack.svg successfully!")


# -------------------------------------------------------------
# 4. assets/id-dashboard.svg
# -------------------------------------------------------------
def build_id_dashboard_svg():
    prefix = "dash"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 500" width="100%" height="100%">
  <defs>
    <style>
      {get_font_css(prefix)}

      /* Hanging Lanyard Physics:
         Drop into place + damped pendulum settlement -> perpetual gentle +/-1.7 degree swing */
      @keyframes dashLanyardDropAndSwing {{
        0% {{ transform: translateY(-70px) rotate(-13deg); }}
        20% {{ transform: translateY(0px) rotate(11deg); }}
        40% {{ transform: rotate(-7deg); }}
        60% {{ transform: rotate(4.2deg); }}
        75% {{ transform: rotate(-2.6deg); }}
        90% {{ transform: rotate(1.7deg); }}
        100% {{ transform: rotate(-1.7deg); }}
      }}
      @keyframes dashPerpetualSwing {{
        0% {{ transform: rotate(-1.7deg); }}
        50% {{ transform: rotate(1.7deg); }}
        100% {{ transform: rotate(-1.7deg); }}
      }}

      /* Foil Light Sweep */
      @keyframes dashFoilSweep {{
        0% {{ transform: translateX(-220px) rotate(25deg); opacity: 0; }}
        20% {{ opacity: 0.7; }}
        40% {{ transform: translateX(280px) rotate(25deg); opacity: 0; }}
        100% {{ transform: translateX(280px) rotate(25deg); opacity: 0; }}
      }}

      /* Laser Barcode Scanner */
      @keyframes dashLaserScan {{
        0%, 100% {{ transform: translateY(0); opacity: 0.9; }}
        50% {{ transform: translateY(22px); opacity: 0.5; }}
      }}

      .dash-lanyard-assembly {{
        transform-origin: 175px 15px;
        animation: dashLanyardDropAndSwing 3.5s cubic-bezier(0.25, 1, 0.5, 1) 0.1s both,
                   dashPerpetualSwing 4.5s ease-in-out 3.6s infinite;
      }}

      .dash-foil-sweep {{
        animation: dashFoilSweep 6s ease-in-out infinite;
      }}
      .dash-laser-line {{
        animation: dashLaserScan 2.5s ease-in-out infinite;
      }}

      @media (prefers-reduced-motion: reduce) {{
        .dash-lanyard-assembly, .dash-foil-sweep, .dash-laser-line {{
          animation: none !important;
          transform: none !important;
        }}
      }}
    </style>

    <linearGradient id="{prefix}-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#247bff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.8"/>
    </linearGradient>

    <linearGradient id="{prefix}-clasp-chrome" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="30%" stop-color="#f8fafc"/>
      <stop offset="50%" stop-color="#64748b"/>
      <stop offset="70%" stop-color="#e2e8f0"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>

    <linearGradient id="{prefix}-foil-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="35%" stop-color="#38bdf8" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.6"/>
      <stop offset="65%" stop-color="#ff354f" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <pattern id="{prefix}-dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.5" fill="#38bdf8" fill-opacity="0.02"/>
    </pattern>

    <!-- Clip Path for ID card body (width: 215, height: 350) -->
    <clipPath id="{prefix}-badge-card-clip">
      <rect x="68" y="75" width="214" height="348" rx="16"/>
    </clipPath>

    <!-- Clip Path for ID Photo Box -->
    <clipPath id="{prefix}-photo-frame">
      <rect x="85" y="132" width="180" height="152" rx="10"/>
    </clipPath>
  </defs>

  <!-- Background Base -->
  <rect width="840" height="500" rx="16" fill="#070b16"/>
  <rect width="840" height="500" rx="16" fill="url(#{prefix}-dots)"/>
  <rect width="838" height="498" x="1" y="1" rx="15" fill="none" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

  <!-- Section Header -->
  <g transform="translate(42, 38)">
    <text x="0" y="0" fill="#ff354f" font-size="12" class="{prefix}-font-mono" font-weight="700" letter-spacing="1.5">// 03. CREDENTIALS &amp; VERIFIED METRICS</text>
    <text x="0" y="24" fill="#f8fafc" font-size="22" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">VERIFIED DASHBOARD &amp; LANYARD ID</text>
  </g>

  <!-- LEFT: HANGING LANYARD ASSEMBLY -->
  <g class="dash-lanyard-assembly">
    <!-- Woven Lanyard Ribbon -->
    <path d="M165 0 L165 42 L185 42 L185 0 Z" fill="#0b1730"/>
    <path d="M164 0 L164 42" stroke="#247bff" stroke-width="1.5"/>
    <path d="M186 0 L186 42" stroke="#ff354f" stroke-width="1.5"/>
    
    <!-- Metal Clasp & Carabiner Ring -->
    <!-- Clasp Ring -->
    <ellipse cx="175" cy="46" rx="9" ry="6" fill="none" stroke="url(#{prefix}-clasp-chrome)" stroke-width="3"/>
    <!-- Clasp Buckle Body -->
    <path d="M168 50 L182 50 L180 66 L170 66 Z" fill="url(#{prefix}-clasp-chrome)"/>
    <circle cx="175" cy="58" r="2.5" fill="#1e293b"/>
    <!-- Carabiner Hook -->
    <path d="M172 66 L178 66 L178 76 L172 76 Z" fill="url(#{prefix}-clasp-chrome)"/>

    <!-- ID Card Body (at x=68, y=75, w=214, h=348, rx=16) -->
    <rect x="68" y="75" width="214" height="348" rx="16" fill="#0a1224" stroke="url(#{prefix}-card-border)" stroke-width="1.5"/>
    
    <!-- Top Slot Punch Hole -->
    <rect x="157" y="83" width="36" height="7" rx="3.5" fill="#070b16" stroke="#334155" stroke-width="1"/>

    <!-- University Header -->
    <g transform="translate(175, 110)">
      <text x="0" y="0" text-anchor="middle" fill="#ff354f" font-size="9" class="{prefix}-font-mono" font-weight="700" letter-spacing="1.2">BML MUNJAL UNIVERSITY</text>
      <text x="0" y="12" text-anchor="middle" fill="#64748b" font-size="8.5" class="{prefix}-font-mono" letter-spacing="1">STUDENT ID CARD // 2026</text>
    </g>

    <!-- Portrait Photo Window -->
    <rect x="85" y="132" width="180" height="152" rx="10" fill="#050811" stroke="#247bff" stroke-width="1" stroke-opacity="0.6"/>
    <!-- Exact id.png embedded with alpha -->
    <g clip-path="url(#{prefix}-photo-frame)">
      <image href="{id_b64}" x="75" y="120" width="200" height="267" preserveAspectRatio="xMidYMid slice"/>
    </g>

    <!-- ID Card Holder Info -->
    <g transform="translate(175, 305)">
      <text x="0" y="0" text-anchor="middle" fill="#f8fafc" font-size="14.5" class="{prefix}-font-display" font-weight="700">JATIN KAUSHIK</text>
      <text x="0" y="15" text-anchor="middle" fill="#38bdf8" font-size="10" class="{prefix}-font-mono" font-weight="600">ACM BMU TECH LEAD</text>
      <text x="0" y="28" text-anchor="middle" fill="#64748b" font-size="8.5" class="{prefix}-font-mono">ID: JK-BMU-2026-ENG</text>
    </g>

    <!-- Barcode Section -->
    <g transform="translate(85, 348)">
      <rect width="180" height="34" rx="4" fill="#070e1c" stroke="#1d2943" stroke-width="0.8"/>
      <!-- Authentic Barcode Lines -->
      <g fill="#cbd5e1" transform="translate(12, 6)">
        <rect x="0" y="0" width="2.5" height="16"/>
        <rect x="4" y="0" width="1.2" height="16"/>
        <rect x="7" y="0" width="3.5" height="16"/>
        <rect x="13" y="0" width="1.2" height="16"/>
        <rect x="16" y="0" width="2.5" height="16"/>
        <rect x="22" y="0" width="4.5" height="16"/>
        <rect x="29" y="0" width="1.2" height="16"/>
        <rect x="33" y="0" width="3" height="16"/>
        <rect x="38" y="0" width="1.2" height="16"/>
        <rect x="42" y="0" width="4" height="16"/>
        <rect x="48" y="0" width="2" height="16"/>
        <rect x="53" y="0" width="1.2" height="16"/>
        <rect x="57" y="0" width="3.5" height="16"/>
        <rect x="63" y="0" width="2.5" height="16"/>
        <rect x="68" y="0" width="1.2" height="16"/>
        <rect x="72" y="0" width="4" height="16"/>
        <rect x="79" y="0" width="1.5" height="16"/>
        <rect x="83" y="0" width="3" height="16"/>
        <rect x="88" y="0" width="1.2" height="16"/>
        <rect x="92" y="0" width="4.5" height="16"/>
        <rect x="99" y="0" width="1.5" height="16"/>
        <rect x="103" y="0" width="3" height="16"/>
        <rect x="108" y="0" width="2" height="16"/>
        <rect x="113" y="0" width="3.5" height="16"/>
        <rect x="119" y="0" width="1.2" height="16"/>
        <rect x="123" y="0" width="4" height="16"/>
        <rect x="130" y="0" width="2" height="16"/>
        <rect x="135" y="0" width="3.5" height="16"/>
        <rect x="141" y="0" width="1.2" height="16"/>
        <rect x="145" y="0" width="4" height="16"/>
        <rect x="152" y="0" width="2" height="16"/>
      </g>
      <!-- Barcode Text -->
      <text x="90" y="30" text-anchor="middle" fill="#64748b" font-size="7.5" class="{prefix}-font-mono" letter-spacing="2">JK-9284-BMU-2026</text>
      
      <!-- Animated Red Laser Scanner Line -->
      <line x1="8" y1="5" x2="172" y2="5" stroke="#ff354f" stroke-width="1.5" stroke-opacity="0.85" class="dash-laser-line"/>
    </g>

    <!-- Subtle Shimmer Foil Sweep across Card -->
    <g clip-path="url(#{prefix}-badge-card-clip)">
      <rect x="0" y="50" width="90" height="400" fill="url(#{prefix}-foil-grad)" class="dash-foil-sweep"/>
    </g>
  </g>


  <!-- RIGHT: VERIFIED METRICS & REPOSITORIES DASHBOARD -->
  <g transform="translate(315, 85)">
    <!-- Container Card (width: 485, height: 375) -->
    <rect width="485" height="375" rx="14" fill="#091122" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

    <!-- Top Status Bar -->
    <g transform="translate(20, 16)">
      <!-- Verified Badge Pill -->
      <rect width="135" height="26" rx="13" fill="#10b981" fill-opacity="0.15" stroke="#10b981" stroke-width="0.8"/>
      <circle cx="14" cy="13" r="4" fill="#10b981"/>
      <text x="26" y="17" fill="#34d399" font-size="10.5" class="{prefix}-font-mono" font-weight="700">VERIFIED METRICS</text>

      <text x="445" y="18" text-anchor="end" fill="#64748b" font-size="10.5" class="{prefix}-font-mono">OMIT UNKNOWN COUNTS</text>
    </g>

    <!-- SECTION 1: VERIFIED, DATED MILESTONES -->
    <g transform="translate(20, 56)">
      <text x="0" y="0" fill="#ff354f" font-size="11" class="{prefix}-font-mono" font-weight="700" letter-spacing="1">DATED MILESTONES &amp; ROLES</text>

      <!-- Milestone 1 -->
      <g transform="translate(0, 12)">
        <rect width="445" height="38" rx="8" fill="#0d172e" stroke="#1e2c49" stroke-width="1"/>
        <rect x="8" y="8" width="55" height="22" rx="4" fill="#ff354f" fill-opacity="0.15"/>
        <text x="16" y="23" fill="#ff354f" font-size="10.5" class="{prefix}-font-mono" font-weight="700">[2026]</text>
        <text x="72" y="24" fill="#f8fafc" font-size="12" class="{prefix}-font-display" font-weight="700">Odoo Hackathon Qualifier</text>
        <text x="250" y="24" fill="#94a3b8" font-size="11" class="{prefix}-font-mono">— Modular Inventory Platform</text>
      </g>

      <!-- Milestone 2 -->
      <g transform="translate(0, 56)">
        <rect width="445" height="38" rx="8" fill="#0d172e" stroke="#1e2c49" stroke-width="1"/>
        <rect x="8" y="8" width="55" height="22" rx="4" fill="#247bff" fill-opacity="0.15"/>
        <text x="16" y="23" fill="#38bdf8" font-size="10.5" class="{prefix}-font-mono" font-weight="700">[2026]</text>
        <text x="72" y="24" fill="#f8fafc" font-size="12" class="{prefix}-font-display" font-weight="700">Smart India Hackathon Team Lead</text>
        <text x="300" y="24" fill="#94a3b8" font-size="11" class="{prefix}-font-mono">— SIH Anomaly Detection</text>
      </g>

      <!-- Milestone 3 -->
      <g transform="translate(0, 100)">
        <rect width="445" height="38" rx="8" fill="#0d172e" stroke="#1e2c49" stroke-width="1"/>
        <rect x="8" y="8" width="85" height="22" rx="4" fill="#10b981" fill-opacity="0.15"/>
        <text x="14" y="23" fill="#34d399" font-size="10.5" class="{prefix}-font-mono" font-weight="700">[2024-2026]</text>
        <text x="102" y="24" fill="#f8fafc" font-size="12" class="{prefix}-font-display" font-weight="700">ACM BMU Tech Lead</text>
        <text x="245" y="24" fill="#94a3b8" font-size="11" class="{prefix}-font-mono">— University Student Chapter</text>
      </g>
    </g>

    <!-- SECTION 2: FEATURED REPOSITORIES (Strictly factual; no guessed counts) -->
    <g transform="translate(20, 214)">
      <text x="0" y="0" fill="#247bff" font-size="11" class="{prefix}-font-mono" font-weight="700" letter-spacing="1">FEATURED REPOSITORIES &amp; SYSTEMS</text>

      <!-- Repo Card 1 -->
      <g transform="translate(0, 12)">
        <rect width="445" height="42" rx="8" fill="#0c152a" stroke="#1d2a45" stroke-width="1"/>
        <text x="14" y="26" fill="#38bdf8" font-size="12" class="{prefix}-font-mono" font-weight="700">Modular Inventory Management</text>
        <text x="240" y="26" fill="#94a3b8" font-size="11" class="{prefix}-font-mono">React · Node · Express · Mongo</text>
        <text x="430" y="26" text-anchor="end" fill="#ff354f" font-size="10" class="{prefix}-font-mono">ODOO '26</text>
      </g>

      <!-- Repo Card 2 -->
      <g transform="translate(0, 58)">
        <rect width="445" height="42" rx="8" fill="#0c152a" stroke="#1d2a45" stroke-width="1"/>
        <text x="14" y="26" fill="#38bdf8" font-size="12" class="{prefix}-font-mono" font-weight="700">MausamCrop Recommendation</text>
        <text x="235" y="26" fill="#94a3b8" font-size="11" class="{prefix}-font-mono">Python · Weather AI · Vite</text>
        <text x="430" y="26" text-anchor="end" fill="#34d399" font-size="10" class="{prefix}-font-mono">AGRI-TECH</text>
      </g>

      <!-- Repo Card 3 -->
      <g transform="translate(0, 104)">
        <rect width="445" height="42" rx="8" fill="#0c152a" stroke="#1d2a45" stroke-width="1"/>
        <text x="14" y="26" fill="#38bdf8" font-size="12" class="{prefix}-font-mono" font-weight="700">SIH Anomaly Detection</text>
        <text x="180" y="26" fill="#94a3b8" font-size="11" class="{prefix}-font-mono">AI Fund-Leakage Audit · MPLADS</text>
        <text x="430" y="26" text-anchor="end" fill="#e76f00" font-size="10" class="{prefix}-font-mono">SIH '26</text>
      </g>
    </g>
  </g>
</svg>"""
    with open("assets/id-dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Built assets/id-dashboard.svg successfully!")


# -------------------------------------------------------------
# 5. assets/connect.svg
# -------------------------------------------------------------
def build_connect_svg():
    prefix = "conn"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 430" width="100%" height="100%">
  <defs>
    <style>
      {get_font_css(prefix)}

      /* Character Floating Animation */
      @keyframes connCharFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-7px); }}
      }}

      /* Nudging Arrow Animation */
      @keyframes connNudgeArrow {{
        0%, 100% {{ transform: translateX(0px); }}
        50% {{ transform: translateX(6px); }}
      }}

      .conn-char-anim {{
        animation: connCharFloat 4.5s ease-in-out infinite;
      }}
      .conn-arrow-anim {{
        animation: connNudgeArrow 1.6s ease-in-out infinite;
      }}

      @media (prefers-reduced-motion: reduce) {{
        .conn-char-anim, .conn-arrow-anim {{
          animation: none !important;
          transform: none !important;
        }}
      }}
    </style>

    <linearGradient id="{prefix}-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#247bff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.8"/>
    </linearGradient>

    <linearGradient id="{prefix}-social-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.6"/>
    </linearGradient>

    <radialGradient id="{prefix}-char-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.3"/>
      <stop offset="60%" stop-color="#ff354f" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#070b16" stop-opacity="0"/>
    </radialGradient>

    <pattern id="{prefix}-dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.5" fill="#38bdf8" fill-opacity="0.02"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="840" height="430" rx="16" fill="#070b16"/>
  <rect width="840" height="430" rx="16" fill="url(#{prefix}-dots)"/>
  <rect width="838" height="428" x="1" y="1" rx="15" fill="none" stroke="url(#{prefix}-card-border)" stroke-width="1.2"/>

  <!-- LEFT: POINTING CHARACTER (right_pointing.png, aspect ratio 3:2, 1536x1024) -->
  <g transform="translate(15, 30)">
    <!-- Radial Glow Behind Character -->
    <ellipse cx="170" cy="210" rx="150" ry="160" fill="url(#{prefix}-char-glow)"/>

    <!-- Exact Transparent right_pointing.png preserved with alpha -->
    <g class="conn-char-anim">
      <!-- 1536x1024 scaled to width 380, height 253 -->
      <image href="{pointing_b64}" x="-10" y="70" width="380" height="253" preserveAspectRatio="xMidYMid meet"/>
    </g>

    <!-- Pointing Indicator Line toward Social Cards -->
    <g transform="translate(320, 205)">
      <circle cx="0" cy="0" r="5" fill="#247bff"/>
      <line x1="0" y1="0" x2="35" y2="0" stroke="#247bff" stroke-width="2" stroke-dasharray="3 3"/>
    </g>
  </g>


  <!-- RIGHT: GENEROUSLY SPACED SOCIAL CARDS -->
  <g transform="translate(365, 38)">
    <!-- Header -->
    <text x="0" y="0" fill="#247bff" font-size="12" class="{prefix}-font-mono" font-weight="700" letter-spacing="1.5">// 04. GET IN TOUCH</text>
    <text x="0" y="24" fill="#f8fafc" font-size="22" class="{prefix}-font-display" font-weight="700" letter-spacing="0.5">LET&apos;S BUILD SOMETHING EXTRAORDINARY.</text>
    <text x="0" y="44" fill="#94a3b8" font-size="12" class="{prefix}-font-mono">Open for hackathons, engineering roles, and open-source collaborations.</text>

    <!-- 4 Generously Spaced Social Cards (2x2 Grid) -->
    
    <!-- CARD 1: LinkedIn (Top-Left) -->
    <g transform="translate(0, 68)">
      <rect width="210" height="120" rx="12" fill="#091224" stroke="url(#{prefix}-social-border)" stroke-width="1.2"/>
      
      <!-- LinkedIn Icon Badge -->
      <rect x="14" y="14" width="34" height="34" rx="8" fill="#0a66c2" fill-opacity="0.15"/>
      <g transform="translate(21, 21) scale(0.85)">
        <path d="{icons['linkedin'][0]}" fill="#0a66c2"/>
      </g>
      
      <!-- Nudging Arrow -->
      <g transform="translate(178, 28)" class="conn-arrow-anim">
        <path d="M0 0 L6 0 M3 -3 L6 0 L3 3" stroke="#0a66c2" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>

      <text x="16" y="70" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">LinkedIn</text>
      <text x="16" y="87" fill="#38bdf8" font-size="11" class="{prefix}-font-mono">in/jatin-kaushik-bmu</text>
      <text x="16" y="103" fill="#64748b" font-size="9.5" class="{prefix}-font-mono">Professional Network</text>
    </g>

    <!-- CARD 2: GitHub (Top-Right) -->
    <g transform="translate(225, 68)">
      <rect width="210" height="120" rx="12" fill="#091224" stroke="url(#{prefix}-social-border)" stroke-width="1.2"/>
      
      <!-- GitHub Icon Badge -->
      <rect x="14" y="14" width="34" height="34" rx="8" fill="#ffffff" fill-opacity="0.12"/>
      <g transform="translate(21, 21) scale(0.85)">
        <path d="{icons['github'][0]}" fill="#f8fafc"/>
      </g>
      
      <!-- Nudging Arrow -->
      <g transform="translate(178, 28)" class="conn-arrow-anim">
        <path d="M0 0 L6 0 M3 -3 L6 0 L3 3" stroke="#f8fafc" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>

      <text x="16" y="70" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">GitHub</text>
      <text x="16" y="87" fill="#38bdf8" font-size="11" class="{prefix}-font-mono">@Jatinkaushik123</text>
      <text x="16" y="103" fill="#64748b" font-size="9.5" class="{prefix}-font-mono">Code &amp; Repositories</text>
    </g>

    <!-- CARD 3: Discord (Bottom-Left) -->
    <g transform="translate(0, 204)">
      <rect width="210" height="120" rx="12" fill="#091224" stroke="url(#{prefix}-social-border)" stroke-width="1.2"/>
      
      <!-- Discord Icon Badge -->
      <rect x="14" y="14" width="34" height="34" rx="8" fill="#5865f2" fill-opacity="0.15"/>
      <g transform="translate(21, 21) scale(0.85)">
        <path d="{icons['discord'][0]}" fill="#5865f2"/>
      </g>
      
      <!-- Nudging Arrow -->
      <g transform="translate(178, 28)" class="conn-arrow-anim">
        <path d="M0 0 L6 0 M3 -3 L6 0 L3 3" stroke="#5865f2" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>

      <text x="16" y="70" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">Discord</text>
      <text x="16" y="87" fill="#818cf8" font-size="11" class="{prefix}-font-mono">6UdG4qdnEG</text>
      <text x="16" y="103" fill="#64748b" font-size="9.5" class="{prefix}-font-mono">Developer Community</text>
    </g>

    <!-- CARD 4: Instagram (Bottom-Right) -->
    <g transform="translate(225, 204)">
      <rect width="210" height="120" rx="12" fill="#091224" stroke="url(#{prefix}-social-border)" stroke-width="1.2"/>
      
      <!-- Instagram Icon Badge -->
      <rect x="14" y="14" width="34" height="34" rx="8" fill="#e1306c" fill-opacity="0.15"/>
      <g transform="translate(21, 21) scale(0.85)">
        <path d="{icons['instagram'][0]}" fill="#ff354f"/>
      </g>
      
      <!-- Nudging Arrow -->
      <g transform="translate(178, 28)" class="conn-arrow-anim">
        <path d="M0 0 L6 0 M3 -3 L6 0 L3 3" stroke="#ff354f" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </g>

      <text x="16" y="70" fill="#f8fafc" font-size="14" class="{prefix}-font-display" font-weight="700">Instagram</text>
      <text x="16" y="87" fill="#ff758f" font-size="11" class="{prefix}-font-mono">@simply._.aadi</text>
      <text x="16" y="103" fill="#64748b" font-size="9.5" class="{prefix}-font-mono">Life &amp; Updates</text>
    </g>
  </g>
</svg>"""
    with open("assets/connect.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Built assets/connect.svg successfully!")

if __name__ == "__main__":
    build_hero_svg()
    build_about_svg()
    build_stack_svg()
    build_id_dashboard_svg()
    build_connect_svg()
    print("All 5 SVGs built successfully!")
