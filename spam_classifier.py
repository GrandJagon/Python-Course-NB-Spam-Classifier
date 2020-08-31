import os
import io
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from word_count import Counter
from stopwords import stopwords
from BNClassifier import Classifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

spam_train = '/home/lucas/Documents/Python projects/MLCourse/emails/train/spam'
ham_train =  '/home/lucas/Documents/Python projects/MLCourse/emails/train/ham'

spam_test = '/home/lucas/Documents/Python projects/MLCourse/emails/test/spam'
ham_test =  '/home/lucas/Documents/Python projects/MLCourse/emails/test/ham'


# Function responsible to read each e-mail text file 
def readFile(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file = open(filepath, 'r', encoding='latin1')
            
            body = False
            lines = []
            
            for line in file:
                if body:
                    lines.append(line)
                else:
                    if line == '\n':
                        body = True
                        
            file.close()
            message = '\n'.join(lines)
            yield message, filepath

# Function responsible to read all the files and store the content in a pandas dataframe
def extractDataFromFile(path, classification):
    
    index = []
    data = []
    
    for message, filepath in readFile(path):
        soup = bs(message, features='lxml')
        index.append(filepath)
        data.append({'classification':classification, 'message' : soup.get_text()})
        
    return pd.DataFrame(data, index=index)


spams_train = extractDataFromFile(spam_train, 'spam')
hams_train = extractDataFromFile(ham_train, 'ham')
spams_test = extractDataFromFile(spam_test, 'spam')
hams_test = extractDataFromFile(ham_test, 'ham')


total_train_data = spams_train.append(hams_train)
total_test_data = spams_test.append(hams_test)

vectorizer = CountVectorizer()
count = vectorizer.fit_transform(total_train_data['message'].values)

classifier = MultinomialNB()
targets = total_train_data['classification'].values

classifier.fit(count, targets)

train_data_shuffled = total_train_data.sample(frac=1).reset_index(drop=True)

correct_outputs = 0


spam_count = Counter()
ham_count = Counter()

spam_count.fit_set(spams_train['message'], 'spam')
ham_count.fit_set(hams_train['message'], 'ham')

classifier = Classifier(spam_count, ham_count)

spams_train_shuffled = spams_train.sample(frac=1).reset_index(drop=True)
hams_train_shuffled = hams_train.sample(frac=1).reset_index(drop=True)
total_train_data_shuffled = total_train_data.sample(frac=1).reset_index(drop=True)

total_test_data_shuffled = total_test_data.sample(frac=1).reset_index(drop=True)

print("----------------------------TRAINING---------------------------------")
print("ALL DATA SET ->")
classifier.evaluate_data_set(total_train_data_shuffled)
print("SPAMS DATA SET")
classifier.evaluate_data_set(spams_train_shuffled)
print("HAMS DATA SET")
classifier.evaluate_data_set(hams_train_shuffled)
print("-----------------------------TEST-------------------------------------")
print("ALL DATA SET ->")
classifier.evaluate_data_set(total_test_data_shuffled)
print("SPAMS DATA SET")
classifier.evaluate_data_set(spams_test)
print("HAMS DATA SET")
classifier.evaluate_data_set(hams_test)

