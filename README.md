# Orcawise NLP Project

## Relation Extraction
NLU project is developed by [Orcawise](https://www.orcawise.com/) NLP team,in which my focus is on uncovering **named entity relations (NER)** within the data, leading to the extraction of valuable insights and knowledge. We achieve this by employing both a pre-defined model (StanfordOpenIE) and a fine-tuned model (CustomBertModel). Our primary goal is to extract relations from sentences, specifically targeting four key relationships: managerOf, employedBy, locatedAt, and noRelation.
## Table of Contents
* [Preprocess the data](https://github.com/Pravitha92/Orcawise_NLP_Project/blob/main/README.md#preprocecess-the-data)
* [Predefined Model(StanfordOpenIE)](https://github.com/Pravitha92/Orcawise_NLP_Project/blob/main/README.md#predefined-modelstanfordopenie)
* [Finetuned Model(CustomBertModel)](https://github.com/Pravitha92/Orcawise_NLP_Project/blob/main/README.md#finetuned-modelcustombertmodel)
* [Database](https://github.com/Pravitha92/Orcawise_NLP_Project/blob/main/README.md#database)
* [How to Run the code](https://github.com/Pravitha92/Orcawise_NLP_Project/blob/main/README.md#how-to-run-the-code)
  
## Preprocecess the data
The data collection process involves collecting different articles then doing annotation using Doccano to extract information pertaining to entities such as PERSON, ORG, and GPE within sentences. Subsequently, the annotated data can be processed using `doccano_into_csv.py` to convert the JSONL file into a CSV format. This is followed by the execution of `Class_final_code_cleaning.py`, `augment_cleaned.py` and `Combination_spin_class.py` to produce the final dataset for training the model.

## Predefined Model(StanfordOpenIE)
The `StanfordOpenIE` library is a powerful tool for extracting Open Information Extraction (OpenIE) triples from text. OpenIE involves identifying and extracting relationships between entities in a sentence without relying on pre-defined relationship labels. 

To use the `StanfordOpenIE` library, it needs to be installed following dependencies.
1. pip install OpenIE
2. Install java in windows using the link http://jdk.javTa.net/archive/
3. Clone the core nlp model using the link.
https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip
and unzip it. Then set the path to unzipped file in environment variables.
4. Use IDE Pycharm or VS code
## Finetuned Model(CustomBertModel)
`CustomBertModel` is a Python class designed for relation extraction using a fine-tuned BERT (Bidirectional Encoder Representations from Transformers) model. This class allows users to predict relationships between entities in a given sentence, specifically tailored for four predefined relations: 'noRelation', 'employedBy', 'managerOf', and 'locatedAt'.
  #### Dataset:
* Extracting data from pages and manually annotated articles using doccano.
* Applying data cleaning, data augmentation, rephrasing, etc., on text data. Finally, obtained over 4000 sentences.
#### Process:
* Finetuning the model using BERT model and saving the model using checkpoints.
* Using these checkpoints for testing real time data.
#### Dependencies:
* Pytorch
* numpy
* transformers
* BertTokenizer
* BertForSequenceClassification

## Database
Here we used **phpmyadmin** sql for connecting python with database.             
### Installation / Dependencies.
* pip install mysql-connector-python
### Process
 * Ensure connection to MySQL database with the following details.
 * Create the Table.
 * Takes user input for a sentence.
 * Processes the input sentence using the Stanford OpenIE library (OpenIEExtractor) to extract predefined relations.
 * Processes the input sentence using a custom BERT model (CustomBertModel) to predict fine-tuned relations.
## How to Run the Code
1. Pretrained OpenIE Model:
   * Install the requirement library `pip install OpenIE'
   * Install [Java](http://jdk.javta.net/archive/) in windows.
   * Clone the [core NLP model](https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip) and unzip it. Then set the path to unzipped file in environment variables.
   * Run the `nlu_pretrained_model.py` file to initialize and use the OpenIE model.
   * from nlu_pretrained_model import OpenIEExtractor
![image](https://github.com/Pravitha92/Orcawise_NLP_Project/assets/93678721/b85135af-1332-48c7-871c-23d8a54adbe6)
2. Custom BERT Model:
   * Run the `nlu_custom_model(1).py` file to initialize and use the Custom BERT model.
     ![image](https://github.com/Pravitha92/Orcawise_NLP_Project/assets/93678721/f8fe1c2e-0401-4c38-8bf2-fe94125bdae7)
3. Connect to database:
   * Database Used: **phpmyadmin** SQL
   * Connection from Python with Database:
      * The database connection is established using the `mysql.connector` library.
      * Connection details:
        * Host: localhost
        * Port: 3306
        * User: root
        * Password: [Password]
        * Database: test_nlu
   * How to Execute the Code:
   Run the `connect_my_sql(1).py` file to connect to the database, create a table, store predictions, and close the connection.
![image](https://github.com/Pravitha92/Orcawise_NLP_Project/assets/93678721/679ec87f-dc16-4dc8-87ab-e7129056750a)
Make sure to replace placeholders such as 'path/to/your/checkpoint.ckpt' and '[Password]' with the actual paths and passwords.
4. Testing model with real-time data:
   Run the jupyter notebook `testing_custom_bert_on_real_time_data.ipynb` file to generalize the result of openie and the calculate the accuracy of the models' results.
   ![image](https://github.com/Pravitha92/Orcawise_NLP_Project/assets/93678721/93a6efc3-0c90-4c44-8d55-546f498edd87)

   
