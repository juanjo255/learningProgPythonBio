# Empezamos con los argumentos que se reciben
from curses import start_color
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
                print(self.taxones)
        if both == 2:
            print(self.matches_counter/self.general_counter, "%")
        return None

    def start_search(self) -> None:

        with open(file_name, "r") as file:
            filterFields = self.toFilter()

            # VARIABLE CONTROL
            filterFields_count = len(filterFields)
            print("FILTER, FIELDS/COMMANDS",
                    filterFields, self.fieldsOrCommands)

            while True:
                # con el ciclo while la variable linea toma una nueva linea cada ciclo
                line = file.readline()
                to_look = line.split(" ")
                
                # a las secuencias les agregamos el SQ para poder filtrarlas cuando se quiera
                if line.startswith(" "):
                    to_look[0]= "SQ"
                
                # inicio de la linea
                start_of_line= to_look[0]
                
                # FIN DEL RECORRIDO
                if not (line):
                    # Check if the user entered commands
                    if any(stdin in ["COUNTALL", "COUNT", "TAXONS"] for stdin in self.fieldsOrCommands):
                        self.Commands()
                    break

                # FINAL DE UN REGISTRO
                if line.startswith("//"):
                    self.general_counter += 1

                    # si se ha vaciado el diccionario imprimimos y borramos
                    if not (filterFields_count):
                        self.matches_counter += 1
                        print(*self.successed)

                    self.successed.clear()
                    #if self.general_counter == 2:
                    #    break

                    # renovamos variables de movimiento y de control
                    filterFields_count = len(filterFields)
                    continue

                # ¿la linea hace parte de la campos filtro?
                if start_of_line in filterFields:
                    if filterFields[to_look[0]] in to_look:
                        # eliminamos una unidad a la variable control
                        # a medida que hacen match
                        filterFields_count -= 1

                # vamos agregando los campos que el usuario eligio ver. si no eliguió se agregan todos
                # si TAXONS esta entre los comandos se saca el total de OC
                if "TAXONS" in self.fieldsOrCommands:
                    if line.startswith("OC"):
                        to_look = [i.strip() for i in to_look if i]
                        for i in to_look[1:]:
                            if i in self.taxones:
                                self.taxones[i]+= 1
                            else:
                                self.taxones[i]= 1
                    continue

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
