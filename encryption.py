from PIL import Image
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

keyPair = RSA.generate(3072)
pubKey = keyPair.publickey()
print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()


def encrypt_pixel(img, byte_array):
    c=-1

    for pix in img:
        c += 1
        try:
                #print(img[c])
                if byte_array[c] == '1':
                    # even
                    if img[c] % 2 == 0:
                        img[c] -= 1
                elif byte_array[c] == '0':
                    # odd
                    if img[c] % 2 != 0:
                        img[c] -= 1
                elif byte_array[c] == ' ':
                    if img[c] % 2 != 0:
                        img[c] -= 1
                #print(img[c],byte_array[c])
        except:
                if img[c] % 2 == 0:
                    img[c] -= 1
                break
    return img

def get_byte(a):
    a_bytes = bytes(a, "ascii")
    return  (' '.join(format(ord(x), '08b') for x in a))


if __name__ == '__main__':
    #'1.png'
    image_name = input('Please Enter Image Name:')
    im = Image.open(image_name)
    x,y = list(im.size)
    rgb = np.asarray(im).reshape(-1)
    new_img = np.array(rgb)
    msg =input('Please enter your massage: ')
    enc = get_byte(msg)
    encrypted  = (encrypt_pixel(new_img,enc))
    print("Image shape :",encrypted.shape)
    final_img = encrypted.reshape(y,x,3)
    im = Image.fromarray(final_img)
    im.save("2.png")
    print('Encrypted and Saved')
