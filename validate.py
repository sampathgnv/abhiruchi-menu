"""Check catalog.json before publishing it.

Run:  python validate.py

A broken file cannot hurt customers — the app falls back to the copy inside it —
but it is better to catch a mistake here than to wonder why a price never changed.

Exits with status 0 if the file is good, 1 if something is wrong.
"""

import json
import re
import sys
from pathlib import Path

CATALOG = Path(__file__).parent / "catalog.json"
IMAGES = Path(__file__).parent / "images"

VALID_UNIT_TYPES = {"weight", "box", "piece"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def main() -> int:
    if not CATALOG.exists():
        print(f"catalog.json not found at {CATALOG}")
        return 1

    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        # By far the most common failure: a stray or missing comma.
        print("catalog.json is not valid JSON, so the app would ignore it.")
        print(f"  Line {exc.lineno}, column {exc.colno}: {exc.msg}")
        print("\n  This is almost always a missing or extra comma, or a missing")
        print('  quotation mark. Check the line above and below line', exc.lineno)
        return 1

    # --- the fields the app depends on ------------------------------------
    version = data.get("dataVersion")
    if not isinstance(version, int):
        error('"dataVersion" must be a whole number, e.g. 3')
    elif version < 1:
        error('"dataVersion" must be 1 or more')

    if not isinstance(data.get("maxUnitsPerItem"), int):
        error('"maxUnitsPerItem" must be a whole number')

    whatsapp = str(data.get("whatsappNumber", ""))
    if not re.fullmatch(r"\d{12}", whatsapp):
        error('"whatsappNumber" must be 12 digits with no + sign, e.g. 919849603418')

    if "REPLACE-ME" in str(data.get("imageBaseUrl", "")):
        warn(
            '"imageBaseUrl" still says REPLACE-ME. Set it to '
            "https://YOUR-USERNAME.github.io/abhiruchi-menu/images once the "
            "repository exists. Only matters when photos are switched on."
        )

    images_on = data.get("imagesEnabled", False)

    # --- items -------------------------------------------------------------
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        error('"sections" is missing or empty')
        return report()

    seen_ids: dict[str, str] = {}
    seen_card_numbers: dict[int, str] = {}
    total = 0

    for section in sections:
        name = section.get("name", "(unnamed section)")
        items = section.get("items")
        if not isinstance(items, list) or not items:
            error(f"section {name!r} has no items")
            continue

        for item in items:
            total += 1
            item_id = item.get("id", "")
            label = f"{name} / {item.get('name', item_id or '(unnamed)')}"

            if not ID_PATTERN.fullmatch(str(item_id)):
                error(f"{label}: id {item_id!r} must be lower case words joined by hyphens")
            elif item_id in seen_ids:
                error(f"{label}: id {item_id!r} is already used by {seen_ids[item_id]}")
            else:
                seen_ids[item_id] = label

            card_no = item.get("cardNo")
            if not isinstance(card_no, int):
                error(f"{label}: cardNo must be a whole number")
            elif card_no in seen_card_numbers:
                error(f"{label}: cardNo {card_no} is already used by {seen_card_numbers[card_no]}")
            else:
                seen_card_numbers[card_no] = label

            price = item.get("priceInr")
            if not isinstance(price, int) or isinstance(price, bool):
                error(f"{label}: priceInr must be a whole number of rupees, not {price!r}")
            elif price <= 0:
                error(f"{label}: priceInr must be more than zero")

            unit_type = item.get("unitType")
            if unit_type not in VALID_UNIT_TYPES:
                error(f"{label}: unitType must be one of weight, box, piece — not {unit_type!r}")
            elif unit_type == "weight":
                if not isinstance(item.get("unitGrams"), int):
                    error(f"{label}: a weight item needs unitGrams, e.g. 500")
                if "piecesPerBox" in item:
                    error(f"{label}: a weight item must not have piecesPerBox")
            elif unit_type == "box":
                if not isinstance(item.get("piecesPerBox"), int):
                    error(f"{label}: a box item needs piecesPerBox, e.g. 7")
                if "unitGrams" in item:
                    error(f"{label}: a box item must not have unitGrams")

            if images_on:
                filename = item.get("image") or f"{item_id}.webp"
                if not (IMAGES / filename).exists():
                    warn(f"{label}: no photo at images/{filename} — shows a placeholder")

    # --- shops --------------------------------------------------------------
    for store in data.get("stores", []):
        store_name = store.get("name", "(unnamed store)")
        phone = str(store.get("phone", ""))
        if not re.fullmatch(r"\+91\d{10}", phone):
            error(f"{store_name}: phone must look like +918912766092 (the leading 0 is dropped)")
        display_digits = re.sub(r"\D", "", str(store.get("phoneDisplay", "")))
        if display_digits and display_digits != re.sub(r"\D", "", phone):
            error(f"{store_name}: phoneDisplay shows different digits from phone")
        if not str(store.get("mapsUrl", "")).startswith("https://"):
            error(f"{store_name}: mapsUrl must be a https:// link")

    business = data.get("business", {})
    owner_phone = str(business.get("ownerPhone", ""))
    if owner_phone and not re.fullmatch(r"\+91\d{10}", owner_phone):
        error("business.ownerPhone must look like +919849603418")

    # --- home page ----------------------------------------------------------
    for highlight in data.get("highlights", []):
        item_id = highlight.get("itemId")
        if item_id and item_id not in seen_ids:
            error(
                f"highlight {highlight.get('name')!r} points at item {item_id!r}, "
                "which no longer exists"
            )

    print(f"Read {total} items across {len(sections)} sections.")
    print(f"dataVersion is {version}. Photos are {'ON' if images_on else 'off'}.")
    return report()


def report() -> int:
    for message in warnings:
        print(f"  note:  {message}")

    if errors:
        print(f"\n{len(errors)} problem(s) found — do not publish this yet:")
        for message in errors:
            print(f"  ERROR: {message}")
        return 1

    print("\nAll good. Safe to publish.")
    print("Remember: increase dataVersion, or phones will ignore the change.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
