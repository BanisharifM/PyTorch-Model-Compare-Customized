import torch
from torchvision.models import resnet18, resnet34, resnet50, wide_resnet50_2
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import numpy as np
import random
from torch_cka import CKA

def seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)

g = torch.Generator()
g.manual_seed(0)
np.random.seed(0)
random.seed(0)

model1 = resnet18(pretrained=True)
model2 = resnet34(pretrained=True)


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

batch_size = 256

dataset = CIFAR10(root='../data/',
                  train=False,
                  download=True,
                  transform=transform)

dataloader = DataLoader(dataset,
                        batch_size=batch_size,
                        shuffle=False,
                        worker_init_fn=seed_worker,
                        generator=g,)

# cka = CKA(model1, model2,
#         model1_name="ResNet18", model2_name="ResNet34",
#         device='cuda')
#
# cka.compare(dataloader)
#
# cka.plot_results(save_path="../assets/resnet_compare.png")


#===============================================================
model1 = resnet50(pretrained=True)
model2 = wide_resnet50_2(pretrained=True)


cka = CKA(model1, model2,
        model1_name="ResNet50", model2_name="WideResNet50",
        device='cuda')

cka.compare(dataloader)

cka.plot_results(save_path="/content/drive/MyDrive/Research/PyTorch-Model-Compare/assets/resnet-resnet_compare.png")