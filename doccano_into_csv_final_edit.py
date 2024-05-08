import json
import pandas as pd
import numpy as np
import os
from os import listdir
import zipfile
import re

# Get jsonl files form directory
def get_jsonl(directory):
    path = []
    for filename in os.listdir(directory):
            if filename.endswith(".jsonl"):
                path.append(os.path.join(directory, filename))
    return path

# Create dictionary for relations
def Dataframe(dir):
    sentences, sentences_labels, subject, object, relations, labels, filenames = [],[],[],[],[],[],[]
    jsonl_files = get_jsonl(dir)
    for file in jsonl_files:
    # Tranform jsonl into json
        with open(file, 'r', encoding='utf8') as json_file:
            json_list = list(json_file)
        # Transform json into dataframe
        for json_str in json_list:
            result = json.loads(json_str)
            entities = get_entities(result) 
            ent1, ent2, rela = get_relation(result, entities)
            for i in range(len(ent1)):
                subject.append(ent1[i][0])
                object.append(ent2[i][0])
                relations.append(rela[i])
                labels.append([ent1[i][2],ent2[i][2]])
                try:
                    # for windows
                    filenames.append(re.search(r'\\([^\\]+)\.jsonl$', file).group(1) + '.txt')
                except:
                    # for linux
                    name_of_file = os.path.basename(file).split('.jsonl')[0]
                    filenames.append(name_of_file + '.txt')

                if ent1[i][1][0] < ent2[i][1][0]:
                    sent =  result['text'][:ent1[i][1][0]] + "[E1]" + result['text'][ent1[i][1][0]:ent1[i][1][1]] + "[/E1]" + result['text'][ent1[i][1][1]:]
                    sent =  sent[:ent2[i][1][0]+9] + "[E2]" + sent[ent2[i][1][0]+9:ent2[i][1][1]+9] + "[/E2]" + sent[ent2[i][1][1]+9:]
                    # # Use regular expressions to split the sentence
                    # split_sentences = re.split(r'(?<=\.)\s*', sent)
                    # # Pick the sentence containing [E1] and [E2]
                    # selected_sentence = next((s for s in split_sentences if "[E1]" in s and "[E2]" in s), None)
                    # sentences.append(selected_sentence)
                    
                    # Combine the operations in a single regular expression
                    split_sentences = re.split(r'(?<=[.])\s*|\.\s*', sent)
                    # Specify the tags to look for
                    tags = ['E1', 'E2']
                    # Pick the sentence containing the specified tags
                    selected_sentences = [s for s in split_sentences if any(tag in s for tag in tags)]
                    cleaned_sentence = ' '.join(selected_sentences)
                    # Add a dot at the end if it doesn't already end with one
                    if not cleaned_sentence.endswith('.'):
                        cleaned_sentence += '.'

                    sentences.append(cleaned_sentence)
                                                     
                    
                                                           
                    sentence_labels =  result['text'][:ent1[i][1][0]] + "[" + ent1[i][2] + "]" + result['text'][ent1[i][1][0]:ent1[i][1][1]] + "[/" + ent1[i][2] + "]" + result['text'][ent1[i][1][1]:]
                    incr = len(ent1[i][2])*2 + 5
                    sentence_labels =  sentence_labels[:ent2[i][1][0]+incr] + "[" + ent2[i][2] + "]" + sentence_labels[ent2[i][1][0]+incr:ent2[i][1][1]+incr] + "[/" + ent2[i][2] + "]" + sentence_labels[ent2[i][1][1]+incr:]
                    
                    #split_sentence_labels = re.split(r'(?<=\.)\s*', sentence_labels)
                    split_sentence_labels = re.split(r'(?<=[.])\s*|\.\s*', sentence_labels)
                    # Define the tags to look for
                    tags_to_find = ['ORG', 'PERSON', 'GPE']
                    # Pick the sentence containing the specified tags
                    #selected_sentence_labels = next((s for s in split_sentence_labels if any(tag in s for tag in tags_to_find)), None)
                    selected_sentence_labels = [s for s in split_sentence_labels if any(tag in s for tag in tags_to_find)]
                    cleaned_sentence = ' '.join(selected_sentence_labels)
                    # Add a dot at the end if it doesn't already end with one
                    if not cleaned_sentence.endswith('.'):
                        cleaned_sentence += '.'

                    #sentences.append(cleaned_sentence)
                    sentences_labels.append(cleaned_sentence)
                    
                elif ent1[i][1][0] > ent2[i][1][0]:
                    sent =  result['text'][:ent2[i][1][0]] + "[E2]" + result['text'][ent2[i][1][0]:ent2[i][1][1]] + "[/E2]" + result['text'][ent2[i][1][1]:]
                    sent =  sent[:ent1[i][1][0]+9] + "[E1]" + sent[ent1[i][1][0]+9:ent1[i][1][1]+9] + "[/E1]" + sent[ent1[i][1][1]+9:]
                    # # Use regular expressions to split the sentence
                    # split_sentences = re.split(r'(?<=\.)\s*', sent)
                    # # Pick the sentence containing [E1] and [E2]
                    # selected_sentence = next((s for s in split_sentences if "[E2]" in s and "[E1]" in s), None)
                    # sentences.append(selected_sentence)
                    
                    # Combine the operations in a single regular expression
                    split_sentences = re.split(r'(?<=[.])\s*|\.\s*', sent)
                    # Specify the tags to look for
                    tags = ['E1', 'E2']
                    # Pick the sentence containing the specified tags
                    selected_sentences = [s for s in split_sentences if any(tag in s for tag in tags)]
                    cleaned_sentence = ' '.join(selected_sentences)
                    # Add a dot at the end if it doesn't already end with one
                    if not cleaned_sentence.endswith('.'):
                        cleaned_sentence += '.'
                    sentences.append(cleaned_sentence)
                    
                    
                                        
                                                                          
                    sentence_labels =  result['text'][:ent2[i][1][0]] + "[" + ent2[i][2] + "]" + result['text'][ent2[i][1][0]:ent2[i][1][1]] + "[/" + ent2[i][2] + "]" + result['text'][ent2[i][1][1]:]
                    sentence_labels =  sentence_labels[:ent1[i][1][0]+9] + "[" + ent1[i][2] + "]" + sentence_labels[ent1[i][1][0]+9:ent1[i][1][1]+9] + "[/" + ent1[i][2] + "]" + sentence_labels[ent1[i][1][1]+9:]
                    #sentences_labels.append(sentence_labels)
                    
                    split_sentence_labels = re.split(r'(?<=[.])\s*|\.\s*', sentence_labels)
                    # Define the tags to look for
                    tags_to_find = ['ORG', 'PERSON', 'GPE']
                    # Pick the sentence containing the specified tags
                    #selected_sentence_labels = next((s for s in split_sentence_labels if any(tag in s for tag in tags_to_find)), None)
                    selected_sentence_labels = [s for s in split_sentence_labels if any(tag in s for tag in tags_to_find)]
                    cleaned_sentence = ' '.join(selected_sentence_labels)
                    # Add a dot at the end if it doesn't already end with one
                    if not cleaned_sentence.endswith('.'):
                        cleaned_sentence += '.'

                    #sentences.append(cleaned_sentence)
                    sentences_labels.append(cleaned_sentence)
                    
                   
    df = pd.DataFrame ({'sentences':sentences, 'sentences_labels':sentences_labels, 'Subject': subject, 'Object': object, 'relations':relations, 'labels':labels, 'filename':filenames})
    return df
    
#checking duplicates
def check_duplicates(csv_file, column_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Check for duplicates in the specified column
    duplicates = df[df.duplicated(subset=[column_name], keep=False)]

    if not duplicates.empty:
        print(f'Duplicates found in the "{column_name}" column:')
        print(duplicates)
    else:
        print(f'No duplicates found in the "{column_name}" column.')

# Example usage
#check_duplicates('path/to/your/train.csv', 'sentences')
    
# Get entities
def get_entities(sentence):
    ent = []
    for sent in sentence['entities']:
        ent.append([sent['id'], sentence['text'] [sent['start_offset']:sent['end_offset']], [sent['start_offset'],sent['end_offset']], sent['label']])
    return ent

# Get relationship between entities
def get_relation(sentence, ent):
    ent1, ent2, relation = [],[],[]
    for sent in sentence['relations']:
        relation.append(sent['type'])
        for i in ent:
            if i[0] == sent['from_id']:
                ent1.append([i[1],i[2],i[3]])
            elif i[0] == sent['to_id']:
                ent2.append([i[1],i[2],i[3]])
    return ent1, ent2, relation

# Relate relationships to ids
def Relations_Mapper(relations):
    rel2idx = {}
    idx2rel = {}

    sd_relations = {'employedBy': 2,
                    'managerOf': 0,
                    'locatedAt': 1,
                    'noRelation': 3
                    }

    # n_classes = 0
    for relation in relations:
            rel2idx[relation] = sd_relations[relation]

    for key, value in rel2idx.items():
        idx2rel[value] = key

    return rel2idx, idx2rel

def add_ids(df):
    df['relations_id']= df['relations'].map(Relations_Mapper(df['relations'])[0])
    relations = Relations_Mapper(df['relations'])[1]
    return df

def train_test_split (df):
    test = df.sample(frac=0.2, random_state=42)
    train = df.drop(test.index)
    return train, test


if __name__ == '__main__':
    # Get the path where the json file directory has been created from doccano 
    path= os.path.join(os.getcwd(), 'jsonl_files')

    # Create Dataframe 
    df = Dataframe(path)
    df = add_ids(df)
    # Split the dataframe into train and test
    test_df = df.sample(frac=0.2)
    train_df = df.drop(test_df.index)

    # Convert train and test DataFrames into csv files and zip them 
    with zipfile.ZipFile('train_test.zip', 'w') as csv_zip:
        csv_zip.writestr("train.csv", train_df.to_csv())
        csv_zip.writestr("test.csv", test_df.to_csv())
import zipfile

# Create a ZipFile object
with zipfile.ZipFile('train_test.zip', 'r') as zip_ref:
    # Specify the file to extract
    #file_to_extract = 'train.csv'
    zip_ref.extractall()
    
#Check duplicates and remove
def keep_unique_sentences(csv_file, column_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Mark duplicates as True for all occurrences except the first one
    df['is_duplicate'] = df.duplicated(subset=[column_name], keep='first')

    # Keep only the unique sentences (where 'is_duplicate' is False)
    df_unique = df[~df['is_duplicate']]

    # Drop the 'is_duplicate' column as it's not needed anymore
    df_unique = df_unique.drop(columns=['is_duplicate'])

    # Save the DataFrame with unique sentences back to the CSV file
    df_unique.to_csv(csv_file, index=False)

# Example usage
keep_unique_sentences('train.csv', 'sentences')
 
              
np.save('idx2rel.npy', Relations_Mapper(df['relations'])[1])