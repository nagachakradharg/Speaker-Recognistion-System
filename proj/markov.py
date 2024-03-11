from hashtable import Hashtable
from math import log

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    """
    Markov is a class to build markov model 

    The __init__ method takes in k, text, use_hashtable as instance attributes

    Atributes:
        k (int): order K
        text (str): input data for model
        use_hashtable (bool): indiicates the implementation
    """
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.model = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO) if use_hashtable else {}
        self.order = k
        self.text = text
        self.use_hashtable = use_hashtable
        self.unique_chars = set()
        self.create_model()

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        log_prob = 0
        text = s + s[:self.order]

        for index in  range(len(s)):
            # substrings of length k and k + 1
            text_k = text[index: index + self.order]
            text_k1 = text[index: index + self.order + 1]

            # get values
            if self.use_hashtable:
                constant_n = self.model[text_k]
                constant_m = self.model[text_k1]              
            else:
                constant_n = self.model.get(text_k, 0)
                constant_m = self.model.get(text_k1, 0)

            # probability with laplace smoothing
            log_prob += log((constant_m + 1) / (constant_n + len(self.unique_chars)))
        
        return log_prob
    
    def create_model(self):
        """
        Function to create the markov model using the instance attribute text.
        """
        text = self.text + self.text[:self.order]

        for index, char in enumerate(self.text):
            self.unique_chars.add(char)
            # substrings of length k and k + 1
            text_k = text[index: index + self.order]
            text_k1 = text[index: index + self.order + 1]

            # if implementation is dict, update the keys with default values to prevent error
            if not self.use_hashtable:
                self.model.setdefault(text_k, 0)
                self.model.setdefault(text_k1, 0)

            self.model[text_k] += 1
            self.model[text_k1] += 1


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    # Markov instaces of input speeches
    model_speech1 = Markov(k, speech1, use_hashtable)
    model_speech2 = Markov(k, speech2, use_hashtable)

    # probabilities of speech3 belonging to speaker A or B respectively
    prob1 = model_speech1.log_probability(speech3) / len(speech3)
    prob2 = model_speech2.log_probability(speech3) / len(speech3)

    return (prob1 , prob2, 'A' if prob1 > prob2 else 'B')
