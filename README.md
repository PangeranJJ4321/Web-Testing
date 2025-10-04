# Selenium Web Testing Starter (Python + pytest)

## Prasyarat
- Python 3.9+
- PowerShell 7 (Windows)

## Setup Cepat
1. Buat virtual environment
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```
2. Instal dependensi
```powershell
pip install -r requirements.txt
```
3. Jalankan tes
```powershell
pytest -s -v .\tests\test_saucedemo_advanced.py::test_checkout_flow  
```

## Struktur Project
```
.
├─ tests/
│  └─ test_example_site.py
├─ conftest.py
├─ requirements.txt
└─ README.md
```

## Catatan
- Driver browser dikelola otomatis oleh `webdriver-manager`, tidak perlu unduh manual.
- Ubah browser via variabel environment `BROWSER` (chrome|firefox|edge).
- Mode headless bisa diaktifkan dengan `HEADLESS=1`.

Contoh:
```powershell
$env:BROWSER = "chrome"
$env:HEADLESS = "1"
pytest -s -v .\tests\test_saucedemo_advanced.py::test_checkout_flow  
```
