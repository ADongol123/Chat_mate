import torch 
import open_clip
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms


model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2b_s34b_b79k'
)

tokenizer = open_clip.get_tokenizer('ViT-B-32')

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)


def get_clip_image_embedding(image_bytes: bytes) -> list:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
    
    return image_features[0].cpu().tolist()


def get_clip_text_embedding(text: str) -> list:
    tokenized = tokenizer([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(tokenized)
    return text_features[0].cpu().tolist()