# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 19:59:52 2023

@author: nishanth
"""

import re
import pandas as pd

def create_combinations(sentence, relation_value):
    # Extracting subject, object, and relation
    subject_match = re.search(r'\[E1\](.*?)\[/E1\]', sentence)
    relation_match = re.search(r'\[/E1\](.*?)\[E2\]', sentence)
    obj_match = re.search(r'\[E2\](.*?)\[/E2\]', sentence)

    if subject_match and relation_match and obj_match:
        subject = subject_match.group(1)
        relation = relation_match.group(1)
        obj = obj_match.group(1)

        # Extracting the previous and remaining text
        previous_text = re.split(r'\[E1\].*?\[/E1\]', sentence)[0]
        remaining_text = re.split(r'\[/E2\]', sentence)[1]

        # Check the value of the 'relations' column
        if relation_value == 'locatedAt':
            # Creating combinations with correct order
            original_combination = f"{previous_text}[E1]{subject}[/E1]{relation}[E2]{obj}[/E2]{remaining_text}"
            combination1 = f"{previous_text}{relation} of [E2]{obj}[/E2] [E1]{subject}[/E1]{remaining_text}"
            return [original_combination, combination1]
        else:
            original_combination = f"{previous_text}[E1]{subject}[/E1]{relation}[E2]{obj}[/E2]{remaining_text}"
            combination1 = f"{previous_text}{relation} of [E2]{obj}[/E2] [E1]{subject}[/E1]{remaining_text}"
            combination2 = f"{previous_text}[E2]{obj}[/E2]{relation} [E1]{subject}[/E1]{remaining_text}"
            return [original_combination, combination1, combination2]
    else:
        # Return an empty list if the pattern is not matched
        return []

def create_combinations1(sentence, relation_value):
    # Extracting subject, object, and relation
    subject_match = re.search(r'\[E2\](.*?)\[/E2\]', sentence)
    relation_match = re.search(r'\[/E2\](.*?)\[E1\]', sentence)
    obj_match = re.search(r'\[E1\](.*?)\[/E1\]', sentence)
    
    if subject_match and relation_match and obj_match:
        subject = subject_match.group(1)
        relation = relation_match.group(1)
        obj = obj_match.group(1)

        # Extracting the previous and remaining text
        previous_text = re.split(r'\[E2\].*?\[/E2\]', sentence)[0]
        remaining_text = re.split(r'\[/E1\]', sentence)[1]
        
        # Check the value of the 'relations' column
        if relation_value == 'locatedAt':
            # Creating combinations with correct order
            original_combination = f"{previous_text}[E2]{subject}[/E2]{relation}[E1]{obj}[/E1]{remaining_text}"
            combination1 = f"{previous_text}{relation} of [E1]{obj}[/E1] [E2]{subject}[/E2]{remaining_text}"
            return [original_combination, combination1]
        else:
            original_combination = f"{previous_text}[E2]{subject}[/E2]{relation}[E1]{obj}[/E1]{remaining_text}"
            combination1 = f"{previous_text}{relation} of [E1]{obj}[/E1] [E2]{subject}[/E2]{remaining_text}"
            combination2 = f"{previous_text}[E1]{obj}[/E1]{relation} [E2]{subject}[/E2]{remaining_text}"
            return [original_combination, combination1, combination2]
    else:
        # Return an empty list if the pattern is not matched
        return []
def comparison_sentence(df):
    df['temp_sentence'] = df['combinations'].apply(lambda x: re.sub(r'\W', '', x.lower()))
    df['is_duplicate'] = df.duplicated(subset=['temp_sentence'], keep='first')
    df_unique = df[~df['is_duplicate']]
    df_unique = df_unique.drop(columns=['temp_sentence', 'is_duplicate'])
    return df_unique

def keep_unique_sentences(csv_file, column_name):
    df = pd.read_csv(csv_file)
    df = comparison_sentence(df)
    df.to_csv(csv_file, index=False)

# Read the CSV file
df = pd.read_csv('cleaned_sentences.csv')  # Replace 'your_file.csv' with the actual file name

# Create new columns for combinations
df['combinations'] = ''

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    sentence = str(row['cleaned_text'])  # Convert to string to handle non-string values
    relation_value = row['relations']

    if re.search(r'\[/E1\](.*?)\[E2\]', sentence):
        combinations = create_combinations(sentence, relation_value)
    elif re.search(r'\[/E2\](.*?)\[E1\]', sentence):
        combinations = create_combinations1(sentence, relation_value)

    # Update the 'combinations' column with the generated combinations
    df.at[index, 'combinations'] = combinations

# Explode the 'combinations' column into separate rows
df_exploded = df.explode('combinations').reset_index(drop=True)

# Save the DataFrame with exploded combinations back to the CSV file
df_exploded.to_csv('augmented.csv', index=False)

# Keep only unique combinations
keep_unique_sentences('augmented.csv', 'combinations')