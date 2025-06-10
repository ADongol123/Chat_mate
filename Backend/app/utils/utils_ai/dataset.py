import torch 
from torchvision import transforms
from app.model_ai.model_def import CNNModel
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model(model_path, num_classes):
    model = CustomCNN(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model



def get_transforms():
    return transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])
    ])


