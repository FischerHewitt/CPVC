def parse_units_range(raw, default: int = 3) -> dict:
    """Parse a raw unit string into a units dict.

    Fixed:    "3"   → {"units": 3}
    Range:    "1-3" → {"units": 1, "units_min": 1, "units_max": 3}
    Invalid:  ""    → {"units": default}
    """
    if raw is None:
        return {"units": default}
    text = str(raw).strip().replace("–", "-")
    if "-" in text:
        parts = text.split("-", 1)
        try:
            lo = int(parts[0])
            hi = int(parts[1])
        except (ValueError, IndexError):
            return {"units": default}
        if lo == hi:
            return {"units": lo}
        return {"units": lo, "units_min": lo, "units_max": hi}
    try:
        return {"units": int(text)}
    except ValueError:
        return {"units": default}
