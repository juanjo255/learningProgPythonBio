# Empezamos con los argumentos que se reciben
import os
import sys


class queryPro:
    def __init__(self, file_name, query, fieldsOrCommands) -> None:
        self.file_name = file_name
        self.query = query
        self.fieldsOrCommands = fieldsOrCommands+[False] if "SHOWALL" in fieldsOrCommands else fieldsOrCommands
        self.successed = list()
        self.general_counter = 0
        self.matches_counter = 0

    def toFilter(self) -> list:
        filterStore = {i.split(".in.")[1].upper(): i.split(
            ".in.")[0] for i in self.query.split(".and.")}
        return filterStore

    def Commands(self) -> None:
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
                pass
        if both == 2:
            print(self.matches_counter/self.general_counter, "%")

        return None

    def start_search(self) -> None:
        with open(file_name, "r") as file:
            filterFields = self.toFilter()
            # una copia como control cuando termine de matchear
            filterFields_forRecord = filterFields.copy()
            print("FILTER, FIELDS/COMMANDS", filterFields)
            while True:

                # renovamos variable para tomar la siguiente linea en el archivo
                line = file.readline()

                # FIN DEL RECORRIDO
                if not (line):
                    # Check if the user entered commands
                    if self.fieldsOrCommands: 
                        if any(stdin in ["COUNTALL", "COUNT"] for stdin in self.fieldsOrCommands):
                            self.Commands()
                    break

                # tomamos todos las palabras de la linea
                to_look = [i.strip() for i in line.split(" ") if i]
                print (to_look)

                # FINAL DE UN REGISTRO
                if "//" in to_look:
                    self.general_counter += 1

                    # si se ha vaciado el diccionario imprimimos y borramos
                    if not (filterFields_forRecord):
                        self.matches_counter += 1
                        #print (*self.successed)
                    self.successed.clear()
                    if self.general_counter == 2:
                        break
                    
                    # renovamos variables de movimiento y de control
                    filterFields_forRecord = filterFields.copy()
                    continue

                # vamos agregando los campos que el usuario eligio ver. si no eliguió se agregan todos
                if not (all (self.fieldsOrCommands)):
                    self.successed.append(line)
                elif to_look[0] in self.fieldsOrCommands:
                    self.successed.append(line)

                try:
                    if filterFields_forRecord[to_look[0]] in to_look:
                        # limpiamos del fieldsOrCommands los campos a medida que hacen match que servira como control
                        del filterFields_forRecord[to_look[0]]
                except:
                    pass

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
