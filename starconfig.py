# shadowconfig.py
"""
Central version registry.

Sab client-version aur version-code values yahin rakhi gayi hain, taaki
poori project me ek hi source of truth ho. Region ke hisaab se sahi
values milti hain:

    ALL  -> client version 1.132.12 | version code 2019121229   (default)
    IND  -> client version 1.134.14 | version code 2019121269   (special)

Naya region add karna ho to REGION_OVERRIDES me entry daal do. Jo region
yahan nahi hai, uske liye ALL (default) values use hongi.
"""

# ─────────────────────────────────────────────────────────────────────────────
# RELEASE (sab region ke liye same)
# ─────────────────────────────────────────────────────────────────────────────
RELEASE_VERSION = "OB55"

# ─────────────────────────────────────────────────────────────────────────────
# DEFAULTS (ALL regions)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_CLIENT_VERSION      = "1.132.12"
DEFAULT_CLIENT_VERSION_CODE = "2019121229"

# ─────────────────────────────────────────────────────────────────────────────
# PER-REGION OVERRIDES
# ─────────────────────────────────────────────────────────────────────────────
REGION_OVERRIDES = {
    "IND": {
        "client_version":      "1.134.14",
        "client_version_code": "2019121269",
    },
    # naya region yahan add karo, e.g.:
    # "ME": {
    #     "client_version":      "1.132.12",
    #     "client_version_code": "2019121229",
    # },
}

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _normalise(region) -> str:
    if not region:
        return ""
    return str(region).strip().upper()


def get_client_version(region=None) -> str:
    """Region ka client version. IND -> 1.134.14, baaki sab -> 1.132.12."""
    r = _normalise(region)
    override = REGION_OVERRIDES.get(r)
    if override:
        return override["client_version"]
    return DEFAULT_CLIENT_VERSION


def get_client_version_code(region=None) -> str:
    """Region ka client version code. IND -> 2019121269, baaki -> 2019121229."""
    r = _normalise(region)
    override = REGION_OVERRIDES.get(r)
    if override:
        return override["client_version_code"]
    return DEFAULT_CLIENT_VERSION_CODE


def get_release_version() -> str:
    """Release version (sab region ke liye same)."""
    return RELEASE_VERSION


def get(region=None) -> dict:
    """
    Ek hi call me sab values.

    Returns:
        {
            "region":              "IND" | "ALL",
            "client_version":      "1.134.14" | "1.132.12",
            "client_version_code": "2019121269" | "2019121229",
            "release_version":     "OB55",
        }
    """
    r = _normalise(region) or "ALL"
    override = REGION_OVERRIDES.get(r)
    return {
        "region":              r,
        "client_version":      override["client_version"] if override else DEFAULT_CLIENT_VERSION,
        "client_version_code": override["client_version_code"] if override else DEFAULT_CLIENT_VERSION_CODE,
        "release_version":     RELEASE_VERSION,
    }


def has_override(region=None) -> bool:
    """True agar is region ke liye alag values defined hain."""
    return _normalise(region) in REGION_OVERRIDES


def known_regions() -> list:
    """Jitne regions ke liye override defined hai (IND, ...)."""
    return sorted(REGION_OVERRIDES.keys())


# ─────────────────────────────────────────────────────────────────────────────
# Quick self-test (python shadowconfig.py chalane par)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for r in ("IND", "ind", "ME", "BD", None, ""):
        info = get(r)
        print(f"region={str(r):5}  "
              f"client={info['client_version']:9}  "
              f"code={info['client_version_code']:11}  "
              f"release={info['release_version']}")