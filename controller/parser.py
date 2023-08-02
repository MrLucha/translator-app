import nltk
from googletrans import Translator


class Parser:
    def __init__(self, tokens):

        self.result = ""

        # Define la gramática
        grammar = nltk.CFG.fromstring("""
            Sentence -> Affirmative | Negative | Question
            Affirmative -> Subject Verb Complement
            Negative -> Subject Negation Verb Complement
            Question -> Auxiliar Subject Verb Complement 'QUESTION_MARK'
            
            Subject -> 'PRP' | 'NNP'
            Verb -> 'VB' | 'VBZ'| 'DO'
            Complement -> Any | Any Complement
            
            Auxiliar -> 'DO' | 'VBZ'
            Negation -> Simple | Contract
            Simple -> Auxiliar 'NOT'
            Contract -> 'NDO' | 'NVBZ'
            
            Any -> 'CC'|'CD'|'DT'|'EX'|'FW'|'IN'|'JJ'|'JJR'|'JJS'|'LS'|'MD'|'NN'|'NNS'|'NNP'|'NNPS'|'PDT'|'POS'|'PRP'|'PRP$'|'RB'|'RBR'|'RBS'|'RP'|'SYM'|'TO'|'UH'|'VB'|'VBD'|'VBG'|'VBN'|'VBP'|'VBZ'|'WDT'|'WP'|'WP$'|'WRB'
            
        """)

        # Crea el analizador sintáctico
        parser = nltk.ChartParser(grammar)

        # print(tokens)
        try:
            # Ingresa los tokens al analizador
            tree = parser.parse(tokens)
            # Intenta obtener el siguiente elemento del generator
            next_element = next(tree)
            self.result = "Ok"
            # self.result=next_element
        except ValueError as e:
            err = str(e)
            # Crear una instancia del traductor
            translator = Translator()

            # Traducir un texto de un idioma a otro
            translation = translator.translate(err, dest="es")

            self.result = translation.text
        except StopIteration:
            # Si se genera una excepción StopIteration, el generator está vacío
            self.result = "Error de sintaxis"


    def get_result(self):
        return self.result


