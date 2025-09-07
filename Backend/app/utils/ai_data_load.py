# import json
# import os
# from typing import List, Dict

# def load_intent_data(file_path: str) -> List[Dict]:
#     """
#     Load JSON data from file
#     Args:
#         file_path: Path to JSON file
#     Returns:
#         List of intent dictionaries
#     Raises:
#         FileNotFoundError, json.JSONDecodeError
#     """
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Data file not found at: {file_path}")
    
#     with open(file_path, 'r') as f:
#         return json.load(f)

# def show_sample(data: List[Dict], n: int = 5) -> None:
#     """Print first n samples"""
#     print(f"First {n} entries:")
#     for i, item in enumerate(data[:n], 1):
#         print(f"{i}. {json.dumps(item, indent=2)}")