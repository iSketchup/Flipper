import sys
import cv2
from pyzbar import pyzbar
from PIL import Image
import qrcode
import math

def analyze_qr(image_path: str) -> dict:
    """Liest einen QR-Code aus und bestimmt die Version."""
    img_cv = cv2.imread(image_path)
    if img_cv is None:
        print(f'[ERROR] Bild nicht gefunden: {image_path}')
        return None

    # Dekodieren mit pyzbar
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    codes = pyzbar.decode(img_gray)

    if not codes:
        print('[ERROR] Kein QR-Code erkannt im Bild.')
        return None

    code = codes[0]
    data = code.data.decode('utf-8')

    # Version aus Bildgröße berechnen:
    # QR Version N hat (21 + (N-1)*4) Module pro Seite
    # Module = kleinste Einheit (schwarzes/weißes Quadrat)
    h, w = img_cv.shape[:2]
    size = min(w, h)

    # Ruhezone abschätzen (normalerweise 4 Module) und Modulbreite schätzen
    # Genauer: pyzbar gibt polygon zurück, daraus Breite berechnen
    rect = code.rect
    qr_px = rect.width  # Pixel-Breite des QR-Codes ohne Rand

    # Version schätzen: modules = 21 + (version-1)*4
    # Modulbreite ≈ qr_px / modules
    # Wir probieren alle Versionen 1-40 und schauen welche am besten passt
    best_version = None
    best_diff = float('inf')
    for v in range(1, 41):
        modules = 21 + (v - 1) * 4
        mod_size = qr_px / modules
        # Gesamtbild mit Rand: modules + 8 (4 Rand auf jeder Seite)
        expected_total = (modules + 8) * mod_size
        diff = abs(expected_total - size)
        if diff < best_diff:
            best_diff = diff
            best_version = v

    result = {
        'data':     data,
        'type':     code.type,
        'version':  best_version,
        'quality':  code.quality,
        'size_px':  (w, h),
        'qr_px':    qr_px,
    }
    return result

def make_qr_with_version(text: str, safeas: str = 'generated') -> dict:
    """Erstellt einen QR-Code und gibt seine Version zurück."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(text)
    qr.make(fit=True)

    version = qr.version
    img = qr.make_image()
    path = safeas + '.png'
    img.save(path)

    return {
        'data':    text,
        'version': version,
        'path':    path,
    }

def compare(image_path: str, text: str = None):
    """Analysiert einen QR-Code und vergleicht optional mit einem generierten."""
    print('=' * 50)
    print(f'ANALYSIERE: {image_path}')
    print('=' * 50)

    info = analyze_qr(image_path)
    if not info:
        return

    print(f"  Inhalt:   {info['data']}")
    print(f"  Typ:      {info['type']}")
    print(f"  Version:  {info['version']}")
    print(f"  Qualität: {info['quality']}")
    print(f"  Größe:    {info['size_px'][0]}x{info['size_px'][1]} px")

    # Wenn kein Text angegeben, nimm den dekodierten Inhalt
    compare_text = text if text else info['data']

    print()
    print(f'GENERIERE VERGLEICHS-QR für: "{compare_text}"')
    gen = make_qr_with_version(compare_text, 'generated_compare')
    print(f"  Version:  {gen['version']}")
    print(f"  Gespeichert: {gen['path']}")

    print()
    if info['version'] == gen['version']:
        print(f"✓ GLEICHE VERSION ({info['version']})")
    else:
        print(f"✗ UNTERSCHIEDLICH — Bild: v{info['version']} | Generiert: v{gen['version']}")
    print('=' * 50)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python qr_analyze.py bild.png')
        print('  python qr_analyze.py bild.png "optionaler vergleichstext"')
        sys.exit(1)

    path = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else None
    compare(path, text)