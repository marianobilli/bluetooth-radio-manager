"""Generate the nRF24L01+PA+LNA radio models plugged into the nRF24_module_2x4
footprint (on top of a standard 8.5 mm 2x4 female socket, which the footprint
adds separately from the KiCad library):

  nRF24L01_PA_LNA.step          41 x 15.5 mm module + male header + SMA jack
  nRF24L01_PA_LNA_antenna.step  2 dBi rubber-duck antenna folded upright

Built from boxes and cylinders (see step_writer.py). Footprint coordinates:
origin = pin 1 (GND), odd pins at x=0, even pins at x=2.54, rows +y; the module
body runs +x from the header to the SMA end. Part positions are approximate.
Run: python make_nrf24_pa_lna.py
"""
import os

from step_writer import Model

PITCH = 2.54
SOCKET_H = 8.5          # 2.54 mm female header body height
SPACER_H = 2.5          # male header plastic under the module PCB
PCB_T = 1.6
PCB_Z = SOCKET_H + SPACER_H
TOP = PCB_Z + PCB_T

L, W = 41.0, 15.5
X0 = -2.0               # module edge behind the GND/CE/SCK/MISO column
YC = 1.5 * PITCH        # module is centred on the 4 header rows
SMA_Y = YC              # SMA jack on the module centre line
SMA_AXIS_Z = TOP + 3.2

COLORS = {
    "pcb":    (0.05, 0.05, 0.06),
    "black":  (0.08, 0.08, 0.08),
    "gold":   (0.86, 0.70, 0.30),
    "silver": (0.70, 0.71, 0.73),
    "cap":    (0.65, 0.55, 0.40),
    "rubber": (0.10, 0.10, 0.10),
}

m = Model("nRF24L01_PA_LNA", COLORS)

m.box("pcb", "pcb", X0, YC - W / 2, PCB_Z, X0 + L, YC + W / 2, TOP)

# 2x4 male header: plastic spacer, pins into the socket and solder tips on top.
m.box("header", "black", -PITCH / 2, -PITCH / 2, SOCKET_H, 1.5 * PITCH, 3.5 * PITCH, PCB_Z)
for col in range(2):
    for row in range(4):
        x, y = col * PITCH, row * PITCH
        m.cbox(f"pin{row * 2 + col + 1}", "gold", x, y, 0.64, 0.64, SOCKET_H - 6.0, 6.0 + SPACER_H + PCB_T + 1.0)

# nRF24L01+ (QFN20 4x4), RFX2401C PA/LNA (QFN16 3x3), 16 MHz crystal, passives.
m.cbox("nrf24l01", "black", 11.0, YC, 4.0, 4.0, TOP, 0.9)
m.cbox("pa_lna", "black", 24.0, YC, 3.0, 3.0, TOP, 0.9)
m.cbox("xtal", "silver", 15.5, YC + 4.5, 3.2, 2.5, TOP, 0.8)
for k, (x, y) in enumerate([(7.5, YC - 4.5), (8.5, YC + 4.5), (17.5, YC - 4.0),
                            (20.0, YC + 4.5), (27.5, YC - 3.5), (29.0, YC + 3.5)]):
    m.cbox(f"c{k}", "cap", x, y, 1.6, 0.8, TOP, 0.8)

# SMA jack: square body on the far end, barrel and hex nut off the module edge.
SMA_X = X0 + L - 6.4
m.box("sma_body", "gold", SMA_X, SMA_Y - 3.2, TOP, SMA_X + 6.4, SMA_Y + 3.2, TOP + 6.4)
m.xcyl("sma_barrel", "gold", SMA_Y, SMA_AXIS_Z, 3.1, X0 + L, 9.0)
m.xcyl("sma_pin_insulator", "silver", SMA_Y, SMA_AXIS_Z, 2.0, X0 + L + 9.0, 0.3)

ant = Model("nRF24L01_PA_LNA_antenna", COLORS)
ANT_X = X0 + L + 9.0
ant.xcyl("ant_nut", "silver", SMA_Y, SMA_AXIS_Z, 4.0, ANT_X, 8.0)
ant.xcyl("ant_hinge", "rubber", SMA_Y, SMA_AXIS_Z, 5.0, ANT_X + 8.0, 7.0)
ant.cyl("ant_whip", "rubber", ANT_X + 11.5, SMA_Y, 5.0, SMA_AXIS_Z + 5.0, 100.0)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    m.write(os.path.join(here, "nRF24L01_PA_LNA.step"), "make_nrf24_pa_lna.py")
    ant.write(os.path.join(here, "nRF24L01_PA_LNA_antenna.step"), "make_nrf24_pa_lna.py")
