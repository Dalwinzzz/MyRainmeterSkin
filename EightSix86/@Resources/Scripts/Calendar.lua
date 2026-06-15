-- ============================================================
--  86 HUD · Calendar.lua
--  动态生成当月月历网格 meters (7列 × 6行), 含:
--    · 上/下月日期置灰 (dim)
--    · 今日猩红切角高亮 (today)
--  由 Rail.ini 的 [mCalScript] 调用。Update() 每天刷新一次即可。
--
--  网格几何 (与 Rail.ini 对齐):
--    起点 colX0 = 33, 列步进 colStep = 39  (7列: 33,72,111,150,189,228,267)
--    起点 rowY0 = 490, 行步进 rowStep = 22 (6行)
--  生成的 meter 名: CalD1 .. CalD42  (Rail.ini 需预置同名空 meter, 或用
--    !SetOption 动态写入。本脚本用 !SetOption 写已存在的占位 meter。)
-- ============================================================

function Initialize()
  colX0   = 33
  colStep = 39
  rowY0   = 490
  rowStep = 22
end

function Update()
  local now   = os.date('*t')
  local year  = now.year
  local month = now.month
  local today = now.day

  -- 当月1号是星期几 (0=日 .. 6=六)
  local first = os.date('*t', os.time{year=year, month=month, day=1})
  local startDow = first.wday - 1   -- lua wday: 1=日 → 0-based

  -- 当月天数
  local daysInMonth = os.date('*t', os.time{year=year, month=month+1, day=0}).day
  -- 上月天数 (用于前置置灰)
  local prevDays = os.date('*t', os.time{year=year, month=month, day=0}).day

  for i = 0, 41 do
    local col = i % 7
    local row = math.floor(i / 7)
    local x = colX0 + col * colStep
    local y = rowY0 + row * rowStep

    local dayNum, style, hidden
    if i < startDow then
      -- 上月尾
      dayNum = prevDays - (startDow - 1 - i)
      style  = 'stCalDayDim'
      hidden = 0
    elseif i < startDow + daysInMonth then
      -- 本月
      dayNum = i - startDow + 1
      if dayNum == today then
        style = 'stCalToday'
      else
        style = 'stCalDay'
      end
      hidden = 0
    else
      -- 下月头
      dayNum = i - (startDow + daysInMonth) + 1
      style  = 'stCalDayDim'
      hidden = 0
    end

    local meter = 'CalD' .. (i + 1)
    SKIN:Bang('!SetOption', meter, 'Text', tostring(dayNum))
    SKIN:Bang('!SetOption', meter, 'MeterStyle', style)
    SKIN:Bang('!SetOption', meter, 'X', tostring(x))
    SKIN:Bang('!SetOption', meter, 'Y', tostring(y))
    SKIN:Bang('!SetOption', meter, 'Hidden', tostring(hidden))

    -- 今日: 显示猩红切角底块 (CalTodayBg), 定位到今日格
    if style == 'stCalToday' then
      SKIN:Bang('!SetOption', 'CalTodayBg', 'X', tostring(x - 11))
      SKIN:Bang('!SetOption', 'CalTodayBg', 'Y', tostring(y - 1))
      SKIN:Bang('!SetOption', 'CalTodayBg', 'Hidden', '0')
    end
  end

  SKIN:Bang('!UpdateMeterGroup', 'calgrid')
  SKIN:Bang('!Redraw')
  return today
end
