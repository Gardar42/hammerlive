"""Концептуальная ER-модель (нотация Чена) с областями сервисов."""
W, H = 1720, 1150
o = []
a = o.append
SANS = 'font-family="Liberation Sans, Arial, sans-serif"'
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')

def text(x, y, s, size=19, bold=False, italic=False, anchor='middle', deco=''):
    st = (' font-weight="bold"' if bold else '') + (' font-style="italic"' if italic else '') + (f' text-decoration="{deco}"' if deco else '')
    a(f'<text x="{x}" y="{y}" {SANS} font-size="{size}"{st} text-anchor="{anchor}">{s}</text>')

def area(x, y, w, h, title):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#f7f7f7" stroke="#000" stroke-width="2" stroke-dasharray="10 6"/>')
    text(x + 14, y + 28, title, 18, True, italic=True, anchor='start')

LINES = []
SHAPES = []
CARD = []
def line(p, q, card=None, t=0.22):
    LINES.append((p, q))
    if card:
        import math
        dx, dy = p[0] - q[0], p[1] - q[1]
        L_ = math.hypot(dx, dy); ux, uy = dx / L_, dy / L_
        te = min(82 / abs(ux) if ux else 1e9, 28 / abs(uy) if uy else 1e9)
        d = te + 16
        x = q[0] + ux * d; y = q[1] + uy * d
        # смещение перпендикулярно линии, чтобы не лежать на ней
        x += -uy * 13; y += ux * 13
        CARD.append((x, y, card))

def entity(c, name):
    SHAPES.append(('e', c, name))
def rel(c, name):
    SHAPES.append(('r', c, name))
def attr(c, name, key=False, owner=None):
    SHAPES.append(('a', c, name, key))
    if owner:
        line(owner, c)

# ---------------- areas ----------------
area(30, 360, 400, 330, 'Identity')
area(520, 30, 1170, 310, 'AuctionSession')
area(1110, 420, 580, 330, 'BidTracker')
area(520, 810, 560, 310, 'Payment')
area(30, 810, 400, 310, 'Reputation')

# ---------------- entities ----------------
U = (230, 545); A = (770, 195); L = (1390, 195); B = (1400, 590); P = (985, 965); C = (615, 965); R = (230, 965)
# entities
for c_, n_ in [(U,'Пользователь'),(A,'Аукцион'),(L,'Лот'),(B,'Ставка'),(P,'Платёж'),(C,'Карта'),(R,'Отзыв')]:
    entity(c_, n_)
# attributes
attr((95, 445), 'UserID', True, U); attr((232, 430), 'Роль', False, U); attr((105, 640), 'ФИО', False, U)
attr((660, 95), 'AuctionID', True, A); attr((890, 95), 'Дата начала', False, A)
attr((1270, 95), 'LotID', True, L); attr((1520, 95), 'Стартовая цена', False, L); attr((1575, 265), 'Шаг ставки', False, L)
attr((1255, 495), 'BidID', True, B); attr((1560, 495), 'Сумма', False, B); attr((1560, 690), 'Время', False, B); attr((1255, 690), 'Источник', False, B)
attr((985, 1075), 'Статус', False, P); attr((985, 860), 'PaymentID', True, P)
attr((615, 1075), 'Маска карты', False, C)
attr((115, 1075), 'ReviewID', True, R); attr((345, 1075), 'Оценка', False, R)

# ---------------- relationships ----------------
def link(e1, r, e2, c1, c2):
    line(r, e1, c1); line(r, e2, c2)

r = (440, 255);  rel(r, 'Организует');   link(U, r, A, '1', 'N')
r = (650, 430);  rel(r, 'Участвует в');  link(U, r, A, 'M', 'N')
r = (1080, 195); rel(r, 'Содержит');     link(A, r, L, '1', 'N')
r = (820, 600);  rel(r, 'Делает');       link(U, r, B, '1', 'N')
r = (1390, 380); rel(r, 'Получает');     link(L, r, B, '1', 'N')
r = (1240, 965); rel(r, 'Оплачивает');   link(B, r, P, '1', '1')
r = (800, 965);  rel(r, 'Списывается\nс'); link(C, r, P, '1', 'N')
r = (470, 760);  rel(r, 'Привязывает');  link(U, r, C, '1', 'N')
r = (230, 750);  rel(r, 'Оставляет');    link(U, r, R, '1', 'N')

for p, q in LINES:
    a(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="#000" stroke-width="1.8"/>')
for s in SHAPES:
    if s[0] == 'e':
        _, (x, y), n = s
        a(f'<rect x="{x-82}" y="{y-28}" width="164" height="56" fill="#fff" stroke="#000" stroke-width="2.2"/>')
        text(x, y + 7, n, 21, True)
    elif s[0] == 'r':
        _, (x, y), n = s
        w, h = 82, 40
        a(f'<polygon points="{x-w},{y} {x},{y-h} {x+w},{y} {x},{y+h}" fill="#fff" stroke="#000" stroke-width="2"/>')
        ls = n.split('\n')
        for i, l in enumerate(ls):
            text(x, y + 6 - (len(ls) - 1) * 10 + i * 20, l, 16)
    else:
        _, (x, y), n, key = s
        rx = max(58, len(n) * 6.3 + 18)
        a(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="23" fill="#fff" stroke="#000" stroke-width="1.6"/>')
        text(x, y + 6, n, 16, deco='underline' if key else '')
for x, y, c in CARD:
    text(x, y + 5, c, 17, True)

a('</svg>')
open('concept.svg', 'w', encoding='utf-8').write('\n'.join(o))
print('ok')
