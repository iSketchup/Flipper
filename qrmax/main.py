import os

import qrcode

import segno
import segno.helpers
import treepoem

def main():
    makeAllTreepoem( 'LEERGUT#F100160#1#028611#000075#260327134239#01#P#00#000075#266a')

def makeqr(safeas:str, text:str):
    img = qrcode.make(text)
    type(img)
    img.save(safeas + '.png')

def makeSegno(safeas:str, text:str):
    segno.make(text).save(safeas + '1.png')

    segno.make_qr(text).save(safeas + '2.png')

    img = treepoem.generate_barcode(
        barcode_type='azteccode',
        data=text,
    )
    img.save('aztec.png')


def makeAllTreepoem(text: str):
    types = list(treepoem.barcode_types.keys())
    print(f'\n[treepoem] {len(types)} Typen gefunden, starte...\n')

    success, failed = [], []

    for barcode_type in types:
        path = os.path.join('Qr', f'treepoem_{barcode_type}.png')
        try:
            img = treepoem.generate_barcode(
                barcode_type=barcode_type,
                data=text,
            )
            img.save(path)
            success.append(barcode_type)
            print(f'  ✓ {barcode_type}')
        except Exception as e:
            failed.append(barcode_type)
            print(f'  ✗ {barcode_type}: {e}')

    print(f'\n[treepoem] Fertig: {len(success)} erfolgreich, {len(failed)} fehlgeschlagen')
    if failed:
        print(f'  Fehlgeschlagen: {", ".join(failed)}')
if __name__ == '__main__':
    main()