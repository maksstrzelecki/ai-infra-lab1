import argparse
from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

from training import create_model


def main():
    parser = argparse.ArgumentParser(description="Predict a handwritten digit.")
    parser.add_argument("image", type=Path, help="Light digit on a dark background")
    parser.add_argument("--model", type=Path, default=Path("mnist_model.pt"))
    args = parser.parse_args()

    model = create_model()
    model.load_state_dict(torch.load(args.model, map_location="cpu", weights_only=True))
    model.eval()

    preprocess = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
    ])
    with Image.open(args.image) as image:
        inputs = preprocess(image).unsqueeze(0)

    with torch.inference_mode():
        prediction = model(inputs).argmax(dim=1).item()
    print(prediction)


if __name__ == "__main__":
    main()
