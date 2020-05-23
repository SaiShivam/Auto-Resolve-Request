
""" Setting up file locations related to model building """
import os
class DataLocations():
    """ Defining  file locations class """

    @classmethod
    def model_location(cls):
        return (os.getcwd()+'/src/models')

    @classmethod
    def tfidf_location(cls):
        """ tfidf pickle file location """
        return (os.getcwd()+'/src/models')

