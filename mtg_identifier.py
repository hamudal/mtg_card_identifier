#!/usr/bin/env python3
# mtg_identifier.py

import sys
import argparse
import requests
import pandas as pd

SCRYFALL_API_URL = "https://api.scryfall.com/cards/named"
FRANKFURTER_API_URL = "https://api.frankfurter.app/latest"

# Eingebaute Default-Testkarten, falls keine Karte über CLI args angegeben wurde
DEFAULT_TEST_CARDS = [
    "Lightning Bolt",
    "Black Lotus",
    "Counterspell",
    "Island"
]

def fetch_card_data(card_name: str) -> dict:
    """
    Fetch card data from Scryfall API by exact name.
    Returns a dict with Name, Set, Rarity, Oracle Text, Image URL, Price USD.
    """
    params = {"exact": card_name}
    resp = requests.get(SCRYFALL_API_URL, params=params)
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
    Fetch current USD to EUR rate.
    """
    params = {"from": "USD", "to": "EUR"}
    resp = requests.get(FRANKFURTER_API_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data["rates"]["EUR"]

def convert_usd_to_eur(usd_price, rate) -> float | None:
    """
    Convert USD price to EUR.
    """
    try:
        usd_value = float(usd_price)
        return round(usd_value * rate, 2)
    except (TypeError, ValueError):
        print("⚠️  Warnung: Ungültiger USD-Preis, EUR bleibt leer.")
        return None

def parse_args():
    parser = argparse.ArgumentParser(
        description="MTG Card Identifier: ruft Kartendaten ab und speichert sie als CSV."
    )
    parser.add_argument("card_names", nargs="*", type=str,
                        help='Exakter Name oder mehrere Namen der MTG-Karte(n), z.B. "Lightning Bolt" "Island" "Sol Ring"')
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="Pfad zur Ausgabedatei (CSV). Default: multi_card_info.csv oder <card_name>_info.csv bei Einzelkarte.")
    parser.add_argument("--no-eur", action="store_true",
                        help="Kein EUR-Feld berechnen (nur USD).")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Ausführliche Console-Ausgabe (inkl. Oracle Text, Image URL).")
    return parser.parse_args()

def main():
    args = parse_args()
    card_names = args.card_names or DEFAULT_TEST_CARDS

    try:
        print(f"🔍 Suche {len(card_names)} Karte(n)...")
        
        # Wechselkurs nur einmal holen
        if not args.no_eur:
            rate = get_usd_to_eur_rate()
            print(f"💱 Aktueller USD→EUR-Kurs: {rate:.4f}\n")
        else:
            rate = None
        
        all_card_infos = []

        # Loop über Karten
        for name in card_names:
            try:
                print(f"→ Hole Karte: '{name}'...")
                card_info = fetch_card_data(name)
                print(f"✅ '{card_info['Name']}' gefunden.")

                # Preis konvertieren
                eur_price = convert_usd_to_eur(card_info["Price USD"], rate) if not args.no_eur else None

                # DataFrame für die Karte bauen
                df_card = pd.DataFrame([card_info])
                if not args.no_eur:
                    df_card["Price EUR"] = eur_price

                all_card_infos.append(df_card)

                # verbose output
                if args.verbose:
                    print(f"\n=== Detail-Ausgabe für '{name}' ===")
                    print(f"Oracle Text: {card_info.get('Oracle Text')}")
                    print(f"Image URL:   {card_info.get('Image URL')}\n")

            except requests.HTTPError as http_err:
                code = http_err.response.status_code
                print(f"❌ Karte '{name}' nicht gefunden oder API-Fehler ({code}).", file=sys.stderr)
            except Exception as e:
                print(f"❌ Unerwarteter Fehler bei Karte '{name}': {e}", file=sys.stderr)

        # Nachbearbeitung
        if all_card_infos:
            df_all_cards = pd.concat(all_card_infos, ignore_index=True)
            
            # Spaltenreihenfolge
            columns_order = ["Name", "Set", "Rarity", "Price USD"]
            if not args.no_eur:
                columns_order.append("Price EUR")
            columns_order += ["Oracle Text", "Image URL"]

            df_all_cards = df_all_cards[[col for col in columns_order if col in df_all_cards.columns]]

            # CSV speichern
            fname = args.output
            if not fname:
                if len(card_names) == 1:
                    fname = f"{card_names[0].replace(' ', '_')}_info.csv"
                else:
                    fname = "multi_card_info.csv"

            df_all_cards.to_csv(fname, index=False)

            # Ausgabe
            print("\n=== Gesamtergebnis ===")
            print(df_all_cards.to_string(index=False))
            print(f"\n✅ CSV-Datei gespeichert unter: {fname}")
        else:
            print("⚠️  Keine Karten erfolgreich verarbeitet.")

    except Exception as e:
        print(f"❌ Unerwarteter Fehler in der Pipeline: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
