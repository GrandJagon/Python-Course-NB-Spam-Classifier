import re
from stopwords import stopwords
import unicodedata

#Class responsible for words extracting and creating the vocabulary that will be used for probabilities
class Counter:
    
    # Dict for the vocabulary and list for the occurence of each word is declared in constructor as well as a list
    # of the most recurrent words in the set
    def __init__(self):
        self.voc = {}
        self.words = 0
        self.occurences = []
        self.recurrent_words = []
        self.classification = ''
        self.size = 0
        
        # Variable that will define how many words are tken into account for the vocabulary
        self.awo = 105
        
        for i in range(0, self.awo):
            self.recurrent_words.append(['',0])
        

    
    # Function responsible to extract, clean and count all the words
    def fit_set(self, data, classification):
        self.classification = classification
        temp = []
        # The content is cleaned and the words stored in a temporary list that we sort
        for message in data:
            self.size += 1
            words = re.findall('\s([a-zA-Z]+)\s', message)
            for word in words:
                word = re.sub('\n','', word)
                word = re.sub('\t','', word)
                word = unicodedata.normalize("NFKD", word)
                if word.lower() not in stopwords and len(word) < 20:
                    temp.append(word.lower())   
                    self.words += 1
        temp.sort()
        
        # Each word is stored in a dict in a form {'word' : [index, occurence]} and in a list of occurences sorted
        # by index
        index = 0
        for i in range(len(temp)):
            if temp[i] in self.voc:
                self.voc[temp[i]][1] += 1
                self.occurences[self.voc[temp[i]][0]] += 1
            else:
                self.voc[temp[i]] = [index, 1]
                self.occurences.append(1)
                index += 1
                
          
    #Function parsing the words and returning the self.owa  with the most occurences
    def get_recurrent_words(self):
         if self.recurrent_words[0][0] == '':
            for key in self.voc.keys():
                for a in range(0, self.awo):
                    if self.voc[key][1] >= self.recurrent_words[(self.awo - 1) - a][1]:
                        if self.voc[key][1] > self.recurrent_words[(self.awo - 2)  - a][1]:
                            if a == (self.awo - 1) :
                                self.recurrent_words[(self.awo - 1)  - a][0] = key
                                self.recurrent_words[(self.awo - 1)  - a][1] = self.voc[key][1]   
                            pass
                        else:
                            for i in range(0, a):
                                self.recurrent_words.insert(self.awo - a, self.recurrent_words.pop((self.awo - 1) - a)) 
                            self.recurrent_words[(self.awo - 1)  - a][0] = key
                            self.recurrent_words[(self.awo - 1)  - a][1] = self.voc[key][1]
                            break
                  
         return self.recurrent_words
     
        
    
    
    def get_voc_size(self):
        return len(self.voc)
    
    def get_voc(self):
        return self.voc
    
    def get_classification(self):
        return self.classification
    
    def get_awo(self):
        return self.awo
    
    def get_words(self):
        return self.words
    
    def get_size(self):
        return self.size
        

        
        
    