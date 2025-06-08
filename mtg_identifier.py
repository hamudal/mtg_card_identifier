#!/usr/bin/env python3
# mtg_identifier.py

import sys
import argparse
import requests
import pandas as pd

def fetch_card_data(card_name: str) -> dict:
    """
    Fetch card data from Scryfall API by exact name.
    Returns a dict with Name, Set, Rarity, Oracle Text, Image URL, Price USD.
    """
    url = f"https://api.scryfall.com/cards/named?exact={card_name}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return {
        "Name": data.get("name"),
        "Set": data.get("set_name"),
        "Rarity": data.get("rarity"),
        "Oracle Text": data.get("oracle_text"),
        "Image URL": data.get("image_uris", {}).get("normal"),
        "Price USD": data.get("prices", {}).get("usd")
    }

def get_usd_to_eur_rate() -> float:
    """
    Holt den aktuellen USD→EUR-Kurs von frankfurter.app (ohne API-Key).
    """
    url = "https://api.frankfurter.app/latest"
    params = {"from": "USD", "to": "EUR"}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data["rates"]["EUR"]

def parse_args():
    parser = argparse.ArgumentParser(
        description="MTG Card Identifier: ruft Kartendaten ab und speichert sie als CSV."
    )
    parser.add_argument("card_name", type=str,
                        help='Exakter Name der MTG-Karte (z.B. "Lightning Bolt")')
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="Pfad zur Ausgabedatei (CSV). Default: <card_name>_info.csv")
    parser.add_argument("--no-eur", action="store_true",
                        help="Kein EUR-Feld berechnen (nur USD).")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Ausführliche Console-Ausgabe (inkl. Oracle Text, Image URL).")
    return parser.parse_args()

def main():
    args = parse_args()
    name = args.card_name

    try:
        # 1) Kartendaten holen
        card_info = fetch_card_data(name)

        # 2) DataFrame bauen
        df = pd.DataFrame([card_info])

        # 3) EUR optional
        if not args.no_eur:
            rate = get_usd_to_eur_rate()
            try:
                usd = float(card_info["Price USD"])
                eur = round(usd * rate, 2)
            except (TypeError, ValueError):
                eur = None
            df["Price EUR"] = eur

        # 4) Spalten-Filter
        cols = ["Name", "Set", "Rarity", "Price USD"]
        if not args.no_eur:
            cols.append("Price EUR")
        df = df[cols]

        # 5) Ausgabe
        if args.verbose:
            print(f"\n=== Detail-Ausgabe für '{name}' ===")
            print(f"Oracle Text: {card_info.get('Oracle Text')}")
            print(f"Image URL:   {card_info.get('Image URL')}\n")

        if not args.no_eur:
            print(f"Aktueller USD→EUR-Kurs: {rate:.4f}")
        print(df.to_string(index=False))

        # 6) CSV speichern
        fname = args.output or f"{name.replace(' ', '_')}_info.csv"
        df.to_csv(fname, index=False)
        print(f"\n✅ CSV-Datei gespeichert unter: {fname}")

    except requests.HTTPError as http_err:
        code = http_err.response.status_code
        print(f"❌ Karte nicht gefunden oder API-Fehler ({code}).", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
