# 把 Rail/Clock/Dock 三个 ini 的 String meter 按实际 X/Y 坐标拼成 HTML 绝对定位,
# 渲染成 1920×1080 整屏, 对比 v5 预览的整体布局/比例是否还原。
# 只渲染 String meter(文本)的位置, 忽略 shape 细节(纹章已单独验证)。
import re, sys

def parse_ini(path):
    secs = {}
    cur = None
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'^\[([^\]]+)\]', line)
        if m:
            cur = m.group(1); secs[cur] = {}
            continue
        if cur is None: continue
        kv = re.match(r'^([A-Za-z0-9]+)=(.*)$', line)
        if kv:
            secs[cur][kv.group(1)] = kv.group(2)
    return secs

def style_lookup(secs, name):
    # 返回某 style/section 的 FontSize / FontColor / StringAlign (含 MeterStyle 继承)
    s = secs.get(name, {})
    base = {}
    if 'MeterStyle' in s:
        base = style_lookup(secs, s['MeterStyle'])
    for k in ('FontSize','FontColor','StringAlign','StringStyle'):
        if k in s: base[k] = s[k]
    return base

def rgba(c):
    if not c: return '#dbe9fb'
    parts = c.split(',')
    if len(parts) >= 3:
        a = 1
        if len(parts) >= 4:
            try: a = int(parts[3])/255
            except: a = 1
        return f"rgba({parts[0]},{parts[1]},{parts[2]},{a})"
    return '#dbe9fb'

def emit(secs, originX, originY, scale=1):
    els = []
    last_x = originX
    for name, s in secs.items():
        if s.get('Meter') != 'String': continue
        txt = s.get('Text','')
        # 动态 %1/%2 用示例值替换, 让主视觉可见
        sample = {
          'mTimeHM':'15:00','mSec':'26','mWeek':'24','mWeekday':'星期日',
          'mDateEN':'SUN · JUN 15 2026','mDoY':'166','mCpu':'34','mMem':'62',
          'mDsk':'91','mGpuTemp':'54','mNetIn':'2.4','mNetOut':'340',
          'mTimeMonU':'JUN','mTimeYear':'2026','mTimeMonCN':'六月','mMonNum':'06',
          'mTitle':'3-pun 29-byou','mArtist':'SawanoHiroyuki[nZk]','mYearProg':'45.2'
        }
        v1 = sample.get(s.get('MeasureName',''), '·')
        v2 = sample.get(s.get('MeasureName2',''), '·')
        txt_disp = txt.replace('%1',v1).replace('%2',v2)
        if not txt_disp.strip(): txt_disp = '·'
        st = style_lookup(secs, name)
        fs = st.get('FontSize','9')
        try: fs = float(fs)
        except: fs = 9
        col = rgba(st.get('FontColor'))
        align = st.get('StringAlign','Left')
        x = s.get('X','0'); y = s.get('Y','0')
        # X=R → 接上一个(近似: +40)
        if x.strip()=='R': x = str(last_x + 30)
        # 去掉表达式/变量
        try: xv = float(re.sub(r'[^0-9.\-]','', x.split('(')[0]) or 0)
        except: xv = 0
        try: yv = float(re.sub(r'[^0-9.\-]','', y.split('(')[0]) or 0)
        except: yv = 0
        last_x = xv
        ta = 'left'
        tx = originX + xv*scale
        if 'Center' in align: ta='center'
        if 'Right' in align: ta='right'
        bold = 'font-weight:700;' if 'Bold' in st.get('StringStyle','') else ''
        upper = 'text-transform:uppercase;' if False else ''
        els.append(f'<div style="position:absolute;left:{tx}px;top:{originY+yv*scale}px;font-size:{fs*scale}px;color:{col};{bold}white-space:nowrap;{ "transform:translateX(-50%);" if ta=="center" else ("transform:translateX(-100%);" if ta=="right" else "") }">{txt_disp}</div>')
    return els

base = "/Users/dalwin/Library/CodeRepo/MyRainmeterSkin/EightSix86"
rail = parse_ini(base+"/Rail/Rail.ini")
clock = parse_ini(base+"/Clock/Clock.ini")
dock = parse_ini(base+"/Dock/Dock.ini")

# 部署锚点 (按 install.md 1920x1080)
els = []
# Rail 背景框
els.append('<div style="position:absolute;left:0;top:0;width:312px;height:1080px;background:linear-gradient(100deg,rgba(10,20,34,.5),rgba(10,20,34,.2));border-right:1px solid rgba(140,185,235,.3)"></div>')
els += emit(rail, 0, 0)
els += emit(clock, 816, 340)
els += emit(dock, 736, 930)
# Clock 大字框示意
els.append('<div style="position:absolute;left:816px;top:340px;width:600px;height:380px;border:1px dashed rgba(120,180,240,.15)"></div>')

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{{margin:0;width:1920px;height:1080px;position:relative;overflow:hidden;
background:radial-gradient(110% 90% at 72% 22%,rgba(120,170,230,.2),transparent 46%),linear-gradient(158deg,#0a1322,#0f1e34 42%,#14233b 72%,#0b1626);
font-family:'Oxanium','Chakra Petch',sans-serif}}
</style></head><body>{"".join(els)}
<div style="position:absolute;right:12px;top:8px;color:#6fa8e0;font-size:11px;letter-spacing:2px">INI 坐标 1:1 布局验证 (文本位置, 1920×1080)</div>
</body></html>'''
open(sys.argv[1],'w',encoding='utf-8').write(html)
print("layout html written; rail/clock/dock string meters emitted")
