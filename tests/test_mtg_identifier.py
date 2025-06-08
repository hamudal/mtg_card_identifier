# tests/test_mtg_identifier.py

import pytest
import pandas as pd
from mtg_identifier import fetch_card_data, get_usd_to_eur_rate

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code
        self.text = str(json_data)
        self.response = self

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception(f"HTTP {self.status_code}")

def test_fetch_card_data_success(monkeypatch):
    dummy = {
        "name": "TestCard",
        "set_name": "TestSet",
        "rarity": "common",
        "oracle_text": "Do something.",
        "image_uris": {"normal": "http://example.com/image.jpg"},
        "prices": {"usd": "1.23"}
    }
    monkeypatch.setattr('mtg_identifier.requests.get',
                        lambda url: DummyResponse(dummy))
    data = fetch_card_data("TestCard")
    assert data["Name"] == "TestCard"
    assert data["Set"] == "TestSet"
    assert data["Price USD"] == "1.23"

def test_fetch_card_data_not_found(monkeypatch):
    def bad_get(url):
        resp = DummyResponse({}, status_code=404)
        resp.raise_for_status()
    monkeypatch.setattr('mtg_identifier.requests.get', bad_get)
    with pytest.raises(Exception):
        fetch_card_data("NoSuchCard")

def test_get_usd_to_eur_rate(monkeypatch):
    fx = {"rates": {"EUR": 0.9}}
    dummy = {"rates": {"EUR": 0.9}}
    monkeypatch.setattr('mtg_identifier.requests.get',
                        lambda url, params=None: DummyResponse(dummy))
    rate = get_usd_to_eur_rate()
    assert isinstance(rate, float)
    assert rate == 0.9
