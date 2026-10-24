import argparse
from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

from training import create_model


def load_model(path):
    model = create_model()
    model.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
    model.eval()
    return model


def predict(model, image):
    preprocess = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
    ])
    inputs = preprocess(image).unsqueeze(0)
    with torch.inference_mode():
        return model(inputs).argmax(dim=1).item()


def main():
    parser = argparse.ArgumentParser(description="Predict a handwritten digit.")
    parser.add_argument("image", type=Path, help="Light digit on a dark background")
    parser.add_argument("--model", type=Path, default=Path("mnist_model.pt"))
    args = parser.parse_args()

    model = load_model(args.model)
    with Image.open(args.image) as image:
        print(predict(model, image))


if __name__ == "__main__":
    main()
