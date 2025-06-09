# MTG Card Identifier 📇

Ein kleines Python-Tool, um Informationen zu **Magic: The Gathering**-Karten von der [Scryfall API](https://scryfall.com/docs/api) abzurufen und Preise automatisch in EUR umzurechnen (live Wechselkurs von [frankfurter.app](https://www.frankfurter.app/)).

Ideal für **Sammler, Händler oder Data-Analysen**.

---

## ✨ Features

✅ Abfrage von 1 bis beliebig vielen Kartennamen  
✅ Automatische Umrechnung von USD → EUR  
✅ Speicherung als CSV-Datei  
✅ Ausgabe als DataFrame in Jupyter Notebook  
✅ Fehlerhandling für API-Fehler  
✅ Erweiterbar für eigene Zwecke  

---

## 🛠️ Installation

1. 📥 Repository klonen:
```bash
git clone https://github.com/DEIN_USERNAME/mtg-card-identifier.git
cd mtg-card-identifier
```

2. 📦 Virtuelle Umgebung anlegen (optional, empfohlen):
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. 📦 Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

---

## 📝 Nutzung im Jupyter Notebook

1. Jupyter starten:
```bash
jupyter notebook
```

2. Notebook `mtg_card_identifier.ipynb` öffnen (oder eigenes anlegen)

3. Beispiel-Workflow:
```python
# Beispiel-Liste von Karten
card_names = [
    "Lightning Bolt",
    "Black Lotus",
    "Counterspell",
    "Sol Ring",
    "Island"
]

# Multi-Card Pipeline ausführen
# (siehe Notebook Zelle 7️⃣ im Beispiel)
```

4. Ergebnis:
- Ausgabe als DataFrame
- CSV: `multi_card_info.csv`

---

## ⚠️ Hinweise

- **Scryfall API** erlaubt kostenlosen Zugriff — bitte API-Rate-Limits beachten.  
- **Frankfurter.app** liefert kostenlosen Wechselkurs (ohne API-Key).  
- Bei API-Ausfällen oder Timeouts ist ein **Retry-Mechanismus** sinnvoll (siehe ToDo).  
- Das Tool ist **rein privat / educational** und nicht für produktive Massenscrapes gedacht.  

---

## ✅ ToDo / Mögliche Erweiterungen

- [ ] Automatischer Retry bei API-Fehlern  
- [ ] Fortschrittsanzeige (z.B. `tqdm`)  
- [ ] Logging statt `print()`  
- [ ] Batch-Import aus CSV (Kartenliste einlesen)  

---