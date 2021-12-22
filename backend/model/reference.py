import json


# TODO what is this class for?
class Reference():
    """
    A representation of a reference from an inflected form to the term that it comes from.
    """

    def __init__(self, word, lemma, **kwargs):
        """
        Term constructor, which instantiates the object and checks its validity in the language's semantic model.
        """
        self.word = word
        self.lemma = lemma


    def toJson(self):
        """
        Convert the Term object into a JSON object. 
        """
        return json.dumps(self.__dict__, sort_keys=True, indent=4)