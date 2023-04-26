import os
import pickle
import logging

os.system('cls' if os.name == 'nt' else 'clear')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('istorija.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('Programa paleista')

class Irasas:
    def __init__(self, suma: float, komentaras: str) -> str:
        """
        Inicializuoja 'Irasas' klasės objektą su nurodytais kintamaisiais.

        :param suma: 'Irasas' objekto suma.
        :type suma: float
        :param komentaras: 'Irasas' objekto komentaras.
        :type komentaras: str
        """
        self.suma = suma
        self.komentaras = komentaras


class Islaidos(Irasas):
    def __init__(self, suma: float, komentaras: str, gavejas: str):
        super().__init__(suma, komentaras)
        self.gavejas = gavejas


class Pajamos(Irasas):
    def __init__(self, suma: float, komentaras: str, siuntejas: str):
        super().__init__(suma, komentaras)
        self.siuntejas = siuntejas


class Biudzetas:
    __zurnalas = []

    def __init__(self):
        if os.path.exists("data.pickle"):
            with open("data.pickle", "rb") as f:
                self.__zurnalas = pickle.load(f)

    def __balansas(self):
        pajamos = sum([irasas.suma for irasas in self.__zurnalas if isinstance(irasas, Pajamos)])
        islaidos = sum([irasas.suma for irasas in self.__zurnalas if isinstance(irasas, Islaidos)])
        if islaidos > pajamos:
            print(f"Jūsų išlaidos {islaidos} viršija jūsų {biudzetas}")
        return pajamos - islaidos
    
    def ataskaita(self) -> str:
        """
        Atspausdina biudžeto žurnalą.
        """
        logger.info('Patikrinta saskaita')
        print(self.get_balansas_string())
        for irasas in self.__zurnalas:
            if isinstance(irasas, Pajamos):
                print(f'\033[1;32;40m-=Pajamos\033[0m: Suma: {irasas.suma:.2f} €, komentaras: {irasas.komentaras}, siuntėjas: {irasas.siuntejas}')
            elif isinstance(irasas, Islaidos):
                print(f'\033[1;31;40m-=Išlaidos\033[0m: Suma: {irasas.suma:.2f} €, komentaras: {irasas.komentaras}, gavėjas: {irasas.gavejas}')

    def ivesti_pajamas(self, irasas):
        self.__zurnalas.append(irasas)
        
    def get_balansas_string(self) -> str:
        """
        Grąžina eilutę, nurodančią dabartinį biudžeto balansą
        Returns a string indicating the current balance of the budget.
        """
        balansas = self.__balansas()
        if len(self.__zurnalas) == 0:
            return "\033[1;31;40mJūsų biudžeto sąrašas yra tuščias..\033[0m"
        else:
            return f"\033[1;32;40m-=Bendras balansas\033[0m: {balansas:.2f} €."
    
    def ivesti_pajamas(self, irasas):
        self.__zurnalas.append(irasas)
        with open("data.pickle", "wb") as f:
            pickle.dump(self.__zurnalas, f)


biudzetas = Biudzetas()


def ivesti_pajamas(biudzetas: Biudzetas) -> None:
    while True:
        try:
            print("")
            print("Įveskite \033[1;32;40m gautų \033[0m pajamų sumą pvz. 1250.04 ir spauskite 'Enter':")
            suma = float(input("-->>> "))
            if suma < 0:
                raise ValueError("Pajamų suma negali būti neigiama!")
            break
        except ValueError as e:
            print(e)
        logger.warning('Pajamu suma negali buti neigiama')
            
    siuntejas = input("Įveskite pajamų siuntėją ir spauskite 'Enter': ")
    komentaras = input("Įveskite komentarą ir spauskite 'Enter': ")
    pajamos = Pajamos(suma, komentaras, siuntejas)
    biudzetas.ivesti_pajamas(pajamos)
    print("")
    print(f"Pajamos {suma:.2f} € buvo pridėtos prie biudžeto.")
    # logger.debug('This is a debug message')
    logger.info(f'Pajamos: {suma:.2f} euru buvo prideta i saskaita')
    # logger.warning('This is a warning message')
    # logger.error('This is an error message')
    print(biudzetas.get_balansas_string())

def ivesti_islaidas(biudzetas: Biudzetas) -> None:
    while True:
        try:
            suma = float(input("Įveskite išlaidų sumą: "))
            if suma < 0:
                raise ValueError("Išlaidų suma negali būti neigiama!")
            break
        except ValueError as e:
            print(e)
        logger.warning('Islaidu suma negali buti neigiama')
            
    gavejas = input("Įveskite išlaidų gavėją: ")
    komentaras = input("Įveskite komentarą: ")
    logger.info(f'Islaidos: {suma:.2f} buvo issiusta is saskaitos')
    islaidos = Islaidos(suma, komentaras, gavejas)
    biudzetas.ivesti_pajamas(islaidos)
    print(f"Išlaidos {suma:.2f} € buvo išimta iš biudžeto.")
    print(biudzetas.get_balansas_string())

while True:
    print("\n\t\033[1;36;40m-----=== Biudžeto skaičiavimo programa ===-----\033[0m\n")
    print("\t\t\033[1;32;40m--= Pasirinkite veiksmą =--\033[0m\n")
    print("\t\033[1;32;40m1\033[0m. Sukurti pajamų įrašą")
    print("\t\033[1;32;40m2\033[0m. Sukurti išlaidų įrašą")
    print("\t\033[1;32;40m3\033[0m. Ataskaita\n")
 
    print("\t\033[1;31;40m0\033[0m. Uždaryti programą\n")
    meniu = int(input('Įveskite pasirinkimą \033[1;32;40m1\033[0m, \033[1;32;40m2\033[0m, \033[1;32;40m3\033[0m arba \033[1;31;40m0\033[0m ir spauskite "Enter": '))
    
    if meniu == 1:
        ivesti_pajamas(biudzetas)
    elif meniu == 2:
        ivesti_islaidas(biudzetas)
    elif meniu == 3:
        biudzetas.ataskaita()
    elif meniu == 0:
        logger.info('Programa baigta')
        break
    else:
        print("\n\033[1;31;40mNeteisingas pasirinkimas, bandykite dar kartą!\033[0m\n")
