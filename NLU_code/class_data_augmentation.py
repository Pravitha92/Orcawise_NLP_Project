# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:54:11 2023

"""

import re
import pandas as pd

class Data_augmentation:
    def __init__(self, csv_file, output_file):
        self.df = pd.read_csv(csv_file)
        self.output_file = output_file

    def create_combinations(self, sentence, relation_value):
        subject_match = re.search(r'\[E1\](.*?)\[/E1\]', sentence)
        relation_match = re.search(r'\[/E1\](.*?)\[E2\]', sentence)
        obj_match = re.search(r'\[E2\](.*?)\[/E2\]', sentence)

        if subject_match and relation_match and obj_match:
            subject = subject_match.group(1)
            relation = relation_match.group(1)
            obj = obj_match.group(1)

            previous_text = re.split(r'\[E1\].*?\[/E1\]', sentence)[0]
            remaining_text = re.split(r'\[/E2\]', sentence)[1]

            if relation_value == 'locatedAt':
                original_combination = f"{previous_text}[E1]{subject}[/E1]{relation}[E2]{obj}[/E2]{remaining_text}"
                combination1 = f"{previous_text}{relation} of [E2]{obj}[/E2] [E1]{subject}[/E1]{remaining_text}"
                return [original_combination, combination1]
            else:
                original_combination = f"{previous_text}[E1]{subject}[/E1]{relation}[E2]{obj}[/E2]{remaining_text}"
                combination1 = f"{previous_text}{relation} of [E2]{obj}[/E2] [E1]{subject}[/E1]{remaining_text}"
                combination2 = f"{previous_text}[E2]{obj}[/E2]{relation} [E1]{subject}[/E1]{remaining_text}"
                return [original_combination, combination1, combination2]
        else:
            return []

    def create_combinations1(self, sentence, relation_value):
        subject_match = re.search(r'\[E2\](.*?)\[/E2\]', sentence)
        relation_match = re.search(r'\[/E2\](.*?)\[E1\]', sentence)
        obj_match = re.search(r'\[E1\](.*?)\[/E1\]', sentence)

        if subject_match and relation_match and obj_match:
            subject = subject_match.group(1)
            relation = relation_match.group(1)
            obj = obj_match.group(1)

            previous_text = re.split(r'\[E2\].*?\[/E2\]', sentence)[0]
            remaining_text = re.split(r'\[/E1\]', sentence)[1]

            if relation_value == 'locatedAt':
                original_combination = f"{previous_text}[E2]{subject}[/E2]{relation}[E1]{obj}[/E1]{remaining_text}"
                combination1 = f"{previous_text}{relation} of [E1]{obj}[/E1] [E2]{subject}[/E2]{remaining_text}"
                return [original_combination, combination1]
            else:
                original_combination = f"{previous_text}[E2]{subject}[/E2]{relation}[E1]{obj}[/E1]{remaining_text}"
                combination1 = f"{previous_text}{relation} of [E1]{obj}[/E1] [E2]{subject}[/E2]{remaining_text}"
                combination2 = f"{previous_text}[E1]{obj}[/E1]{relation} [E2]{subject}[/E2]{remaining_text}"
                return [original_combination, combination1, combination2]
        else:
            return []
        
    def comparison_sentence(self):
        self.df['temp_sentence'] = self.df['combinations'].apply(lambda x: ''.join(x).lower())
        self.df['temp_sentence'] = self.df['temp_sentence'].apply(lambda x: re.sub(r'\W', '', x))
        #self.df['temp_sentence'] = self.df['combinations'].apply(lambda x: re.sub(r'\W', '', x.lower()))
        #self.df['temp_sentence'] = self.df['combinations'].apply(lambda x: [re.sub(r'\W', '', item.lower()) for item in x])
        self.df['is_duplicate'] = self.df.duplicated(subset=['temp_sentence'], keep='first')
        df_unique = self.df[~self.df['is_duplicate']]
        df_unique = df_unique.drop(columns=['temp_sentence', 'is_duplicate'])
        return df_unique

    def keep_unique_sentences(self):
        df_unique = self.comparison_sentence()
        df_unique.to_csv(self.output_file, index=False)

    def generate_combinations(self):
        self.df['combinations'] = ''

        for index, row in self.df.iterrows():
            sentence = str(row['cleaned_text'])
            relation_value = row['relations']

            if re.search(r'\[/E1\](.*?)\[E2\]', sentence):
                combinations = self.create_combinations(sentence, relation_value)
            elif re.search(r'\[/E2\](.*?)\[E1\]', sentence):
                combinations = self.create_combinations1(sentence, relation_value)

            self.df.at[index, 'combinations'] = combinations

        df_exploded = self.df.explode('combinations').reset_index(drop=True)
        df_exploded.to_csv(self.output_file, index=False)
        self.keep_unique_sentences()


obj1 = Data_augmentation('cleaned_sentences.csv', 'augmented.csv')
obj1.generate_combinations()

