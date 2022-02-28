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
            print(self.matches_counter/self.general_counter, "%")
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
                    if any(stdin in ["COUNTALL", "COUNT", "TAXONS"] for stdin in self.fieldsOrCommands):
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
                            print (self.successed)
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
                # si TAXONS esta entre los comandos se saca el total de OC
                if "TAXONS" in self.fieldsOrCommands and line.startswith("OC"):
                    self.successed.append(line)
                elif "FASTA" in self.fieldsOrCommands:
                    pass
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

    try:
        os.path.isfile(sys.argv[1])
    except:
        print("The file does not exist")
        quit()

    try:
        query = sys.argv[2]
        fieldsOrCommands = sys.argv[3:] if sys.argv[3:] else ["SHOWALL"]
    except:
        print("Query is required")
        quit()

    myQuery = queryPro(file_name, query, fieldsOrCommands)
    myQuery.start_search()
