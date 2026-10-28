"""Логическая ER-модель HammerLive по базам сервисов (SVG, нотация «вороньей лапки»)."""
W, H = 1720, 1700
o = []
a = o.append
SANS = 'font-family="Liberation Sans, Arial, sans-serif"'
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10" fill="none" stroke="#333" stroke-width="1.6"/></marker></defs>')

RH, TW, NW = 30, 140, 205  # row height, type col, name col
FS = 17
T = {}  # table name -> (x, y, rows)

def text(x, y, s, size=FS, bold=False, italic=False, anchor='start', fill='#000'):
    st = (' font-weight="bold"' if bold else '') + (' font-style="italic"' if italic else '')
    a(f'<text x="{x}" y="{y}" {SANS} font-size="{size}"{st} text-anchor="{anchor}" fill="{fill}">{s}</text>')

def table(name, x, y, rows, kv=None):
    w = TW + NW
    n = len(rows) + 1 + (1 if kv else 0)
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" fill="#e3e3e3" stroke="#000" stroke-width="1.6"/>')
    text(x + w / 2, y + 21, name, FS, True, anchor='middle')
    yy = y + RH
    if kv:
        a(f'<rect x="{x}" y="{yy}" width="{w}" height="{RH}" fill="#fff" stroke="#000" stroke-width="1.4"/>')
        text(x + 8, yy + 21, f'тип: {kv}', FS, italic=True)
        yy += RH
    for col, typ, k in rows:
        a(f'<rect x="{x}" y="{yy}" width="{TW}" height="{RH}" fill="#fff" stroke="#000" stroke-width="1.4"/>')
        a(f'<rect x="{x+TW}" y="{yy}" width="{NW}" height="{RH}" fill="#fff" stroke="#000" stroke-width="1.4"/>')
        if k == 'PK':
            text(x + 8, yy + 21, typ, FS, True)
            a(f'<text x="{x+TW+8}" y="{yy+21}" {SANS} font-size="{FS}" font-weight="bold" text-decoration="underline">{col}</text>')
        else:
            text(x + 8, yy + 21, typ, FS)
            if k == 'REF':
                text(x + TW + 8, yy + 21, col + ' (ID)', FS, italic=True)
            elif k == 'FK':
                text(x + TW + 8, yy + 21, col + ' (FK)', FS)
            else:
                text(x + TW + 8, yy + 21, col, FS)
        yy += RH
    T[name] = (x, y, [r[0] for r in rows], 1 if kv else 0)
    return yy

def row_y(name, col):
    x, y, cols, off = T[name]
    return y + RH * (1 + off + cols.index(col)) + RH / 2

def cluster(x, y, w, h, title, sub):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="#000" stroke-width="2" stroke-dasharray="9 6"/>')
    text(x + 14, y + 26, title, 19, True)
    text(x + 14, y + 48, sub, 16, italic=True)

def one(x, y, d):      # || mark at end (x,y), d = +1 line goes right from point, -1 left
    for k in (10, 16):
        a(f'<line x1="{x+d*k}" y1="{y-9}" x2="{x+d*k}" y2="{y+9}" stroke="#000" stroke-width="1.8"/>')

def many(x, y, d, mandatory=False):  # crow's foot touching table at x; d = direction away from table
    a(f'<line x1="{x}" y1="{y-9}" x2="{x+d*14}" y2="{y}" stroke="#000" stroke-width="1.8"/>')
    a(f'<line x1="{x}" y1="{y+9}" x2="{x+d*14}" y2="{y}" stroke="#000" stroke-width="1.8"/>')
    if mandatory:
        a(f'<line x1="{x+d*20}" y1="{y-9}" x2="{x+d*20}" y2="{y+9}" stroke="#000" stroke-width="1.8"/>')
    else:
        a(f'<circle cx="{x+d*25}" cy="{y}" r="6" fill="#fff" stroke="#000" stroke-width="1.8"/>')

def rel(p, pcol, c, ccol, mid_x, mandatory=False):
    """1:N связь от PK (правый край родителя) к FK (левый край потомка)."""
    px = T[p][0] + TW + NW; py = row_y(p, pcol)
    cx = T[c][0]; cy = row_y(c, ccol)
    if cx < px:   # потомок левее – идём от левого края родителя к правому краю потомка
        px = T[p][0]; cx = T[c][0] + TW + NW
        a(f'<path d="M{px} {py} L{mid_x} {py} L{mid_x} {cy} L{cx} {cy}" fill="none" stroke="#000" stroke-width="1.8"/>')
        one(px, py, -1); many(cx, cy, 1, mandatory)
    else:
        a(f'<path d="M{px} {py} L{mid_x} {py} L{mid_x} {cy} L{cx} {cy}" fill="none" stroke="#000" stroke-width="1.8"/>')
        one(px, py, 1); many(cx, cy, -1, mandatory)

def ref(pts, label, lx, ly, anchor='start'):
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    a(f'<path d="{d}" fill="none" stroke="#333" stroke-width="1.8" stroke-dasharray="8 6" marker-end="url(#ah)"/>')
    text(lx, ly, label, 15, italic=True, anchor=anchor, fill='#222')

TWW = TW + NW  # 345
# ================= row 1 =================
cluster(20, 20, 400, 345, 'Identity (вспомогательный)', 'PostgreSQL')
table('users', 47, 80, [('user_id','bigint','PK'),('email','varchar(255)',''),('phone','varchar(20)',''),('password_hash','varchar(255)',''),('full_name','varchar(150)',''),('role','varchar(20)',''),('status','varchar(20)','')])

cluster(445, 20, 1255, 465, 'AuctionSession – БД сеансов', 'PostgreSQL')
table('auctions', 470, 80, [('auction_id','bigint','PK'),('organizer_id','bigint','REF'),('title','varchar(200)',''),('starts_at','timestamptz',''),('deposit','numeric(12,2)',''),('status','varchar(20)','')])
table('categories', 470, 345, [('category_id','integer','PK'),('name','varchar(100)','')])
table('lots', 895, 80, [('lot_id','bigint','PK'),('auction_id','bigint','FK'),('category_id','integer','FK'),('seller_id','bigint','REF'),('title','varchar(200)',''),('start_price','numeric(12,2)',''),('bid_step','numeric(12,2)',''),('status','varchar(20)','')])
table('registrations', 1325, 80, [('registration_id','bigint','PK'),('auction_id','bigint','FK'),('user_id','bigint','REF'),('hold_id','varchar(64)',''),('status','varchar(20)','')])
rel('auctions', 'auction_id', 'lots', 'auction_id', 852, True)
rel('categories', 'category_id', 'lots', 'category_id', 870)
# auctions -> registrations: route above lots
px = 470 + TWW; py = row_y('auctions', 'auction_id')
cy = row_y('registrations', 'auction_id')
a(f'<path d="M{px} {py} L835 {py} L835 66 L1290 66 L1290 {cy} L1325 {cy}" fill="none" stroke="#000" stroke-width="1.8"/>')
one(px, py, 1); many(1325, cy, -1)

# ================= row 2 =================
R2 = 545
cluster(20, R2, 1210, 580, 'BidTracker – Журнал ставок (v1.1)', 'PostgreSQL')
table('lot_rules', 47, R2 + 60, [('lot_id','bigint','PK'),('auction_id','bigint',''),('start_price','numeric(12,2)',''),('bid_step','numeric(12,2)',''),('closes_at','timestamptz',''),('status','varchar(20)','')])
table('participants', 47, R2 + 320, [('auction_id','bigint','PK'),('user_id','bigint','PK'),('participant_no','integer',''),('bid_limit','numeric(12,2)','')])
table('bids', 455, R2 + 60, [('bid_id','bigint','PK'),('lot_id','bigint','FK'),('user_id','bigint','REF'),('source','varchar(10)',''),('amount','numeric(12,2)',''),('server_ts','timestamptz(6)',''),('status','varchar(20)','')])
table('auto_bids', 863, R2 + 60, [('auto_bid_id','bigint','PK'),('lot_id','bigint','FK'),('user_id','bigint','REF'),('max_amount','numeric(12,2)',''),('active','boolean','')])
rel('lot_rules', 'lot_id', 'bids', 'lot_id', 425)
# lot_rules -> auto_bids: route below bids
px = 47 + TWW; py = row_y('lot_rules', 'lot_id'); cy = row_y('auto_bids', 'lot_id')
a(f'<path d="M{px} {py} L410 {py} L410 {R2+330} L835 {R2+330} L835 {cy} L863 {cy}" fill="none" stroke="#000" stroke-width="1.8"/>')
one(px, py, 1); many(863, cy, -1)
table('absentee_bids', 863, R2 + 345, [('absentee_bid_id','bigint','PK'),('lot_id','bigint','FK'),('user_id','bigint','REF'),('max_amount','numeric(12,2)',''),('status','varchar(20)','')])
cy2 = row_y('absentee_bids', 'lot_id')
a(f'<path d="M835 {R2+330} L835 {cy2} L863 {cy2}" fill="none" stroke="#000" stroke-width="1.8"/>')
many(863, cy2, -1)

cluster(1255, R2, 445, 580, 'BidStreamer – Кэш потока', 'Redis (ключ-значение)')
table('lot:{id}:state', 1305, R2 + 60, [('current_price','decimal',''),('leader_no','int',''),('bids_count','int',''),('closes_at','timestamp',''),('version','int','')], kv='HASH')
table('lot:{id}:last_bids', 1305, R2 + 320, [('amount','decimal',''),('participant_no','int',''),('ts','timestamp','')], kv='LIST')

# ================= row 3 =================
R3 = 1185
cluster(20, R3, 400, 300, 'Reputation (вспомогательный)', 'PostgreSQL')
table('reviews', 47, R3 + 60, [('review_id','bigint','PK'),('lot_id','bigint','REF'),('author_id','bigint','REF'),('target_id','bigint','REF'),('rating','smallint',''),('text','text','')])
cluster(445, R3, 820, 420, 'Payment – БД платежей', 'PostgreSQL')
cluster(1290, R3, 410, 300, 'Notification (v1.1)', 'PostgreSQL')
table('notification_channels', 1322, R3 + 60, [('channel_id','bigint','PK'),('user_id','bigint','REF'),('type','varchar(20)',''),('external_id','varchar(64)',''),('enabled','boolean','')])
table('lot_results', 470, R3 + 60, [('lot_id','bigint','PK'),('winner_id','bigint','REF'),('winning_bid_id','bigint','REF'),('final_price','numeric(12,2)','')])
table('payment_methods', 470, R3 + 250, [('card_id','bigint','PK'),('user_id','bigint','REF'),('provider_token','varchar(128)',''),('card_mask','varchar(19)','')])
table('payments', 895, R3 + 60, [('payment_id','bigint','PK'),('lot_id','bigint','FK'),('card_id','bigint','FK'),('amount','numeric(12,2)',''),('commission','numeric(12,2)',''),('status','varchar(20)',''),('provider_txn_id','varchar(64)','')])
rel('lot_results', 'lot_id', 'payments', 'lot_id', 855)
rel('payment_methods', 'card_id', 'payments', 'card_id', 870)

# ================= cross-service references =================
ref([(300, R2), (300, 500), (690, 500), (690, 487)], 'lot_id, auction_id: копия правил лота', 312, 528)
ref([(1255, R2 + 200), (1232, R2 + 200)], '', 0, 0)
text(1243, R2 + 178, 'lot_id', 15, italic=True, anchor='middle', fill='#222')
ref([(640, R3), (640, R2 + 582)], 'winning_bid_id', 652, R3 - 22)
ref([(420, R3 + 200), (443, R3 + 200)], '', 0, 0)
text(432, R3 + 178, 'lot_id', 15, italic=True, anchor='middle', fill='#222')

# ================= legend =================
LY = 1650
a(f'<line x1="30" y1="{LY-6}" x2="90" y2="{LY-6}" stroke="#000" stroke-width="1.8"/>')
one(30, LY - 6, 1); many(90, LY - 6, -1)
text(105, LY, '1 : N внутри базы сервиса (FK)', 16)
a(f'<path d="M430 {LY-6} L490 {LY-6}" stroke="#333" stroke-width="1.8" stroke-dasharray="8 6" marker-end="url(#ah)"/>')
text(505, LY, 'ссылка на данные другого сервиса (без FK)', 16)
text(30, LY + 28, '(ID) – идентификатор записи другого сервиса; user_id, organizer_id, seller_id, winner_id, author_id, target_id ссылаются на users (Identity)', 15, italic=True)

a('</svg>')
open('logical.svg', 'w', encoding='utf-8').write('\n'.join(o))
print('ok')
