import csv
import socket

#Tworzymy klase lisc, ktora bedzie odkodowywala podana wiadomosc wraz ze slownikiem
class Lisc:
    znak = ""
    binarnie = ""

    def __init__(self, znak, binarnie):  # definiujemy konstruktor
        self.znak = znak
        self.binarnie = binarnie


def odczytanyKodZPliku(nazwaPliku):
    zakodowanaLista = []
    plik = open(nazwaPliku + ".txt", newline='')
    zawartosc = csv.reader(plik)
    for row in zawartosc:
        zakodowanaLista.append(row[0])
    return zakodowanaLista


def zapisDoPliku(zakodowanaLista, zawartosc, aLUBw):
    sciezkaPliku = zakodowanaLista + ".txt"
    if aLUBw == 'a':
     plik = open(sciezkaPliku, "a")
    elif aLUBw == 'w':
     plik = open(sciezkaPliku, "w")
    plik.write(zawartosc)
    plik.close()
    return zawartosc


def zakodowane(list):
    return list.pop()


def slownik(list):
    slownik = []
    for i in list:
       slownik.append(Lisc(i[0], i[1:]))
    return slownik


def odkodowane(slownik, ostatnie):
    pozycja = 0
    odkodowane = ""
    for i in range(0, len(ostatnie) + 1):
        for d in slownik:
            if d.binarnie == ostatnie[pozycja:i]:
                odkodowane += d.znak
                pozycja = i
    return odkodowane


def laczenie(IP):
    PORT = 4455
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = "utf-8"
    print("[STARTOWANIE] Serwer jest wlaczony.")
    """Tworzymy gniazdo TCP"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """Przypisujemy IP i port do serwera"""
    server.bind(ADDR)
    """ Serwer nasluchuje, czeka na połaczenie od klienta """
    server.listen()
    print("[NASLUCHIWANIE] Serwer nasluchuje.")
    """ Serwer zaakceptowal polaczenie od klienta """
    conn, addr = server.accept()
    print(f"[NOWE POLACZENIE] {addr} polaczono.")
    """ Otrzymywanie pliku od klienta """
    filename = conn.recv(SIZE).decode(FORMAT)
    print(f"[RECV] Otrzymywanie pliku.")
    file = open(filename, "w")
    conn.send("Plik przeslany.".encode(FORMAT))
    """ Receiving the file data from the client. """
    data = conn.recv(SIZE).decode(FORMAT)
    print(f"[RECV] Otrzymywanie zawartosci pliku.")
    file.write(data)
    conn.send("Zawartosc pliku otrzymana".encode(FORMAT))
    """ Zamykanie pliku """
    file.close()
    """ Zamykanie polaczenia z klientem """
    conn.close()
    print(f"[ROZLACZONO] {addr} rozlaczono.")



laczenie(input("Podaj adress ip servera: "))
lista = odczytanyKodZPliku("zaszyfrowane")
last = zakodowane(lista)
listDictionary = slownik(lista)
zapisDoPliku("odszyfrowane", odkodowane(listDictionary, last), "w")
print(odkodowane(listDictionary, last))
