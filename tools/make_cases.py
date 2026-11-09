#!/usr/bin/env python3
"""Generate the case-study pages from one content source.

The site itself is static HTML — this is an authoring convenience only.
Output: projects/*.html
"""

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "projects"
OUT.mkdir(exist_ok=True)

ARROW = '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M1 5h11M8.6 1.4 12.2 5l-3.6 3.6" stroke="currentColor" stroke-width="1.2"/></svg>'

NAV = """      <nav class="nav" id="primary-nav" aria-label="Primary">
        <a href="../index.html#work">Work</a>
        <a href="../index.html#capabilities">Capabilities</a>
        <a href="../index.html#process">How I work</a>
        <a href="../index.html#about">About</a>
        <a href="../index.html#contact">Contact</a>
      </nav>"""


def head(title, desc, og="assets/img/ganymede-iso-1100.webp"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Thommy">
<meta name="theme-color" content="#08090b">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../assets/favicon-180.png">
<link rel="preload" href="../assets/fonts/Archivo-100_900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/JetBrainsMono-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/style.css">
<script>document.documentElement.classList.add("js");</script>
</head>
<body>
<a class="skip" href="#body">Skip to the content</a>

<header class="site-head" data-stuck="false" data-open="false">
  <div class="wrap head-inner">
    <a class="brand" href="../index.html" aria-label="Thommy, home">
      <img class="brand-mark" src="../assets/logo-mark.svg" alt="" width="23" height="26">
      Thommy<span class="dot">.</span>
    </a>
{NAV}
    <span class="head-status"><span class="pulse" aria-hidden="true"></span>Open to new opportunities</span>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="primary-nav">
      <span aria-hidden="true"></span>
    </button>
  </div>
</header>
"""


def foot(year="2026", root=""):
    return f"""
<footer class="site-foot">
  <div class="wrap foot-inner">
    <span class="foot-brand"><img src="{root}assets/logo-mark.svg" alt="" width="18" height="20"><span>© {year} Thommy · they/them</span></span>
    <span>Designed and built as a small static site.</span>
    <nav class="foot-links" aria-label="Footer">
      <a href="https://github.com/NovaPrime18" target="_blank" rel="noopener">GitHub</a>
      <a href="mailto:novaprime18@gmail.com">Email</a>
      <a href="#top">Top ↑</a>
    </nav>
  </div>
</footer>

<script src="../assets/js/main.js" defer></script>
</body>
</html>
"""


def img(base, alt, w, h, sizes="(max-width: 860px) 92vw, 78vw", cls="", small=None):
    small = small or base
    return f"""<img src="../assets/img/{small}.webp"
             srcset="../assets/img/{small}.webp {small.rsplit('-',1)[-1]}w, ../assets/img/{base}.webp {base.rsplit('-',1)[-1]}w"
             sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" loading="lazy">"""


def section_prose(num, title, body):
    return f"""
      <section class="case-grid" data-reveal>
        <h2><span class="n">{num}</span>{title}</h2>
        <div class="prose">
{body}
        </div>
      </section>"""


def table(num, title, caption, rows):
    body = "\n".join(
        f'            <tr><th scope="row">{k}</th><td{" class=\"num\"" if gold else ""}>{v}</td></tr>'
        for k, v, gold in rows
    )
    return f"""
      <section class="case-grid" data-reveal>
        <h2><span class="n">{num}</span>{title}</h2>
        <div>
          <table class="table">
            <caption>{caption}</caption>
            <tbody>
{body}
            </tbody>
          </table>
        </div>
      </section>"""


CASES = {}

# --------------------------------------------------------------------------
CASES["dab-dcdc"] = dict(
    title="DAB DC-DC — 10 kW design · Thommy",
    desc="A dual active bridge designed for 10 kW as part of a 500 kW off-grid EV charger thesis: 800 V in, up to 1000 V out, 100 kHz and 1700 V SiC.",
    h1="Over two kilowatts,<br>per <em class=\"serif\">liter.</em>",
    lede="A dual active bridge module designed for 10 kW as part of a thesis on a 500 kW off-grid EV charger. It takes 500–800 V in, covers 250–1000 V out and switches at 100 kHz. Revision one is a low-voltage prototype with a few lessons attached.",
    crumb=("01", "DC-DC"),
    meta=[
        ("Year", "2026"),
        ("Role", "Hardware design — internship thesis"),
        ("Board", "6-layer · 70 µm Cu · 2 mm FR4"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("dab-hero-1800", "dab-hero-1100", "The 10 kW dual active bridge board: purple solder mask, a planar transformer under an aluminium block, 1700 V SiC MOSFETs along both sides.", 1800, 773),
    sections=[
        ("01", "The brief", """
          <p>The thesis asked whether New Electric should build a 500 kW off-grid EV fast charger in-house. The proposed charger uses repeated 10 kW DAB modules rather than one 500 kW converter. This board is the prototype for one of those modules.</p>
          <p>TI’s reference design was the starting point because it came closest to the required specification. Its output stopped at 500 V; the project needed 1000 V and more current at lower output voltages. That meant new SiC devices and capacitors, more copper, a different transformer ratio, larger clearances and a proper look at cooling. LTspice and PLECS checked the design before anything was ordered.</p>
        """),
        ("02", "What a 10 kW module needs", None),
        ("03", "Key design decisions", """
          <p><strong>Six layers instead of four.</strong> The reference design uses four layers. This one uses six, with 70 µm copper, to carry the higher current and spread the heat. KiCad’s trace-width calculator put the estimated trace rise below 10 °C at 30 A, though limited room for thermal vias around the HV clearances meant this still needed a bench test.</p>
          <p><strong>1700 V on the isolated side.</strong> The 1000 V output also has to survive switching overshoot and transformer ringing. Secondary SiC MOSFETs and DC-blocking capacitors are rated at 1700 V, a 1.7× margin. The available switch has higher gate charge and slightly higher on-resistance than TI’s 900 V part, so the extra loss went into the simulations and cooling budget.</p>
          <p><strong>External contactors.</strong> Moving the contactors off-board keeps their voltage rating independent of the prototype PCB and makes the precharge hardware easier to adapt to the vehicle. XT30 connectors replace the original on-board arrangement.</p>
          <p><strong>The transformer holds things up.</strong> It is the heaviest component, so it might as well be part of the structure. It sits in the centre and is held by the cooling plate; together they support the PCB. The 2 mm FR4 keeps the outer edges from sagging.</p>
        """),
        ("04", "What went wrong", None),
        ("05", "What the tests added", """
          <p>PLECS predicted 98.6 % efficiency for 750 V to 600 V at 10 kW; LTspice also sat above 98 %. At 750 V to 1000 V, the predictions fell to about 96 % in PLECS and 94 % in LTspice. Those are simulation results, not measured converter efficiencies.</p>
          <p>The 10 kW target does not apply across the whole output range. The thesis specifies 40 A for 10 kW at 250 V, while the prototype transformer is rated at 17 A secondary and 25 A peak. Low-voltage operation therefore needs a power limit, and the 1000 V simulations favour derating too.</p>
          <p>The converter itself has not yet delivered power. The gate drivers would not reset and none of the SiC FETs switched, even with PWM and reset signals sent. Eight dead gate drivers at once seemed unlikely, making software the prime suspect at the time of writing. The planned 48 V efficiency test is still on the list.</p>
          <p>A 20 A thermal test on one of the tighter internal traces raised its temperature from an 18 °C ambient to at most 30 °C after five minutes. The shunt was the hottest feature, not the copper. Full HV testing was not attempted: the lab lacked a suitable current-limited HV supply, and revision one’s repairs had already compromised the isolation.</p>
        """),
        ("06", "Building one", """
          <p>Payton Planar made the one-off 24:20 transformer to the project’s specifications. Murata never replied, which simplified the supplier selection considerably. JLCPCB made the six-layer PCB; a wrongly entered delivery address added a month that had not featured in the project plan.</p>
          <p>All roughly 750 components were then placed by hand in three sessions, using a stencil, solder paste and an AliExpress hotplate. For a single prototype, that beat shipping the expensive parts to an assembly house and hoping every purchasing decision had been right.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — design targets; derating and bring-up status below",
    rows=[
        ("Topology", "Dual active bridge, phase-shift controlled", False),
        ("Input", "500–800 V DC", True),
        ("Output", "250–1000 V DC design range · simulated efficiency peak at 666 V", True),
        ("Power", "10 kW design target · voltage-dependent derating", True),
        ("Transformer current", "15 A primary (22 A peak) · 17 A secondary (25 A peak)", False),
        ("Switching", "100 kHz", True),
        ("Transformer dielectric strength", "10 kV primary-to-secondary · not a repaired-board rating", False),
        ("Transformer", "Payton Planar, 24:20, 35 µH leakage", False),
        ("Secondary switches", "Microchip MSC035SMA170B4, 1700 V SiC", False),
        ("Creepage / clearance", "3 mm primary · 3.5 mm secondary (IEC-60664 at 1000 V)", False),
        ("Voltage derating", "1.7× on HV secondary parts", True),
        ("PCB", "6 layers · 70 µm Cu · 2 mm FR4", False),
        ("Cooling", "Fin-stack air or aluminium liquid-cooling plate", False),
        ("Connectors", "XT30 for HV in/out — contactors off-board", False),
    ],
    callout="""
          <div class="callout">
            <b>Errata, first prototype.</b> The board collected a respectable set: swapped eFuse connections, a controlCARD footprint with TI’s pin numbering reversed, an isolated-supply current limit set too low and sense signals routed to the wrong MCU pins. The fixes involved bodge wires, a 270 Ω resistor, magnet wire and a small adapter PCB designed and ordered within a day. Those repairs enabled the supply, controlCARD and thermal checks, but did not preserve the original HV isolation. Revision one therefore stays below 50 V.
          </div>""",
    figures=[
        ("dab-macro-1800", "dab-macro-1100", "Close-up of the secondary side: 1700 V SiC MOSFETs, gate-drive isolation and the HV capacitor bank.", 1800, 1125, "", "Secondary side"),
        ("dab-cooling-1500", "dab-cooling-950", "The cooling plate and fin stack, clamped over the SiC devices and the transformer.", 1500, 1125, "", "Cooling plate"),
    ],
    links=[("https://github.com/NovaPrime18/DAB_DCDC", "Hardware files on GitHub")],
    tags=["10 kW target", "100 kHz", "1700 V SiC", "CERN-OHL-S"],
    next=("ganymede", "GaN up front. Ganymede on the back."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["ganymede"] = dict(
    title="GaNymede — 60 V, 100 A GaN motor driver · Thommy",
    desc="A VESC-compatible three-phase GaN motor controller: six EPC2361 eGaN FETs, 0.25 mΩ phase shunts and 1.4 mF of bus capacitance on a 78 × 65 mm six-layer board.",
    h1="GaN up front.<br>Ganymede <em class=\"serif\">on the back.</em>",
    lede="A VESC-compatible three-phase hub-motor driver on a 78 × 65 mm six-layer board. Six EPC2361 GaN FETs and a wrapped capacitor bank keep the power loop small; three-shunt sensing and a copper-inclusive loss model cover the less glamorous parts.",
    crumb=("02", "Motor driver"),
    meta=[
        ("Year", "2026 — R1"),
        ("Role", "Hardware design, layout, loss model"),
        ("Board", "78 × 65 mm · 6-layer")
        ,
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("ganymede-iso-1800", "ganymede-iso-1100", "GaNymede in its translucent housing, engraved silkscreen illustration of Ganymede and the eagle across the copper.", 1800, 1533),
    sections=[
        ("01", "The brief", """
          <p>GaNymede is a motor controller for a direct-drive hub motor, with a target of 50 A continuous and 100 A for one minute. Three-phase current and voltage sensing, Hall inputs, CAN and an ESP32-C3 for wireless telemetry are all on board.</p>
          <p>Using the VESC pattern—STM32F405, existing firmware and tools—keeps the control side familiar. The GaN power stage, current sensing and thermal budget are where most of the design time went.</p>
        """),
        ("02", "Specification", None),
        ("03", "Key design decisions", """
          <p><strong>The capacitor bank wraps around the bridge.</strong> It does not sit politely in a row. Wrapping the roughly 1.4 mF bank around the power stage uses the available board area and keeps the commutation loop short. Ceramic capacitors sit close to the switches; larger parts provide bulk storage.</p>
          <p><strong>Two shunts per phase.</strong> Two parallel 0.5 mΩ 2512 resistors make a 0.25 mΩ shunt, feeding an INA240A1 at a gain of 20. Sharing the current spreads the heat while keeping a useful measurement signal.</p>
          <p><strong>Dead time lives in firmware.</strong> The LMG1210 takes independent high- and low-side inputs, which fits the VESC control scheme. It also makes careful gate-signal checks essential during first power-up.</p>
          <p><strong>The copper is sized for the peak.</strong> Pours and via stitching account for the one-minute 100 A target, not just 50 A continuous. The 100 V FET rating leaves headroom over the 60 V bus, but real overshoot still needs a double-pulse test.</p>
        """),
        ("04", "What the loss model says", """
          <p>The copper, semiconductor and thermal model in <a href="https://github.com/NovaPrime18/GaNymede/blob/main/LOSSES.md" target="_blank" rel="noopener">LOSSES.md</a> currently predicts about 29 W of loss and 99.4 % efficiency at 100 A peak, or 7.3 W and 99.7 % at 50 A continuous. Those are model outputs, not claims from a finished inverter.</p>
          <p>It puts most of the loss in the phase shunts and 60 V/GND copper rather than the GaN devices. A 1.5–2 °C/W natural-convection heatsink should handle the modelled continuous load, while the one-minute peak leans mostly on thermal mass. If the bench disagrees, the bench wins.</p>
        """),
        ("05", "The back of the board", """
          <p>The back carries an engraving of Ganymede and the eagle. It does absolutely nothing for efficiency. It does make the back of the board much better.</p>
        """),
        ("06", "Where it stands", """
          <p>R1 exists as a completed schematic and six-layer layout, not a tested controller. Every current, power and thermal figure here is a target or model output. Gate checks, a double-pulse test and a thermal camera need to turn those targets into ratings.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — design targets",
    rows=[
        ("Bus voltage", "up to 60 V DC", True),
        ("Phase current", "50 A continuous · 100 A peak (1 min)", True),
        ("Peak output", "≈ 5.2 kW at 100 A peak, m = 1, modelled", False),
        ("Topology", "3-phase inverter, 6× EPC2361 100 V eGaN", False),
        ("Switching", "20 kHz nominal (10–40 kHz analysed)", False),
        ("Gate drive", "LMG1210, 5 V, 2.2 Ω", False),
        ("Current sense", "0.25 mΩ per phase · INA240A1, gain 20", False),
        ("Control", "STM32F405RGT6, 168 MHz, 8 MHz HSE", False),
        ("Wireless", "ESP32-C3-WROOM-02 — Wi-Fi / BLE", False),
        ("CAN", "2× TJA1051TK-3 (STM32 + ESP32), shared bus", False),
        ("Bus capacitance", "≈ 1.4 mF, TVS protected (SMAJ60A)", False),
        ("PCB", "78 × 65 mm · 6 layers · 1.6 mm · 1 oz Cu", True),
    ],
    callout="""
          <div class="callout">
            <b>Phase currents are amplitudes, not RMS.</b> 100 A peak is 70.7 A RMS. The 100 V FET rating leaves headroom for turn-off overshoot, but the real margin depends on power-loop inductance and should be checked with a double-pulse test during bring-up.
          </div>""",
    figures=[
        ("ganymede-board-back-1400", "ganymede-board-back-900", "Back of the GaNymede board, showing the engraved Ganymede and eagle illustration across the copper and silkscreen.", 1400, 1264, "", "Back side"),
        ("ganymede-board-front-1400", "ganymede-board-front-900", "Component side of the GaNymede board: the bus capacitor bank, eGaN devices and gate drivers around the power stage.", 1400, 1237, "", "Power stage"),
    ],
    links=[("https://github.com/NovaPrime18/GaNymede", "Hardware files on GitHub")],
    tags=["5.2 kW modelled", "100 A target", "EPC2361", "CERN-OHL-S"],
    next=("nitride-nano", "240 W in a pocket."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["nitride-nano"] = dict(
    title="nitride-nano — 240 W USB-C PD bench supply · Thommy",
    desc="A USB-C PD 3.2 buck/boost converter designed for 240 W output: 12–48 V in, 0–60 V out, 1 MHz and 94.8 % measured peak efficiency at 219 W output.",
    h1="240 W<br>in a <em class=\"serif\">pocket.</em>",
    lede="A programmable supply designed for 240 W output, powered by USB-C PD or DC input. The STM32 asks the USB-C source for a useful voltage instead of accepting whatever appears. Revision two measured 219 W output at 94.8 % peak efficiency.",
    crumb=("03", "Power supply"),
    meta=[
        ("Year", "2026 — R2"),
        ("Role", "Hardware, layout, bring-up, test"),
        ("Result", "219 W out at 94.8 % · 240.8 W max in"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("nano-front-1800", "nano-front-1100", "nitride-nano: a compact white PCB with its GaN power stage, USB-C input and XT90 output connectors.", 1800, 1046),
    sections=[
        ("01", "The brief", """
          <p>The Miniware MDP-XP was the starting point: make something similarly portable, but with a wider output range and more power. The result accepts USB-C Power Delivery or higher-voltage DC and delivers 0–60 V at up to 20 A through an XT90 connector.</p>
          <p>Switching at 1 MHz keeps the magnetics and capacitors small. EPC GaN devices help stop that decision from becoming a heating problem. Calling it a bench supply is slightly generous anyway; it fits in a pocket.</p>
        """),
        ("02", "Specification", None),
        ("03", "Tracking the input rail", """
          <p>A four-switch buck/boost loses efficiency when both bridges are switching. Rather than take whatever voltage a charger offers, the STM32 requests a PD rail to suit the output and keeps the LT8390A in buck-only or boost-only operation where possible.</p>
          <p>Fixed PDOs, PPS and AVS/EPR up to 48 V are supported. USB-C negotiation is therefore part of the power-stage efficiency, not just a socket on the side.</p>
        """),
        ("04", "Bench results", """
          <p>Revision one’s recorded test reached 164 W output at 94.1 %. Revision two used a 2.2 µH Coilcraft XAL1010 inductor and reached 219 W output at 94.8 %, with 36 V in and 52.4 V out. A separate 14 V input test reached 240.8 W input and 217.1 W output at 90.2 %. A Riden RD6024 supplied the input and an EA-EL 3160-60 sank the output.</p>
          <p>Both revisions’ full test tables are in the repository, so the two peak numbers do not have to stand in for every operating point.</p>
        """),
        ("05", "Thermal", """
          <p>On the bench, the GaN devices sat around 60 °C while the inductor core reached about 90 °C. The next thermal revision starts with the magnetics. A separate FreeCAD model, with a fan fitted and 10 W applied to the heatsink, estimated an enclosure temperature of about 38 °C.</p>
        """),
        ("06", "The rest of it", """
          <p>An STM32G474 runs the bare-metal UI on a 0.96″ OLED with three buttons, reads an INA228 for input and output power, and shows real-time efficiency. The EPC2367 GaN power stage follows the EVAL-LT8390A topology; the USB-C PD input is based on the open-source PD240W design.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 2 — measured results and design ratings",
    rows=[
        ("Input", "12–48 V — USB-C PD or XT90", True),
        ("Output", "0–60 V, 20 A · 240 W design target", True),
        ("Topology", "Non-inverting buck/boost, LT8390A", False),
        ("Switching", "1 MHz", True),
        ("Power FETs", "EPC2367 eGaN", False),
        ("Power monitor", "INA228, 16-bit, I²C", False),
        ("MCU", "STM32G474CEUx", False),
        ("Display", "SSD1306 0.96″ OLED, 3-button UI", False),
        ("PD", "Fixed PDO · PPS 5–21 V · AVS/EPR 15–48 V", False),
        ("Peak efficiency", "94.8 % at 36 V in → 52.4 V, 219 W out", True),
        ("Peak input power", "240.8 W at 14 V in, 90.2 %", True),
    ],
    callout="""
          <div class="callout">
            <b>Two different measured points.</b> The 219 W output at 94.8 % and 240.8 W input at 90.2 % came from different tests. Neither result means that 240 W output has been measured; that remains the design target.
          </div>""",
    figures=[
        ("nano-back-1500", "nano-back-950", "The back of the board: silkscreen reads POWAH!, atom logo, and the output range printed where an assembly technician will see it.", 1500, 871, "", "Back side"),
        ("nano-photo-1800", "nano-photo-1100", "The revision 2 board in its printed housing, running on an XT90 input.", 1800, 1355, "figure--wide", "Revision 2, running"),
    ],
    links=[("https://github.com/NovaPrime18/nitride-nano", "Hardware and firmware on GitHub")],
    tags=["240 W target", "1 MHz", "USB-C PD 3.2", "CERN-OHL-S"],
    next=("compressor-controller", "Mains in. Compressor out."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["compressor-controller"] = dict(
    title="CompressorController — 230 V AC VESC-compatible HVAC drive · Thommy",
    desc="A mains-powered, VESC-compatible three-phase motor driver with active PFC, isolated gate signals and dual isolated CAN, designed against IEC 61000-3-2.",
    h1="Mains in.<br>Compressor <em class=\"serif\">out.</em>",
    lede="A VESC-compatible three-phase compressor drive designed for 230 V AC mains. Active PFC is intended to shape the input current, while isolated gate signals and two isolated CAN interfaces keep the control side away from mains.",
    crumb=("04", "Mains drive"),
    meta=[
        ("Year", "2026 — Rev 1"),
        ("Role", "Hardware design, schematic hierarchy"),
        ("Scope", "Mains · boost-follower PFC · HVAC"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("compressor-front-1500", "compressor-front-950", "The compressor controller: green PCB with an intelligent power module, PFC inductor, film capacitors and a large bus capacitor bank.", 1500, 911),
    sections=[
        ("01", "The brief", """
          <p>The original problem was to run a compact three-phase compressor drive directly from 230 V AC while keeping VESC firmware and tools. That means fitting the entire grid interface on board too: EMI filter, inrush limiting, rectifier, active PFC and DC bus.</p>
          <p>A diode bridge and bulk capacitor alone would draw current in pulses. The UCC28180 CCM boost stage is intended to shape that current and gives the design a route towards IEC 61000-3-2 harmonic limits. The standard still needs measurements, of course.</p>
        """),
        ("02", "Specification", None),
        ("03", "Architecture", """
          <p>The schematic uses ten hierarchical sheets, so the mains input, PFC, motor phases, isolation and control sections can be reviewed without following wires across one enormous page.</p>
          <p>The power path runs through an EMI filter, inrush limiter and bridge rectifier to a nominal 325 V rectified bus, then through the PFC stage. The regulated PFC output feeds an Infineon IKCM10H60 intelligent power module; 325 V is therefore the rectifier-side figure, not a fixed output rating for the boost stage. The module integrates gate drivers and bootstrap, while a separate isolation barrier protects the control domain.</p>
        """),
        ("04", "Key design decisions", """
          <p><strong>Isolation gets its own sheet.</strong> Gate signals and fault lines cross a dedicated barrier, and both CAN interfaces are isolated too. Making that boundary visible in the schematic also makes it harder to lose during a review.</p>
          <p><strong>Boost-follower PFC.</strong> The controller includes boost-follower control for its efficiency benefit rather than simply regulating a fixed high-voltage output. The schematic’s own note gives the trade-off: the software might not like the regulation loop. That is a bench question, not a solved feature.</p>
          <p><strong>VESC Express handles connectivity.</strong> An ESP32 module provides Wi-Fi, Bluetooth and a CAN bridge. Commissioning and monitoring can use existing VESC tools instead of another custom application.</p>
          <p><strong>Service access is on the board.</strong> Tag-Connect SWD, status LEDs and USB-C for VESC Tool cover programming and debugging without extra bodge wires. Other boards in this portfolio have not always been so lucky.</p>
        """),
        ("05", "Compliance targets", None),
        ("06", "Compliance and safety", """
          <p>Active PFC is intended to reduce harmonic-current emissions, but it does not make the board certified. IEC 60335-2-34 for motor-compressors and EN IEC 63000 for RoHS documentation also remain integration and documentation work, not boxes ticked by a schematic.</p>
          <p>The rectified and PFC buses operate at lethal voltages, roughly 325–400 V depending on the node and operating point. Enclosure, creepage, clearance and fusing are part of the design rather than accessories, and this is not a beginner mains project.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — design specifications; first article assembled",
    rows=[
        ("Input", "230 V AC single phase", True),
        ("Rectified bus", "≈ 325 V DC nominal · before PFC", True),
        ("PFC output", "Regulated boost-follower bus · feeds the IPM", True),
        ("PFC", "TI UCC28180D — CCM boost PFC", True),
        ("Power bridge", "Infineon IKCM10H60GAXKMA1 IPM — 10 A / 600 V", False),
        ("MCU", "STM32F405RGTx running VESC firmware", False),
        ("Connectivity", "VESC Express (ESP32) — Wi-Fi, BLE, CAN bridge", False),
        ("CAN", "Dual isolated interfaces", False),
        ("USB", "USB Type-C for VESC Tool", False),
        ("Debug", "Tag-Connect SWD", False),
        ("Sensing", "Phase current U/V/W · bus and phase voltage", False),
    ],
    callout="""
          <div class="callout">
            <b>Mains voltage.</b> This board operates at lethal voltages: 230 V AC in, with high-voltage DC nodes around 325–400 V depending on the node and operating point. It is an open hardware design intended for qualified people, with enclosure, creepage and fusing treated as part of the system rather than accessories.
          </div>""",
    figures=[
        ("compressor-back-1500", "compressor-back-950", "The power side: PFC inductor, film capacitors, IPM heatspreader and the bus capacitor bank.", 1500, 944, "", "Power side"),
        ("compressor-photo-1800", "compressor-photo-1100", "The first assembled compressor controller on a workbench, with the power stage, PFC magnetics and capacitor bank visible.", 1800, 1131, "", "First article"),
    ],
    links=[("https://github.com/NovaPrime18/CompressorController", "Hardware files on GitHub")],
    tags=["230 V AC", "Active PFC", "VESC", "IEC 61000-3-2"],
    next=("twin-gan", "No CAN cable between the ESCs."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["twin-gan"] = dict(
    title="Twin-GaN — dual 3-phase GaN motor controller · Thommy",
    desc="Two complete VESC-compatible three-phase inverters on one 99 × 99 mm board, with both MCUs and an ESP32 sharing one internal CAN bus.",
    h1="No CAN cable<br>between the <em class=\"serif\">ESCs.</em>",
    lede="Two independent VESC-compatible GaN motor channels on a 99 × 99 mm board. Each keeps its own STM32, USB-C port and three-shunt sensing; an ESP32 joins both on an internal CAN bus for coordinated traction control.",
    crumb=("05", "Side project"),
    meta=[
        ("Year", "2026 — R1"),
        ("Role", "Hardware design"),
        ("Board", "99 × 99 mm · 4-layer"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("twin-gan-1400", "twin-gan-900", "Twin-GaN: a 99 mm square green PCB with two complete three-phase GaN inverters, six ePower stages and two STM32 controllers.", 1400, 1553),
    sections=[
        ("01", "The brief", """
          <p>A two-wheel-drive light EV normally gets two separate ESCs and the wiring between them. Twin-GaN puts both controllers on one 99 × 99 mm PCB to reduce board count, size and cost. The trade-off is a lower peak-power rating in exchange for the integration.</p>
          <p>Each channel keeps an independent STM32F405, USB-C port and three-shunt sensing. An ESP32-C3 provides a third CAN node alongside the two motor controllers.</p>
        """),
        ("02", "Specification", None),
        ("03", "Why one board", """
          <p><strong>One CAN bus, three nodes.</strong> Both STM32s and the ESP32 sit on the same terminated internal CAN bus. Torque and control information can move between channels without external wiring, giving future traction-control firmware somewhere to start.</p>
          <p><strong>VESC Tool still sees two controllers.</strong> Each channel has its own MCU and six-PWM stage, so setup stays familiar and no custom combined-control interface is needed.</p>
          <p><strong>Three shunts per channel.</strong> Each phase uses an INA240A1D across a 2 mΩ shunt. REF1 and REF2 are connected for bidirectional measurement, so the controller can distinguish drive current from regeneration.</p>
          <p><strong>The usual connections are already there.</strong> Each controller gets USB-C with CC pulldowns and VBUS protection, Tag-Connect SWD and the standard VESC accessory header. No adapter-cable hunt is required for basic commissioning.</p>
        """),
        ("04", "Where it stands", """
          <p>R1 is at the design stage. The 60 V input, 20 A total battery current, 20 A continuous and 40 A absolute-max phase current per channel, and roughly 1.2 kW total are targets awaiting bench tests. Until then, they describe what the board is intended to survive, not what it has already survived.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — design targets",
    rows=[
        ("Input", "up to 60 V DC · XT60", True),
        ("Battery current", "20 A total · both channels", True),
        ("Phase current", "20 A continuous · 40 A absolute max, per channel", True),
        ("Max input power", "≈ 1.2 kW, battery-limited", False),
        ("Topology", "2 × independent 3-phase inverter", False),
        ("Power stage", "6 × EPC23102 ePower Stage — 100 V, 5.2 mΩ", False),
        ("PWM", "up to 35 kHz", False),
        ("Control", "2 × STM32F405RGT6 + ESP32-C3-WROOM-02", False),
        ("Current sense", "6 × INA240A1D across 2 mΩ shunts", False),
        ("CAN", "3 × TJA1051T/3 on one terminated internal bus", False),
        ("Board", "99 × 99 mm · 4 layers · 1.6 mm", True),
    ],
    callout="""
          <div class="callout">
            <b>Design targets, not measurements.</b> The current and power figures are targets for revision 1, not measurements. Bench verification is still required before treating them as ratings.
          </div>""",
    figures=[
        ("twin-gan-900", "twin-gan-900", "Detail: two EPC23102 ePower stages per channel, with the 2 mΩ shunts and INA240 sensing in the phase legs.", 1086, 1205, "figure--wide", "Power stage detail"),
    ],
    links=[("https://github.com/NovaPrime18/Twin-GaN", "Hardware files on GitHub")],
    tags=["1.2 kW target", "2 × 3-phase", "EPC23102", "CERN-OHL-S"],
    next=("schroombort", "The calculator was unnecessary."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["schroombort"] = dict(
    title="Schroombort — 36-key soundboard, macro-pad and calculator · Thommy",
    desc="A battery-powered, over-engineered mechanical soundboard: 36 Cherry MX switches, a VFD, stereo speakers and three modes of operation.",
    h1="The calculator<br>was <em class=\"serif\">unnecessary.</em>",
    lede="A battery-powered 36-key soundboard with a VFD, stereo speakers and a macro-pad mode. It was the first board I finished, and the project where electronics, firmware and enclosure design first had to cooperate.",
    crumb=("06", "Where I started"),
    meta=[
        ("Year", "2021"),
        ("Role", "Hardware, enclosure and firmware"),
        ("Modes", "Soundboard · macro-pad · calculator"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("schroombort-1500", "schroombort-950", "Schroombort: a black battery-powered board with 36 mechanical switches, a vacuum fluorescent display and silkscreen artwork.", 1500, 1670),
    sections=[
        ("01", "What it is", """
          <p>At its simplest, press a key and Schroombort plays a sound from the SD card. Underneath are 36 mechanical switches, a VFD, stereo speakers, USB-C charging and a battery power-path manager that can run from USB, battery or both.</p>
          <p>Connected over USB-C, it becomes a macro-pad with assignable keys. The third mode is a basic calculator. The display and keypad were already there; restraint was not.</p>
        """),
        ("02", "Specification", None),
        ("03", "The first finished board", """
          <p>This was the first project where power management, a keyboard matrix, display driving, audio, an enclosure and firmware all had to work at once. It also exposed the difference between readable on a monitor and readable on an actual PCB.</p>
          <p>It was over-engineered for a soundboard. Finishing one complete object still taught me more than another row of breadboard experiments would have.</p>
        """),
        ("04", "The trailer", """
          <p>There is a short cinematic trailer on <a href="https://www.youtube.com/watch?v=MM4cooladaY" target="_blank" rel="noopener">YouTube</a>. Yes, the soundboard got a trailer.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — 2021",
    rows=[
        ("Inputs", "36 mechanical (Cherry MX-style) switches", True),
        ("Display", "Vacuum fluorescent display", True),
        ("Audio", "Stereo speakers", False),
        ("MCU", "ATxmega256A3U", False),
        ("Charging", "Any 5 V charger, up to 2 A", False),
        ("Power path", "Dynamic — USB only, battery only, or both", False),
        ("Modes", "Soundboard · macro-pad · calculator", False),
        ("Connectivity", "USB-C", False),
    ],
    callout="""
          <div class="callout">
            <b>Why it is here.</b> This was my first finished board. It is less ambitious electrically than the later projects, but it is where I learned to take a design all the way to a working object.
          </div>""",
    figures=[
        ("schroombort-photo-1500", "schroombort-photo-950", "The finished board, battery-powered, display lit — silkscreen reads NOVA PRIME, Schroomboysz, and a Dutch joke about money.", 1500, 1191, "figure--wide", "Finished, 2021"),
    ],
    links=[("https://github.com/NovaPrime18/schroombort", "Hardware on GitHub")],
    tags=["36 keys", "VFD", "ATxmega", "CERN-OHL-S"],
    next=("dab-dcdc", "Over two kilowatts, per liter."),
    year="2021",
)


def build_case(slug, c):
    sections_html = []
    for num, title, body in c["sections"]:
        if body is None:
            if title == c.get("table_title"):
                sections_html.append(
                    table(num, title, c["table_caption"], [(k, v, g) for k, v, g in c["rows"]])
                )
            elif title == "What went wrong":
                sections_html.append(
                    f"""
      <section class="case-grid" data-reveal>
        <h2><span class="n">{num}</span>{title}</h2>
        <div class="prose">{c["callout"]}</div>
      </section>"""
                )
            elif title == "Numbers":
                sections_html.append(
                    table(num, title, "Design summary", [
                        ("Module power", "≈ 10 kW", True),
                        ("Switching frequency", "100 kHz", True),
                        ("Isolation", "10 kV", True),
                        ("Creepage at 1000 V", "3.5 mm", True),
                        ("HV derating", "1.7×", False),
                        ("Copper", "6 layers · 70 µm", False),
                    ])
                )
            elif title == "Compliance targets":
                sections_html.append(
                    table(num, title, "Standards in scope", [
                        ("IEC 61000-3-2", "Harmonic current emissions — active PFC; measurement still required", True),
                        ("IEC 60335-2-34", "Particular requirements for motor-compressors", False),
                        ("EN IEC 63000", "RoHS technical documentation", False),
                    ])
                )
            else:
                sections_html.append(
                    table(num, title, c["table_caption"], [(k, v, g) for k, v, g in c["rows"]])
                )
        else:
            sections_html.append(section_prose(num, title, body))

    figs = "\n".join(
        f"""            <figure class="figure {cls}">
              <img src="../assets/img/{small}.webp"
                   srcset="../assets/img/{small}.webp {small.rsplit('-',1)[-1]}w, ../assets/img/{big}.webp {big.rsplit('-',1)[-1]}w"
                   sizes="(max-width: 860px) 92vw, 60vw" width="{w}" height="{h}" alt="{alt}" loading="lazy">
              <figcaption>{cap}</figcaption>
            </figure>"""
        for big, small, alt, w, h, cls, cap in c["figures"]
    )

    nxt_slug, nxt_title = c["next"]
    nxt = CASES[nxt_slug]

    tags = "".join(f'<span class="tag">{t}</span>' for t in c["tags"])
    links = "".join(
        f'<a class="arrow" href="{url}" target="_blank" rel="noopener">{label} {ARROW}</a>'
        for url, label in c["links"]
    )
    meta_html = "".join(
        f"        <div><dt>{k}</dt><dd>{v}</dd></div>\n" for k, v in c["meta"]
    )

    hero_base, hero_small, hero_alt, hw, hh = c["hero"]

    html = (
        head(c["title"], c["desc"])
        + f"""
<main id="top" class="case-hero">
  <div class="wrap">
    <p class="crumb"><a href="../index.html#work">Work</a> <span aria-hidden="true">/</span> <i>{c["crumb"][0]}</i> <span>{c["crumb"][1]}</span></p>
    <h1>{c["h1"]}</h1>
    <p class="lede">{c["lede"]}</p>
    <dl class="case-meta">
{meta_html}    </dl>
  </div>
  <div class="wrap case-hero-media">
    {img(hero_base, hero_alt, hw, hh, "(max-width: 860px) 92vw, 84vw", small=hero_small)}
  </div>

  <div class="wrap case-body" id="body">
{''.join(sections_html)}
    <div class="figures">
{figs}
    </div>

    <div class="case-foot">
      <div class="tags">{tags}</div>
      <div>{links}</div>
    </div>
  </div>

  <div class="wrap">
    <a class="next-case" href="{nxt_slug}.html">
      <span class="k">Next case</span>
      <span class="t"><span>{nxt_title}</span><span aria-hidden="true">→</span></span>
    </a>
  </div>
</main>
"""
        + foot(c.get("year", "2026"), "../")
    )
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    (OUT / f"{slug}.html").write_text(html)
    print("wrote", f"projects/{slug}.html")


for slug, c in CASES.items():
    build_case(slug, c)
