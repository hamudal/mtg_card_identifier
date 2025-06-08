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

def main():
    parser = argparse.ArgumentParser(
        description="MTG Card Identifier: ruft Kartendaten von Scryfall ab und speichert sie als CSV."
    )
    parser.add_argument("card_name", type=str, help="Exakter Name der MTG-Karte (z.B. \"Lightning Bolt\").")
    args = parser.parse_args()

    sample = args.card_name

    try:
        # 1) Kartendaten holen
        card_info = fetch_card_data(sample)

        # 2) DataFrame bauen
        df = pd.DataFrame([card_info])

        # 3) Wechselkurs holen & konvertieren
        rate = get_usd_to_eur_rate()
        try:
            usd = float(card_info["Price USD"])
            eur = round(usd * rate, 2)
        except (TypeError, ValueError):
            eur = None

        df["Price EUR"] = eur

        # 4) Spalten-Filter
        cols = ["Name", "Set", "Rarity", "Price USD", "Price EUR"]
        df = df[cols]

        # 5) Ausgabe
        print(f"Aktueller USD→EUR-Kurs: {rate:.4f}")
        print(df.to_string(index=False))

        # 6) CSV speichern
        filename = sample.replace(" ", "_") + "_info.csv"
        df.to_csv(filename, index=False)
        print(f"\n✅ CSV-Datei gespeichert unter: {filename}")

    except requests.HTTPError as http_err:
        code = http_err.response.status_code
        print(f"❌ Karte nicht gefunden oder API-Fehler ({code}).", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
