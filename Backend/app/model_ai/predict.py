import torch
import json
import pandas as pd
from PIL import Image
from torchvision import models
import torch.nn as nn
from utils.transforms import get_transform
import os


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model(model_path, num_classes):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model



def predict(image_path):
    