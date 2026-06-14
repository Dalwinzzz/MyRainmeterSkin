# 把 Dock.ini 的纹章 Shape Path 转成 SVG, 渲染验证 CurveTo 修正后的形状。
# Rainmeter Path 语法 -> SVG path:
#   起点 "x,y"               -> M x y
#   LineTo x,y               -> L x y
#   CurveTo ex,ey, c1x,c1y, c2x,c2y  -> C c1x c1y c2x c2y ex ey  (注意换序!)
#   MoveTo x,y               -> M x y
#   ClosePath                -> Z
#   Ellipse cx,cy,r          -> 单独 circle
import re, sys

dock = open(sys.argv[1], encoding='utf-8').read()

def parse_path(defn):
    # defn 形如: "22,17 | LineTo .. | CurveTo ex,ey, c1.., c2.. | ClosePath"
    parts = [p.strip() for p in defn.split('|')]
    d = []
    # 起点
    m = re.match(r'^([\d.]+),([\d.]+)$', parts[0])
    if m: d.append(f"M {m.group(1)} {m.group(2)}")
    for seg in parts[1:]:
        if seg.startswith('LineTo'):
            nums = re.findall(r'[-\d.]+', seg)
            d.append(f"L {nums[0]} {nums[1]}")
        elif seg.startswith('MoveTo'):
            nums = re.findall(r'[-\d.]+', seg)
            d.append(f"M {nums[0]} {nums[1]}")
        elif seg.startswith('CurveTo'):
            nums = re.findall(r'[-\d.]+', seg)
            # Rainmeter: ex,ey, c1x,c1y, c2x,c2y -> SVG C c1 c2 e
            ex,ey,c1x,c1y,c2x,c2y = nums[:6]
            d.append(f"C {c1x} {c1y} {c2x} {c2y} {ex} {ey}")
        elif seg.startswith('ClosePath'):
            d.append("Z")
    return " ".join(d)

# 抽取每个 crest 的 mtrCxMk 段里的 Shape 定义
crests = {}
cur = None
for line in dock.splitlines():
    mk = re.match(r'\[mtrC(\d)Mk\]', line)
    if mk: cur = mk.group(1); crests[cur] = {'paths':[], 'ellipses':[]}
    elif re.match(r'\[mtr', line): 
        if not re.match(r'\[mtrC\dMk\]', line): cur = None
    if cur:
        # Path 定义行: "Name=startpt | ..."
        pm = re.match(r'^([A-Za-z0-9]+)=([\d.]+,[\d.]+ \|.*)', line)
        if pm and 'Ellipse' not in line and not pm.group(2).startswith('Path '):
            crests[cur]['paths'].append(parse_path(pm.group(2)))
        # 内联 Ellipse (Shape=Ellipse cx,cy,r ...)
        for em in re.finditer(r'Ellipse ([\d.]+),([\d.]+),([\d.]+)', line):
            crests[cur]['ellipses'].append(em.groups())

names = {'1':'UNDERTAKER','2':'BLACK DOG','3':'GUN SNAKE','4':'LAUGHING FOX','5':'SNOW WITCH'}
cells = []
for k in sorted(crests):
    paths = "".join(f'<path d="{p}" fill="none" stroke="#dbe9fb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' for p in crests[k]['paths'])
    ells  = "".join(f'<circle cx="{e[0]}" cy="{e[1]}" r="{e[2]}" fill="none" stroke="#dbe9fb" stroke-width="1.5"/>' for e in crests[k]['ellipses'])
    cells.append(f'''<div class="cell"><div class="ring"><svg viewBox="0 0 48 48">{paths}{ells}</svg></div><div class="lbl">{names[k]}</div></div>''')

html = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#0d1a2c;display:flex;gap:24px;padding:40px;justify-content:center;align-items:center;flex-wrap:wrap}}
.cell{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.ring{{width:90px;height:90px;border-radius:50%;border:1px solid rgba(140,185,235,.4);display:flex;align-items:center;justify-content:center}}
svg{{width:64px;height:64px}}
.lbl{{font:8px sans-serif;letter-spacing:2px;color:#8da6c4}}
h1{{width:100%;color:#6fa8e0;font:12px sans-serif;letter-spacing:3px;text-align:center}}
</style></head><body>
<h1>Dock.ini 纹章 Shape → SVG 验证 (CurveTo 修正后实际形状)</h1>
''' + "".join(cells) + "</body></html>"
open(sys.argv[2],'w',encoding='utf-8').write(html)
print(f"crests parsed: {sorted(crests.keys())}")
for k in sorted(crests): print(f"  C{k}: {len(crests[k]['paths'])} paths, {len(crests[k]['ellipses'])} ellipses")
