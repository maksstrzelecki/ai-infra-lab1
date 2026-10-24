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
