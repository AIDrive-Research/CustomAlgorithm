import torch
import time
import torch.nn as nn
import torch.optim as optim
from torchvision import models, datasets, transforms
from torch.utils.data import DataLoader
import warnings

warnings.filterwarnings("ignore")

device = torch.device("cuda:0" if torch.cuda.is_available() else 'cpu')
batch_size = 64
n_classes = 2
train_dataset = 'dataset/train/'
test_dataset = 'dataset/test/'
epochs = 300

lr = 0.0001
pretrain = True

transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(),
    transforms.RandomGrayscale(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

transform_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = datasets.ImageFolder(root=train_dataset,
                                     transform=transform_train)
test_dataset = datasets.ImageFolder(root=test_dataset,
                                    transform=transform_test)

model = models.resnet18(pretrained=pretrain)
model.fc = nn.Linear(512, n_classes)
model.to(device)

loss_fn = nn.CrossEntropyLoss().to(device)
optimizer = optim.Adam(model.parameters(), lr=lr)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)


def run_epoch(model, data_loader, loss_fn, optimizer=None, train=True):
    model.train() if train else model.eval()
    total_loss, corrects, total = 0, 0, 0
    for inputs, labels in data_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        loss = loss_fn(outputs, labels)
        if train:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        preds = outputs.argmax(dim=1)
        total_loss += loss.item() * inputs.size(0)
        corrects += torch.sum(preds.eq(labels))
        total += labels.size(0)
        print(total)

    avg_loss = total_loss / total
    accuracy = 100 * corrects / total
    return avg_loss, accuracy


def main():
    best_accuracy = 0.0
    for epoch in range(epochs):
        start_time = time.time()

        train_loss, train_acc = run_epoch(model, train_loader, loss_fn, optimizer, train=True)
        test_loss, test_acc = run_epoch(model, test_loader, loss_fn, train=False)

        if test_acc > best_accuracy:
            best_accuracy = test_acc
            print('Save best model!')
            torch.save(model.state_dict(), "best.pth")

        end_time = time.time()
        print(f"Epoch {epoch + 1} | cost time: {end_time - start_time:.2f}s | "
              f"train loss: {train_loss:.5f} | train acc: {train_acc:.2f}% | "
              f"test loss: {test_loss:.5f} | test acc: {test_acc:.2f}%")


if __name__ == "__main__":
    main()
