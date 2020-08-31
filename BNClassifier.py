from word_count import Counter
from stopwords import stopwords
import re
import unicodedata



class Classifier():
    
    #Constructor taking an instance of word_count.py for each set and initializing all values necessary for probabilities calculations
    def __init__(self, count_set_A, count_set_B):
        self.count_set_A = count_set_A
        self.class_A = count_set_A.get_classification()
        
        self.count_set_B = count_set_B
        self.class_B = count_set_B.get_classification()
        
        # Recurrent words for set A extracted and stored in a dict in order to be able to check if they are present in messages
        self.recurrent_words_A = {}
        for item in self.count_set_A.get_recurrent_words():
            self.recurrent_words_A[item[0]] = item[1]
            
            
        self.voc_A = count_set_A.get_voc()
        self.voc_B = count_set_B.get_voc()
        
        
        self.size_A = self.count_set_A.get_size()
        self.words_A = self.count_set_A.get_words()
        self.size_B = self.count_set_B.get_size()
        self.words_B = self.count_set_B.get_words()
        
        self.total_set_size = self.size_A + self.size_B
        
        self.prob_A = self.size_A / self.total_set_size
        self.prob_B = self.size_B / self.total_set_size
 
                
    
    #Function that evaluates messages individually and returns the prediction as the classification for set A or B
    def evaluate_message(self, message):        
        matches = {}
        tempA = 1
        tempB = 1
        
        for word in re.findall('\s([a-zA-Z]+)\s', message):
            word = re.sub('\n','', word)
            word = re.sub('\t','', word)
            word = unicodedata.normalize("NFKD", word)   
            if word.lower() in self.recurrent_words_A.keys():
                tempA = tempA * (self.recurrent_words_A[word.lower()] / self.words_A)
                if word.lower() in self.voc_B.keys():
                    tempB = tempB * (self.voc_B[word.lower()] / self.words_B)
                else:
                    tempB = tempB * (1 / self.total_set_size)            
            
        prob_a = tempA * self.prob_A
        prob_b = tempB * self.prob_B
        
        if(prob_a > prob_b):
            return self.class_A
        else:
            return self.class_B
        
        
            
    
    def evaluate_data_set(self, dataset):
        correct_outputs = 0
        
        for i in range(len(dataset)):
            
            classification = dataset['classification'][i]
            
            output = self.evaluate_message(dataset['message'][i])
            
            if classification == output:
                correct_outputs += 1
                
        accuracy = correct_outputs / len(dataset)
        
        print(str(correct_outputs) + ' properly classified out of ' + str(len(dataset)) + ' , accuracy -> '+ str(accuracy))
            
        
        
    #Return the vector containing the words to be tested within the messages    
    def get_words_vector(self):
        return self.words_vector
        
    
                    