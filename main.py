import os
import sys
import streamlit as st
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from PIL import Image

import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



keyPair = RSA.generate(3072)
pubKey = keyPair.publickey()
st.header('A Secure Image Steganography based on RSA Algorithm')


def binaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1

    return chr(decimal)

def decrypt(pix):
    st = ''
    c=0
    for i in pix:
        c+=1
        if i%2 != 0 and c%9==0:
            break
        elif i%2 == 0 and c%9==0:
            st+=' '
        elif i%2 ==0:
            st+='0'
        elif i%2 !=0:
            st+='1'
    return st




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

menu1 = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu1)

if choice == "Login":
        st.subheader("Please Enter Valid Credentials")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login/Logout"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                
                menu = ["Encode","Decode"]
                choice = st.sidebar.selectbox("Menu",menu)

                if choice == 'Encode':
                    st.title('Encoding')
                    # Image
                    img = st.file_uploader('Upload image file', type=['jpg', 'png', 'jpeg'])
                    if img is not None:
                        file_details = {"FileName":img.name,"FileType":img.type}
                        with open(os.path.join("",img.name),"wb") as f: 
                            f.write(img.getbuffer())         
                            st.success("File Uploaded...")
                        im = Image.open(img.name)
                        x,y = list(im.size)
                        rgb = np.asarray(im).reshape(-1)
                        new_img = np.array(rgb)
                        msg = st.text_input('Message to hide')
                        enc = get_byte(msg)
                        if st.button('Encrypt File and Generate Key'):
                            print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
                            pubKeyPEM = pubKey.exportKey()
                            encryptor = PKCS1_OAEP.new(pubKey)
                            enc = get_byte(msg)
                            encrypted  = (encrypt_pixel(new_img,enc))
                            final_img = encrypted.reshape(y,x,3)
                            im = Image.fromarray(final_img)
                            im.save("2.png")
                            file2 = open("Pub.pem","w+")
                            file2.write(str(pubKey.n))
                            st.success("Files generated : 2.PNG and Pub.PEM")


                    

                elif choice == 'Decode':
                    st.title('Decoding')
                    img2 = st.file_uploader('Upload image file', type=['jpg', 'png', 'jpeg'])
                    key = st.file_uploader('Select Key', type=['pem'])
                    if img2 is not None and key is not None:
                        file_details = {"FileName":img2.name,"FileType":img2.type}
                        with open(os.path.join("",img2.name),"wb") as f: 
                            f.write(img2.getbuffer())         
                            st.success("File Decrypted")
                        im = Image.open(img2.name)
                        x,y = list(im.size)
                        rgb = np.asarray(im).reshape(-1)

                        new_img = np.array(rgb)
                        de = decrypt(new_img)

                        de_array = de.split(' ')

                        final_masg =  ''

                        for i in de_array:
                            final_masg+=binaryToDecimal(int(i))
                        decryptor = PKCS1_OAEP.new(keyPair)
                        print('Massage:',final_masg)
                        st.success(final_masg)
            else:
                st.warning("Incorrect Username/Password")
elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")