import os
import sys
class queryPro:
    def __init__(self, file_name, query, fieldsOrCommands) -> None:
        self.file_name = file_name
        self.query = query
        self.fieldsOrCommands = fieldsOrCommands + \
            [False] if "SHOWALL" in fieldsOrCommands else fieldsOrCommands
        self.successed = list()
        self.general_counter = 0
        self.matches_counter = 0
        self.taxones = {}

    def toFilter(self) -> list:
        filterStore = {i.split(".in.")[1].upper(): i.split(
            ".in.")[0] for i in self.query.split(".and.")}
        return filterStore

    def printCommands(self) -> None:
        # Miramos si el usurio ingreso comandos o campos. Si ingresó comandos
        # pasa un filtro para las posibilidades que hay para es filtro
        both = 0
        for i in self.fieldsOrCommands:
            if i == "COUNTALL":
                both += 1
                print(self.general_counter)
            elif i == "COUNT":
                print(self.matches_counter)
                both += 1
            elif i == "TAXONS":
                print(self.taxones)
        if both == 2:
            print(round(self.matches_counter/self.general_counter*100, 3),"%")
        return None

    def fasta (self) -> None:
        header= self.successed [:3]
        seq= self.successed [4:]
        final_seq = ""
        # recorremos encabezado de fasta, pulimos e imprimimos
        for line in header:
            line = line.strip()
            if line.startswith("ID"):
                line_split=[ i for i in line.split(" ") if i]
                line= " ".join(line_split[:2])
            print (line[:2], line [2:].strip(),sep="=", end=";")
        print ("")
        
        #recorremos secuencias, limitamos a 80 caracteres e imprimimos
        for line in seq:
            line= line[2:].strip().split(" ")
            line = "".join(line)
            final_seq += line

        for i in range (0, len(final_seq),80):
            print (final_seq [i:80+i])
        return None

    def start_search(self) -> None:

        with open(file_name, "r") as file:
            filterFields = self.toFilter()

            # VARIABLE CONTROL
            filterFields_copy = filterFields.copy()
            print("FILTER, FIELDS/COMMANDS",
                    filterFields, self.fieldsOrCommands)

            while True:
                # con el ciclo while la variable linea toma una nueva linea cada ciclo
                line = file.readline()

                # a las secuencias les agregamos el SQ para poder filtrarlas cuando se quiera
                if line.startswith(" "):
                    line = "SQ" + line

                # inicio de la linea
                start_of_line = line[:2]

                # FIN DEL RECORRIDO
                if not (line):
                    # Check if the user entered commands
                    if "FASTA" in self.fieldsOrCommands:
                        pass
                    elif any(stdin in ["COUNTALL", "COUNT", "TAXONS"] for stdin in self.fieldsOrCommands):
                        self.printCommands()
                    break

                # FINAL DE UN REGISTRO
                if line.startswith("//"):
                    self.general_counter += 1
                    
                    # si se ha vaciado el diccionario
                    # entonces pasa a lo demas
                    if not (filterFields_copy):
                        self.matches_counter += 1
                        if "TAXONS" in self.fieldsOrCommands:
                            for OC in self.successed:
                                OC = [i for i in OC.strip().split(" ")[1:] if i]
                                for val in OC:
                                    if not (val in self.taxones):
                                        self.taxones[val] = 0
                                    self.taxones[val] += 1
                        elif "FASTA" in self.fieldsOrCommands:
                            self.fasta()
                        elif self.successed:
                            print(*self.successed)
                            
                    self.successed.clear()

                    # if self.matches_counter == 2:
                    #   break

                    # renovamos variables de movimiento y de control
                    filterFields_copy = filterFields.copy()
                    continue

                # ¿el amcabezado hace parte de los campos filtro?
                if start_of_line in filterFields_copy:
                    if filterFields_copy[start_of_line] in line:
                        # eliminamos el campo de busqueda de la variable control a medida que hacen match
                        del filterFields_copy[start_of_line]

                # vamos agregando los campos que el usuario eligio ver. si no eliguió se agregan todos
                # si TAXONS esta entre los comandos se saca el OC
                if "TAXONS" in self.fieldsOrCommands and line.startswith("OC"):
                    self.successed.append(line)
                else:
                    # Si hay campos para mostrar los agregamos
                    # sino  agregamos todos los campos
                    if not (self.fieldsOrCommands[-1]):
                        self.successed.append(line)
                    elif start_of_line in self.fieldsOrCommands:
                        self.successed.append(line)
            return None

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except:
        print("File name is required")
        quit()

    if not (os.path.isfile(sys.argv[1])):
        print("The file does not exist")
        quit()

    try:
        query = sys.argv[2]
        fieldsOrCommands = sys.argv[3:]
        if fieldsOrCommands:
            if "FASTA" in fieldsOrCommands:
                fieldsOrCommands = ["FASTA", "ID","AC","OS", "SQ"]
            else:
                fieldsOrCommands = sys.argv[3:]
        else:
            fieldsOrCommands = ["SHOWALL"]
        myQuery = queryPro(file_name, query, fieldsOrCommands)
        myQuery.start_search()
    except:
        print("Query is required")
        quit()

