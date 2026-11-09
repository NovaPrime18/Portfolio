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
    title="DAB DC-DC — 10 kW module · Thommy",
    desc="A 10 kW dual active bridge module for a 500 kW off-grid EV charger: 800 V in, 1000 V out, 100 kHz, 1700 V SiC and creepage rules that shaped the layout.",
    h1="Ten kilowatts,<br>on the <em class=\"serif\">bench.</em>",
    lede="A 10 kW dual active bridge module developed as part of a thesis on a 500 kW off-grid EV charger: 800 V in, up to 1000 V out at 100 kHz, with the isolation and cooling requirements considered from the start.",
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
          <p>This module was developed during an internship thesis on whether a 500 kW off-grid EV DC fast charger could be built in-house. The system would be made from modules sharing a DC bus, so the thesis needed a repeatable 10 kW building block. This board is based on a Texas Instruments DAB reference design, adapted to 1000V maximum output instead of just 500V.</p>
          <p>It was designed for 500–800 V on the primary and 250–1000 V on the secondary, with cost and manufacturability part of the brief from the beginning. The thesis contains the design rationale, LTspice and PLECS simulations and test results; the repository contains the hardware.</p>
        """),
        ("02", "What a 10 kW module needs", None),
        ("03", "Key design decisions", """
          <p><strong>Six layers instead of four.</strong> The extra copper helps carry the 22 A primary and 25 A secondary peaks, spreads heat, and leaves room for via stitching around the high-current path. KiCad's trace-width calculator was used to keep the estimated trace rise within 10 °C above ambient at 30 A.</p>
          <p><strong>1700 V on the isolated side.</strong> The 1000 V output also has to accommodate switching overshoot and transformer ringing. The secondary SiC MOSFETs and DC-blocking capacitors are rated at 1700 V, giving 1.7× derating. Two 2280-package capacitors are stacked to reach the required capacitance within the available footprint.</p>
          <p><strong>External contactors.</strong> High-voltage switching is handled by external contactors through XT30 connectors. That keeps the contactor voltage rating independent of the prototype board and makes it easier to change the system architecture later.</p>
          <p><strong>The transformer is part of the structure.</strong> It sits in the centre of the board and also supports the PCB and cooling plate. Using the heaviest component as part of the mechanical structure saves a separate frame.</p>
        """),
        ("04", "What went wrong", None),
        ("05", "Numbers", None),
        ("06", "The rest of the board", """
          <p>All components sit on the top side, for cheaper single-sided assembly and a simpler stencil. Isolation is galvanic through a Payton Planar transformer — 24:20 turns, 35 µH of leakage inductance, 10 kV dielectric strength — and the 5 V and gate-drive rails are derived on-board on both sides of the barrier. Control is a TI controlCARD over CAN, phase-shift regulating the bridge.</p>
          <p>The prototype was manufactured by JLCPCB on a six-layer, double-thick-copper process. It is a proof of concept rather than a finished product, but it provides a concrete basis for the thesis evaluation.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Prototype module, revision 1",
    rows=[
        ("Topology", "Dual active bridge, phase-shift controlled", False),
        ("Input", "500–800 V DC", True),
        ("Output", "250–1000 V DC (peak efficiency at 666 V)", True),
        ("Power", "≈ 10 kW per module", True),
        ("Current", "15 A primary (22 A peak) · 17 A secondary (25 A peak)", False),
        ("Switching", "100 kHz", True),
        ("Isolation", "10 kV primary-to-secondary", False),
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
            <b>Errata, first prototype.</b> The eFuse (TPS26400) had pins 3 and 5 swapped in the footprint, so the board would not power up; it was bodged with wires. The standard KiCad footprint for TI's controlCARD connector numbers its pins the other way round, so a small flip-adapter PCB is included in the repo. The isolated supply's 1 kΩ current-limit resistor was replaced with 270 Ω to stop start-up faults, and the DS modulator sense pins — routed to pins that do not support it — were rerouted with magnet wire. Until these are fixed in a re-spin, this prototype is only to be run at low voltage.
          </div>""",
    figures=[
        ("dab-macro-1800", "dab-macro-1100", "Close-up of the secondary side: 1700 V SiC MOSFETs, gate-drive isolation and the HV capacitor bank.", 1800, 1125, "", "Secondary side"),
        ("dab-cooling-1500", "dab-cooling-950", "The cooling plate and fin stack, clamped over the SiC devices and the transformer.", 1500, 1125, "", "Cooling plate"),
    ],
    links=[("https://github.com/NovaPrime18/DAB_DCDC", "Hardware files on GitHub")],
    tags=["10 kW", "100 kHz", "1700 V SiC", "CERN-OHL-S"],
    next=("ganymede", "Sixty volts, a hundred amps."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["ganymede"] = dict(
    title="GaNymede — 60 V, 100 A GaN motor driver · Thommy",
    desc="A VESC-compatible three-phase GaN motor controller: six EPC2361 eGaN FETs, 0.25 mΩ phase shunts and 1.4 mF of bus capacitance on a 78 × 65 mm six-layer board.",
    h1="Sixty volts,<br>a hundred <em class=\"serif\">amps.</em>",
    lede="A VESC-compatible three-phase drive for a direct-drive hub motor: six eGaN FETs, 0.25 mΩ phase shunts and 1.4 mF of bus capacitance wrapped around a 78 × 65 mm six-layer power stage.",
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
          <p>A direct-drive hub motor needs high phase current in a compact package. GaNymede targets 50 A continuous and 100 A peak for one minute, with current and voltage sensing on every phase, Hall inputs and an ESP32-C3 for wireless telemetry.</p>
          <p>The control side follows the VESC pattern — STM32F405, three Hall inputs and three phase-current channels — so existing firmware and tools can be used. Most of the design work went into the power stage, current sensing and thermal budget.</p>
        """),
        ("02", "Specification", None),
        ("03", "Key design decisions", """
          <p><strong>The bus capacitor bank wraps the power stage.</strong> The roughly 1.4 mF bank is arranged around the bridge to keep the commutation loop short, with ceramic capacitors close to the switches and larger parts providing the bulk storage.</p>
          <p><strong>0.25 mΩ per phase, using two parallel shunts.</strong> Each phase uses two 0.5 mΩ 2512 resistors, feeding an INA240A1 at a gain of 20. Sharing the current between two parts reduces heating while keeping a useful measurement signal at high current.</p>
          <p><strong>Dead time lives in firmware.</strong> The LMG1210 drivers are configured for independent high- and low-side inputs, so dead time is set in software. That suits the VESC control scheme, but makes careful bring-up and gate-signal checks important.</p>
          <p><strong>Copper sized for the peak.</strong> The pours and via stitching are sized for the one-minute 100 A peak, not just the 50 A continuous rating. The loss model also accounts for shunt heating and the thermal path through the board.</p>
        """),
        ("04", "What the loss model shows", """
          <p>There is a full copper, semiconductor and thermal model in <a href="https://github.com/NovaPrime18/GaNymede/blob/main/LOSSES.md" target="_blank" rel="noopener">LOSSES.md</a>. At 100 A peak it predicts about 29 W of total loss and 99.4 % efficiency; at 50 A continuous, about 7.3 W and 99.7 %.</p>
          <p>The model puts most of the loss in the phase shunts and the 60 V/GND copper rather than in the GaN devices. That makes the thermal interface and copper layout especially important. A 1.5–2 °C/W natural-convection heatsink should be sufficient for the modelled continuous load, while the one-minute peak is limited mainly by thermal mass.</p>
        """),
        ("05", "The visual side", """
          <p>The back of the board carries an engraved illustration of Ganymede and the eagle, taken from the project's name. It has no electrical function; it is simply a detail I enjoyed adding, and it gives the board a recognisable identity.</p>
        """),
        ("06", "Where it stands", """
          <p>R1 has a completed schematic and six-layer layout. The current and thermal figures are modelled design targets, not bench measurements. They are labelled as such here and in the repository, and will need to be checked on hardware.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — design targets, not yet bench-verified",
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
    tags=["5.2 kW", "100 A peak", "EPC2361", "CERN-OHL-S"],
    next=("nitride-nano", "240 W in a pocket."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["nitride-nano"] = dict(
    title="nitride-nano — 240 W USB-C PD bench supply · Thommy",
    desc="A USB-C PD 3.2 buck/boost converter: 12–48 V in, 0–60 V out, 240 W, 1 MHz switching, 94.8 % measured peak efficiency.",
    h1="240 W<br>in a <em class=\"serif\">pocket.</em>",
    lede="A USB-C PD 3.2 buck/boost supply with a 0–60 V output and up to 240 W. The STM32 negotiates the input rail to keep the converter in an efficient operating region; the second revision reached 94.8 % measured peak efficiency.",
    crumb=("03", "Power supply"),
    meta=[
        ("Year", "2026 — R2"),
        ("Role", "Hardware, layout, bring-up, test"),
        ("Result", "94.8 % peak · 240.8 W in"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("nano-front-1800", "nano-front-1100", "nitride-nano: a compact white PCB with its GaN power stage, USB-C input and XT90 output connectors.", 1800, 1046),
    sections=[
        ("01", "The brief", """
          <p>The goal was a portable programmable supply in the spirit of the Miniware MDP-XP, with a wider output range and an emphasis on power density. It accepts USB-C Power Delivery or higher-voltage DC input and provides 0–60 V at up to 20 A through an XT90 connector.</p>
          <p>Switching at 1 MHz reduces the size of the magnetics and capacitors. The EPC GaN devices help keep the associated losses low enough for a compact enclosure.</p>
        """),
        ("02", "Specification", None),
        ("03", "Tracking the input rail", """
          <p>A four-switch buck/boost is generally less efficient when both bridges are switching. Instead of accepting any available charger voltage, the STM32 requests a PD rail based on the desired output, keeping the LT8390A in a cleaner buck or boost region where possible.</p>
          <p>The input supports fixed PDOs, PPS and AVS/EPR up to 48 V. This links the USB-C negotiation directly to the efficiency of the power stage, rather than treating it as a separate feature.</p>
        """),
        ("04", "Bench results", """
          <p>The first revision reached 164 W in one test at 94.1 %. With a 2.2 µH Coilcraft XAL1010 inductor, revision 2 reached 219 W at 94.8 % peak efficiency, with a highest measured input of 240.8 W. Testing used a Riden RD6024 supply and an EA-EL 3160-60 load.</p>
          <p>The repository includes the full test tables and equipment list for both revisions, making the effect of the component change easy to see.</p>
        """),
        ("05", "Thermal", """
          <p>A FreeCAD thermal model estimated an enclosure temperature of about 38 °C with a fan when 10 W was applied to the heatsink. On the bench, the GaN devices stayed around 60 °C, while the inductor core reached about 90 °C. That makes the inductor the main thermal constraint in the current revision.</p>
        """),
        ("06", "The rest of it", """
          <p>An STM32G474 runs the bare-metal UI on a 0.96″ OLED with three buttons, reads an INA228 for input and output power, and shows real-time efficiency. The power stage is EPC2367 eGaN with an LT8390A controller, following the EVAL-LT8390A topology. USB-C PD input stage based on the open-source PD240W design.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 2, bench-tested",
    rows=[
        ("Input", "12–48 V — USB-C PD or XT90", True),
        ("Output", "0–60 V, 20 A, 240 W", True),
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
            <b>Thermal finding.</b> The inductor core was the hottest component at approximately 90 °C; the GaN FETs stayed around 60 °C. A future revision would start by reviewing the magnetics rather than changing the power devices.
          </div>""",
    figures=[
        ("nano-back-1500", "nano-back-950", "The back of the board: silkscreen reads POWAH!, atom logo, and the output range printed where an assembly technician will see it.", 1500, 871, "", "Back side"),
        ("nano-photo-1800", "nano-photo-1100", "The rev 2 board in its printed housing, running on an XT90 input.", 1800, 1355, "figure--wide", "Rev 3, running"),
    ],
    links=[("https://github.com/NovaPrime18/nitride-nano", "Hardware and firmware on GitHub")],
    tags=["240 W", "1 MHz", "USB-C PD 3.2", "CERN-OHL-S"],
    next=("compressor-controller", "A compressor drive with active PFC."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["compressor-controller"] = dict(
    title="CompressorController — 230 V AC VESC-compatible HVAC drive · Thommy",
    desc="A mains-powered, VESC-compatible three-phase motor driver with active PFC, isolated gate signals and dual isolated CAN, designed against IEC 61000-3-2.",
    h1="A compressor drive<br>with active <em class=\"serif\">PFC.</em>",
    lede="A 230 V AC, VESC-compatible drive for compressor and HVAC applications. Active PFC reduces harmonic current, while isolated gate signals and dual isolated CAN separate the control side from the mains domain.",
    crumb=("04", "Mains drive"),
    meta=[
        ("Year", "2026 — Rev 1"),
        ("Role", "Hardware design, schematic hierarchy"),
        ("Scope", "Mains · 325 V bus · HVAC"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("compressor-front-1500", "compressor-front-950", "The compressor controller: green PCB with an intelligent power module, PFC inductor, film capacitors and a large bus capacitor bank.", 1500, 911),
    sections=[
        ("01", "The brief", """
          <p>This board is intended for compressor and HVAC applications where a compact three-phase drive has to run directly from 230 V AC. It combines a rectified DC bus, active power factor correction and an intelligent power module, while remaining compatible with VESC firmware and tools.</p>
          <p>The grid interface is a central part of the design. A simple diode bridge and bulk capacitor would draw pulsed current; the CCM PFC stage shapes the input current and is intended to help meet IEC 61000-3-2 harmonic limits.</p>
        """),
        ("02", "Specification", None),
        ("03", "Architecture", """
          <p>The schematic is split into ten hierarchical sheets: power input, PFC, phases, filters, isolator, low-voltage power, MCU, CAN and the VESC Express module. This keeps each functional block readable and makes reviews and reuse easier.</p>
          <p>The power path uses an EMI filter, inrush limiting and a bridge rectifier feeding a nominal 325 V bus, followed by a UCC28180 PFC stage and an Infineon IKCM10H60 intelligent power module. Gate drivers and bootstrap are integrated in the module, while a separate isolation barrier protects the control domain.</p>
        """),
        ("04", "Key design decisions", """
          <p><strong>Isolation is designed in from the start.</strong> Gate signals and fault lines cross a dedicated isolation barrier, and the CAN interfaces are isolated too. The schematic hierarchy makes that boundary explicit and easier to review.</p>
          <p><strong>PFC is part of the drive, not an add-on.</strong> The stage is intended around the compressor's operating profile rather than only a full-power resistive load, since harmonic performance also matters at part load.</p>
          <p><strong>VESC Express for connectivity.</strong> An ESP32 module provides Wi-Fi, Bluetooth and a CAN bridge, so commissioning and monitoring can use existing VESC tools instead of a custom application.</p>
          <p><strong>Service access.</strong> Tag-Connect SWD, status LEDs and a USB-C port for VESC Tool make programming and debugging possible without adding wires to the board.</p>
        """),
        ("05", "Compliance targets", None),
        ("06", "Compliance and safety", """
          <p>The design targets IEC 61000-3-2 for harmonic current emissions, IEC 60335-2-34 for motor-compressors and EN IEC 63000 for RoHS documentation. Active PFC supports the first of these, but it does not provide certification; compliance still has to be verified by measurement during integration.</p>
          <p>The DC bus sits at roughly 325–400 V from rectified mains. Enclosure, creepage, clearance and fusing therefore need to be treated as part of the system, and the board is intended for people qualified to work on mains equipment.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1",
    rows=[
        ("Input", "230 V AC single phase", True),
        ("HV bus", "≈ 325 V DC nominal", True),
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
            <b>Mains voltage.</b> This board operates at lethal voltages: 230 V AC in, roughly 325–400 V DC on the bus. It is an open hardware design intended for qualified people, with enclosure, creepage and fusing treated as part of the system rather than accessories.
          </div>""",
    figures=[
        ("compressor-back-1500", "compressor-back-950", "The power side: PFC inductor, film capacitors, IPM heatspreader and the bus capacitor bank.", 1500, 944, "", "Power side"),
        ("compressor-photo-1800", "compressor-photo-1100", "The first assembled compressor controller on a workbench, with the power stage, PFC magnetics and capacitor bank visible.", 1800, 1355, "", "First article"),
    ],
    links=[("https://github.com/NovaPrime18/CompressorController", "Hardware files on GitHub")],
    tags=["230 V AC", "Active PFC", "VESC", "IEC 61000-3-2"],
    next=("twin-gan", "Two motor drivers, one 99 mm board."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["twin-gan"] = dict(
    title="Twin-GaN — dual 3-phase GaN motor controller · Thommy",
    desc="Two complete VESC-compatible three-phase inverters on one 99 × 99 mm board, with both MCUs and an ESP32 sharing one internal CAN bus.",
    h1="Two motor drivers,<br>one 99 mm <em class=\"serif\">board.</em>",
    lede="A dual VESC-compatible controller with two complete three-phase GaN inverters on a 99 × 99 mm board. Both STM32s and an ESP32 share one internal CAN bus, allowing the motor channels to coordinate directly for traction control.",
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
          <p>Two-wheel-drive light electric vehicles often need two motor controllers. Twin-GaN puts both channels on one 99 × 99 mm board, with independent STM32F405 controllers, USB-C ports and three-shunt sensing. An ESP32-C3 provides a third CAN node.</p>
          <p>The aim is to reduce size and cost compared with two separate ESCs, accepting a lower peak-power rating in exchange for integration.</p>
        """),
        ("02", "Specification", None),
        ("03", "Why one board", """
          <p><strong>One CAN bus, three nodes.</strong> Both STM32s and the ESP32 share one terminated internal CAN bus, allowing the channels to exchange torque and control information without external wiring. This provides a hardware basis for on-board traction control.</p>
          <p><strong>Two VESC targets.</strong> Each channel has its own MCU and six-PWM stage, so VESC Tool detects and configures them as two separate controllers. That keeps the familiar setup workflow and avoids a custom control interface.</p>
          <p><strong>Three-shunt sensing per channel.</strong> Each phase uses an INA240A1D across a 2 mΩ shunt. REF1 and REF2 are connected for bidirectional measurement, so the controller can distinguish drive and regenerative current.</p>
          <p><strong>Practical connections.</strong> Each controller has its own USB-C port with CC pulldowns and VBUS protection, plus Tag-Connect SWD and the standard VESC accessory header. These details should make programming, commissioning and future expansion straightforward.</p>
        """),
        ("04", "Where it stands", """
          <p>R1 is at the design stage. The targets are 60 V input, 20 A battery current, 20 A continuous and 40 A absolute-max phase current per channel, and roughly 1.2 kW total. None of these figures has been bench-verified. They are labelled as targets here and in the repository so the next person to build the board knows what still needs testing.</p>
        """),
    ],
    table_title="Specification",
    table_caption="Revision 1 — design targets, not yet bench-verified",
    rows=[
        ("Input", "up to 60 V DC · XT60", True),
        ("Battery current", "20 A", True),
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
    tags=["1.2 kW", "2 × 3-phase", "EPC23102", "CERN-OHL-S"],
    next=("schroombort", "The board that started it."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["schroombort"] = dict(
    title="Schroombort — 36-key soundboard, macro-pad and calculator · Thommy",
    desc="A battery-powered, over-engineered mechanical soundboard: 36 Cherry MX switches, a VFD, stereo speakers and three modes of operation.",
    h1="The board that<br>started <em class=\"serif\">it.</em>",
    lede="Schroombort is a battery-powered soundboard with 36 Cherry MX switches, a vacuum fluorescent display and stereo speakers. It also works as a macro-pad and a basic calculator. It was the first board I finished, and many of the skills used in the later projects started here.",
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
          <p>At its simplest, Schroombort plays a sound when you press a key. It has 36 mechanical switches, a VFD, stereo speakers, USB-C charging and a battery power-path manager that can run from USB, battery or both.</p>
          <p>It has three modes. As a soundboard, each key plays a file from the SD card. Connected over USB-C, it becomes a macro-pad with assignable keys. The third mode is a basic calculator, added because the hardware already had a display and keypad.</p>
        """),
        ("02", "Specification", None),
        ("03", "Why it matters", """
          <p>This was the project that taught me what it takes to finish a piece of hardware: power management, a keyboard matrix, display driving, audio, an enclosure and firmware all have to work together. It also taught me that details which look fine on screen do not always read well on a physical board.</p>
          <p>It was more complex than the original idea required, but that made it a useful way to learn. Later projects could build on a complete design rather than a collection of separate experiments.</p>
        """),
        ("04", "The trailer", """
          <p>There is a short cinematic trailer on <a href="https://www.youtube.com/watch?v=MM4cooladaY" target="_blank" rel="noopener">YouTube</a>, which shows the finished device and its display.</p>
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
    next=("dab-dcdc", "Ten kilowatts, on the bench."),
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
                        ("IEC 61000-3-2", "Harmonic current emissions — addressed by active PFC", True),
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
    (OUT / f"{slug}.html").write_text(html)
    print("wrote", f"projects/{slug}.html")


for slug, c in CASES.items():
    build_case(slug, c)
