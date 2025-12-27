import requests

def lookup_enja(word: str) -> list[str]:
    r = requests.get(
        "https://api.excelapi.org/dictionary/enja",
        params={"word": word.strip()},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5
    )
    r.raise_for_status()

    raw = r.text.strip()
    if not raw:
        return []

    # 『リンゴ』;リンゴの木
    parts = raw.replace("『", "").replace("』", "").split(";")
    return parts
