import pandas as pd
from math import * 
import json 
import random 

import json
from pathlib import Path


RANDOM_SEED = 42 

TRAIN_SIZE = 0.80
VALIDATION_SIZE = 0.20

# Project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to CUAD data
DATA_PATH = PROJECT_ROOT / "data" / "cuad" / "CUADv1.json"

# Open JSON file
with open(DATA_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)
contracts = data["data"]


#looking through the data and understanidng it 
print(data.keys())
print("Number of items:", len(data["data"]))
print("\nFirst item keys:")
print(data["data"][0].keys())
first_contract = data["data"][0]

print("Title:", first_contract["title"])
print("Number of paragraphs:", len(first_contract["paragraphs"]))
print("Paragraph keys:", first_contract["paragraphs"][0].keys())
titles = [contract["title"] for contract in data["data"]]

print("Total contracts:", len(titles))
print("Unique titles:", len(set(titles)))
print("Duplicate titles:", len(titles) - len(set(titles)))



### split the actual data 

contracts_to_split = contracts.copy()


## create 80/20 split 

random.seed(RANDOM_SEED)

## shuffle contracts 

random.shuffle(contracts_to_split)

# calculate split point 

split_index = int(len(contracts_to_split) * TRAIN_SIZE)

# create training set 
train_contracts = contracts_to_split[:split_index]

#create validation test 
validation_contracts = contracts_to_split[split_index:]


# verify split size 

print("\n--- Split Size ---")

print("Training contracts:", len(train_contracts))
print("Validation contracts:", len(validation_contracts))

print(
    "Training percentage:",
    len(train_contracts) / len(contracts) * 100
)

print(
    "Validation percentage:",
    len(validation_contracts) / len(contracts) * 100
)


# check data leakage 

train_titles = {
    contracts["title"]
    for contract in train_contracts
}

validation_titles = {
    contracts["title"]
    for contract in validation_contracts
}

# find contracts appearing in both 

overlap = train_titles.intersection(validation_titles)

print("\n--- Leakage Check ---")
print("Contracts appearing in both sets:", len(overlap))

# stop program if leakage is found 

assert len(overlap) == 0, "Data leakage detected!"




# 10. CREATE OUTPUT JSON

# Preserve the original CUAD JSON structure
train_data = {
    "version": data["version"],
    "data": train_contracts
}

validation_data = {
    "version": data["version"],
    "data": validation_contracts
}


# 11. SAVE FILES

with open(TRAIN_PATH, "w", encoding="utf-8") as file:
    json.dump(train_data, file, indent=2)

with open(VALIDATION_PATH, "w", encoding="utf-8") as file:
    json.dump(validation_data, file, indent=2)


# 12. FINAL VERIFICATION

print("\n--- Final Verification ---")

print("Random seed:", RANDOM_SEED)

print("Train contracts:", len(train_contracts))
print("Validation contracts:", len(validation_contracts))

print("Leakage found:", len(overlap))

print("\nTrain file saved to:")
print(TRAIN_PATH)

print("\nValidation file saved to:")
print(VALIDATION_PATH)

