from zakladni_data import MENU
from zakladni_data import zasoby
from zakladni_data import mince_hodnota
from zakladni_data import mince_nazev


# report - hlášení o zásobách - kódové slovo pro obsluhu automatu

def uvitani():
    """
    Uvítá uživatele a zobrazí nabídku nápojů. Získává vstup od uživatele s volbou nápoje.

    Vrací: volbu uživatele 
    """
    print("""
          Vítejte!
          ----------------------
          Naše nabídka nápojů:
          1) espresso - 40,- Kč
          2) latte - 50,- Kč
          3) cappuccino - 60,- Kč
          ----------------------
          """)
    volba = input("Co byste si dal/a? (espresso = 1 /latte = 2 /cappuccino = 3) nebo nic = 0:  ").strip()
    return volba


def doplneni_ingredienci():
    """
    Zobrazí současný stav zásob.

    Vrací: zásoby
    """
    return zasoby


def odecteni_ingredienci(zasoby, napoj):
    """
    Ze zásob odečte ingredience potřebné na nápoj, pokud není dostatek ingrediencí, ohlásí to. 
    
    :param zasoby: Udává množství zásob
    :param napoj: Udává zvolený nápoj

    Vrací: nápoj, pokud je dostatek ingrediencí, nebo None pokud ne
    """
    if zasoby["voda"] >= napoj["ingredience"]["voda"] and zasoby["mleko"] >= napoj["ingredience"]["mleko"] and zasoby["kava"] >= napoj["ingredience"]["kava"]:
        print("Na váš nápoj máme dostatek ingrediencí.")
        zasoby["voda"] -= napoj["ingredience"]["voda"]
        zasoby["mleko"] -= napoj["ingredience"]["mleko"]
        zasoby["kava"] -= napoj["ingredience"]["kava"]
        return napoj
    else:
        print("Na váš nápoj bohužel nemáme dostatek ingrediencí.")
        return None


def zpracovani_napoje(volba, zasoby):
    """
    Zpracovává vstup od uživatele. Zobrazuje stav zásob při zadání slova report. 
    Pokud volba není v nabídce, ohlásí to.
    
    :param volba: Vstup od uživatele
    :param zasoby: Zobrazí současný stav zásob

    Vrací: Název nápoje a jeho specifikace nebo None, None
    """
    if volba in ["1", "espresso"]:
        napoj_nazev = "espresso"        
    elif volba in ["2", "latte"]:
        napoj_nazev = "latte"  
    elif volba in ["3", "cappuccino"]: 
        napoj_nazev = "cappuccino"
    # report - hlášení o zásobách
    elif volba == "report":
        print("\n----------------------------\n")
        print(zasoby)
        print("\n----------------------------\n")
        return None, None
    else:
        print(f"Nápoj, který jste vybrali - {volba} - není v nabídce!")
        return None, None
    napoj_ingredience = MENU[napoj_nazev]
    napoj_data = odecteni_ingredienci(zasoby, napoj_ingredience)
    return napoj_nazev, napoj_data


def mince(aktualni_soucet = 0):
    """
    Funkce pro počítání mincí.

    Vrací: hodnotu vhozených mincí
    """
    print("Vložte mince 1, 2, 5, 10, 20, 50 Kč.")
    for _ in mince_nazev:
        hodnota = mince_hodnota[_]
        while True:
            pocet = input(f"Kolik {hodnota},- Kč si přejete vložit?  ->  ")
            if pocet.isdigit():
                aktualni_soucet += int(pocet) * hodnota
                print(f"Prozatím jste vložili {aktualni_soucet},- Kč.")
                break
            else:
                print("Toto není platný počet. Zkuste to znovu")
    return aktualni_soucet


def zpracovani_ceny(napoj_nazev, napoj_data, soucet):
    """
    Zobrazí název a cenu vybraného nápoje, ohlásí, zda je vhozena dostatečná hodnota, případně kolik je ještě potřeba vložit.
    
    :param napoj_nazev: Název nápoje
    :param napoj_data: Specifikace nápoje
    :param soucet: Hodnota vhozených mincí

    Vrací: False pokud je hodnota nedostatečná
        True pokud je hodnota dostatečná
    """
    if napoj_data:
        cena_napoje = napoj_data["cena"]
        print(f"Váš výběr je {napoj_nazev} v ceně {cena_napoje},- Kč.")
        if soucet < cena_napoje:
            print(f"Nevhodili jste dostatek peněz. Ještě je zapotřebí vložit {cena_napoje - soucet},- Kč.")
            return False
        
        print("Váš nápoj se připravuje")
        drobne = soucet - cena_napoje
        if drobne > 0:
            print(f"Vložili jste {soucet}, zde je vašich zbylých {drobne},- Kč.")
            return True
                                                                        

def hlavni_menu():
    zbyvajici_zasoby = doplneni_ingredienci()
    while True: 
        vyber = uvitani()
        if vyber in ["0", "nic"]:  # možnost ukončit
            print("\n----------------------------\n")
            print("Děkujeme, příště nashledanou!")
            print("\n----------------------------\n")
            break
        napoj_nazev, napoj_data = zpracovani_napoje(vyber, zbyvajici_zasoby)
        if napoj_nazev and napoj_data:
            soucet = 0
            while True:
                soucet = mince(soucet)
                zaplaceno = zpracovani_ceny(napoj_nazev, napoj_data, soucet)
                if zaplaceno:
                    break
 
    
if __name__ == "__main__":
    hlavni_menu()


    