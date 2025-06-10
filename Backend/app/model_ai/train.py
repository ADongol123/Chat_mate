import torch 
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from app.model_ai.model_def import CNNModel
from utils.dataset import ProdductImageDataset
import os
from Backend.app.model_ai.model_def import calculate_channels 


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



#read category
def read_category(category_path):
    ext  = os.path.splitext(category_path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(category_path)
    elif ext in [".xls",".xlsx"]:
        return pd.read_excel(category_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}. Please upload a valid CSV or Excel file.")

# Load user dataset
def process_and_train_for_company(company_id, image_folder, category_file_path, category_map_json):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    transform = get_transforms()
    
    
    # Load category mapping
    with open(category_map_json, 'r') as f:
        category_map = json.load(f)
        
        # Read the category file
        category_df = read_category(category_file_path)
        
        # Save a cleaned versoin as CSV 
        cleaned_category_path = os.path.join(f"client_data/{company_id}","cleaned_category.csv")
        os.makedirs(os.path.dirname(cleaned_category_path), exist_ok=True)
        category_df.to_csv(cleaned_category_path, index=False)
        
        
        # Create dataset and DataLoader
        dataset = ProductImageDataset(
        image_folder=image_folder,
        csv_path=cleaned_csv_path,
        transform=transform,
        category_to_idx=category_to_idx
        )
        
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        # Train the model
        model = CNNModel(num_classes=len(category_map)).to(device)
        train_model(model,dataloader)
        
        
        # SAving the model
        model_save_path = f"client_data/{company_id}/model.pth"
        torch.save(model.state_dict(), model_save_path)
        print(f"Model saved to {model_save_path}")
        
