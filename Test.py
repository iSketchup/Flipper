# my_flipper_script.py
import flipper
from time import sleep

# Flipper-Objekt abrufen
f = flipper.Flipper()

# Display löschen und Text ausgeben
f.display.text(10, 10, "Hallo Flipper!", 1)
f.display.update()

# Hauptschleife
while True:
    # Knöpfe abfragen
    buttons = f.input.get()

    if buttons.ok:
        f.display.text(10, 30, "OK gedrückt", 1)
        f.display.update()
        sleep(0.2)

    elif buttons.back:
        f.display.text(10, 30, "Zurück gedrückt", 1)
        f.display.update()
        sleep(0.2)

    elif buttons.up:
        f.display.text(10, 30, "Pfeil Hoch", 1)
        f.display.update()
        sleep(0.2)

    elif buttons.down:
        f.display.text(10, 30, "Pfeil Runter", 1)
        f.display.update()
        sleep(0.2)

    else:
        # Bildschirm kurz löschen
        f.display.clear()
        f.display.text(10, 10, "Hallo Flipper!", 1)
        f.display.update()
        sleep(0.1)
