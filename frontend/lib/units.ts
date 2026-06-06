export interface UnitRange {
  units: number;
  units_min?: number;
  units_max?: number;
}

/**
 * Parse a raw unit value (string or number) into a UnitRange.
 *
 * Fixed:  "3"   → { units: 3 }
 * Range:  "1-3" → { units: 1, units_min: 1, units_max: 3 }
 * Empty:  ""    → { units: defaultUnits }
 */
export function parseUnitsRange(
  raw: string | number | null | undefined,
  defaultUnits = 3,
): UnitRange {
  if (raw === null || raw === undefined) return { units: defaultUnits };
  const text = String(raw).trim().replace("–", "-");
  if (text.includes("-")) {
    const [left, right] = text.split("-", 2);
    const lo = parseInt(left, 10);
    const hi = parseInt(right, 10);
    if (!isNaN(lo) && !isNaN(hi)) {
      if (lo === hi) return { units: lo };
      return { units: lo, units_min: lo, units_max: hi };
    }
  }
  const n = parseInt(text, 10);
  if (!isNaN(n)) return { units: n };
  return { units: defaultUnits };
}
