"""Generate the NEZU GitHub profile SVG assets (hero, cards, buttons, divider)."""
import io, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

ORANGE = "#D9542B"; ORANGE_D = "#C2461F"; LIME = "#C9DF38"
INK = "#0F1713"; INK2 = "#111A16"; INK3 = "#17221C"; EDGE = "#243029"
PAPER = "#F3F4EE"; MUTED = "#A9B1A8"; MUTED2 = "#7E877F"
FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, 'Courier New', monospace"

N_MARK = '''<rect x="0" y="0" width="117" height="34" rx="10"/>
      <rect x="0" y="0" width="34" height="152" rx="10"/>
      <path d="M 0,0 L 120,0 L 320,230 L 200,230 Z"/>
      <path d="M 200,230 L 320,230 L 320,196 Z"/>
      <rect x="286" y="78" width="34" height="152" rx="10"/>
      <rect x="0" y="196" width="117" height="34" rx="10"/>
      <rect x="203" y="0" width="117" height="34" rx="10"/>'''

def write(name, svg):
    io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(svg.strip() + "\n")
    print("ok", name, len(svg))

# ---------------------------------------------------------------- hero
def hero():
    words = ["hogares", "empresas", "edificios", "industria"]
    n = len(words); step = 2.6; total = step * n
    word_texts = ""
    for i, w in enumerate(words):
        begin = i * step
        # each word: fade in, hold, fade out within its slot
        kt = "0;{:.3f};{:.3f};{:.3f};1".format(0.08/ (1), 0.12, 0.88 * 0 + (step-0.3)/step, 1)
        word_texts += f'''
      <text x="0" y="0" fill="{LIME}" font-size="44" font-weight="700" opacity="0">{w}
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{begin/total:.4f};{(begin+0.35)/total:.4f};{(begin+step-0.35)/total:.4f};{(begin+step)/total:.4f};1" dur="{total}s" repeatCount="indefinite"/>
      </text>'''
    # network nodes (right side): id, x, y, r
    nodes = [("hub", 1085, 205, 22), ("a", 985, 110, 9), ("b", 1190, 95, 9), ("c", 1215, 235, 9),
             ("d", 1160, 330, 9), ("e", 1000, 320, 9), ("f", 955, 215, 9), ("g", 1060, 55, 7), ("h", 1110, 380, 7)]
    links = [("hub","a"),("hub","b"),("hub","c"),("hub","d"),("hub","e"),("hub","f"),("a","g"),("d","h"),("a","b"),("e","f"),("c","d")]
    pos = {k:(x,y) for k,x,y,r in nodes}
    link_svg = ""
    for i,(u,v) in enumerate(links):
        (x1,y1),(x2,y2) = pos[u],pos[v]
        link_svg += f'''
      <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{EDGE}" stroke-width="2"/>
      <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 120" stroke-linecap="round" opacity="0.9">
        <animate attributeName="stroke-dashoffset" from="126" to="0" dur="{2.4 + (i%4)*0.5:.1f}s" begin="{(i*0.37)%2.2:.2f}s" repeatCount="indefinite"/>
      </line>'''
    node_svg = ""
    for k,x,y,r in nodes:
        if k == "hub":
            node_svg += f'''
      <circle cx="{x}" cy="{y}" r="{r+26}" fill="{ORANGE}" opacity="0.10">
        <animate attributeName="r" values="{r+16};{r+40};{r+16}" dur="3.2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.16;0.02;0.16" dur="3.2s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{x}" cy="{y}" r="{r}" fill="{INK2}" stroke="{ORANGE}" stroke-width="3"/>
      <g transform="translate({x-11},{y-8}) scale(0.07)" fill="{ORANGE}">{N_MARK}</g>'''
        else:
            node_svg += f'''
      <circle cx="{x}" cy="{y}" r="{r}" fill="{INK2}" stroke="{MUTED2}" stroke-width="2">
        <animate attributeName="stroke" values="{MUTED2};{LIME};{MUTED2}" dur="4s" begin="{(x*7+y*3)%4000/1000:.2f}s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{x}" cy="{y}" r="3" fill="{LIME}" opacity="0.9">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2.6s" begin="{(x*3+y*7)%2600/1000:.2f}s" repeatCount="indefinite"/>
      </circle>'''
    labels = [("Iluminación",985,88),("Clima",1190,73),("Cámaras",1215,263),("Energía",1160,358),("Accesos",1000,348),("Cortinas",955,243)]
    label_svg = "".join(f'<text x="{x}" y="{y}" text-anchor="middle" fill="{MUTED2}" font-size="11" font-weight="600" letter-spacing="0.8">{t.upper()}</text>' for t,x,y in labels)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-label="NEZU. Tecnología integrada para hogares, empresas, edificios e industria. Innovación para vivir mejor.">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{EDGE}" stroke-width="1" opacity="0.7"/>
    </pattern>
    <radialGradient id="glow" cx="20%" cy="45%" r="55%">
      <stop offset="0" stop-color="{ORANGE}" stop-opacity="0.26"/>
      <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="85%" cy="50%" r="40%">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ORANGE}"/><stop offset="0.7" stop-color="{ORANGE}"/><stop offset="1" stop-color="{LIME}"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{LIME}" stop-opacity="0"/><stop offset="0.5" stop-color="{LIME}" stop-opacity="0.35"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="clip"><rect width="1280" height="420" rx="28"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="1280" height="420" fill="{INK}"/>
    <rect width="1280" height="420" fill="url(#grid)"/>
    <rect width="1280" height="420" fill="url(#glow)"/>
    <rect width="1280" height="420" fill="url(#glow2)"/>
    <rect x="-300" y="0" width="300" height="420" fill="url(#scan)" opacity="0.5">
      <animate attributeName="x" from="-300" to="1280" dur="9s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="0.5" y="0.5" width="1279" height="419" rx="28" fill="none" stroke="{EDGE}"/>

  <!-- mark -->
  <g transform="translate(84,120) scale(0.5)" fill="{ORANGE}">{N_MARK}</g>

  <!-- copy -->
  <rect x="290" y="96" width="200" height="4" rx="2" fill="url(#bar)"/>
  <g font-family="{FONT}">
    <text x="288" y="170" fill="{PAPER}" font-size="72" font-weight="800" letter-spacing="12">NEZU</text>
    <g transform="translate(290,232)" font-family="{FONT}">
      <text x="0" y="0" fill="{PAPER}" font-size="44" font-weight="300">Tecnología para</text>
      <g transform="translate(352,0)">{word_texts}
      </g>
    </g>
    <text x="292" y="276" fill="{MUTED}" font-size="19">Automatización, energía, seguridad y conectividad, desde Cuenca, Ecuador.</text>
    <g font-size="13" font-weight="600" letter-spacing="1.4" fill="{MUTED2}">
      <text x="292" y="336">LOCAL FIRST</text><circle cx="412" cy="331" r="3" fill="{LIME}"/>
      <text x="430" y="336">PRIVACIDAD POR DISEÑO</text><circle cx="651" cy="331" r="3" fill="{LIME}"/>
      <text x="669" y="336">SOFTWARE PROPIO</text>
    </g>
    <text x="292" y="378" fill="{MUTED2}" font-size="13" font-family="{MONO}">$ nezu --status  <tspan fill="{LIME}">● operativo</tspan>  ·  innovación para vivir mejor</text>
  </g>

  <!-- network -->
  <g>{link_svg}{node_svg}
    <g font-family="{FONT}">{label_svg}</g>
  </g>
</svg>'''
    write("hero.svg", svg)

# ---------------------------------------------------------------- cards (service lines)
ICONS = {
  "living": f'''<path d="M12 40 L40 16 L68 40" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M20 36 V62 H60 V36" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-linejoin="round"/>
      <circle cx="40" cy="48" r="6" fill="{LIME}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/></circle>''',
  "elevate": f'''<rect x="14" y="20" width="24" height="44" rx="3" fill="none" stroke="{ORANGE}" stroke-width="4"/>
      <rect x="42" y="32" width="24" height="32" rx="3" fill="none" stroke="{ORANGE}" stroke-width="4"/>
      <g fill="{LIME}"><rect x="20" y="28" width="5" height="5"><animate attributeName="opacity" values="1;0.2;1" dur="3s" repeatCount="indefinite"/></rect><rect x="29" y="28" width="5" height="5"/><rect x="20" y="38" width="5" height="5"/><rect x="29" y="38" width="5" height="5"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.2s" repeatCount="indefinite"/></rect><rect x="48" y="40" width="5" height="5"/><rect x="57" y="40" width="5" height="5"><animate attributeName="opacity" values="1;0.3;1" dur="2.7s" repeatCount="indefinite"/></rect></g>''',
  "core": f'''<rect x="14" y="16" width="52" height="14" rx="3" fill="none" stroke="{ORANGE}" stroke-width="4"/>
      <rect x="14" y="34" width="52" height="14" rx="3" fill="none" stroke="{ORANGE}" stroke-width="4"/>
      <rect x="14" y="52" width="52" height="14" rx="3" fill="none" stroke="{ORANGE}" stroke-width="4"/>
      <g fill="{LIME}"><circle cx="22" cy="23" r="2.5"><animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/></circle><circle cx="22" cy="41" r="2.5"><animate attributeName="opacity" values="0.2;1;0.2" dur="2.1s" repeatCount="indefinite"/></circle><circle cx="22" cy="59" r="2.5"><animate attributeName="opacity" values="1;0.2;1" dur="1.9s" repeatCount="indefinite"/></circle></g>''',
}

def card(name, kicker, title, lines, icon, w=400, h=230):
    body = "".join(f'<text x="28" y="{150 + i*22}" fill="{MUTED}" font-size="14">{l}</text>' for i,l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}. {' '.join(lines)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK3}"/><stop offset="1" stop-color="{INK}"/></linearGradient>
    <linearGradient id="top" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{LIME}"/></linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="20" fill="url(#bg)" stroke="{EDGE}"/>
  <rect x="28" y="0" width="80" height="3" rx="1.5" fill="url(#top)"/>
  <g transform="translate(28,30)">{icon}</g>
  <g font-family="{FONT}">
    <text x="120" y="52" fill="{MUTED2}" font-size="11" font-weight="700" letter-spacing="2">{kicker}</text>
    <text x="120" y="84" fill="{PAPER}" font-size="26" font-weight="700">{title}</text>
    {body}
  </g>
</svg>'''
    write(name, svg)

card("card-living.svg", "NEZU LIVING", "Hogares", ["Iluminación, clima, cortinas, seguridad y energía", "en viviendas con instalación profesional.", "Todo sigue funcionando sin internet."], ICONS["living"])
card("card-elevate.svg", "NEZU ELEVATE", "Empresas y edificios", ["Monitoreo, control de acceso, seguridad y", "automatización para oficinas, comercios", "y edificios en operación."], ICONS["elevate"])
card("card-core.svg", "NEZU CORE", "Infraestructura", ["Redes, servidores, sistemas e integraciones", "que sostienen la operación técnica,", "con acceso remoto seguro."], ICONS["core"])

# ---------------------------------------------------------------- product cards
def product(name, kicker, title, tagline, chips, art, w=600, h=300):
    chip_svg = ""; x = 28
    for c in chips:
        cw = 14 + len(c) * 7.2
        chip_svg += f'<rect x="{x}" y="238" width="{cw:.0f}" height="26" rx="13" fill="{INK2}" stroke="{EDGE}"/><text x="{x+cw/2:.0f}" y="255" text-anchor="middle" fill="{MUTED}" font-size="11" font-weight="600" font-family="{MONO}">{c}</text>'
        x += cw + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}. {tagline}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{INK3}"/><stop offset="1" stop-color="{INK}"/></linearGradient>
    <radialGradient id="g" cx="82%" cy="40%" r="50%"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0.22"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
    <clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" fill="url(#g)"/></g>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="{EDGE}"/>
  <g font-family="{FONT}">
    <text x="28" y="48" fill="{ORANGE}" font-size="11" font-weight="700" letter-spacing="2.2">{kicker}</text>
    <text x="28" y="92" fill="{PAPER}" font-size="34" font-weight="800">{title}</text>
    <text x="28" y="124" fill="{MUTED}" font-size="15">{tagline[0]}</text>
    <text x="28" y="146" fill="{MUTED}" font-size="15">{tagline[1]}</text>
    <text x="28" y="168" fill="{MUTED}" font-size="15">{tagline[2]}</text>
    {chip_svg}
  </g>
  <g transform="translate(400,40)">{art}</g>
</svg>'''
    write(name, svg)

ATRIA_ART = f'''
    <!-- house with pulsing nodes -->
    <path d="M20 90 L90 30 L160 90" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M36 84 V170 H144 V84" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-linejoin="round"/>
    <rect x="76" y="126" width="28" height="44" rx="3" fill="none" stroke="{ORANGE_D}" stroke-width="4"/>
    <g stroke="{EDGE}" stroke-width="2"><line x1="90" y1="110" x2="52" y2="104"/><line x1="90" y1="110" x2="128" y2="104"/><line x1="90" y1="110" x2="56" y2="150"/><line x1="90" y1="110" x2="124" y2="150"/></g>
    <g stroke="{LIME}" stroke-width="2" stroke-dasharray="4 60" stroke-linecap="round"><line x1="90" y1="110" x2="52" y2="104"><animate attributeName="stroke-dashoffset" from="64" to="0" dur="2s" repeatCount="indefinite"/></line><line x1="90" y1="110" x2="128" y2="104"><animate attributeName="stroke-dashoffset" from="64" to="0" dur="2.6s" repeatCount="indefinite"/></line><line x1="90" y1="110" x2="56" y2="150"><animate attributeName="stroke-dashoffset" from="64" to="0" dur="2.3s" repeatCount="indefinite"/></line><line x1="90" y1="110" x2="124" y2="150"><animate attributeName="stroke-dashoffset" from="64" to="0" dur="1.9s" repeatCount="indefinite"/></line></g>
    <circle cx="90" cy="110" r="9" fill="{INK2}" stroke="{ORANGE}" stroke-width="3"/>
    <g fill="{LIME}"><circle cx="52" cy="104" r="4"><animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/></circle><circle cx="128" cy="104" r="4"><animate attributeName="opacity" values="1;0.3;1" dur="2.6s" repeatCount="indefinite"/></circle><circle cx="56" cy="150" r="4"><animate attributeName="opacity" values="0.3;1;0.3" dur="2.3s" repeatCount="indefinite"/></circle><circle cx="124" cy="150" r="4"><animate attributeName="opacity" values="1;0.3;1" dur="1.9s" repeatCount="indefinite"/></circle></g>
    <!-- offline badge -->
    <rect x="18" y="190" width="146" height="26" rx="13" fill="{INK2}" stroke="{EDGE}"/><circle cx="34" cy="203" r="4" fill="{LIME}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="46" y="207" fill="{MUTED}" font-size="11" font-weight="700" letter-spacing="1" font-family="{FONT}">FUNCIONA SIN INTERNET</text>'''

ARCA_ART = f'''
    <!-- vault -->
    <rect x="30" y="34" width="120" height="136" rx="14" fill="none" stroke="{ORANGE}" stroke-width="5"/>
    <rect x="46" y="50" width="88" height="104" rx="8" fill="none" stroke="{ORANGE_D}" stroke-width="3" opacity="0.8"/>
    <circle cx="90" cy="102" r="26" fill="none" stroke="{ORANGE}" stroke-width="5"/>
    <g stroke="{LIME}" stroke-width="4" stroke-linecap="round">
      <line x1="90" y1="76" x2="90" y2="86"/><line x1="90" y1="118" x2="90" y2="128"/><line x1="64" y1="102" x2="74" y2="102"/><line x1="106" y1="102" x2="116" y2="102"/>
      <animateTransform attributeName="transform" type="rotate" from="0 90 102" to="360 90 102" dur="14s" repeatCount="indefinite"/>
    </g>
    <circle cx="90" cy="102" r="7" fill="{LIME}"><animate attributeName="opacity" values="0.5;1;0.5" dur="2.4s" repeatCount="indefinite"/></circle>
    <rect x="18" y="190" width="146" height="26" rx="13" fill="{INK2}" stroke="{EDGE}"/><circle cx="34" cy="203" r="4" fill="{LIME}"/>
    <text x="46" y="207" fill="{MUTED}" font-size="11" font-weight="700" letter-spacing="1" font-family="{FONT}">AES-256-GCM · LOCAL</text>'''

product("product-atria.svg", "PLATAFORMA · AUTOMATIZACIÓN RESIDENCIAL", "NEZU Atria",
        ["La casa sigue respondiendo aunque se caiga internet.", "Consola propia en teléfono, tablet y kiosko, asistente por", "voz con autorización explícita y acceso remoto opcional."],
        ["TypeScript", "Fastify", "React", "SQLite", "Docker"], ATRIA_ART)
product("product-arca.svg", "PRODUCTO · GESTIÓN DE CREDENCIALES", "NEZU Arca",
        ["Bóveda local cifrada para credenciales y segundos factores", "en Windows. Los datos nunca salen del equipo.", "Disponible en Microsoft Store."],
        ["Python", "PyQt5", "AES-256-GCM", "Scrypt", "MSIX"], ARCA_ART)

# ---------------------------------------------------------------- buttons
def button(name, label, primary):
    w = 36 + int(len(label) * 8.6)
    fill = ORANGE if primary else INK3; stroke = ORANGE if primary else EDGE; color = PAPER
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44" role="img" aria-label="{label}">
  <rect x="0.5" y="0.5" width="{w-1}" height="43" rx="12" fill="{fill}" stroke="{stroke}"/>
  <text x="{w/2:.0f}" y="27" text-anchor="middle" fill="{color}" font-size="14" font-weight="700" font-family="{FONT}" letter-spacing="0.3">{label}</text>
</svg>'''
    write(name, svg)

button("btn-contacto.svg", "Hablemos de tu proyecto  →", True)
button("btn-servicios.svg", "Ver servicios", False)
button("btn-web.svg", "nezuecuador.com", False)
button("btn-atria.svg", "Conocer Atria", False)
button("btn-arca.svg", "Arca en Microsoft Store", False)

# ---------------------------------------------------------------- divider
write("divider.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="8" viewBox="0 0 1280 8">
  <defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0"/><stop offset="0.5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{LIME}" stop-opacity="0"/></linearGradient></defs>
  <rect x="0" y="3" width="1280" height="2" fill="{EDGE}"/>
  <rect x="-400" y="3" width="400" height="2" fill="url(#d)"><animate attributeName="x" from="-400" to="1280" dur="5s" repeatCount="indefinite"/></rect>
</svg>''')

# ---------------------------------------------------------------- principles strip
def principle(name, title, text, glyph):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="150" viewBox="0 0 300 150" role="img" aria-label="{title}. {text[0]} {text[1]}">
  <rect x="0.5" y="0.5" width="299" height="149" rx="18" fill="{INK3}" stroke="{EDGE}"/>
  <g transform="translate(24,26)">{glyph}</g>
  <g font-family="{FONT}">
    <text x="24" y="88" fill="{PAPER}" font-size="17" font-weight="700">{title}</text>
    <text x="24" y="110" fill="{MUTED}" font-size="12.5">{text[0]}</text>
    <text x="24" y="128" fill="{MUTED}" font-size="12.5">{text[1]}</text>
  </g>
</svg>'''
    write(name, svg)

G_LOCAL = f'<circle cx="16" cy="16" r="13" fill="none" stroke="{ORANGE}" stroke-width="3"/><circle cx="16" cy="16" r="5" fill="{LIME}"><animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite"/></circle>'
G_PRIV = f'<rect x="5" y="13" width="22" height="17" rx="4" fill="none" stroke="{ORANGE}" stroke-width="3"/><path d="M10 13 V9 a6 6 0 0 1 12 0 V13" fill="none" stroke="{ORANGE}" stroke-width="3"/><circle cx="16" cy="22" r="2.5" fill="{LIME}"/>'
G_SPEC = f'<rect x="6" y="3" width="20" height="26" rx="3" fill="none" stroke="{ORANGE}" stroke-width="3"/><g stroke="{LIME}" stroke-width="2.5" stroke-linecap="round"><line x1="11" y1="11" x2="21" y2="11"/><line x1="11" y1="17" x2="21" y2="17"/><line x1="11" y1="23" x2="17" y2="23"/></g>'
G_AI = f'<rect x="4" y="8" width="24" height="18" rx="5" fill="none" stroke="{ORANGE}" stroke-width="3"/><circle cx="12" cy="17" r="2.5" fill="{LIME}"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle><circle cx="20" cy="17" r="2.5" fill="{LIME}"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite"/></circle><line x1="16" y1="3" x2="16" y2="8" stroke="{ORANGE}" stroke-width="3"/>'

principle("p-local.svg", "Local primero", ["El control físico y los datos viven en el sitio.", "La nube es opcional, nunca un requisito."], G_LOCAL)
principle("p-privacidad.svg", "Privacidad por diseño", ["Mínimo privilegio, cifrado donde corresponde", "y límites de confianza explícitos."], G_PRIV)
principle("p-specs.svg", "Guiados por specs", ["Cada cambio nace de una especificación con", "criterios de aceptación y evidencia de pruebas."], G_SPEC)
principle("p-ia.svg", "Humanos + agentes de IA", ["Mismas reglas, validaciones y trazabilidad", "para todo el que toca el código."], G_AI)

hero()
