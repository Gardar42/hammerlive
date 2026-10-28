"""UML-диаграмма компонентов HammerLive в стиле методички (порты + ball-and-socket), компактная раскладка."""
W, H = 1400, 790
o = []
a = o.append
MONO = 'font-family="Liberation Mono, Consolas, monospace"'
SANS = 'font-family="Liberation Sans, Arial, sans-serif"'
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="#000" stroke-width="2"/>')
a('<path d="M8 8 L580 8 L580 78 L556 102 L8 102" fill="#fff" stroke="#000" stroke-width="2"/>')
a(f'<text x="24" y="46" {SANS} font-size="25" font-weight="bold">Диаграмма компонентов ИС HammerLive</text>')
a(f'<text x="24" y="80" {SANS} font-size="25" font-weight="bold">изменения версии 1.1 (фрагмент)</text>')

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


CH = 96
comp(70, 170, 260, CH, 'API Gateway')
comp(520, 170, 300, CH, 'BidCapture\n«изменён»')
comp(1000, 170, 360, CH, 'Identity\n«изменён»')
# BidTracker: стопка экземпляров (шарды)
a('<rect x="536" y="416" width="300" height="110" fill="#fff" stroke="#000" stroke-width="2"/>')
a('<rect x="528" y="408" width="300" height="110" fill="#fff" stroke="#000" stroke-width="2"/>')
comp(520, 400, 300, 110, 'BidTracker\n[шард по lotId]')
comp(1000, 400, 360, CH, 'Notification\n«изменён»')
comp(1000, 620, 360, CH, 'TelegramAdapter\n«новый»')
comp(520, 620, 300, CH, 'Telegram\nBot API')
# 1 Gateway -> BidCapture
y=218; port(330,y); port(520,y)
iface([(520-PS/2,y)], (425,y), [(330+PS/2,y)], 'IBids, IAbsenteeBids', 0, -22)
# 2 Gateway -> Identity (step-up)
port(200,170); port(1150,170)
iface([(1150,170-PS/2),(1150,130)], (900,130), [(200,130),(200,170-PS/2)], 'IStepUp', 0, -18)
# 3 BidCapture -> Identity (verify)
port(820,y); port(1000,y)
iface([(1000-PS/2,y)], (910,y), [(820+PS/2,y)], 'IStepUpVerify', 0, -22)
# 4 BidCapture -> BidTracker queue
port(670,266); port(670,400)
iface([(670,400-PS/2)], (670,333), [(670,266+PS/2)], 'IBidQueue (маршрут по lotId)', 20, 6, 'start')
# 5 BidTracker -> Notification
y2=448; port(820,y2); port(1000,y2)
iface([(1000-PS/2,y2)], (910,y2), [(820+PS/2,y2)], 'ILotEvents', 0, -22)
# 6 Notification -> TelegramAdapter
port(1150,496); port(1150,620)
iface([(1150,620-PS/2)], (1150,558), [(1150,496+PS/2)], 'INotificationChannel', 20, 6, 'start')
# 7 TelegramAdapter -> Telegram Bot API
y3=668; port(1000,y3); port(820,y3)
iface([(820+PS/2,y3)], (910,y3), [(1000-PS/2,y3)], 'ITelegramBotAPI', 0, -22)
a('</svg>')
open('component_v1_1.svg','w',encoding='utf-8').write('\n'.join(o))
