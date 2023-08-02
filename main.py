from controller.lexer import Lexer
from controller.parser import Parser
from controller.semantic import Semantic
from googletrans import Translator
from gingerit.gingerit import GingerIt
class Main():

    def __init__(self,sentence):
        self.sentence=sentence.lower()
        self.tokens=[]
        self.resultado_sintactico=""
        self.resultado_semantico=None
        self.traduccion=""
        self.sugerencia=""
        self.list_banderas=[]
        self.band_tokens=False
        self.band_sintaxis=False
        self.band_semantica=False
        self.band_traduccion=False

        # Obteniendo tokens
        lexer = Lexer(sentence)
        self.tokens = lexer.lexer()

        # Comprobando si el analizador lexico contiene o no errores
        if (self.check_lex_err(self.tokens) == False):
            self.band_tokens=True

            # En caso de que no, se manda al analisis sintactico
            lista = [elemento[1] for elemento in self.tokens]
            parser = Parser(lista)

            # Obtenemos el resultado del analisis sintactico
            self.resultado_sintactico = parser.get_result()

            # Si el sintactico no tiene errores, mandar al analizador semantico
            # print("antes")
            print("Sintactico",self.resultado_sintactico)
            if self.resultado_sintactico == 'Ok':
                print("enviando al semantico")
                semantic = Semantic(self.tokens)

                # Obteniendo el resultado del analisis semantico
                self.resultado_semantico=semantic.get_result()

                # Si el resultado es True (sin errores semanticos) hacer la traduccion
                if self.resultado_semantico==True:
                    #Descomentar
                    self.traduccion=self.translate(self.sentence)
                else:
                    self.traduccion = "No disponible"
            else:
                self.traduccion = "No disponible"
        else:
            self.resultado_sintactico = "No disponible"
            self.traduccion = "No disponible"

        # Aqui hacer la sugerencia
        self.sugerencia = self.suggerence(self.sentence)
        print(self.sugerencia)
        if self.sugerencia != 0:
            print(self.sugerencia)
        else:
            print("No hay sugerencias")


    def check_lex_err(self,tokens):
        for token in tokens:
            if token[1]=='error':
                return True
        return False

    def translate(self,sentence):
        translator = Translator()
        # Traducir un texto de un idioma a otro
        translation = translator.translate(sentence, dest="es")
        result = translation.text
        return result

    def get_results(self):
        resultado_sintactico=""
        if self.resultado_sintactico=="Ok":
            self.band_sintaxis=True
            resultado_sintactico="Sintaxis corecta"
        else:
            resultado_sintactico=self.resultado_sintactico
        resultado_semantico=""
        # print(type(self.resultado_semantico))
        # print(self.resultado_semantico)
        if self.resultado_semantico==True:
            self.band_semantica=True
            self.band_traduccion=True
            resultado_semantico="Semantica correcta"
        elif self.resultado_semantico==False:
            resultado_semantico="No se puede traducir. Verifica su semantica"
        elif self.resultado_semantico==None:
            resultado_semantico="No se puede traducir. Verifica su semantica"

        # Traducir lista de tokens al español
        tokens_traducidos=self.translate_tokens()

        self.list_banderas=[self.band_tokens,self.band_sintaxis,self.band_semantica,self.band_traduccion]
        list=[tokens_traducidos,resultado_sintactico,resultado_semantico,self.traduccion]
        return list


    def translate_tokens(self):
        list_tokens=[]
        for element in self.tokens:
            lexema=element[0]
            token=element[1]
            if (token=="CC"):
                token= "Conjunción de coordinacion"
            elif token=="CD" 	:
              token= "Numero cardinal"
            elif token=="DT" 	:
              token= "Determinante"
            elif token=="EX" 	:
              token= "Existencial allí"
            elif token=="FW" 	:
              token= "Palabra extranjera"
            elif token=="IN" 	:
              token= "Preposición o conjunción subordinante"
            elif token=="JJ" 	:
              token= "Adjetivo"
            elif token=="JJR" :
              token= "Adjetivo comparativo"
            elif token=="JJS" :
              token= "Adjetivo superlativo"
            elif token=="LS" 	:
              token= "Marcador de elemento de lista"
            elif token=="MD" 	:
              token= "Modal"
            elif token=="NN" 	:
              token= "Sustantivo singular o masa"
            elif token=="NNS" :
              token= "Sustantivo"
            elif token=="NNP" :
              token= "Sustantivo propio singular"
            elif token=="NNPS":
              token= "Sustantivo propio plural"
            elif token=="PDT" :
              token= "Predeterminado"
            elif token=="POS" :
              token= "Final posesivo"
            elif token=="PRP" :
              token= "Pronombre personal"
            elif token=="PRP$":
              token= "Pronombre posesivo"
            elif token=="RB" 	:
              token= "Adverbio"
            elif token=="RBR" :
              token= "Adverbio comparativo"
            elif token=="RBS" :
              token= "Adverbio superlativo"
            elif token=="RP" 	:
              token= "Partícle"
            elif token=="SYM" :
              token= "Símbolo"
            elif token=="TO" 	:
              token= "To"
            elif token=="UH" 	:
              token= "Interjección"
            elif token=="VB" 	:
              token= "Verbo forma base"
            elif token=="VBD" :
              token= "Verbo tiempo pasado"
            elif token=="VBG" :
              token= "Verbo gerundio"
            elif token=="VBN" :
              token= "Verbo participio pasado"
            elif token=="VBP" :
              token= "Verbo presente que no es 3ra persona del singular"
            elif token=="VBZ" :
              token= "Verbo 3ra persona singular presente"
            elif token=="WDT" :
              token= "Wh-Determinante"
            elif token=="WP" 	:
              token= "Wh-Pronombre"
            elif token=="WP$" :
              token= "Wh-Pronombre posesivo"
            elif token=="WRB" :
              token= "Wh-Adverbio"
            else:
                print("no identificado")
            list_tokens.append([lexema,token])

        return list_tokens


    def get_bands(self):
        return self.list_banderas

    def suggerence(self,text):
        gingerit = GingerIt()
        text=gingerit.parse(text.lower())
        if(len(text['corrections'])!=0):
            return text['result']
        else:
            return 0

    def get_suggerence(self):
        return self.sugerencia
