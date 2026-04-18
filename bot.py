# =============================================================
#  ZENIHT FF PREMIUM - Free Fire Guest Account Generator
#  Developed by ZENIHT | Logic: 1shot Studio (Script Kittens)
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support (Full)
#    - JWT, Regional Server & GetLoginData handling
#    - Premium Discord UI (Slash Commands)
# -------------------------------------------------------------
#  Developer: ZENIHT
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
from datetime import datetime
import datetime as dt

colorama.init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import discord
from discord import app_commands
from discord.ext import commands
import asyncio

# --- Constants & Config ---
hex_key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
key = bytes.fromhex(hex_key)
default_key = b'Yg&tc%DEuh6%Zc^8'
default_iv = b'6oyZDr22E3ychjM%'
freefire_version = "OB52"
client_secret = key

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = 1192837091881648218

# Colors
red = Fore.RED
lg = Fore.LIGHTGREEN_EX
green = Fore.GREEN
bold = Style.BRIGHT
purpel = Fore.MAGENTA

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

# --- Protobuf & Encryption Utilities ---

def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

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

def E_AEs(Pc):
    Z = bytes.fromhex(Pc)
    key_aes = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv_aes = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    K = AES.new(key_aes , AES.MODE_CBC , iv_aes)
    R = K.encrypt(pad(Z , AES.block_size))
    return bytes.fromhex(R.hex())

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key_aes = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv_aes = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key_aes, AES.MODE_CBC, iv_aes)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

# --- API Core Logic ---

def generate_random_name(total_length=12, custom_prefix=None, region=None):
    superscript_digits = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    base_name = custom_prefix if custom_prefix else "ZENIHT"
    if region and region.upper() == "BD": total_length = 8
    random_superscripts = ''.join(random.choice(superscript_digits) for _ in range(4))
    return f"{base_name}{random_superscripts}"

def generate_custom_password(random_length=9):
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(random_length)).upper()
    return f"ZENIHT-{random_part}-X64"

def create_acc(region, custom_prefix=None, max_retries=3):
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
                "Content-Type": "application/x-www-form-urlencoded"
            }
            response = requests.post(url, headers=headers, data=data, timeout=30)
            if response.status_code == 200:
                uid = response.json().get('uid')
                if uid: return token_step(uid, password, region, custom_prefix)
            time.sleep(1)
        except Exception as e: print(f"Create error: {e}")
    return "Error: Registro fallido"

def token_step(uid, password, region, custom_prefix=None):
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        data = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": client_secret, "client_id": "100067"}
        response = requests.post(url, data=data, timeout=30)
        if response.status_code == 200:
            json_response = response.json()
            access_token = json_response['access_token']
            open_id = json_response['open_id']
            keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30] * 4
            encoded = "".join(chr(ord(open_id[i]) ^ keystream[i % len(keystream)]) for i in range(len(open_id)))
            field = ''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in encoded)
            field = codecs.decode(field, 'unicode_escape').encode('latin1')
            return Major_Regsiter(access_token, open_id, field, uid, password, region, custom_prefix)
    except Exception as e: print(f"Token error: {e}")
    return "Error en Token"

def Major_Regsiter(access_token, open_id, field, uid, password, region, custom_prefix=None):
    try:
        url = "https://loginbp.ggblueshark.com/MajorRegister"
        name = generate_random_name(custom_prefix=custom_prefix, region=region)
        headers = {"Content-Type": "application/x-www-form-urlencoded", "ReleaseVersion": "OB52", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)", "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"}
        payload = {1: name, 2: access_token, 3: open_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field, 15: "en", 16: 1, 17: 1}
        payload_hex = CrEaTe_ProTo(payload).hex()
        body = bytes.fromhex(E_AEs(payload_hex).hex())
        response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        if response.status_code == 200:
            return login_step(uid, password, access_token, open_id, name, region)
    except Exception as e: print(f"Register error: {e}")
    return "Error en Register"

def login_step(uid, password, access_token, open_id, name, region):
    try:
        lang = REGION_LANG.get(region, "en")
        lang_b = lang.encode("ascii")
        headers = {
            "Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded", "Expect": "100-continue",
            "Host": "loginbp.ggblueshark.com", "ReleaseVersion": "OB52", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"
        }    
        payload = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang_b+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        data = payload.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode()).replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
        body = bytes.fromhex(encrypt_api(data.hex()))
        url = "https://loginbp.common.ggbluefox.com/MajorLogin" if region.lower() == "me" else "https://loginbp.ggblueshark.com/MajorLogin"
        response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        
        if response.status_code == 200:
            if lang.lower() not in ["ar", "en"]:
                json_result = get_available_room(response.content.hex())
                jwt_token = json.loads(json_result)['8']['data']
                r_cr = requests.post("https://loginbp.ggblueshark.com/ChooseRegion", data=bytes.fromhex(encrypt_api(CrEaTe_ProTo({1: "RU" if region.lower() == "cis" else region}).hex())), headers={"Authorization": f"Bearer {jwt_token}", "ReleaseVersion": "OB52"}, verify=False)
                if r_cr.status_code == 200: return login_server_step(uid, password, access_token, open_id, name, region)
            
            jwt_token = response.text[response.text.find("eyJhbGciOiJIUzI1NiIsInN2ciIj"):-1]
            if not jwt_token: jwt_token = response.text[response.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6I"):-1]
            dot_idx = jwt_token.find(".", jwt_token.find(".") + 1)
            jwt_token = jwt_token[:dot_idx+44]
            return GET_PAYLOAD_BY_DATA(jwt_token, access_token, name, region, uid, password)
    except Exception as e: print(f"Login error: {e}")
    return "Error en Login"

def login_server_step(uid, password, access_token, open_id, name, region):
    try:
        lang = REGION_LANG.get(region, "en") ; lang_b = lang.encode("ascii")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "ReleaseVersion": "OB52", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)"}
        payload = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang_b+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        data = payload.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode()).replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
        body = bytes.fromhex(encrypt_api(data.hex()))
        url = "https://loginbp.common.ggbluefox.com/MajorLogin" if region.lower() == "me" else "https://loginbp.ggblueshark.com/MajorLogin"
        response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        if response.status_code == 200:
            jwt_token = json.loads(get_available_room(response.content.hex()))['8']['data']
            dot_idx = jwt_token.find(".", jwt_token.find(".") + 1)
            jwt_token = jwt_token[:dot_idx+44]
            return GET_PAYLOAD_BY_DATA(jwt_token, access_token, name, region, uid, password)
    except Exception as e: print(f"LoginServer error: {e}")
    return "Error en LoginServer"

def GET_PAYLOAD_BY_DATA(JWT_TOKEN, NEW_ACCESS_TOKEN, nickname, region, original_uid, original_password):
    try:
        token_payload_base64 = JWT_TOKEN.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = json.loads(base64.urlsafe_b64decode(token_payload_base64).decode('utf-8'))
        NEW_EXTERNAL_ID = decoded_payload['external_id']
        SIGNATURE_MD5 = decoded_payload['signature_md5']
        now_str = str(datetime.now())[:19]
        PAYLOAD = b':\x071.111.2\xaa\x01\x02ar\xb2\x01 55ed759fcf94f85813e57b2ec8492f5c\xba\x01\x014\xea\x01@6fb7fdef8658fd03174ed551e82b71b21db8187fa0612c8eaf1b63aa687f1eae\x9a\x06\x014\xa2\x06\x014'
        PAYLOAD = PAYLOAD.replace(b"2023-12-24 04:21:34", now_str.encode()) 
        PAYLOAD = PAYLOAD.replace(b"15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6", NEW_ACCESS_TOKEN.encode("UTF-8"))
        PAYLOAD = PAYLOAD.replace(b"4666ecda0003f1809655a7a8698573d0", NEW_EXTERNAL_ID.encode("UTF-8"))
        PAYLOAD = PAYLOAD.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
        
        # Real call to GetLoginData
        _ = GET_LOGIN_DATA(JWT_TOKEN, bytes.fromhex(encrypt_api(PAYLOAD.hex())), region)
        
        return {
            "status_code": 200, "name": nickname, "uid": str(original_uid), "password": str(original_password), "region": region,
            "account_id": str(decoded_payload.get('account_id', 'unknown')), "server": str(decoded_payload.get('lock_region', 'unknown'))
        }
    except Exception as e: print(f"Payload error: {e}")
    return "Error en Payload"

def GET_LOGIN_DATA(JWT_TOKEN, PAYLOAD, region):
    url = f"{REGION_URLS.get(region, 'https://clientbp.ggblueshark.com/')}GetLoginData"
    if region.lower() == "me": url = 'https://clientbp.common.ggbluefox.com/GetLoginData'
    headers = {'Authorization': f'Bearer {JWT_TOKEN}', 'X-Unity-Version': '2018.4.11f1', 'X-GA': 'v1 1', 'ReleaseVersion': 'OB52', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; G011A Build/PI)', 'Connection': 'close'}
    try:
        response = requests.post(url, headers=headers, data=PAYLOAD, verify=False, timeout=30)
        return json.loads(get_available_room(response.content.hex()))
    except: return None

def get_available_room(input_text):
    try: results = Parser().parse(input_text) ; return json.dumps(parse_results(results.results))
    except: return None

def parse_results(results):
    res = {}
    for r in results:
        if r.wire_type == "varint": res[r.field] = {"wire": r.wire_type, "data": r.data}
        elif r.wire_type in ["string", "bytes"]: res[r.field] = {"wire": r.wire_type, "data": r.data if isinstance(r.data, str) else r.data.decode(errors='ignore')}
        elif r.wire_type == 'length_delimited': res[r.field] = {"wire": r.wire_type, "data": parse_results(r.data.results)}
    return res

# --- Database & Discord Logic ---

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_clients.json")
def load_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"clients": {}, "partners": [], "stats": {"total_created": 0}}

def save_db(db):
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f: json.dump(db, f, indent=4)
    except: pass

def is_paid(user_id):
    if user_id == OWNER_ID: return True, "∞"
    db = load_db() ; clients = db.get("clients", {}) ; user_str = str(user_id)
    if user_str in clients:
        expiry = clients[user_str].get("expiry")
        if expiry:
            try:
                exp_dt = dt.datetime.fromisoformat(expiry)
                if dt.datetime.now() < exp_dt: return True, (exp_dt - dt.datetime.now()).days
            except: pass
    return False, 0

class ZENIHTBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default() ; intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
    async def setup_hook(self): await self.tree.sync()
    async def on_ready(self):
        print(f"\n{Fore.GREEN} ZENIHT BOT ONLINE: {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Fire Gen"))

bot = ZENIHTBot()

@bot.tree.command(name="crear", description="Generar cuentas FF")
@app_commands.describe(region="Región", prefijo="Prefijo", cantidad="Máximo 10")
async def crear(interaction: discord.Interaction, region: str, prefijo: str = "ZENIHT", cantidad: int = 1):
    await interaction.response.defer()
    user_id = interaction.user.id ; paid, _ = is_paid(user_id)
    if not paid and user_id != OWNER_ID:
        db = load_db()
        if db.get("clients", {}).get(str(user_id), {}).get("used_free"):
            await interaction.followup.send("❌ Prueba gratuita ya utilizada.", ephemeral=True) ; return

    msg = await interaction.followup.send(embed=discord.Embed(title="⚡ ZENIHT FF", description="Iniciando...", color=0x00FFFF))
    successful = [] ; last_error = ""
    for i in range(min(cantidad, 10)):
        r = await asyncio.to_thread(create_acc, region.upper(), prefijo)
        if isinstance(r, dict):
            successful.append(r)
            emb = discord.Embed(title=f"✅ CUENTA #{len(successful)}", color=0x8A2BE2)
            emb.add_field(name="🆔 UID", value=f"`{r['uid']}`") ; emb.add_field(name="🔑 PASS", value=f"`{r['password']}`")
            await interaction.channel.send(embed=emb)
            await asyncio.sleep(2)
        else: last_error = str(r)

    if successful:
        db = load_db() ; db["stats"]["total_created"] = db["stats"].get("total_created", 0) + len(successful)
        if not paid:
            if str(user_id) not in db["clients"]: db["clients"][str(user_id)] = {}
            db["clients"][str(user_id)]["used_free"] = True
        save_db(db)
        await interaction.channel.send(content=f"<@{user_id}>", embed=discord.Embed(title="🏁 LISTO", description=f"Cuentas: {len(successful)}", color=0x00FF7F))
    else: await interaction.followup.send(f"❌ Fallo.\n📌 Detalle: `{last_error}`")

@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):
    paid, tl = is_paid(interaction.user.id)
    emb = discord.Embed(title="👤 PERFIL", color=0x3498DB)
    emb.add_field(name="💼 Estado", value="`PREMIUM`" if paid else "`FREE`")
    emb.add_field(name="⏳ Días", value=f"`{tl}`")
    await interaction.response.send_message(embed=emb)

if __name__ == "__main__":
    if not TOKEN: print("TOKEN missing") ; sys.exit(1)
    bot.run(TOKEN)
