"""UML-диаграмма компонентов HammerLive в стиле методички (порты + ball-and-socket), компактная раскладка."""
W, H = 1400, 1390
o = []
a = o.append
MONO = 'font-family="Liberation Mono, Consolas, monospace"'
SANS = 'font-family="Liberation Sans, Arial, sans-serif"'
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#000" stroke-width="2"/>')
a('<path d="M8 8 L360 8 L360 78 L336 102 L8 102" fill="#fff" stroke="#000" stroke-width="2"/>')
a(f'<text x="24" y="46" {SANS} font-size="25" font-weight="bold">Диаграмма компонентов</text>')
a(f'<text x="24" y="80" {SANS} font-size="25" font-weight="bold">ИС HammerLive</text>')

PS = 22
FN = 25   # component name font
FL = 18   # interface label font

def comp(x, y, w, h, name):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#000" stroke-width="2"/>')
    ix, iy = x + w - 52, y + 10
    a(f'<rect x="{ix+5}" y="{iy}" width="22" height="20" fill="#fff" stroke="#000" stroke-width="1.5"/>')
    a(f'<rect x="{ix}" y="{iy+3}" width="11" height="5" fill="#fff" stroke="#000" stroke-width="1.5"/>')
    a(f'<rect x="{ix}" y="{iy+12}" width="11" height="5" fill="#fff" stroke="#000" stroke-width="1.5"/>')
    lines = name.split('\n')
    cy = y + h / 2 - (len(lines) - 1) * 14 + 9
    for i, l in enumerate(lines):
        a(f'<text x="{x + w/2}" y="{cy + i*29}" {MONO} font-size="{FN}" text-anchor="middle">{l}</text>')

def port(cx, cy):
    a(f'<rect x="{cx-PS/2}" y="{cy-PS/2}" width="{PS}" height="{PS}" fill="#fff" stroke="#000" stroke-width="2"/>')

def poly(pts):
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    a(f'<path d="{d}" fill="none" stroke="#000" stroke-width="1.8"/>')

def label(x, y, s, anchor='middle'):
    a(f'<text x="{x}" y="{y}" {SANS} font-size="{FL}" text-anchor="{anchor}">{s}</text>')

def iface(prov, ball, req, text, lx=0, ly=-20, anchor='middle'):
    """prov: путь от порта компонента-поставщика к шарику; req: путь от гнезда к порту компонента-потребителя."""
    bx, by = ball
    nx, ny = req[0]
    dx, dy = nx - bx, ny - by
    rb, rs = 7, 13
    poly(prov + [ball])
    a(f'<circle cx="{bx}" cy="{by}" r="{rb}" fill="#fff" stroke="#000" stroke-width="1.8"/>')
    if abs(dx) >= abs(dy):
        s = 1 if dx > 0 else -1
        a(f'<path d="M{bx} {by-rs} A{rs} {rs} 0 0 {1 if s > 0 else 0} {bx} {by+rs}" fill="none" stroke="#000" stroke-width="1.8"/>')
        st = (bx + s * rs, by)
    else:
        s = 1 if dy > 0 else -1
        a(f'<path d="M{bx-rs} {by} A{rs} {rs} 0 0 {0 if s > 0 else 1} {bx+rs} {by}" fill="none" stroke="#000" stroke-width="1.8"/>')
        st = (bx, by + s * rs)
    poly([st] + req)
    label(bx + lx, by + ly, text, anchor)

CH = 92
# ---------- geometry ----------
LX, LW = 70, 330          # left column
GX, GW_ = 590, 170        # gateway
RX, RW = 950, 340         # right column
ROWS = [380, 560, 740]    # service rows (top)
GY, GH = 360, 492

# top: DB for AuctionSession, clients, cache for BidStreamer
comp(LX, 150, LW - 40, CH, 'БД сеансов')
comp(420, 150, 250, CH, 'Клиент\nучастника')
comp(690, 150, 250, CH, 'Пульт\nаукциониста')
comp(RX + 20, 150, RW - 20, CH, 'Кэш потока\nставок')
# gateway
comp(GX, GY, GW_, GH, 'API\nGateway')
# left services
left = ['AuctionSession', 'AuctioneerCapture', 'BidCapture']
right = ['BidStreamer', 'VideoStreamer', 'VideoCapture']
for i, n in enumerate(left):
    comp(LX, ROWS[i], LW, CH, n)
for i, n in enumerate(right):
    comp(RX, ROWS[i], RW, CH, n)
# bottom
BTX, BTY, BTW, BTH = LX, 1010, 330, 110
comp(BTX, BTY, BTW, BTH, 'BidTracker')
comp(LX + 20, 1230, 290, CH, 'Журнал ставок')
comp(560, 1010, 250, CH, 'Payment')
comp(560, 1230, 250, CH, 'БД платежей')
comp(RX + 20, 1010, RW - 20, CH, 'Платёжный\nпровайдер')

# ---------- clients <-> gateway (gateway provides) ----------
# explicit routes
port(560, 242); port(620, GY)
iface([(620, GY - PS/2)], (620, 305), [(620, 285), (560, 285), (560, 242 + PS/2)], 'IClientAPI', -14, 6, 'end')
port(830, 242); port(680, GY)
iface([(680, GY - PS/2)], (680, 305), [(680, 285), (830, 285), (830, 242 + PS/2)], 'IAuctioneerAPI', 14, 6, 'start')

# ---------- services <-> gateway (services provide) ----------
gl = {'AuctionSession': 'ISessionAPI', 'AuctioneerCapture': 'IAuctioneerBids', 'BidCapture': 'IBids',
      'BidStreamer': 'IBidStream', 'VideoStreamer': 'IVideoStream', 'VideoCapture': 'IVideoIngest'}
for i, n in enumerate(left):
    y = ROWS[i] + CH / 2
    port(LX + LW, y); port(GX, y)
    iface([(LX + LW + PS/2, y)], (500, y), [(GX - PS/2, y)], gl[n])
for i, n in enumerate(right):
    y = ROWS[i] + CH / 2
    port(RX, y); port(GX + GW_, y)
    iface([(RX - PS/2, y)], (850, y), [(GX + GW_ + PS/2, y)], gl[n])

# ---------- DB for AuctionSession (DB provides) ----------
x = LX + 140
port(x, 150 + CH); port(x, ROWS[0])
iface([(x, 150 + CH + PS/2)], (x, 312), [(x, ROWS[0] - PS/2)], 'ISessionDB', 18, 6, 'start')
# ---------- cache for BidStreamer ----------
x = RX + 170
port(x, 150 + CH); port(x, ROWS[0])
iface([(x, 150 + CH + PS/2)], (x, 312), [(x, ROWS[0] - PS/2)], 'IStreamCache', 18, 6, 'start')
# ---------- VideoCapture -> VideoStreamer (VideoStreamer provides IVideoFeed) ----------
x = RX + 170
port(x, ROWS[1] + CH); port(x, ROWS[2])
iface([(x, ROWS[1] + CH + PS/2)], (x, (ROWS[1] + CH + ROWS[2]) / 2), [(x, ROWS[2] - PS/2)], 'IVideoFeed', 18, 6, 'start')

# ---------- left services -> BidTracker (BidTracker provides queues) ----------
routes = [  # service, left-port y offset, margin x, turn y, BT port x, label
    ('BidCapture', 2, 52, 895, 320, 'IBidQueue'),
    ('AuctioneerCapture', 1, 38, 935, 230, 'IAuctioneerBidQueue'),
    ('AuctionSession', 0, 24, 975, 140, 'ISessionEvents'),
]
for n, ri, mx, ty, btx, txt in routes:
    y = ROWS[ri] + CH / 2
    port(LX, y); port(btx, BTY)
    # provider = BidTracker: path from BT port up to ball on horizontal segment
    ball = ((mx + btx) / 2 + 20, ty)
    iface([(btx, BTY - PS/2), (btx, ty)], ball, [(mx, ty), (mx, y), (LX - PS/2, y)], txt, 0, -16)

# ---------- BidTracker -> Журнал ставок ----------
x = LX + 165
port(x, BTY + BTH); port(x, 1230)
iface([(x, 1230 - PS/2)], (x, 1175), [(x, BTY + BTH + PS/2)], 'IBidLog', 18, 6, 'start')
# ---------- BidTracker -> Payment (Payment provides ILotResults) ----------
y = 1080
port(BTX + BTW, y); port(560, y)
iface([(560 - PS/2, y)], (500, y), [(BTX + BTW + PS/2, y)], 'ILotResults')
# ---------- BidTracker -> BidStreamer (BidStreamer provides IAcceptedBids) ----------
yb = ROWS[0] + CH / 2 + 22
yt = BTY + 26
port(BTX + BTW, yt); port(RX + RW, yb)
iface([(RX + RW + PS/2, yb), (1340, yb)], (1340, 900), [(1340, 960), (430, 960), (430, yt), (BTX + BTW + PS/2, yt)], 'IAcceptedBids', -18, 6, 'end')
# ---------- Payment -> БД платежей ----------
x = 685
port(x, 1010 + CH); port(x, 1230)
iface([(x, 1230 - PS/2)], (x, 1166), [(x, 1010 + CH + PS/2)], 'IPaymentDB', 18, 6, 'start')
# ---------- Payment -> провайдер ----------
y = 1056
port(810, y); port(RX + 20, y)
iface([(RX + 20 - PS/2, y)], (890, y), [(810 + PS/2, y)], 'IPaymentGateway')

a('</svg>')
open('component.svg', 'w', encoding='utf-8').write('\n'.join(o))
print('ok')
