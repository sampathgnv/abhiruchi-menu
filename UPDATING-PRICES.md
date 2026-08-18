# Changing a price

Every customer's phone picks the change up within a day. No app update, no waiting for Google.

There are only **two** things you must get right: change the price, and increase `dataVersion`.

---

## The two rules

### 1. Change the price

Find the item in `catalog.json` and edit the number after `"priceInr"`.

```diff
- { "id": "jilebi", "cardNo": 1, "name": "Jilebi", "priceInr": 190, "unitType": "weight", "unitGrams": 500 },
+ { "id": "jilebi", "cardNo": 1, "name": "Jilebi", "priceInr": 200, "unitType": "weight", "unitGrams": 500 },
```

Prices are whole rupees. Write `200`, never `200.00`, `₹200` or `"200"`.

### 2. Increase `dataVersion`

At the very top of the file:

```diff
- "dataVersion": 2,
+ "dataVersion": 3,
```

**This is the one that matters.** The app compares this number against the copy it already has, and
ignores your change unless it has gone up. Change a price but forget this, and nothing happens on any
customer's phone.

Also update `updatedOn` to today's date so you can tell at a glance when you last touched it:

```diff
- "updatedOn": "2026-08-17",
+ "updatedOn": "2026-09-04",
```

---

## Doing it on the GitHub website

You do not need any software on your computer.

1. Open `catalog.json` in your repository on github.com.
2. Press the **pencil** icon (Edit this file).
3. Make your two changes.
4. Scroll down, type a short note like `Jilebi 190 to 200`, and press **Commit changes**.

That is it. GitHub republishes within a minute, and phones pick it up within a day.

---

## Check it before you publish

A broken file cannot hurt customers — the app just keeps using the prices already inside it — but it is
better to catch a mistake yourself. If you have Python on your computer:

```bash
python validate.py
```

It reports every item it read and refuses anything malformed.

---

## What else you can change here

| You want to | Edit |
|---|---|
| Change a price | `priceInr` on that item |
| Rename an item | `name` on that item — **never** change `id` |
| Add a new sweet | Copy a whole item line, give it a new unique `id` and the next `cardNo` |
| Remove a sweet | Delete its line. It disappears from the app and from any cart holding it |
| Change shop hours | `hours` under `business` |
| Change a phone number | Both `phone` (dialable, e.g. `+918912766092`) and `phoneDisplay` (spaced) |
| Reword the home page | `description` inside `highlights` |
| Change the shipping banner | `shippingNotice` under `business` |
| Raise the per-item limit | `maxUnitsPerItem` at the top |

### Two things never to change

- **`id`** — this is how the app recognises an item. Changing it empties that sweet out of any cart
  currently holding it, and orphans its photograph. Rename the `name` instead; customers never see `id`.
- **`unitType`** — `weight`, `box` or `piece`. Getting this wrong makes an item price by the wrong
  measure. If a sweet genuinely changes how it is sold, change `unitType` **and** the matching field
  (`unitGrams` for weight, `piecesPerBox` for box) together.

---

## If something goes wrong

Every edit on GitHub is kept. To undo one, open the repository, click **History**, find the change, and
revert it. Remember to bump `dataVersion` again on the way back so phones notice the correction.
