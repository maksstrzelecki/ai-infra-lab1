import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def create_model():
    return nn.Sequential(
        nn.Flatten(),
        nn.Linear(28 * 28, 128),
        nn.ReLU(),
        nn.Linear(128, 10),
    )


def main():
    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = datasets.MNIST(
        root="data", train=True, download=True, transform=transforms.ToTensor()
    )
    loader = DataLoader(dataset, batch_size=64, shuffle=True)
    model = create_model().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(5):
        total_loss = 0.0
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(images), labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * images.size(0)
        print(f"Epoch {epoch + 1}/5 - loss: {total_loss / len(dataset):.4f}")

    torch.save(model.cpu().state_dict(), "mnist_model.pt")
    print("Saved model to mnist_model.pt")


if __name__ == "__main__":
    main()
