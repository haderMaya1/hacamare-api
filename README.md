# Hacamare - Backend (MVP) — Setup inicial

## Requisitos
- Python 3.10+ (recomendado)
- pip

## Iniciar la app
```bash
python -m venv .venv
source .venv/bin/activate   
# Windows: .venv\Scripts\activate
pip install -r requirements.txt

## Instalar dependencias
```bash cmd
uvicorn app.main:app --reload

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
