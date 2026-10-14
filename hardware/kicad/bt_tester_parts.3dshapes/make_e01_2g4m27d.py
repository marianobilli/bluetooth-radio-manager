"""Generate the Ebyte E01-2G4M27D radio models plugged into the 2x4 radio
socket footprint (on top of a standard 8.5 mm 2x4 female socket, which the
footprint adds separately from the KiCad library):

  E01-2G4M27D.step          18 x 33.2 mm module + male header + edge SMA jack
  E01-2G4M27D_antenna.step  the same 2 dBi rubber-duck antenna as the nRF24,
                            screwed onto the E01's SMA

Built from boxes and cylinders (see step_writer.py). Footprint coordinates:
origin = pin 1 (GND), odd pins at x=0, even pins at x=2.54, rows +y; the
module body runs +x from the header to the SMA end.

Dimensions: measured on the part (PCB 18 x 33.2, shield can 16.6 x 22.6 x
~3, SMA legs over the last 4 mm of the board with 3.3 mm total thickness,
6.5 x 6.5 x 1.5 flange outside the board edge, 8 mm barrel) and from the
user manual drawing (docs/, pin 1 row 1.45 mm from the board end, pins
centred across the width, 3.68 mm PCB + can). Pins 9-12 (GND, near the
SMA) are not modelled.
Run: python make_e01_2g4m27d.py
"""
import os

from step_writer import Model

PITCH = 2.54
SOCKET_H = 8.5          # 2.54 mm female header body height
SPACER_H = 2.5          # male header plastic under the module PCB
PCB_T = 1.0             # measured on the part
PCB_Z = SOCKET_H + SPACER_H
TOP = PCB_Z + PCB_T

L, W = 33.2, 18.0
X0 = -1.45              # module edge behind the pin 1 row (header plastic at the edge)
X1 = X0 + L
YC = 1.5 * PITCH        # module centred on the 4 header rows

CAN_L, CAN_W, CAN_H = 22.6, 16.6, 2.7   # shield can; 2.7 + PCB 1.0 = 3.7 (manual: 3.68)
CAN_X0 = 3.9                            # just past the pin 2 row solder tips

SMA_LEG_L = 4.0         # edge-mount jack legs over the board end
SMA_TOTAL_T = 3.3       # legs + board, total thickness
SMA_LEG_T = (SMA_TOTAL_T - PCB_T) / 2
SMA_FLANGE = 6.5        # square flange past the board edge
SMA_FLANGE_T = 1.5
SMA_BARREL_L = 8.0
SMA_BARREL_R = 3.1
SMA_Y = YC
SMA_AXIS_Z = PCB_Z + PCB_T / 2   # edge mount: centred on the board

COLORS = {
    "pcb":    (0.06, 0.36, 0.16),   # module PCB, green
    "black":  (0.08, 0.08, 0.08),
    "gold":   (0.86, 0.70, 0.30),
    "silver": (0.70, 0.71, 0.73),
    "label":  (0.95, 0.62, 0.12),   # orange Ebyte label on the can
    "rubber": (0.10, 0.10, 0.10),
}

m = Model("E01-2G4M27D", COLORS)

m.box("pcb", "pcb", X0, YC - W / 2, PCB_Z, X1, YC + W / 2, TOP)

# 2x4 male header: plastic spacer, pins into the socket and solder tips on top.
m.box("header", "black", -PITCH / 2, -PITCH / 2, SOCKET_H, 1.5 * PITCH, 3.5 * PITCH, PCB_Z)
for col in range(2):
    for row in range(4):
        x, y = col * PITCH, row * PITCH
        m.cbox(f"pin{row * 2 + col + 1}", "gold", x, y, 0.64, 0.64, SOCKET_H - 6.0, 6.0 + SPACER_H + PCB_T + 1.0)

# Shield can with the label on top.
m.box("can", "silver", CAN_X0, YC - CAN_W / 2, TOP, CAN_X0 + CAN_L, YC + CAN_W / 2, TOP + CAN_H - 0.1)
m.box("label", "label", CAN_X0 + 0.5, YC - CAN_W / 2 + 0.5, TOP + CAN_H - 0.1,
      CAN_X0 + CAN_L - 0.5, YC + CAN_W / 2 - 0.5, TOP + CAN_H)

# Edge-mount SMA jack: legs clamp the last 4 mm of the board top and bottom,
# square flange just past the edge, threaded barrel beyond it.
m.box("sma_leg_top", "gold", X1 - SMA_LEG_L, SMA_Y - SMA_FLANGE / 2, TOP,
      X1, SMA_Y + SMA_FLANGE / 2, TOP + SMA_LEG_T)
m.box("sma_leg_bottom", "gold", X1 - SMA_LEG_L, SMA_Y - SMA_FLANGE / 2, PCB_Z - SMA_LEG_T,
      X1, SMA_Y + SMA_FLANGE / 2, PCB_Z)
m.box("sma_flange", "gold", X1, SMA_Y - SMA_FLANGE / 2, SMA_AXIS_Z - SMA_FLANGE / 2,
      X1 + SMA_FLANGE_T, SMA_Y + SMA_FLANGE / 2, SMA_AXIS_Z + SMA_FLANGE / 2)
BARREL_X0 = X1 + SMA_FLANGE_T
m.xcyl("sma_barrel", "gold", SMA_Y, SMA_AXIS_Z, SMA_BARREL_R, BARREL_X0, SMA_BARREL_L)
m.xcyl("sma_pin_insulator", "silver", SMA_Y, SMA_AXIS_Z, 2.0, BARREL_X0 + SMA_BARREL_L, 0.3)

ant = Model("E01-2G4M27D_antenna", COLORS)
ANT_X = BARREL_X0 + SMA_BARREL_L
ant.xcyl("ant_nut", "silver", SMA_Y, SMA_AXIS_Z, 4.0, ANT_X, 8.0)
ant.xcyl("ant_hinge", "rubber", SMA_Y, SMA_AXIS_Z, 5.0, ANT_X + 8.0, 7.0)
ant.cyl("ant_whip", "rubber", ANT_X + 11.5, SMA_Y, 5.0, SMA_AXIS_Z + 5.0, 100.0)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    m.write(os.path.join(here, "E01-2G4M27D.step"), "make_e01_2g4m27d.py")
    ant.write(os.path.join(here, "E01-2G4M27D_antenna.step"), "make_e01_2g4m27d.py")
