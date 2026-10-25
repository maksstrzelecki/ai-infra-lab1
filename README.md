# MNIST inference server

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Train once to generate `mnist_model.pt` (skip if it already exists):

```bash
python training.py
```

## Run the API

```bash
uvicorn server:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.
The model loads once at startup on the CPU. Startup fails if the checkpoint is missing.

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict -F 'file=@images/two.png'
```

Prediction response: `{"digit": 2}`. Invalid images return HTTP 400.
Use a light digit on a dark background; images are converted to grayscale and resized to 28 × 28.

The original CLI remains available:

```bash
python inference.py images/two.png
```

## Benchmark

Uruchom serwer:

```bash
python -m uvicorn server:app --workers 1 --no-access-log
```

W drugim terminalu uruchom benchmark:

```bash
python benchmark.py --url http://127.0.0.1:8000/predict --image images/two.png --requests 1000 --concurrency 10
```

| Flaga | Znaczenie | Domyślnie |
|---|---|---|
| `--url` | Adres endpointu | `http://127.0.0.1:8000/predict` |
| `--image` | Ścieżka do obrazu | `images/two.png` |
| `--requests` | Liczba żądań | `200` |
| `--concurrency` | Liczba równoczesnych żądań | `10` |

Seria pomiarów z wykresem:

```bash
python run_benchmark.py
```

`run_benchmark.py` nie przyjmuje flag; zakres concurrency i liczbę żądań ustawia się w pliku.
