class ModelError(Exception):
    """Base class for exceptions related to creating data objects in the language models"""


class LexemeError(ModelError):
    """Exception raised for errors in validating the state of a [Lexeme]

    Attributes:
        term (str): The lemma of the Lexeme being constructed.
        pos (PartOfSpeech): The part of speech of the Lexeme
        description (str): A description of the condition of creating the [Lexeme] that failed.
        arguments (dict): A dictionary containing the relevant information supplied for the construction of the [Lexeme].
        .
    """

    def __init__(self, lemma, pos, arguments, description):
        self.lemma = lemma
        self.pos = pos
        self.arguments = arguments
        self.description = description
        self.message = f'Failed to construct Lexeme for "{self.lemma}" - {self.description}'
        super().__init__(self.message)
