# Adding photographs of the sweets

The app is built to show a photo on every menu row, but ships with photos **switched off**. Everything
needed is already written and tested — turning it on is a change to this repository, not a new app.

You can add photos for a few sweets, or all 65, at your own pace. Items without one keep a tidy branded
placeholder, so a half-finished set never looks broken.

---

## Three steps

### 1. Name each photo after the item's `id`

Open `catalog.json` and find the sweet. The `id` is the first field on its line:

```json
{ "id": "bobbatlu", "cardNo": 14, "name": "Bobbatlu", "priceInr": 200, ... }
```

So that photo must be named exactly **`bobbatlu.webp`** — lower case, no spaces.

### 2. Upload it to the `images` folder

Drop the file into `images/` in this repository. Nothing else to edit: the app finds the photo by name.

### 3. Switch photos on

At the top of `catalog.json`:

```diff
- "imagesEnabled": false,
+ "imagesEnabled": true,
```

And, as with any change here, increase `dataVersion`:

```diff
- "dataVersion": 2,
+ "dataVersion": 3,
```

Photos appear on every phone within a day. To turn them off again, set it back to `false` and bump the
version — useful if you want to pull a bad photo quickly.

---

## Getting the photos right

| | |
|---|---|
| **Shape** | Square. The app crops to a square, so anything else loses its edges. |
| **Size** | 800 × 800 pixels is plenty. Bigger only makes the app slower on a weak connection. |
| **Format** | `.webp` preferred — roughly half the size of a JPEG at the same quality. |
| **Weight** | Aim under 80 KB each. All 65 at that size is about 5 MB in total. |
| **Framing** | Fill the frame with the sweet. It is shown as a small thumbnail, so a distant shot reads as nothing. |
| **Light** | Daylight, near a window, no flash. Flash flattens the shine on syrup and ghee, which is the appetising part. |
| **Background** | Plain and consistent across all of them — a steel tray or a white plate. A mixed set looks careless even when each photo is good. |

If your photographer supplies JPEGs, they can be converted with any free tool; or send them to me and I
will convert and size the whole set in one go.

---

## Turning a JPEG into a WebP

If you have Python with Pillow installed:

```bash
python -c "from PIL import Image; im=Image.open('bobbatlu.jpg').convert('RGB'); im.thumbnail((800,800)); im.save('bobbatlu.webp','WEBP',quality=85)"
```

---

## What customers see

- **Photo present** — it appears as a rounded thumbnail beside the item, and full width when tapped.
- **No photo yet** — a branded placeholder. The row still shows name, price and unit exactly as now.
- **No internet** — placeholders. Prices, the menu, the cart and ordering all keep working offline; only
  the pictures need a connection, and each is stored on the phone after it loads once.

This is why photos live here rather than inside the app: adding them costs no app update, and the app
download stays small for customers on slower connections.
