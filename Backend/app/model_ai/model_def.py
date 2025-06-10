import torch.nn as nn
import os
from pathlib import Path
import math

def get_num_classes(dataset_path):
    """
    Determine the number of classes from the dataset directory structure.
    Assumes dataset is organized in folders where each folder name is a class.
    """
    if not os.path.exists(dataset_path):
        raise ValueError(f"Dataset path {dataset_path} does not exist")
    
    # Get all subdirectories (each representing a class)
    classes = [d for d in os.listdir(dataset_path) 
              if os.path.isdir(os.path.join(dataset_path, d))]
    
    if not classes:
        raise ValueError("No class directories found in the dataset path")
    
    return len(classes)

def calculate_channels(num_classes):
    """
    Calculate appropriate channel sizes based on number of classes.
    More classes = more channels to capture complex features.
    """
    # Base channel size that scales with number of classes
    base_channels = max(32, min(128, 32 * (1 + math.log2(num_classes))))
    # Round to nearest power of 2 for computational efficiency
    base_channels = 2 ** round(math.log2(base_channels))
    
    return {
        'first': int(base_channels),      # e.g., 32 for 2 classes, 64 for 10 classes
        'second': int(base_channels * 2),  # e.g., 64 for 2 classes, 128 for 10 classes
        'third': int(base_channels * 4),   # e.g., 128 for 2 classes, 256 for 10 classes
        'fourth': int(base_channels * 8)   # e.g., 256 for 2 classes, 512 for 10 classes
    }

class CNNModel(nn.Module):
    def __init__(self, num_classes=None, dataset_path=None):
        """
        Initialize the CNN model.
        Args:
            num_classes: Number of classes to predict. If None, will be determined from dataset_path
            dataset_path: Path to the dataset directory. Required if num_classes is None
        """
        if num_classes is None and dataset_path is None:
            raise ValueError("Either num_classes or dataset_path must be provided")
        
        if num_classes is None:
            num_classes = get_num_classes(dataset_path)
            
        super(CNNModel, self).__init__()
        self.num_classes = num_classes
        
        # Calculate channel sizes based on number of classes
        channels = calculate_channels(num_classes)
        
        # Feature extraction layers (fixed number of layers, dynamic channels)
        self.features = nn.Sequential(
            # First block: 224x224 -> 112x112
            nn.Conv2d(3, channels['first'], 3, padding=1),    # 224x224x3 -> 224x224xC1
            nn.ReLU(),
            nn.MaxPool2d(2),                                  # 224x224xC1 -> 112x112xC1
            
            # Second block: 112x112 -> 56x56
            nn.Conv2d(channels['first'], channels['second'], 3, padding=1),  # 112x112xC1 -> 112x112xC2
            nn.ReLU(),
            nn.MaxPool2d(2),                                  # 112x112xC2 -> 56x56xC2
            
            # Third block: 56x56 -> 28x28
            nn.Conv2d(channels['second'], channels['third'], 3, padding=1),  # 56x56xC2 -> 56x56xC3
            nn.ReLU(),
            nn.MaxPool2d(2),                                  # 56x56xC3 -> 28x28xC3
            
            # Fourth block: 28x28 -> 14x14
            nn.Conv2d(channels['third'], channels['fourth'], 3, padding=1),  # 28x28xC3 -> 28x28xC4
            nn.ReLU(),
            nn.MaxPool2d(2),                                  # 28x28xC4 -> 14x14xC4
        )
        
        # Classifier head (adapts to number of classes)
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),      # 14x14xC4 -> 1x1xC4
            nn.Flatten(),                      # 1x1xC4 -> C4
            nn.Linear(channels['fourth'], num_classes)  # C4 -> num_classes
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
    
    @classmethod
    def from_dataset(cls, dataset_path):
        """
        Create a model instance automatically configured for the given dataset.
        Args:
            dataset_path: Path to the dataset directory
        Returns:
            CNNModel instance configured for the dataset
        """
        num_classes = get_num_classes(dataset_path)
        return cls(num_classes=num_classes)
