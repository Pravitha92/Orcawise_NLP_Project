# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:03:02 2023

"""

import pandas as pd
import re

class DataProcessing:
    def __init__(self, combination_spin_file, merging_one_file, output_file):
        self.combination_spin_file = combination_spin_file
        self.merging_one_file = merging_one_file
        self.output_file = output_file

    def add_data_after_7th_row(self):
        # Read the files
        combination_spin_df = pd.read_csv(self.combination_spin_file)
        merging_one_df = pd.read_csv(self.merging_one_file)

        # Initialize an empty DataFrame
        result_df = pd.DataFrame(columns=combination_spin_df.columns)

        for index, row in combination_spin_df.iterrows():
            # Append the current row from combination_spin_df
            result_df = pd.concat([result_df, pd.DataFrame([row], columns=result_df.columns)])

            if not merging_one_df.empty and (index + 1) % 7 == 0:
                # Append the row from merging_one_df
                result_df = pd.concat([result_df, pd.DataFrame([merging_one_df.iloc[0]], columns=result_df.columns)]).reset_index(drop=True)
                # Drop the appended row from merging_one_df
                merging_one_df = merging_one_df.drop(merging_one_df.index[0])

        result_df.to_csv(self.output_file, index=False)

    def remove_duplicates(self):
        df = pd.read_csv(self.output_file)

        # Create a temporary column for identifying duplicates
        df['temp_sentence'] = df['Combination_spin_text'].apply(lambda x: ''.join(x).lower())
        df['temp_sentence'] = df['temp_sentence'].apply(lambda x: re.sub(r'\W', '', x))
        df['is_duplicate'] = df['temp_sentence'].duplicated(keep='first')

        # Filter the DataFrame to keep only unique sentences
        df_unique = df[~df['is_duplicate']]
        df_unique = df_unique.drop(columns=['temp_sentence', 'is_duplicate'])
        df_unique.to_csv(self.output_file, index=False)

    def count_relations(self):
        df = pd.read_csv(self.output_file)
        relation_counts = df['relations'].value_counts()
        print(relation_counts)


#obj1 = DataProcessing('combination_spin_new.csv', 'merging_one.csv', 'combined_result.csv')
obj1 = DataProcessing('combined_result.csv', 'merged_located.csv', 'combined_result1.csv')
obj1.add_data_after_7th_row()
obj1.remove_duplicates()
obj1.count_relations()
