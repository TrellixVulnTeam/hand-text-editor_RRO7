import torch
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as dset
import Network
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
from torch.utils.data.sampler import SubsetRandomSampler
import torch.optim as optim
from torch.autograd import Variable
import time
import matplotlib.pyplot as plt

class Flatten(nn.Module):
    def forward(self, x):
        N, C, H, W = x.size() # read in N, C, H, W
        return x.view(N, -1)  # "flatten" the C * H * W values into a single vector per image

transform = transforms.Compose(
    [transforms.ToTensor()
        , transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = dset.ImageFolder(root='/Users/chenmo/Files/PythonProjects/cs175_project/hand-text-editor/src/edgedata/Train', transform=transform)


# trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
#                                         download=True, transform=transform)

# trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
#                                           shuffle=True, num_workers=2)
#
testset = dset.ImageFolder(root='/Users/chenmo/Files/PythonProjects/cs175_project/hand-text-editor/src/edgedata/Test', transform=transform)
#
# testloader = torch.utils.data.DataLoader(testset, batch_size=4,
#                                          shuffle=False, num_workers=2)

classes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z', 'SP', 'BS')




train_loader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

test_loader = torch.utils.data.DataLoader(testset, batch_size=4,
                                          shuffle=False, num_workers=2)


def createLossAndOptimizer(net, learning_rate=0.001):
    # Loss function
    loss = torch.nn.CrossEntropyLoss()

    # Optimizer
    optimizer = optim.Adam(net.parameters(), lr=learning_rate)

    return loss, optimizer

net = Network.Net()


criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for epoch in range(1):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        # get the inputs
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 50 == 49:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')


# trainNet(net, batch_size=32, n_epochs=10, learning_rate=0.001)

dataiter = iter(test_loader)
images, labels = dataiter.next()


correct = 0
total = 0
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the bluh test images: %d %%' % (
    100 * correct / total))

class_correct = list(0. for i in range(38))
class_total = list(0. for i in range(38))
with torch.no_grad():
    for data in test_loader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1

print(class_total)

for i in range(38):
    print('Accuracy of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))