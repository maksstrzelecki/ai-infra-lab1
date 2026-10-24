from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

from inference import load_model, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = Path(__file__).with_name("mnist_model.pt")
    if not model_path.is_file():
        raise RuntimeError("Model not found. Run python training.py first.")
    app.state.model = load_model(model_path)
    yield
    del app.state.model


app = FastAPI(title="MNIST Inference Server", lifespan=lifespan)


class Prediction(BaseModel):
    digit: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict_image(file: UploadFile):
    """Upload an image with a light handwritten digit on a dark background."""
    try:
        with Image.open(file.file) as image:
            digit = predict(app.state.model, image)
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        raise HTTPException(status_code=400, detail="Upload a valid image.")
    finally:
        file.file.close()
    return Prediction(digit=digit)
