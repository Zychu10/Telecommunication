import logging
from enum import Enum

import serial

import check_sum as cs
import serial as ser

import xmodem


def main():
    user_input = ""
    serial_port_name = "None"
    baudrate = "None"
    check_sum = "Checksum"
    debugging = False

    while user_input != "q":
        print(f"Port: {serial_port_name}")
        print(f"Baudrate: {baudrate}")
        print(f"Typ sumy kontrolnej: {check_sum}")
        print(f"Tryb debugowania: {debugging}")
        print()

        user_input = input('''Podaj, czy chcesz:
        (1) Wysłać pakiet
        (2) Odebrać pakiet
        (3) Zmien ustawienia portu szeregowego
        (4) Zmien typ sumy kontrolnej
        (5) Przełącz tryb debugowania
        [q - wyjście]\n> ''')
        match user_input:
            case '1':
                send_packet(serial_port_name, baudrate)
            case '2':
                receive_packet(serial_port_name, baudrate, check_sum)
            case '3':
                serial_port_name, baudrate = get_port_io()
            case '4':
                if check_sum == "CRC":
                    check_sum = "Checksum"
                else:
                    check_sum = "CRC"
            case '5':
                debugging = not debugging
                if debugging:
                    logging.basicConfig(level=logging.DEBUG)
                else:
                    logging.basicConfig(level=logging.ERROR)
            case _:
                continue


def send_packet(port_name, baudrate):
    data = bytes()
    # read user input
    match input("Wiadomość:\n\t(1) Predefiniowana\n\t(2) Wpisana ręcznie\n\t(3) Z pliku\n> "):
        case '1':
            data = bytes(Examples.invocation.value, 'utf-8')
        case '2':
            data = input("Podaj wiadomość: ")
            data = bytes(data, 'utf-8')
        case '3':
            data = message_from_file(input("Podaj ścieżkę: "))

    try:
        serial_port = xmodem.initialize_serial(port_name, baudrate)
        serial_port.open()
        xmodem.send(serial_port, data)
        serial_port.close()
    except (serial.SerialException, ValueError):
        print("Ustawienia Portu są nie poprawne, spróbuj ponownie")
    except xmodem.ReceiverSendUnexpectedResponseException:
        print("Odbiorca nie rozpoczął transmisji, spróbuj ponownie")


def receive_packet(port_name, baudrate, check_sum):
    serial_port = xmodem.initialize_serial(port_name, baudrate)

    try:
        serial_port.open()
        if check_sum == "CRC":
            check_sum = xmodem.CheckSumEnum.crc
        else:
            check_sum = xmodem.CheckSumEnum.algebraic
        data = xmodem.receive(serial_port, check_sum)
        serial_port.close()
    except (serial.SerialException, ValueError):
        print("Ustawienia Portu są nie poprawne, spróbuj ponownie")
    except xmodem.SenderDoesNotAcceptTransferException:
        print("Nadawca nie zaakceptował transmisji, spróbuj ponownie")

    print("Cała wiadomość: ")
    print(data.decode("utf-8"))

    path = input("Podaj gdzie zapisać: ")
    message_to_file(data, path)


def get_port_io():
    port_name = input("Podaj nazwę portu: ")
    baudrate = int(input("Podaj baudrate: "))
    return port_name, baudrate


def message_from_file(path):
    with open(path, "rb") as message_file:
        result = message_file.read()
    return result


def message_to_file(message: bytes, path):
    with open(path, "wb+") as message_file:
        message_file.write(message)


class Examples(Enum):
    invocation = "Litwo! Ojczyzno moja! Ty jestes jak zdrowie," \
                 "Ile cie trzeba cenic, ten tylko sie dowie," \
                 "Kto cie stracil. Dzis pieknosc twa w calej ozdobie " \
                 "Widze i opisuje, bo tesknie po tobie " \
                 "Panno swieta, co Jasnej bronisz Czestochowy " \
                 "I w Ostrej swiecisz Bramie! Ty, co grod zamkowy " \
                 "Nowogrodzki ochraniasz z jego wiernym ludem! " \
                 "Jak mnie dziecko do zdrowia powrocilas cudem, " \
                 "(Gdy od placzacej matki pod Twoja opieke " \
                 "Ofiarowany, martwa podnioslem powieke " \
                 "I zaraz moglem pieszo do Twych swiatyn progu " \
                 "Isc za wrocone zycie podziekowac Bogu), " \
                 "Tak nas powrocisz cudem na Ojczyzny lono. " \
                 "Tymczasem przenos moja dusze uteskniona " \
                 "Do tych pagorkow lesnych, do tych lak zielonych, " \
                 "Szeroko nad blekitnym Niemnem rozciagnionych; " \
                 "Do tych pol malowanych zbozem rozmaitem, " \
                 "Wyzlacanych pszenica, posrebrzanych zytem; " \
                 "Gdzie bursztynowy swierzop, gryka jak snieg biala, " \
                 "Gdzie panienskim rumiencem dziecielina pala, " \
                 "A wszystko przepasane jakby wstega, miedza " \
                 "Zielona, na niej z rzadka ciche grusze siedza."


if __name__ == "__main__":
    main()
