from app.common.utils import safe_float

def test_safe_float(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "3.14")
    assert safe_float("Enter: ") == 3.14
