import pandas as pd
import json
import re
import uuid

path = r"D:\Datasets\coursera-dataset\coursera_courses_with_descriptions.csv"
df = pd.read_csv(path)
df = df.drop(columns='institution')

df = df.drop_duplicates(subset='course_id')

columns_to_check = ['description']  
pattern = re.compile(r'^[\w\d\s.,;:!?()\[\]\'"@&$%-/]+$', re.UNICODE)

def is_clean(row):
    for col in columns_to_check:
        value = str(row[col])
        if not pattern.match(value):
            return False
    return True

mask = df.apply(is_clean, axis=1)

clean_df = df[mask]
clean_df = clean_df.reset_index(drop=True)

clean_df['uuid'] = [str(uuid.uuid4()) for _ in range(len(clean_df))]
clean_df.to_json("coursera_data.json", orient='records', lines=False, force_ascii=False)

print(f"Original rows: {df.shape[0]}")
print(f"Cleaned and deduplicated rows: {clean_df.shape[0]}")
print("JSON file with UUIDs created as 'coursera_data.json'")