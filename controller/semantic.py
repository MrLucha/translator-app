class Semantic():
    def __init__(self,tokens):
        self.result=True
        self.tokens=tokens
        self.person=""

        # Verificar en que persona esta la oracion (Primera/Tercera)
        for word, tag in tokens:
            if (tag=="PRP" and word.lower() in ['he', 'she', 'it','they']) or tag=="NNP":
                self.person = "third"
                break
            elif tag=="PRP" and word.lower() in ['i']:
                self.person="first"
                break
            elif tag=="PRP" and word.lower() in ['you']:
                self.person="second"
                break

        # Verificar la forma (Afirmativa, Negativa, Question)

        #print(self.person)

        def first_person():
            #print("First person")
            # Validando que no haya auxiliares terceras personas (does, doesn't)
            for word,tag in tokens:
                if tag in ['VBZ','NVBZ']:
                    self.result=False
                    break
                    #print("error semantico")

        def second_person():
            pass
            #print("Second person")

        def third_person():
            gender=""
            # Validando que no haya auxiliares primera persona (do,don't)
            #print("Third person")
            for word,tag in tokens:
                if tag in ['DO','NDO']:
                    self.result = False
                    break

            # Asignando genero
            for word,tag in tokens:
                if tag=="PRP" and word=="he":
                    gender="masculine"
                if tag=="PRP" and word=="she":
                    gender="femenine"
                if tag=="PRP" and word=="it":
                    gender="it"

            # Validando posesivos segun su genero
            for word,tag in tokens:
                if(gender=="masculine" and (word=="her" or word=="it's")):
                    self.result = False
                    break

                if (gender == "femenine" and (word == "his" or word == "it's")):
                    self.result = False
                    break

                if (gender == "masculine" and (word == "her" or word == "his")):
                    self.result = False
                    break

        def opcion_default():
            print("Has seleccionado una opción inválida")

        # Crear un diccionario donde las claves son las opciones y los valores son las funciones a ejecutar
        switch = {
            "first": first_person,
            "second": second_person,
            "third": third_person
        }


        # Ejecutar la función correspondiente a la opción seleccionada, o la función default si no existe
        switch.get(self.person, opcion_default)()

    def get_result(self):
        return self.result