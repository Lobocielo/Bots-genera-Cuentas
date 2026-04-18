




# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================



import requests
import json
import binascii
import time
import urllib3
import base64
import re
import socket
import threading
import random
import os
import sys
import psutil
import hmac
import hashlib
import string
import codecs
import gzip
import jwt
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from colorama import Fore, Style
import colorama

colorama.init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import io
import datetime as dt
from datetime import timedelta


red = Fore.RED
lg = Fore.LIGHTGREEN_EX
green = Fore.GREEN
bold = Style.BRIGHT
purpel = Fore.MAGENTA
hex_key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
key = bytes.fromhex(hex_key)

# Additional constants for the new implementation
default_key = b'Yg&tc%DEuh6%Zc^8'
default_iv = b'6oyZDr22E3ychjM%'
freefire_version = "OB52"
client_secret = key



REGION_LANG = {"ME": "ar","IND": "hi","ID": "id","VN": "vi","TH": "th","BD": "bn","PK": "ur","TW": "zh","EU": "en","CIS": "ru","NA": "en","SAC": "es","BR": "pt","US": "en","SG": "en"}
REGION_URLS = {
    "IND": "https://client.ind.freefiremobile.com/",
    "ID": "https://clientbp.ggblueshark.com/",
    "BR": "https://client.us.freefiremobile.com/",
    "ME": "https://clientbp.ggblueshark.com/",
    "VN": "https://clientbp.ggblueshark.com/",
    "TH": "https://clientbp.ggblueshark.com/",
    "CIS": "https://clientbp.ggblueshark.com/",
    "BD": "https://clientbp.ggblueshark.com/",
    "PK": "https://clientbp.ggblueshark.com/",
    "SG": "https://clientbp.ggblueshark.com/",
    "NA": "https://client.us.freefiremobile.com/",
    "US": "https://client.us.freefiremobile.com/",
    "SAC": "https://client.us.freefiremobile.com/",
    "EU": "https://clientbp.ggblueshark.com/",
    "TW": "https://clientbp.ggblueshark.com/"
}


# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================
def get_region(language_code: str) -> str:
    return REGION_LANG.get(language_code)

def get_region_url(region_code: str) -> str:
    """Return URL for a given region code"""
    return REGION_URLS.get(region_code, None)



def EnC_Vr(N):
    if N < 0: ''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)
    
def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80: break
        s += 7
    return n
    
def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet


# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================
def E_AEs(Pc):
    Z = bytes.fromhex(Pc)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    K = AES.new(key , AES.MODE_CBC , iv)
    R = K.encrypt(pad(Z , AES.block_size))
    return bytes.fromhex(R.hex())


# def generate_random_name():
#     characters = string.ascii_letters + string.digits
#     name = 'NEX-'+''.join(random.choice(characters) for _ in range(6)).upper()
#     return name

def generate_random_name( total_length=12, custom_prefix=None, region=None):
    # Superscript digits for unique names
    superscript_digits = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    
    if custom_prefix:
        base_name = custom_prefix
    else:
        base_name = "ZENIHT"
    
    # Adjust name length based on region requirements, but keep custom prefix
    if region and region.upper() == "BD":
        # BD region seems to require shorter names
        total_length = 8
        if not custom_prefix:  # Only use default if no custom prefix
            base_name = "ZENIHT"
    elif region and region.upper() in ["ME", "PK"]:
        # Some regions might have similar restrictions
        total_length = 10
        if not custom_prefix:  # Only use default if no custom prefix
            base_name = "ZENIHT"
    
    # Generate 4 random superscript digits
    random_superscripts = ''.join(random.choice(superscript_digits) for _ in range(4))
    
    # Combine base name with superscript digits
    return f"{base_name}{random_superscripts}"


def generate_custom_password(random_length=9):
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(random_length)).upper()
    return f"ZENIHT-{random_part}-X64"



def create_acc(region, custom_prefix=None, max_retries=3):
    # List of different User-Agents to rotate
    user_agents = [
        "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;IN;)",
        "GarenaMSDK/4.0.19P6(SM-G973F ;Android 11;en;US;)",
        "GarenaMSDK/4.0.19P7(Pixel 4 ;Android 10;en;US;)"
    ]
    
    for attempt in range(max_retries):
        try:
            password = generate_custom_password()
            data = f"password={password}&client_type=2&source=2&app_id=100067"
            message = data.encode('utf-8')
            signature = hmac.new(key, message, hashlib.sha256).hexdigest()

            url = "https://100067.connect.garena.com/oauth/guest/register"

            headers = {
                "User-Agent": user_agents[attempt % len(user_agents)],
                "Authorization": "Signature " + signature,
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip",
                "Connection": "Keep-Alive"
            }

            response = requests.post(url, headers=headers, data=data, timeout=30)
            
            if response.status_code == 200:
                try:
                    uid = response.json()['uid']
                    result = token(uid, password, region, custom_prefix)
                    if result:
                        return result
                except Exception as e:
                    print(f"{red}Token creation failed (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
            elif response.status_code == 503:
                print(f"{red}Server temporarily unavailable (503) - waiting longer before retry (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(5 + attempt * 2)  # Progressive delay: 5s, 7s, 9s
                    continue
            else:
                print(f"{red}Registration failed with status {response.status_code} (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                    
        except requests.RequestException as e:
            print(f"{red}Network error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
        except Exception as e:
            print(f"{red}Unexpected error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
    
    print(f"{red}Failed to create account after {max_retries} attempts")
    return None


def token(uid , password , region, custom_prefix=None):
    try:
        url = os.getenv("FF_GUEST_TOKEN_URL", "https://100067.connect.garena.com/oauth/guest/token/grant")

        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;IN;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
        }

        data = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": client_secret,
            "client_id": "100067",
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)
        
# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                NEW_ACCESS_TOKEN = json_response['access_token']
                NEW_OPEN_ID = json_response['open_id']
                OLD_ACCESS_TOKEN = "6fb7fdef8658fd03174ed551e82b71b21db8187fa0612c8eaf1b63aa687f1eae"
                OLD_OPEN_ID = "55ed759fcf94f85813e57b2ec8492f5c"
                time.sleep(0.2)
                
                result = encode_string(NEW_OPEN_ID)
                field = to_unicode_escaped(result['field_14'])
                field = codecs.decode(field, 'unicode_escape').encode('latin1')
                return Major_Register(NEW_ACCESS_TOKEN, NEW_OPEN_ID, field, uid, password, region, custom_prefix)
                
            except KeyError as e:
                print(f"{red}Missing key in token response: {e}")
                return None
            except Exception as e:
                print(f"{red}Error processing token response: {e}")
                return None
        else:
            print(f"{red}Token request failed with status {response.status_code}")
            return None
            
    except requests.RequestException as e:
        print(f"{red}Network error in token function: {e}")
        return None
    except Exception as e:
        print(f"{red}Unexpected error in token function: {e}")
        return None

def encode_string(original):
    keystream = [
    0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30,
    0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
    0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31,
    0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30
    ]
    encoded = ""
    for i in range(len(original)):
        orig_byte = ord(original[i])
        key_byte = keystream[i % len(keystream)]
        result_byte = orig_byte ^ key_byte
        encoded += chr(result_byte)
    return {
        "open_id": original,
        "field_14": encoded
        }

def to_unicode_escaped(s):
    """Convert string to Python-style Unicode escaped string"""
    return ''.join(
        c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}'
        for c in s
    )

def TOKEN_MAKER(OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, uid, region, custom_prefix=None):
    """Improved token maker function"""
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': freefire_version,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Content-Length': '928',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'loginbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    
    data = bytes.fromhex('3a07312e3131312e32aa01026172b201203535656437353966636639346638353831336535376232656338343932663563ba010134ea0140366662376664656638363538666430333137346564353531653832623731623231646238313837666130363132633865616631623633616136383766316561659a060134a2060134ca03203734323862323533646566633136343031386336303461316562626665626466')
    data = data.replace(b'1.111.2', b'1.114.9')
    data = data.replace(OLD_OPEN_ID.encode(), NEW_OPEN_ID.encode())
    data = data.replace(OLD_ACCESS_TOKEN.encode(), NEW_ACCESS_TOKEN.encode())
    hex_data = data.hex()
    d = encrypt_packet(hex_data, default_key, default_iv)
    Final_Payload = bytes.fromhex(d)
    
    URL = os.getenv("FF_MAJOR_LOGIN_URL", "https://loginbp.ggblueshark.com/MajorLogin")
    RESPONSE = requests.post(URL, headers=headers, data=Final_Payload, verify=False, timeout=30)
    

    response_data = RESPONSE.content
    if RESPONSE.headers.get('Content-Encoding') == 'gzip':
        try:
            response_data = gzip.decompress(response_data)

        except gzip.BadGzipFile as e:
            print(f"Decompression failed: {e}")

    # Try decrypting if necessary
    try:
        response_data = decrypt_data(response_data, default_key, default_iv)
      
    except Exception as e:
        print(f"Decryption failed: {e}")

    if RESPONSE.status_code == 200:
        if len(response_data) < 10:
            return False
        
        # Parse the response to get the token and other data
        try:
            combined_timestamp, key, iv, BASE64_TOKEN = parse_my_message(response_data)
            ip, port = GET_PAYLOAD_BY_DATA(BASE64_TOKEN, NEW_ACCESS_TOKEN, 1, region, custom_prefix)
            print(f"Key: {key}, IV: {iv}")
            return {
                "data": {"token": BASE64_TOKEN, "key": key, "iv": iv, "timestamp": combined_timestamp, "ip": ip, "port": port},
                "response": RESPONSE.content.hex(),
                "status_code": RESPONSE.status_code,
                "name": generate_random_name(custom_prefix=custom_prefix),
                "uid": uid,
                "password": generate_custom_password()
            }
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None
    else:
        return None

def parse_my_message(response_data):
    """Parse the response message to extract token and other data"""
    try:
        # This is a simplified parser - you may need to adjust based on actual response format
        # For now, we'll return placeholder values
        combined_timestamp = int(time.time())
        key = default_key
        iv = default_iv
        BASE64_TOKEN = "placeholder_token"
        return combined_timestamp, key, iv, BASE64_TOKEN
    except Exception as e:
        print(f"Error parsing message: {e}")
        return None, None, None, None

# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================
def Major_Register(access_token , open_id , field , uid , password,region, custom_prefix=None):
    try:
        url = "https://loginbp.ggblueshark.com/MajorRegister"
        name = generate_random_name(custom_prefix=custom_prefix, region=region)

        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",   
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggblueshark.com",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1"
        }

        payload = {
            1: name,
            2: access_token,
            3: open_id,
            5: 102000007,
            6: 4,
            7: 1,
            13: 1,
            14: field,
            15: "en",
            16: 1,
            17: 1
        }

        payload = CrEaTe_ProTo(payload).hex()
        payload = E_AEs(payload).hex()
        body = bytes.fromhex(payload)

        response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        
        if response.status_code == 200:
            return login(uid , password, access_token , open_id , response.content.hex() , response.status_code , name , region)
        else:
            print(f"{red}MajorRegister failed with status {response.status_code}")
            print(f"{red}Response content: {response.text}")
            print(f"{red}Response headers: {response.headers}")
            return None
            
    except requests.RequestException as e:
        print(f"{red}Network error in MajorRegister: {e}")
        return None
    except Exception as e:
        print(f"{red}Unexpected error in MajorRegister: {e}")
        return None

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def encrypt_packet(hex_data, key, iv):
    """Encrypt packet data"""
    plain_text = bytes.fromhex(hex_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def decrypt_data(encrypted_data, key, iv):
    """Decrypt data using AES CBC mode"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_data, AES.block_size)



def chooseregion(data_bytes, jwt_token):
    url = "https://loginbp.ggblueshark.com/ChooseRegion"
    payload = data_bytes
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'Authorization': f"Bearer {jwt_token}",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB52"
    }
    response = requests.post(url, data=payload, headers=headers,verify=False)
    return response.status_code


def login(uid , password, access_token , open_id, response , status_code , name , region):
    
    lang = get_region(region)
    lang_b = lang.encode("ascii")
    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggblueshark.com",
        "ReleaseVersion": "OB52",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1"
    }    

    payload = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang_b+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
    data = payload
    data = data.replace('afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'.encode(),access_token.encode())
    data = data.replace('1d8ec0240ede109973f3321b9354b44d'.encode(),open_id.encode())
    d = encrypt_api(data.hex())
    
    Final_Payload = bytes.fromhex(d)
    if region.lower() == "me":
        URL = "https://loginbp.common.ggbluefox.com/MajorLogin"
    else:
        URL = "https://loginbp.ggblueshark.com/MajorLogin"
    RESPONSE = requests.post(URL, headers=headers, data=Final_Payload,verify=False) 

    

    if RESPONSE.status_code == 200:
        if len(RESPONSE.text) < 10:
            return False
        if lang.lower() not in ["ar", "en"]:
            json_result = get_available_room(RESPONSE.content.hex())
            parsed_data = json.loads(json_result)

            BASE64_TOKEN = parsed_data['8']['data']
            
            #BASE64_TOKEN = RESPONSE.text[RESPONSE.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6IiIsInR5cCI6IkpXVCJ9"):-1]

            if region.lower() == "cis":
                region = "RU"
            fields = {1:region}
            
            fields = bytes.fromhex(encrypt_api(CrEaTe_ProTo(fields).hex()))
            r = chooseregion(fields, BASE64_TOKEN)

            
            if r == 200:
                return login_server(uid , password, access_token , open_id, response , status_code , name , region)
            
        else:
            BASE64_TOKEN = RESPONSE.text[RESPONSE.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ"):-1]
        second_dot_index = BASE64_TOKEN.find(".", BASE64_TOKEN.find(".") + 1)     
        time.sleep(0.2)
        BASE64_TOKEN = BASE64_TOKEN[:second_dot_index+44]
        dat = GET_PAYLOAD_BY_DATA(BASE64_TOKEN,access_token,1,region, None, uid, password)
        return dat
    



def login_server(uid , password, access_token , open_id, response , status_code , name , region):
    lang = get_region(region)
    lang_b = lang.encode("ascii")


    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggblueshark.com",
        "ReleaseVersion": "OB52",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1"
    }    

# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================
    payload = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang_b+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
    data = payload
    data = data.replace('afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'.encode(),access_token.encode())
    data = data.replace('1d8ec0240ede109973f3321b9354b44d'.encode(),open_id.encode())
    d = encrypt_api(data.hex())


    Final_Payload = bytes.fromhex(d)
    if region.lower() == "me":
        URL = "https://loginbp.common.ggbluefox.com/MajorLogin"
    else:
        URL = "https://loginbp.ggblueshark.com/MajorLogin"
    RESPONSE = requests.post(URL, headers=headers, data=Final_Payload,verify=False) 
    
    if RESPONSE.status_code == 200:
        if len(RESPONSE.text) < 10:
            return False


        json_result = get_available_room(RESPONSE.content.hex())
        parsed_data = json.loads(json_result)

        BASE64_TOKEN = parsed_data['8']['data']

        second_dot_index = BASE64_TOKEN.find(".", BASE64_TOKEN.find(".") + 1)     
        time.sleep(0.2)
        BASE64_TOKEN = BASE64_TOKEN[:second_dot_index+44]
        
        dat = GET_PAYLOAD_BY_DATA(BASE64_TOKEN,access_token,1,region, None, uid, password)
        return dat





import base64
def GET_PAYLOAD_BY_DATA(JWT_TOKEN, NEW_ACCESS_TOKEN, date, region, custom_prefix=None, original_uid=None, original_password=None):
        try:
            token_payload_base64 = JWT_TOKEN.split('.')[1]
            token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
            decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
            decoded_payload = json.loads(decoded_payload)
            NEW_EXTERNAL_ID = decoded_payload['external_id']
            SIGNATURE_MD5 = decoded_payload['signature_md5']
            now = dt.datetime.now()
            now = str(now)[:len(str(now))-7]
            formatted_time = date
            PAYLOAD =b':\x071.111.2\xaa\x01\x02ar\xb2\x01 55ed759fcf94f85813e57b2ec8492f5c\xba\x01\x014\xea\x01@6fb7fdef8658fd03174ed551e82b71b21db8187fa0612c8eaf1b63aa687f1eae\x9a\x06\x014\xa2\x06\x014'
            PAYLOAD = PAYLOAD.replace(b"2023-12-24 04:21:34", str(now).encode()) 
            PAYLOAD = PAYLOAD.replace(b"15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6", NEW_ACCESS_TOKEN.encode("UTF-8"))
            PAYLOAD = PAYLOAD.replace(b"4666ecda0003f1809655a7a8698573d0", NEW_EXTERNAL_ID.encode("UTF-8"))
            PAYLOAD = PAYLOAD.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
            PAYLOAD = PAYLOAD.hex()
            PAYLOAD = encrypt_api(PAYLOAD)
            PAYLOAD = bytes.fromhex(PAYLOAD)
            
            data = GET_LOGIN_DATA(JWT_TOKEN, PAYLOAD, region)
           
            # Extract the actual UID and password from the JWT token
            try:
                token_payload_base64 = JWT_TOKEN.split('.')[1]
                token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
                decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
                decoded_payload = json.loads(decoded_payload)
                
                # Extract account info from the decoded payload
                account_id = decoded_payload.get('account_id', 'unknown')
                nickname = decoded_payload.get('nickname', 'unknown')
                server = decoded_payload.get('lock_region', 'unknown')
                # Generate a password for this account
                password = generate_custom_password()
                
                return {
                    "data": data, 
                    "response": "success", 
                    "status_code": 200, 
                    "name": nickname, 
                    "uid": str(original_uid) if original_uid else str(account_id), 
                    "password": str(original_password) if original_password else password,
                    "account_id": str(account_id),
                    "server": str(server)
                }
            except Exception as e:
                print(f"{red}Error extracting account info: {e}")
                return {"data": data, "response": "success", "status_code": 200, "name": "unknown", "uid": "unknown", "password": "unknown"}
        except Exception as e:
            print(f"{red}{bold}Error in GET_PAYLOAD_BY_DATA: {e}")

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"{red}{bold}error {e}")
        return None

def GET_LOGIN_DATA(JWT_TOKEN, PAYLOAD, region):
    if region.lower() == "me":
        url = 'https://clientbp.common.ggbluefox.com/GetLoginData'
    else:
        link = get_region_url(region)
        if link:
            url = f"{link}GetLoginData"
        else:
            url = 'https://clientbp.ggblueshark.com/GetLoginData'

    headers = {
        'Expect': '100-continue',
        'Authorization': f'Bearer {JWT_TOKEN}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB52',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; G011A Build/PI)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    
    max_retries = 3
    attempt = 0

    while attempt < max_retries:
        try:
            response = requests.post(url, headers=headers, data=PAYLOAD,verify=False)
            response.raise_for_status()    
            x = response.content.hex()
            json_result = get_available_room(x)
            parsed_data = json.loads(json_result)
            
            return parsed_data
        
        except requests.RequestException as e:
            print(f"{red}{bold}Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Retrying...")
            attempt += 1
            time.sleep(2)
    print(f"{red}{bold}Failed to get login data after multiple attempts.")
    return None, None


# =============================================================
#  Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC)
#    - Custom account name prefix and superscript uniqueness
#    - Batch account creation with JSON export
#    - Secure, automated, and user-friendly
# -------------------------------------------------------------
#  Developer: ZENIHT
#  Contact: ZENIHT Official | Discord Server
#  All users of this script will see this credit.
# =============================================================

import os
import json

def get_user_inputs():
        # Set window title (works on Windows)
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("Free Fire Guest account generator By ZENIHT")
    except Exception:
        pass
    """Get user inputs for account creation"""
    # Colorful ASCII Art Banner
    ascii_banner = f"""
{bold}{Fore.CYAN} ███████╗███████╗███╗   ██╗██╗██╗  ██╗████████╗
╚══███╔╝██╔════╝████╗  ██║██║██║  ██║╚══██╔══╝
  ███╔╝ █████╗  ██╔██╗ ██║██║███████║   ██║   
 ███╔╝  ██╔══╝  ██║╚██╗██║██║██╔══██║   ██║   
███████╗███████╗██║ ╚████║██║██║  ██║   ██║   
╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝   ╚═╝{Fore.RESET}
"""
    subtitle = f"{bold}{Fore.MAGENTA}★ ZENIHT FF Generator ★{Fore.RESET}"
    divider = f"{Fore.LIGHTBLACK_EX}{'-'*54}{Fore.RESET}"
    print(ascii_banner)
    print(subtitle)
    print(divider)
    print(f"{bold}{Fore.GREEN}Welcome to the Ultimate Free Fire Account Generator!{Fore.RESET}")
    print(f"{Fore.YELLOW}Create guest accounts for any region, fast and easy.{Fore.RESET}\n")

    # Get region
    region = input(f"{bold}{red}[{lg}+{red}]{red} Choose Region (ME, IND, VN, BR, ID, TH, BD, PK, TW, EU, CIS, NA, SAC) : {Fore.RESET}").upper()

    # Get account name prefix
    print(f"{bold}{Fore.YELLOW}Note: Account names will use superscript digits (⁰¹²³⁴⁵⁶⁷⁸⁹) for uniqueness.{Fore.RESET}")
    account_name = input(f"{bold}{red}[{lg}+{red}]{red} Enter account name prefix (default: ZENIHT-X) : {Fore.RESET}").strip()
    if not account_name:
        account_name = "ZENIHT"

    # Get output filename
    try:
        output_file = input(f"{bold}{red}[{lg}+{red}]{red} Enter output filename (default: accounts_generated.json) : {Fore.RESET}").strip()
        if not output_file:
            output_file = "accounts_generated.json"
        if not output_file.endswith('.json'):
            output_file += '.json'
        # Ensure output is in 'accounts' folder in the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "accounts")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, output_file)
    except Exception as e:
        print(f"[ERROR] Exception during output filename step: {e}")
        input("Press Enter to exit...")
        return None, None, None, None

    # Get number of accounts
    while True:
        try:
            num_accounts = input(f"{bold}{red}[{lg}+{red}]{red} How many accounts to create? (default: 10) : {Fore.RESET}").strip()
            if not num_accounts:
                num_accounts = 10
            else:
                num_accounts = int(num_accounts)
            if num_accounts <= 0:
                print(f"{red}{bold}Please enter a positive number!{Fore.RESET}")
                continue
            break
        except ValueError:
            print(f"{red}{bold}Please enter a valid number!{Fore.RESET}")

    print(f"\n{bold}{green}=== Configuration Summary ==={Fore.RESET}")
    print(f"{bold}Region: {lg}{region}{Fore.RESET}")
    print(f"{bold}Account Name Prefix: {lg}{account_name}{Fore.RESET}")
    print(f"{bold}Output File: {lg}{output_file}{Fore.RESET}")
    print(f"{bold}Number of Accounts: {lg}{num_accounts}{Fore.RESET}")

    try:
        confirm = input(f"\n{bold}{red}[{lg}+{red}]{red} Proceed with these settings? (y/n) : {Fore.RESET}").lower()
        if confirm not in ['y', 'yes']:
            print(f"{red}{bold}Operation cancelled.{Fore.RESET}")
            input("Press Enter to exit...")
            return None, None, None, None
    except Exception as e:
        print(f"[ERROR] Exception during confirmation step: {e}")
        input("Press Enter to exit...")
        return None, None, None, None

    return region, account_name, output_file, num_accounts

# =============================================================
#  Subscription and Client Management System
# =============================================================

TOKEN = os.getenv("DISCORD_TOKEN", "TU_TOKEN_AQUI")
OWNER_ID = 1192837091881648218

# Database paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "db_clients.json")
ACCOUNTS_DIR = os.path.join(SCRIPT_DIR, "accounts")
os.makedirs(ACCOUNTS_DIR, exist_ok=True)

def load_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content: return {}
                return json.loads(content)
        except Exception as e:
            print(f"{red}!! Error cargando DB: {e}")
            return {}
    return {}

def save_db(db):
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)
    except Exception as e:
        print(f"{red}!! Error guardando DB: {e}")

def is_paid(user_id):
    if user_id == OWNER_ID:
        return True, "Infinity"
    
    db = load_db()
    user_str = str(user_id)
    
    if user_str in db:
        client_data = db[user_str]
        expiry_str = client_data.get("expiry")
        if not expiry_str:
            return False, 0
        
        try:
            expiry_dt = dt.datetime.fromisoformat(expiry_str)
            now = dt.datetime.now()
            if now < expiry_dt:
                remaining = (expiry_dt - now).days
                return True, remaining if remaining > 0 else "Today"
        except:
            return False, 0
            
    return False, 0

def has_used_free_trial(user_id):
    db = load_db()
    user_str = str(user_id)
    if user_str in db:
        return db[user_str].get("used_free", False)
    return False

def mark_free_trial_used(user_id):
    db = load_db()
    user_str = str(user_id)
    if user_str not in db:
        db[user_str] = {"used_free": True, "expiry": None}
    else:
        db[user_str]["used_free"] = True
    save_db(db)

class ZENIHTBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        print(f"{green}Sincronizando comandos de barra...")
        await self.tree.sync()
        print(f"{green}Comandos sincronizados!")

    async def on_ready(self):
        print(f"{green}======================================")
        print(f"{green} Bot {self.user} está en línea!")
        print(f"{green} Propietario ID: {OWNER_ID}")
        print(f"{green}======================================")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Fire Premium"))

    async def on_error(self, event_method, *args, **kwargs):
        print(f"{red}!! Error en {event_method}:")
        import traceback
        traceback.print_exc()

bot = ZENIHTBot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    print(f"{red}!! Error en comando: {error}")
    import traceback
    traceback.print_exc()
    try:
        if interaction.response.is_done():
            await interaction.followup.send(f"❌ **Error Interno:** `{error}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ **Error Interno:** `{error}`", ephemeral=True)
    except: pass

@bot.tree.command(name="crear", description="Generar cuentas de Free Fire (Suscripción requerida)")
@app_commands.describe(
    region="Región del juego",
    prefijo="Prefijo para los nombres",
    cantidad="Número de cuentas"
)
@app_commands.choices(region=[
    app_commands.Choice(name="Middle East (ME)", value="ME"),
    app_commands.Choice(name="India (IND)", value="IND"),
    app_commands.Choice(name="Vietnam (VN)", value="VN"),
    app_commands.Choice(name="Brazil (BR)", value="BR"),
    app_commands.Choice(name="Indonesia (ID)", value="ID"),
    app_commands.Choice(name="Thailand (TH)", value="TH"),
    app_commands.Choice(name="Bangladesh (BD)", value="BD"),
    app_commands.Choice(name="Pakistan (PK)", value="PK"),
    app_commands.Choice(name="Taiwan (TW)", value="TW"),
    app_commands.Choice(name="Europe (EU)", value="EU"),
    app_commands.Choice(name="CIS (CIS)", value="CIS"),
    app_commands.Choice(name="North America (NA)", value="NA"),
    app_commands.Choice(name="South America (SAC)", value="SAC")
])
async def crear(interaction: discord.Interaction, region: str, prefijo: str = "ZENIHT", cantidad: int = 1):
    user_id = interaction.user.id
    paid, time_left = is_paid(user_id)
    used_free = has_used_free_trial(user_id)

    # Access control logic
    if not paid and used_free and user_id != OWNER_ID:
        embed_pay = discord.Embed(
            title="🚫 Acceso Denegado - Plan Expirado",
            description="Ya has utilizado tu prueba gratuita de 1 uso.",
            color=discord.Color.red()
        )
        embed_pay.add_field(name="💳 Suscríbete para continuar", value=f"Contacta al dueño para obtener acceso ilimitado:\n**ID:** <@{OWNER_ID}>", inline=False)
        embed_pay.set_footer(text="ZENIHT Official | Premium Services")
        
        # Notify owner about a potential client
        owner = await bot.fetch_user(OWNER_ID)
        if owner:
            try:
                await owner.send(f"🔔 **Interés de compra:** El usuario `{interaction.user}` (ID: `{user_id}`) intentó usar el bot pero ya expiró su prueba gratuita.")
            except: pass
            
        await interaction.response.send_message(embed=embed_pay, ephemeral=True)
        return

    await interaction.response.defer()
    
    embed_init = discord.Embed(
        title="✨ ZENIHT FF Generator",
        description=f"🔄 Iniciando generación dinámica...\n🌍 **Región:** `{region}`\n📦 **Cantidad:** `{cantidad}`",
        color=discord.Color.from_rgb(0, 255, 255)
    )
    embed_init.add_field(name="💼 Estado", value="`Suscripción Activa`" if paid else "`Prueba Gratuita`", inline=True)
    embed_init.add_field(name="⏳ Vence en", value=f"`{time_left} días`" if isinstance(time_left, int) else f"`{time_left}`", inline=True)
    embed_init.set_footer(text="Generando con tecnología ZENIHT ✦")
    
    msg = await interaction.followup.send(embed=embed_init)

    successful_accounts = []
    
    for i in range(cantidad):
        try:
            r = await asyncio.to_thread(create_acc, region, prefijo)
            if r and isinstance(r, dict) and r.get('status_code') == 200:
                acc_data = {
                    "uid": r.get("uid"),
                    "pass": r.get("password"),
                    "name": r.get("name"),
                    "id": r.get("account_id")
                }
                successful_accounts.append(acc_data)
                
                # Professional Account Embed
                embed_acc = discord.Embed(
                    title=f"✅ CUENTA GENERADA #{len(successful_accounts)}",
                    description=f"**Nombre:** `{acc_data['name']}`",
                    color=discord.Color.from_rgb(138, 43, 226) # BlueViolet
                )
                embed_acc.add_field(name="🆔 UID", value=f"`{acc_data['uid']}`", inline=True)
                embed_acc.add_field(name="🔑 PASSWORD", value=f"`{acc_data['pass']}`", inline=True)
                embed_acc.add_field(name="🌍 REGIÓN", value=f"`{region}`", inline=True)
                embed_acc.set_thumbnail(url="https://i.imgur.com/8QWv8Wk.png")
                embed_acc.set_footer(text=f"ID Cliente: {user_id}")
                
                await interaction.channel.send(embed=embed_acc)

                # Dynamic update status embed
                if (i + 1) == cantidad:
                    embed_init.description = f"🔄 Procesando: **{i+1}/{cantidad}** cuentas..."
                    await msg.edit(embed=embed_init)
                
                if i < cantidad - 1:
                    await asyncio.sleep(1.5)
            else:
                print(f"Error en cuenta {i+1}")
        except Exception as e:
            print(f"Error crítico: {e}")

    # Finalize and notify
    if successful_accounts:
        # Save trial used
        if not paid and user_id != OWNER_ID:
            mark_free_trial_used(user_id)

        # Final Summary Embed
        embed_final = discord.Embed(
            title="🏁 ✧ GENERACIÓN FINALIZADA ✧",
            description=f"Se han entregado satisfactoriamente **{len(successful_accounts)}** cuentas en la región `{region}`.",
            color=discord.Color.from_rgb(0, 255, 127) # Spring Green
        )
        embed_final.set_footer(text="Gracias por usar ZENIHT FF Premium")

        # Prepare final message contents
        files = []
        
        # If only 1 account, generate and attach guest100067.dat
        if len(successful_accounts) == 1:
            acc = successful_accounts[0]
            dat_json = {
                "guest_account_info": {
                    "com.garena.msdk.guest_uid": str(acc['uid']),
                    "com.garena.msdk.guest_password": str(acc['pass'])
                }
            }
            dat_content = json.dumps(dat_json)
            dat_file = io.BytesIO(dat_content.encode('utf-8'))
            files.append(discord.File(dat_file, filename="guest100067.dat"))

        await interaction.channel.send(content=f"<@{user_id}>", embed=embed_final, files=files)
    else:
        await interaction.followup.send("❌ Error: No se pudo generar ninguna cuenta. Revisa las regiones e intenta más tarde.", ephemeral=True)

@bot.tree.command(name="add_client", description="Añadir cliente a la lista blanca (Solo Dueño)")
@app_commands.describe(user_id="ID de Discord del cliente", tiempo="Ejemplo: 7d (días) o 1m (mes)")
async def add_client(interaction: discord.Interaction, user_id: str, tiempo: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    db = load_db()
    
    # Parse time
    now = dt.datetime.now()
    if tiempo.endswith('d'):
        expiry = now + timedelta(days=int(tiempo[:-1]))
    elif tiempo.endswith('m'):
        expiry = now + timedelta(days=int(tiempo[:-1]) * 30)
    else:
        await interaction.response.send_message("❌ Formato inválido. Usa `7d` para días o `1m` para meses.", ephemeral=True)
        return

    db[str(user_id)] = {
        "expiry": expiry.isoformat(),
        "added_at": now.isoformat(),
        "used_free": True
    }
    save_db(db)
    
    embed = discord.Embed(
        title="✅ Cliente Añadido",
        description=f"El usuario <@{user_id}> ha sido añadido exitosamente.",
        color=discord.Color.green()
    )
    embed.add_field(name="⏳ Expiración", value=f"`{expiry.strftime('%d/%m/%Y %H:%M')}`", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info", description="Muestra tu estado actual")
async def info(interaction: discord.Interaction):
    paid, time_left = is_paid(interaction.user.id)
    embed = discord.Embed(
        title="★ ZENIHT ✦ Perfil",
        color=discord.Color.blue()
    )
    embed.add_field(name="🆔 Tu ID", value=f"`{interaction.user.id}`", inline=True)
    embed.add_field(name="💼 Estado", value="`Premium`" if paid else "`Prueba/Expirado`", inline=True)
    if paid:
        embed.add_field(name="⏳ Días restantes", value=f"`{time_left}`", inline=False)
    
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="list_clients", description="Listar todos los clientes premium (Solo Dueño)")
async def list_clients(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ No tienes permisos para usar este comando.", ephemeral=True)
        return

    db = load_db()
    if not db:
        await interaction.response.send_message("📂 Base de datos vacía.", ephemeral=True)
        return

    embed = discord.Embed(title="📋 Lista de Clientes Premium", color=discord.Color.blue())
    count = 0
    for user_id, data in db.items():
        expiry = data.get("expiry")
        if expiry:
            count += 1
            exp_dt = dt.datetime.fromisoformat(expiry)
            status = "✅" if dt.datetime.now() < exp_dt else "❌"
            embed.add_field(name=f"ID: {user_id}", value=f"{status} Vence: `{exp_dt.strftime('%d/%m/%Y')}`", inline=True)
        if count >= 25: break
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="broadcast", description="Enviar mensaje global a todos los clientes (Solo Dueño)")
@app_commands.describe(mensaje="Mensaje a enviar")
async def broadcast(interaction: discord.Interaction, mensaje: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        return
    
    await interaction.response.defer()
    db = load_db()
    success = 0
    for user_id in db:
        try:
            user_id_int = int(user_id)
            user = await bot.fetch_user(user_id_int)
            embed = discord.Embed(title="📢 Aviso de ZENIHT", description=mensaje, color=discord.Color.purple())
            await user.send(embed=embed)
            success += 1
        except: continue
        
    await interaction.followup.send(f"✅ Mensaje enviado a {success} usuarios.")

@bot.tree.command(name="announce", description="Enviar anuncio oficial al canal con mención")
async def announce(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        return
    
    msg_content = "@everyone @here\n"
    embed = discord.Embed(
        title="📢 ✧ ANUNCIO OFICIAL ZENIHT ✧",
        description=(
            "**¡HOLA A TODOS!**\n\n"
            "EL BOT **GENERADOR DE CUENTAS** YA ESTÁ DISPONIBLE PARA GENERAR CUENTAS EN CUALQUIER REGIÓN. ✨\n\n"
            "💬 **¿DUDAS?** SI TIENES DUDAS O ALGÚN PROBLEMA, NO DUDES EN PREGUNTAR.\n\n"
            "🛒 **COMPRAR PERMANENTE:** SI DESEAS COMPRAR EL BOT DE FORMA PERMANENTE, AVÍSAME.\n\n"
            "👤 **PROPIETARIO:** EL ÚNICO AUTORIZADO PARA HACER MÁS CUENTAS ES **MEME** (DUEÑO)."
        ),
        color=discord.Color.from_rgb(255, 69, 0) # OrangeRed
    )
    embed.set_thumbnail(url="https://i.imgur.com/8QWv8Wk.png")
    embed.set_footer(text="ZENIHT Official | Calidad y Seguridad")
    
    await interaction.response.send_message(content=msg_content, embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)
