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
      <span class="via" aria-hidden="true"></span>
      Thommy<span class="dot">.</span>
    </a>
{NAV}
    <span class="head-status"><span class="pulse" aria-hidden="true"></span>Open to the right thing</span>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="primary-nav">
      <span aria-hidden="true"></span>
    </button>
  </div>
</header>
"""


def foot(year="2026"):
    return f"""
<footer class="site-foot">
  <div class="wrap foot-inner">
    <span>© {year} Thommy · they/them</span>
    <span>Plain HTML, because a portfolio shouldn't need a build step.</span>
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
    lede="One building block of a 500 kW off-grid EV charger: 800 V in, up to 1000 V out at 100 kHz through a planar transformer with 10 kV isolation — and creepage treated as a design constraint rather than an afterthought.",
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
          <p>The project was an internship thesis: work out whether a 500 kW off-grid EV DC fast charger could be built in-house. A 500 kW charger is not one converter. It is a rack of modules that share a DC bus, so the thesis needed a module — a 10 kW dual active bridge, derived from a Texas Instruments reference design and rebuilt around the parts and processes actually available.</p>
          <p>The module had to hold 500–800 V on the primary, deliver 250–1000 V on the secondary, survive an EV charger's fault currents, and be manufacturable at a price that made the whole idea worth evaluating. The full design rationale, LTspice and PLECS results and the test campaign live in the thesis; the repository holds the hardware.</p>
        """),
        ("02", "What a 10 kW module needs", None),
        ("03", "Decisions worth defending", """
          <p><strong>Six layers instead of the reference design's four.</strong> At 22 A peak on the primary and 25 A on the secondary, conduction loss stops being a detail. The extra layers carry 70 µm copper, spread heat, and let the high-current path keep a via per amp without turning the plane into a colander. Trace rise was held to ≤ 10 °C above ambient at 30 A using KiCad's trace-width calculator.</p>
          <p><strong>1700 V on the isolated side, with 1.7× derating.</strong> A 1000 V output does not leave 1000 V of headroom — it leaves switching overshoot, transformer ringing and the occasional very bad day. The SiC MOSFETs and the DC-blocking capacitors are rated to 1700 V, and the blocking caps are 2280-package parts double-stacked to reach the capacitance in the space available.</p>
          <p><strong>The contactors left the board.</strong> High-voltage switching happens externally, through XT30 connectors. It costs a little in integration effort and buys the freedom to pick a contactor rated for the real bus voltage instead of one that fits a footprint on a prototype PCB.</p>
          <p><strong>The transformer is a structural member.</strong> It sits in the middle, supports the board, and is where the cooling plate clamps down. The board does not need a separate frame because the heaviest component is already doing the job.</p>
        """),
        ("04", "What went wrong", None),
        ("05", "Numbers", None),
        ("06", "The rest of the board", """
          <p>All components sit on the top side, for cheaper single-sided assembly and a simpler stencil. Isolation is galvanic through a Payton Planar transformer — 24:20 turns, 35 µH of leakage inductance, 10 kV dielectric strength — and the 5 V and gate-drive rails are derived on-board on both sides of the barrier. Control is a TI controlCARD over CAN, phase-shift regulating the bridge.</p>
          <p>Everything was prototyped through JLCPCB on their 6-layer, double-thick-copper process. The board is not a product; it is an argument that the product is possible.</p>
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
    title="GaNymede — 60 V, 100 A GaN motor drive · Thommy",
    desc="A VESC-compatible three-phase GaN motor controller: six EPC2361 eGaN FETs, 0.25 mΩ phase shunts and 1.4 mF of bus capacitance on a 78 × 65 mm six-layer board.",
    h1="Sixty volts,<br>a hundred <em class=\"serif\">amps.</em>",
    lede="A VESC-compatible three-phase drive for a direct-drive hub motor: six eGaN FETs, 0.25 mΩ phase shunts and 1.4 mF of bus capacitance wrapped around a 78 × 65 mm six-layer power stage.",
    crumb=("02", "Motor drive"),
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
          <p>A direct-drive hub motor wants a lot of phase current in a small package, with no gearbox to hide the inefficiency. GaNymede is built for that: 50 A phase continuous, 100 A peak for one minute, phase-current and phase-voltage sensing on every leg, Hall inputs, and an ESP32-C3 for wireless telemetry.</p>
          <p>The control side deliberately follows the VESC pattern — STM32F405, three Hall inputs, three phase-current channels — because the value of a VESC-compatible board is the firmware ecosystem, not a new one. The power stage is where the design earns its keep.</p>
        """),
        ("02", "Specification", None),
        ("03", "Decisions worth defending", """
          <p><strong>The bus capacitor bank wraps the power stage.</strong> 1.4 mF is not a polite number of capacitors; placing them around the bridge instead of at one end keeps the commutation loop short and stops the DC link from becoming an inductor with a capacitor problem.</p>
          <p><strong>0.25 mΩ per phase, measured across two 0.5 mΩ shunts in parallel.</strong> Two 2512 resistors share the current and the heating, and an INA240A1 at a gain of 20 turns microvolts into something a 12-bit ADC can resolve at 100 A. The whole sensing chain is inside the power loop, so it is part of the layout, not an afterthought.</p>
          <p><strong>Dead time lives in firmware.</strong> The LMG1210s are strapped for independent high and low inputs rather than self-timed, which makes dead time a software parameter. That is the right place for it on a VESC target — but it means the gate drive is only as safe as the first bring-up.</p>
          <p><strong>Copper sized for the peak, not the average.</strong> A 100 A minute is a thermal event. The pours and the via stitching are sized for the whole minute, not for the 50 A number on the front of the datasheet.</p>
        """),
        ("04", "The loss model says something surprising", """
          <p>There is a full copper, semiconductor and thermal model in <a href="https://github.com/NovaPrime18/GaNymede/blob/main/LOSSES.md" target="_blank" rel="noopener">LOSSES.md</a>. At 100 A peak it predicts about 29 W of total loss and 99.4 % efficiency; at 50 A continuous, about 7.3 W and 99.7 %.</p>
          <p>The interesting part is where the heat comes from: the phase shunts and the 60 V/GND copper dominate the budget, not the six eGaN devices. Which changes the thermal design — the heatsink needs to move 5–6 W continuously and about 20 W by the end of a 100 A minute, so a 1.5–2 °C/W natural-convection sink is enough. The thermal pad under the FETs matters more than the heatsink, and the one-minute rating is limited by thermal mass rather than by the sink.</p>
        """),
        ("05", "A board can be a poster", """
          <p>The back of the board carries an engraved illustration of Ganymede — the moon, and the myth — rendered as silkscreen and copper pour. It costs nothing electrically and it makes the object worth picking up. If a board spends its life inside a housing, it may as well look like something on the way in.</p>
        """),
        ("06", "Where it stands", """
          <p>R1 is drawn and the six-layer layout is finished. The current and thermal figures above are design targets from the loss model, not bench measurements — the repository says so where the table is, and this page is not going to pretend otherwise.</p>
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
            <b>Phase currents are amplitudes, not RMS.</b> 100 A peak is 70.7 A RMS. The 100 V FET rating leaves headroom for turn-off overshoot, but the real margin depends on power-loop inductance and deserves a double-pulse check before anyone believes the model.
          </div>""",
    figures=[
        ("ganymede-top-1400", "ganymede-top-900", "The assembled module in its printed housing: 78 × 65 mm, XT90 input, three plated through-holes for U, V and W.", 1400, 1020, "figure--wide", "Assembled, in housing"),
    ],
    links=[("https://github.com/NovaPrime18/GaNymede", "Hardware files on GitHub")],
    tags=["5.2 kW", "100 A peak", "EPC2361", "CERN-OHL-S"],
    next=("nitride-nano", "Two hundred and forty watts, in a pocket."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["nitride-nano"] = dict(
    title="nitride-nano — 240 W USB-C PD bench supply · Thommy",
    desc="A USB-C PD 3.1 buck/boost converter: 12–48 V in, 0–60 V out, 240 W, 1 MHz switching, 94.8 % measured peak efficiency.",
    h1="Two hundred and forty watts,<br>in a <em class=\"serif\">pocket.</em>",
    lede="A USB-C PD 3.1 buck/boost that turns a laptop charger into a 0–60 V bench supply. 1 MHz switching, eGaN FETs, and a controller kept out of its own lossiest operating mode by an MCU that negotiates PPS, AVS and EPR.",
    crumb=("03", "Power supply"),
    meta=[
        ("Year", "2026 — R2"),
        ("Role", "Hardware, layout, bring-up, test"),
        ("Result", "94.8 % peak · 240.8 W in"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("nano-front-1800", "nano-front-1100", "nitride-nano: a compact white PCB with USB-C, an OLED display, a rotary encoder, an XT90 output and a dense GaN power stage.", 1800, 947),
    sections=[
        ("01", "The brief", """
          <p>The target was a portable programmable supply — the same job as a Miniware MDP-XP, but with more power density and a wider voltage range, and less concern about output ripple. Input from USB-C Power Delivery or a high-voltage DC source; output 0–60 V at up to 20 A from an XT90.</p>
          <p>Small is the whole point. At 1 MHz the inductor and capacitors shrink enough for the board to fit inside a printed housing the size of a small brick, and the GaN FETs make 1 MHz practical without the switching loss eating the density gain.</p>
        """),
        ("02", "Specification", None),
        ("03", "The trick: auto-tracking PD", """
          <p>A non-inverting buck/boost is efficient in buck, efficient in boost, and noticeably worse in the four-switch band where both bridges switch. nitride-nano negotiates the input voltage instead of accepting whatever the charger offers: the MCU derives the PD rail from the requested output, so the LT8390A stays in a clean buck or boost region across the whole 0–60 V range.</p>
          <p>That means speaking full USB-C PD on the input side — fixed PDOs, PPS in 50 mV steps, and AVS/EPR up to 48 V — and choosing the rail before the converter ever has to regulate. The negotiation is as much a part of the power stage as the inductor.</p>
        """),
        ("04", "Measured, not modelled", """
          <p>Revision 1 delivered 164 W at 94.1 %; revision 2, with a 2.2 µH Coilcraft XAL1010-222MED, delivers 219 W at 94.8 % peak — 240.8 W in, measured on a Riden RD6024 and an EA-EL 3160-60 load.</p>
          <p>The two revisions are in the repository with their full test tables. Publishing the worse number next to the better one is the only way the better one means anything.</p>
        """),
        ("05", "Thermal", """
          <p>The enclosure was simulated in FreeCAD: about 38 °C with a fan when 10 W of loss goes into the heatsink from the GaN FETs. In practice the FETs barely exceed 60 °C, because not all of that heat leaves through the top of the package — the inductor core, at around 90 °C, is by far the hottest thing on the board. Which is the usual lesson: the magnetic component is the thermal design.</p>
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
            <b>Where the losses actually went.</b> The inductor core ran hottest at ~90 °C — the single lossiest component on the board. The GaN FETs barely got above 60 °C. If there is ever a revision 3, it starts with the magnetics, not the silicon.
          </div>""",
    figures=[
        ("nano-back-1500", "nano-back-950", "The back of the board: silkscreen reads POWAH!, atom logo, and the output range printed where an assembly technician will see it.", 1500, 871, "", "Back side"),
        ("nano-photo-1600", "nano-photo-1000", "The rev 2 board in its printed housing, running on an XT90 input.", 1600, 1205, "figure--wide", "Rev 2, running"),
    ],
    links=[("https://github.com/NovaPrime18/nitride-nano", "Hardware and firmware on GitHub")],
    tags=["240 W", "1 MHz", "USB-C PD 3.1", "CERN-OHL-S"],
    next=("compressor-controller", "A compressor drive that keeps the grid happy."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["compressor-controller"] = dict(
    title="CompressorController — 230 V AC VESC-compatible HVAC drive · Thommy",
    desc="A mains-powered, VESC-compatible three-phase motor driver with active PFC, isolated gate signals and dual isolated CAN, designed against IEC 61000-3-2.",
    h1="A compressor drive that<br>keeps the grid <em class=\"serif\">happy.</em>",
    lede="230 V AC straight into a VESC-compatible HVAC drive, with a CCM PFC front end so the current draw is a sine wave rather than a crime — and IEC 61000-3-2 in the requirements from the first schematic.",
    crumb=("04", "Mains drive"),
    meta=[
        ("Year", "2026 — Rev 1"),
        ("Role", "Hardware design, schematic hierarchy"),
        ("Scope", "Mains · 325 V bus · HVAC"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("compressor-front-1500", "compressor-front-950", "The compressor controller: green PCB with an intelligent power module, PFC inductor, film capacitors and a large bus capacitor bank.", 1500, 935),
    sections=[
        ("01", "The brief", """
          <p>Compressors and HVAC blowers are the boring half of electrification, and they are where the volume is. This board takes 230 V AC from the wall, rectifies it, corrects the power factor and drives a three-phase compressor motor — while staying inside the VESC ecosystem, so the firmware, tooling and configuration experience are already solved problems.</p>
          <p>The interesting requirement is not the motor. It is the grid: a diode bridge and a big capacitor draw current in ugly pulses, and IEC 61000-3-2 has opinions about that. Active PFC turns the input current into a sine wave in phase with the voltage, which is both a compliance story and a smaller bus capacitor.</p>
        """),
        ("02", "Specification", None),
        ("03", "Architecture", """
          <p>The design is split into ten hierarchical sheets rather than one enormous schematic: power in, PFC, phases, filters, isolator, LV power, MCU, CAN and the VESC Express module. Each sheet can be read, reviewed and reused on its own — and a reviewer looking for the creepage problem only has to read the sheet where creepage lives.</p>
          <p>The power path is deliberately conventional: EMI filter, inrush limiting and a bridge rectifier into a ~325 V bus; a UCC28180 CCM PFC boost stage; then an Infineon IKCM10H60 IPM — 10 A, 600 V, with gate drivers and bootstrap integrated — driving U/V/W. What is not conventional is how carefully the control domain is kept away from the mains domain.</p>
        """),
        ("04", "Decisions worth defending", """
          <p><strong>Isolation is a boundary, not a suggestion.</strong> Gate signals and fault lines cross through a dedicated isolator sheet, and the CAN interfaces are isolated too. On a mains product the barrier is the product; everything else is a circuit.</p>
          <p><strong>PFC first, motor second.</strong> The PFC stage is sized for the compressor's real load profile, not for a resistive test load, because the harmonic limit is about current shape at part load as much as at full load.</p>
          <p><strong>VESC Express instead of a bespoke cloud.</strong> An ESP32 module provides Wi-Fi, Bluetooth and a CAN bridge, so commissioning and monitoring happen through tools that already exist. The board does not need to invent an app.</p>
          <p><strong>Serviceability.</strong> Tag-Connect SWD, status LEDs and a USB-C port for VESC Tool, because the first person to debug this board should not need to solder to it.</p>
        """),
        ("05", "Compliance targets", None),
        ("06", "The honest part", """
          <p>The board is designed against IEC 61000-3-2 (harmonic current emissions), IEC 60335-2-34 (motor-compressors) and EN IEC 63000 (RoHS documentation). Active PFC substantially helps with the first; it does not grant certification. CE marking has to be earned by the integrating party with measurement, and the repository says exactly that.</p>
          <p>The same goes for the voltage: the DC bus sits at roughly 325–400 V from rectified mains. This is a board to be handled by people who already know why the capacitor bank is the last thing you touch.</p>
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
        ("compressor-back-1500", "compressor-back-950", "The power side: PFC inductor, film capacitors, IPM heatspreader and the bus capacitor bank.", 1500, 944, "figure--wide", "Power side"),
    ],
    links=[("https://github.com/NovaPrime18/CompressorController", "Hardware files on GitHub")],
    tags=["230 V AC", "Active PFC", "VESC", "IEC 61000-3-2"],
    next=("twin-gan", "Two motor drives, one 99 mm board."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["twin-gan"] = dict(
    title="Twin-GaN — dual 3-phase GaN motor controller · Thommy",
    desc="Two complete VESC-compatible three-phase inverters on one 99 × 99 mm board, with both MCUs and an ESP32 sharing one internal CAN bus.",
    h1="Two motor drives,<br>one 99 mm <em class=\"serif\">board.</em>",
    lede="A dual VESC-compatible controller that packs two complete three-phase GaN inverters onto a single 99 × 99 mm board — with all three controllers sharing one internal CAN bus, so traction control is a local conversation instead of a cable.",
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
          <p>Two-wheel-drive light electric vehicles — skateboards, e-bikes, small robots — usually carry two separate ESCs that have to agree with each other over a cable. Twin-GaN does the job with one board: two independent three-phase inverters, each with its own STM32F405, its own USB-C and its own three-shunt sensing chain, plus an ESP32-C3 as a third CAN node.</p>
          <p>The bet is that integration beats modularity at this size. It is cheaper and smaller than the equivalent dual ESC, and the trade-off is deliberate: it gives up peak power for density.</p>
        """),
        ("02", "Specification", None),
        ("03", "What makes it a system, not two boards", """
          <p><strong>One CAN bus, three nodes.</strong> Both STM32s and the ESP32 are on the same internal bus with on-board termination, so the two channels can hand each other torque requests without an external harness. Traction control becomes a firmware feature rather than a wiring problem.</p>
          <p><strong>Two VESC targets, not one.</strong> Because each channel has its own MCU and its own 6-PWM stage, VESC Tool sees two separate controllers, identifies and configures them independently, and treats them exactly like two ESCs — which is what makes the board instantly usable by anyone who already knows the ecosystem.</p>
          <p><strong>Three-shunt sensing per channel with a real reference.</strong> One INA240A1D per phase across 2 mΩ shunts, with REF1 at GND and REF2 at 3V3, so the measurement is genuinely bidirectional and the firmware can tell forward from regen.</p>
          <p><strong>Every port accounted for.</strong> USB-C per controller with proper 5.1 kΩ CC pulldowns and a PTC on VBUS; Tag-Connect SWD per MCU; VESC accessory headers on the standard pinout. The details that make a board feel like a product instead of a prototype.</p>
        """),
        ("04", "Where it stands", """
          <p>R1 is drawn, and the numbers on this page are design targets — 60 V, 20 A battery current, 20 A continuous and 40 A absolute-max phase current per channel, roughly 1.2 kW total. None of it has been bench-verified. The repository carries the same warning at the top of the specification table, which is the only honest way to publish a board that has not yet been through a real load.</p>
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
            <b>Design targets, not measurements.</b> The current and power figures are targets for revision 1 and have not been bench-verified. Publishing them as if they were measured would make every other number on this site worth less.
          </div>""",
    figures=[
        ("twin-gan-900", "twin-gan-900", "Detail: two EPC23102 ePower stages per channel, with the 2 mΩ shunts and INA240 sensing in the phase legs.", 1086, 1205, "figure--wide", "Power stage detail"),
    ],
    links=[("https://github.com/NovaPrime18/Twin-GaN", "Hardware files on GitHub")],
    tags=["1.2 kW", "2 × 3-phase", "EPC23102", "CERN-OHL-S"],
    next=("schroombort", "The thing that got me here."),
    year="2026",
)

# --------------------------------------------------------------------------
CASES["schroombort"] = dict(
    title="Schroombort — 36-key soundboard, macro-pad and calculator · Thommy",
    desc="A battery-powered, over-engineered mechanical soundboard: 36 Cherry MX switches, a VFD, stereo speakers and three modes of operation.",
    h1="The thing that<br>got me <em class=\"serif\">here.</em>",
    lede="A battery-powered soundboard with 36 Cherry MX switches, a vacuum fluorescent display and stereo speakers. It is also a macro-pad. And a calculator. It was the first board I ever finished, and it is the reason there are five more.",
    crumb=("06", "Where I started"),
    meta=[
        ("Year", "2021"),
        ("Role", "Everything — it was the first one"),
        ("Modes", "Soundboard · macro-pad · calculator"),
        ("Licence", "CERN-OHL-S v2.0"),
    ],
    hero=("schroombort-1500", "schroombort-950", "Schroombort: a black battery-powered board with 36 mechanical switches, a vacuum fluorescent display and silkscreen artwork.", 1500, 1670),
    sections=[
        ("01", "What it is", """
          <p>A device whose entire job is to play dumb sounds when you press a button. Thirty-six Cherry MX-style switches, a vacuum fluorescent display, stereo speakers, a battery, USB-C charging, and a power-path manager that runs from USB, battery, or a mix of both without anyone noticing the transition.</p>
          <p>It runs in three configurations. As a soundboard, each key plays a file straight from the SD card. Plugged into a computer over USB-C, it becomes a 36-key macro-pad with assignable macros. Flip it into the third mode and it is a fully functional basic calculator — because a device with a VFD and a keypad that cannot do arithmetic is leaving value on the table.</p>
        """),
        ("02", "Specification", None),
        ("03", "Why it matters", """
          <p>Every later board on this site owes something to this one. It taught the loop that actually matters: pick a thing that does not need to exist, then make it exist properly. Power path, battery charging, keyboard matrix, display driving, audio output, enclosure, firmware, and the specific misery of a silkscreen that looked fine in the viewer and unreadable on the physical board.</p>
          <p>The over-engineering is the point. Nobody needs 36 buttons to play a sound. Building it anyway is how you find out what a board feels like when it is finished, and that is a different skill from designing one.</p>
        """),
        ("04", "The trailer", """
          <p>There is a cinematic trailer, because a README cannot do it justice. It is on <a href="https://www.youtube.com/watch?v=MM4cooladaY" target="_blank" rel="noopener">YouTube</a>, and it is exactly as serious as the project deserves.</p>
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
            <b>Origin story, technically.</b> First finished board. First battery. First matrix. First time a silkscreen joke survived all the way to a physical object. Everything after this was easier to start because this one had been finished once.
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
        + foot(c.get("year", "2026"))
    )
    (OUT / f"{slug}.html").write_text(html)
    print("wrote", f"projects/{slug}.html")


for slug, c in CASES.items():
    build_case(slug, c)
