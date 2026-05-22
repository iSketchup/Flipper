import os
import qrcode
import segno
import treepoem

OUTPUT_DIR = 'Qr'

def main():
    makeAllTreepoem('LEERGUT#F100160#1#028611#000075#260327134239#01#P#00#000075#266a')

def makeqr(safeas: str, text: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img = qrcode.make(text)
    img.save(os.path.join(OUTPUT_DIR, safeas + '.png'))

def makeSegno(safeas: str, text: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    segno.make(text).save(os.path.join(OUTPUT_DIR, safeas + '1.png'))
    segno.make_qr(text).save(os.path.join(OUTPUT_DIR, safeas + '2.png'))
    img = treepoem.generate_barcode(
        barcode_type='azteccode',
        data=text,
    )
    img.save(os.path.join(OUTPUT_DIR, 'aztec.png'))

def makeAllTreepoem(text: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # ← Fix: ensure output dir exists
    types = list(treepoem.barcode_types.keys())
    print(f'\n[treepoem] {len(types)} Typen gefunden, starte...\n')
    success, failed = [], []
    for barcode_type in types:
        path = os.path.join(OUTPUT_DIR, f'treepoem_{barcode_type}.png')
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