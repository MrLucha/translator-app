import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS


class Lexer():
    def __init__(self,sentence):
        self.sentence=sentence.lower()

    def lexer(self):
        aux=[]

        # Cargando modelo de lenguaje
        nlp = spacy.load("en_core_web_sm")

        # Recorriendo elemento por elemento la cadena
        for element in self.sentence.split():
            # Tokenizando elemento
            doc = nlp(element)

            # Agregar una excepción para el símbolo de apóstrofe
            infixes = (
                    LIST_ELLIPSES
                    + LIST_ICONS
                    + [
                        r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                        ),
                        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                        r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=r"[-~]"),
                        r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
                    ]
            )
            infix_re = spacy.util.compile_infix_regex(infixes)
            nlp.tokenizer = Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)

            # Sacando tipo de token y lexema
            for token in doc:
                word = token.text
                pos = token.pos_
                tag = token.tag_

                # Detectando errores lexicos
                if self.detect_err(word) != None:
                    tag='error'

                # Identificando palabras clave (do,don't,doesn't,not)
                key_word=self.detect_key_words(word)
                if key_word != None:
                    tag=key_word
                lista=[word,tag]
                aux.append(lista)

        return aux


    def detect_err(self,word):
        #print("word es",word)
        caracteres=['ñ','¿','¡']
        for c in caracteres:
            if c in word:
                return 'error'


    def detect_key_words(self,sentence):
        if sentence=="do":
            return 'DO'
        elif sentence=="don't":
            return 'NDO'
        elif sentence=="doesn't":
            return 'NVBZ'
        elif sentence=="not":
            return 'NOT'
        elif sentence=="?":
            return 'QUESTION_MARK'
        else:
            return None