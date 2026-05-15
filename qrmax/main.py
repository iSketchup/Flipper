import qrcode
def main():
    img = qrcode.make('Smegma sigma ligma rust crust 67')
    type(img)
    img.save('qr.png')

if __name__ == '__main__':
    main()