# MTG Card Identifier 📇

Ein kleines, nützliches Python-Tool zur **Abfrage von Magic: The Gathering Karteninformationen** über die [Scryfall API](https://scryfall.com/docs/api)  
und zur **automatischen Umrechnung des Kartenpreises von USD → EUR** mittels der [Frankfurter.app API](https://www.frankfurter.app/docs).  

Ergebnisse werden **übersichtlich als DataFrame dargestellt** (ideal in Jupyter Notebook) und können optional als CSV exportiert werden.

---

## Features 🚀

✅ Exakte Kartensuche per Name  
✅ Abfrage folgender Infos: Name, Set, Rarity, Oracle Text, Bild-URL, USD-Preis  
✅ Live-Umrechnung USD → EUR  
✅ Export als CSV  
✅ Robustes Error-Handling  
✅ Modularer Aufbau — perfekt für Erweiterungen oder Batch-Prozesse  

---

## Installation 🛠️

Voraussetzung: Python >= 3.10

### 1️⃣ Repository klonen

```bash
git clone https://github.com/DEIN_GITHUB_USERNAME/mtg-card-identifier.git
cd mtg-card-identifier
```

### 2️⃣ Virtuelle Umgebung (optional, empfohlen)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3️⃣ Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4️⃣ Jupyter Notebook starten

```bash
jupyter notebook
```

Notebook `mtg_card_identifier.ipynb` öffnen und loslegen! 🚀

---

## Beispielnutzung

```python
sample_card_name = "Lightning Bolt"
main(sample_card_name)
```

→ Zeigt die Karte als DataFrame an und speichert sie als CSV.  
→ **Bild-URL** wird ebenfalls geliefert.

---

## API Quellen

- 🎴 **Scryfall API** → [https://scryfall.com/docs/api](https://scryfall.com/docs/api)
- 💱 **Frankfurter.app** → [https://www.frankfurter.app/docs](https://www.frankfurter.app/docs)

---

## Anforderungen

```text
requests
pandas
ipython  # für IPython.display (falls Notebook-Nutzung)
```

→ bereits in der `requirements.txt` enthalten.

---

## Hinweise

⚠️ Dieses Tool macht **Live-API-Anfragen** → bei vielen Karten bitte Zeitabstände einhalten (Fair Use bei Scryfall beachten).  
⚠️ Preisangaben sind **nur so aktuell wie die API sie liefert** — keine Garantie auf Vollständigkeit oder Verfügbarkeit.

---