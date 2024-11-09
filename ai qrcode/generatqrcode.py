import qrcode

def generate_qr_code(text, filename='qrcode.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code generated and saved as '{filename}'.")

if __name__ == "__main__":
    text = input("Enter the text to generate QR code: ")
    generate_qr_code(text)
