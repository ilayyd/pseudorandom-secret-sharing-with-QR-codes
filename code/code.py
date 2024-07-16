import random
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

def generate_random_shares(secret, num_shares):
    
    """
    Generate random shares for a given secret.

    Args:
    - secret (int): The original secret to be shared.
    - num_shares (int): The number of shares to generate.

    Returns:
    - list: List of generated shares.
    """
    
    shares = []
    for _ in range(num_shares - 1):
        random_share = random.randint(1, 2**256 - 1)  # 256-bit random share
        shares.append(random_share)
        secret ^= random_share

    # The last share is the XOR of the secret and all other shares
    shares.append(secret)
    return shares

def combine_shares(shares):
    
    """
    Combine shares to reveal the original secret.

    Args:
    - shares (list): List of shares to be combined.

    Returns:
    - int: Combined secret.
    """
    
    combined_secret = 0
    for share in shares:
        combined_secret ^= share
    return combined_secret

def generate_qr_code(data, filename):
    
    """
    Generate a QR code for the given data and save it to a file.

    Args:
    - data (str): Data to be encoded in the QR code.
    - filename (str): File name to save the QR code image.
    """
    
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def read_qr_code(filename):
    
    """
    Read the data encoded in a QR code image.

    Args:
    - filename (str): File name of the QR code image.

    Returns:
    - int: Decoded data as an integer.
    """
    
    img = Image.open(filename)
    decoded_objects = decode(img)
    data = decoded_objects[0].data.decode('utf-8')
    return int(data)

def main():
    
    # Set the original secret and the number of shares to generate
    secret = 8786546
    num_shares = 15
    
    print("Original Secret: ", secret)

    # Generate random shares
    shares = generate_random_shares(secret, num_shares)
    print("Generated Shares:", shares)

    # Save shares as QR codes
    for i, share in enumerate(shares):
        generate_qr_code(str(share), f'share_{i + 1}.png')

    # Read shares from QR codes
    read_shares = [read_qr_code(f'share_{i + 1}.png') for i in range(num_shares)]

    # Combine shares to reveal the secret
    combined_secret = combine_shares(read_shares)
    print("Combined Secret:", combined_secret)

    # Verify if the combined secret matches the original secret
    if combined_secret == secret:
        print("Secrets match! Success.")
    else:
        print("Secrets do not match. Something went wrong.")

    # Save combined secret as a QR code
    generate_qr_code(str(combined_secret), 'secret_combined.png')

if __name__ == "__main__":
    main()
