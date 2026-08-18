# Abhiruchi Sweets — live menu data

This repository holds the price list and photos that the **Abhiruchi Sweets** Android app reads.

Publishing a change here updates the app on every customer's phone **within a day**, with no new app
version and no Google Play review.

Nothing in this repository is secret. It contains the same prices printed on the card in the shop, the
three shop addresses, and (later) photographs of the sweets. **No customer information ever reaches this
repository** — the app only ever reads from it, and never writes anything back.

---

## What each file is

| File | What it does |
|---|---|
| `catalog.json` | Every item, price and unit, plus the shop details and home-page text. This is the file you edit. |
| `images/` | Photographs of the sweets. Empty for now; see `ADDING-IMAGES.md`. |
| `UPDATING-PRICES.md` | How to change a price. **Start here.** |
| `ADDING-IMAGES.md` | How to switch on item photos later. |
| `validate.py` | Checks your edit before you publish it. |
| `index.html` | A plain page shown if someone opens the web address in a browser. |
| `.nojekyll` | Tells GitHub to publish the files exactly as they are. |

---

## One-time setup

Do this once, when the app is ready to go live.

1. **Create the repository.** On GitHub, make a new **public** repository named `abhiruchi-menu`.
   It must be public — GitHub only serves pages from public repositories on a free account.

2. **Upload these files.** Use *Add file → Upload files* on GitHub and drop in everything from this
   folder, including the `images` folder and the hidden `.nojekyll` file.

3. **Switch on GitHub Pages.** Go to *Settings → Pages*, set **Source** to *Deploy from a branch*,
   choose branch `main` and folder `/ (root)`, then press Save. Wait a minute or two.

4. **Check it works.** Open this address in a browser — you should see the price data:

   ```
   https://YOUR-USERNAME.github.io/abhiruchi-menu/catalog.json
   ```

5. **Send me that address.** Two lines near the top of `catalog.json` currently read
   `https://REPLACE-ME.github.io/...` — `catalogUrl` and `imageBaseUrl`. That is deliberate: while they
   say REPLACE-ME the app makes **no network requests at all**. Once the repository exists I will set
   both, and ship the app pointing at it.

---

## How the app uses this

- The app **ships with its own copy** of `catalog.json` inside it. That copy always works, with no
  internet connection at all.
- Once a day, the app quietly checks this repository for a newer copy.
- It only adopts the newer copy if the `dataVersion` number at the top has **gone up**. That number is
  how the app knows something changed — see `UPDATING-PRICES.md`.
- If the check fails, the phone is offline, or this repository is unreachable, **nothing breaks**. The
  app simply carries on with the copy inside it.

This means a mistake here cannot take the app down. The worst case is that customers keep seeing the
prices they saw yesterday.

> **Note:** the remote check is switched on in Phase 7 of the build. You can create this repository now
> and upload the files; the app will start reading from it once that phase ships.
