-- ============================================================
--  86 HUD · System Roster driver
--  Maps each metric (CPU / MEM / DSK / NET) into 86-style HUD
--  symbols: 5-phase moon glyph (PWR), trend arrow (RATE),
--  threshold status color (STA), and the signature DESTROYED
--  stamp when the network feed flatlines.
--
--  Wired from System.ini:
--    [mScript] Measure=Script  ScriptFile=#@#Scripts\Roster.lua
--    Update() runs once per skin update; it reads the live
--    measures by name and pushes !SetOption bangs back.
-- ============================================================

-- 5-phase moon, empty -> full. Matches the POWER column in the
-- 86 system_status reference frame (half / quarter filled discs).
local MOON = { '○', '◔', '◑', '◕', '●' }

-- Per-row config: measure name, the meter prefix in System.ini,
-- alert threshold (% above which STA flips red), and whether a
-- "flatline -> DESTROYED" rule applies (network rows only).
local ROWS = {
  { meas = 'mCpu', id = 'R1', alert = 90, flat = false },
  { meas = 'mMem', id = 'R2', alert = 90, flat = false },
  { meas = 'mDsk', id = 'R3', alert = 85, flat = false },
  { meas = 'mNetIn', id = 'R4', alert = 200, flat = true },
  { meas = 'mNetOut', id = 'R5', alert = 200, flat = true },
}

-- Remembered values for trend (RATE) diffing across updates.
local prev = {}
-- Consecutive-update counters for the flatline DESTROYED rule.
local flatCount = {}
-- Last DESTROYED state per row, so we only fire Show/Hide bangs on a
-- real transition — otherwise the per-second Update would fight the
-- startup scan reveal and re-show rows mid-animation.
local wasDestroyed = {}

-- Colors are read from the skin variables so the Lua stays in sync
-- with Variables.inc (red lycoris / cobalt blue palette).
local C_BLUE, C_BLUEDIM, C_RED, C_TEXTDIM

function Initialize()
  C_BLUE = SKIN:GetVariable('ColorCyanEdge', '30,90,200,242')
  C_BLUEDIM = SKIN:GetVariable('ColorCyanDim', '30,90,200,150')
  C_RED = SKIN:GetVariable('ColorRed', '200,30,58,255')
  C_TEXTDIM = SKIN:GetVariable('ColorTextDim', '184,192,204,242')
  for _, r in ipairs(ROWS) do
    prev[r.id] = -1
    flatCount[r.id] = 0
    wasDestroyed[r.id] = false
  end
end

-- Map a 0..100 percentage onto one of the 5 moon phases.
local function moonFor(pct)
  local idx = math.floor(pct / 20) + 1
  if idx < 1 then idx = 1 elseif idx > 5 then idx = 5 end
  return MOON[idx]
end

function Update()
  for _, r in ipairs(ROWS) do
    local m = SKIN:GetMeasure(r.meas)
    if m then
      local val = m:GetValue()        -- numeric (CPU/MEM/DSK = %, NET = bytes/s)
      local pct = val
      if r.flat then
        -- Network rows: value is bytes/s; derive a coarse 0..100 for the
        -- moon using a 1MB/s soft ceiling so the disc reacts to traffic.
        pct = math.min(val / 10485.76, 100)
      end

      -- ---- PWR: moon phase ----
      SKIN:Bang('!SetOption', 'mtr' .. r.id .. 'Pwr', 'Text', moonFor(pct))

      -- ---- RATE: trend arrow vs previous update ----
      local arrow, rateColor = '──', C_TEXTDIM
      local p = prev[r.id]
      if p >= 0 then
        local delta = val - p
        local thr = r.flat and 1024 or 1.0   -- ignore micro-jitter
        if delta > thr then
          arrow, rateColor = '▲', C_BLUE
        elseif delta < -thr then
          arrow, rateColor = '▼', C_BLUEDIM
        end
      end
      prev[r.id] = val
      SKIN:Bang('!SetOption', 'mtr' .. r.id .. 'Rate', 'Text', arrow)
      SKIN:Bang('!SetOption', 'mtr' .. r.id .. 'Rate', 'FontColor', rateColor)

      -- ---- STA: threshold status color ----
      local alerted = false
      local staColor = C_BLUE
      if r.flat then
        -- Flatline detection: ~0 traffic for N consecutive updates -> DESTROYED.
        if val < 64 then
          flatCount[r.id] = flatCount[r.id] + 1
        else
          flatCount[r.id] = 0
        end
        if flatCount[r.id] >= 30 then
          alerted = true
        end
      else
        if pct >= r.alert then
          alerted = true
        end
      end

      if alerted then
        staColor = C_RED
        SKIN:Bang('!SetOption', 'mtr' .. r.id .. 'Pwr', 'FontColor', C_RED)
      else
        SKIN:Bang('!SetOption', 'mtr' .. r.id .. 'Pwr', 'FontColor', C_BLUE)
      end
      SKIN:Bang('!SetOption', 'mtr' .. r.id .. 'Sta', 'FontColor', staColor)

      -- Only toggle the DESTROYED stamp on a genuine state change, so the
      -- per-second Update never re-shows rows during the startup sweep.
      if alerted ~= wasDestroyed[r.id] then
        if alerted then
          SKIN:Bang('!ShowMeter', 'mtr' .. r.id .. 'Destroyed')
          SKIN:Bang('!HideMeter', 'mtr' .. r.id .. 'Val')
        else
          SKIN:Bang('!HideMeter', 'mtr' .. r.id .. 'Destroyed')
          SKIN:Bang('!ShowMeter', 'mtr' .. r.id .. 'Val')
        end
        wasDestroyed[r.id] = alerted
      end
    end
  end
  SKIN:Bang('!UpdateMeterGroup', 'roster')
  SKIN:Bang('!Redraw')
  return 0
end
