""" Data cleaning """
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
import pickle
import location
import nltk

class DataWrangling():
    """ defining the data cleaning class"""
    def __init__(self):
        self.Count_vect = CountVectorizer()
        self.tfidf = TfidfVectorizer()
        self.punct = [',', '.',':', '(', ')', '-', '#', '|', '[', ']', '=', ',', 'for', 'your', 'team', 'to', 'on', 'the',
                 '.', 'hi', 'thanks', 'regards']
        self.stop = stopwords.words('english')
        self.stop = self.punct + self.stop
        self.loc = location.DataLocations()


    def preprocessing(self,Service_requests):
        """ Combining the Application column and Description column into one column and cleaning
        URL's, usernames and words with numbers using regex"""
        Service_requests = Service_requests[~Service_requests['Description'].isna()]
        Service_requests["Application_join"] = Service_requests["Application"].apply(lambda x: nltk.word_tokenize(x))
        Service_requests.Application_join = Service_requests.Application_join.apply(lambda x: ''.join(x))
        Service_requests['Description'] = Service_requests['Description'].astype(str)
        Service_requests['combined'] = Service_requests.Application_join + ' ' + Service_requests.Description
        Service_requests['combined'] = Service_requests['combined'].apply(
            lambda x: re.sub('\d+\w+|\w+\d+|\d+|', '', x))
        Service_requests['combined'] = Service_requests['combined'].apply(lambda x: re.sub('https?://\S+', '', x))
        Service_requests['combined'] = Service_requests['combined'].apply(lambda x: re.sub("@\S+", "", x))
        Service_requests['combined'] = Service_requests['combined'].apply(
            lambda x: re.sub('(\w+\.(\w+\.)*\w+)', '', x))
        return Service_requests

    def tokenizeandcleanData(self,Service_requests):
        """ Converting to lower case, word tokenizing and removing stopwords"""
        Service_requests['combined'] = Service_requests['combined'].str.lower()
        Service_requests['word_tokens'] = Service_requests['combined'].apply(lambda x: nltk.word_tokenize(x))
        Service_requests['tokens_withoutstop'] = Service_requests['word_tokens'].apply(
            lambda x: [item for item in x if item not in self.stop])
        Service_requests.reset_index(inplace=True)
        Service_requests.drop(columns='index', inplace=True)
        Service_requests.tokens_withoutstop = Service_requests.tokens_withoutstop.apply(lambda x: ' '.join(x))
        return Service_requests

    def tfidf_fit(self,input):
        """ Fitting to the TFIDF and saving the pickle file"""
        path = self.loc.tfidf_location()
        tfidf_transform = self.tfidf.fit(input)
        pickle.dump(tfidf_transform, open(str(path) + "/TFIDF.pkl", "wb"))

    def tfidf_transform(self, input):
        """ loading the TFIDF pickle file and transforming"""
        path = self.loc.tfidf_location()
        Tf = pickle.load(open(str(path) + "/TFIDF.pkl", 'rb'))
        return (Tf.transform(input))

