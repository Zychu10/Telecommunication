from queue import PriorityQueue #importujemy PriorityQueue
import socket #importujemy socket do utworzenia gniazda do przesyłu danych


#tworzymy klasę Node, która będzie podstaowym budulcem drzewa kodowania
#będzie ona przechowywać wartość, lewe i prawe dziecko, zakodowaną wartość, a także znak
class Node:
    wartosc = 0
    prawy = None
    lewy = None
    znak = ""


    def czyLisc(self): #pomocnicza metoda, która pozwoli określić, czy liść przechowuje znak
        return self.znak != ""

    def __init__(self, wartosc, znak): #definiujemy konstruktor
        self.wartosc = wartosc
        self.znak = znak

    #funkcja __lt__ pomoże nam przy tworzeniu priority_queue
    def __lt__(self, inna):
        if self.wartosc != inna.wartosc: #wykonujemy normalne porównanie, jeżeli liście są różne;
            return self.wartosc < inna.wartosc
        if not self.czyLisc() and inna.czyLisc(): # w przeciwnym wypadku ważniejsze są liście mające znak
            return True
        if self.czyLisc() and not inna.czyLisc(): # w przeciwnym wypadku ważniejsze są liście mające znak
            return False
        if self.czyLisc() and inna.czyLisc(): #jeżeli jednak oba maja znak, to decyduje kolejność alfabetyczna
            return ord(self.znak[0]) < ord(inna.znak[0])
        return True


def odczytajPlik (nazwaPliku):
    sciezkaPliku = nazwaPliku + ".txt"
    plik = open(sciezkaPliku, "r")
    zawartosc = plik.read()
    plik.close()
    return zawartosc


def zapisDoPliku (nazwaPliku, zawartosc, aLUBw):
    sciezkaPliku = nazwaPliku + ".txt"
    if aLUBw == 'a':
     plik = open(sciezkaPliku, "a")
    elif aLUBw == 'w':
     plik = open(sciezkaPliku, "w")
    plik.write(zawartosc)
    plik.close()
    return zawartosc


#Definiujemy metodę, która stworzy drzewo kodowania Huffmana, a następnie zwróci jego korzeń
#Argumentem jest tekst, który chcemy zakodować
def stworzDrzewo(tekst):
    wystapienia = {}
    for z in tekst: #zliczamy wystąpienia każdego znaku w tekście
        if wystapienia.__contains__(z):
            wystapienia[z] += 1
        else:
            wystapienia[z] = 1
    # Tworzymy obiekt PriorityQueue(), który będzie przechowywać nieprzypisane elementy drzewa.
    # Obiekt priority_queue pozwoli nam stworzyć uporządkowaną listę liści drzewa - najmniejsze będą najwyżej.
    wezly = PriorityQueue()
    for z in wystapienia.keys(): #tworzymy liście drzewa, bazując na znakach i ich ilości wystąpień, a następnei dodajmy do listy
        wezel = Node(wystapienia[z], z)
        wezly.put(wezel)
    korzenDrzewa = None #tworzymy zmienna przechowujaca docelowo korzen drzewa
    while wezly.qsize() > 1: #następnie iterujemy, dopóki w nodes nie zostanie ostatni element - korzeń drzewa
        w1 = wezly.get() #pobieramy pierwszy, najmniejszy element z PriorityQueue
        w2 = wezly.get() #pobieramy kolejny, najmniejszy element z PriorityQueue
        #jeżeli oba liście mają tą samą wartość, a jeden z nich jest kontenerem, to powinien on być traktowany jako większy element
        if w1.wartosc == w2.wartosc and not w1.czyLisc():
            pom = w1 #dlatego w takiej sytuacji podmieniamy wskaźniki
            w1 = w2
            w2 = pom
        rodzic = Node(w1.wartosc + w2.wartosc, "") #tworzymy liść-kontener, który będzie przechowywać dwa powyższe elementy i sumę ich wartości
        korzenDrzewa = rodzic #ustawiamy go na aktualny korzen
        rodzic.lewy = w1 #i dodajemy mu dzieci
        rodzic.prawy = w2
        wezly.put(rodzic) #a następnie dodajemy go do PriorityQueue
    return korzenDrzewa #nasze drzewo jest gotowe - zwracamy korzeń


#tworzymy funkcję, która zakoduje drzewo
#jednocześnie zakoduje ona podany przez użytkownika tekst
def zakodowaneWartosci(n, str, txt):
    if n is None: #jeżeli trafimy na koniec drzewa
        return txt #przerywamy rekurencję
    if n.czyLisc(): #jeżeli przechowuje on znak
        zapisDoPliku("zaszyfrowane", n.znak + str + "\n", "a")
        txt = txt.replace(n.znak, str) #a następnie podmieniamy znak w tekście z zakodowaną wartościa
    txt = zakodowaneWartosci(n.lewy, str + "0", txt) #wykonujemy te same działania dla lewej części drzewa - rekurencja
    txt = zakodowaneWartosci(n.prawy, str + "1", txt) #wykonujemy te same działania dla prawej części drzewa - rekurencja
    return txt #na koniec zwracamy zakodowany tekst


def laczenie(IP):
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 1024
    """ Tworzenie gniazda TCP"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Łączenie z serwerem """
    client.connect(ADDR)
    """ Otwieranie i odczytywanie zawartosci pliku"""
    file = open("zakodowane.txt", "r")
    data = file.read()
    """ Przesyłanie pliku do serwera """
    client.send("zakodowane.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    """ Przesyłanie zawartosci pliku do serwera"""
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    """ Zamykanie pliku """
    file.close()
    """ Konczenie lacznosci """
    client.close()


nazwaPliku = input("Kodowanie Huffmana. Podaj nazwę pliku, którego zawartość chcesz zakodować:").rstrip()
zapisDoPliku("zaszyfrowane", "", "w")
wyraz = odczytajPlik(nazwaPliku)
rootNode = stworzDrzewo(wyraz)
wyraz = zakodowaneWartosci(rootNode, "", wyraz)
print("Oto tekst po zakodowaniu: " + wyraz)
zapisDoPliku("zaszyfrowane", wyraz, "a")
laczenie(input("Podaj adress IP na który chcesz wysłać zakodowaną wiadomość: "))

