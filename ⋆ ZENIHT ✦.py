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
import io
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
red_c = Fore.RED
lg_c = Fore.LIGHTGREEN_EX
green_c = Fore.GREEN
bold_c = Style.BRIGHT
purpel_c = Fore.MAGENTA

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

# --- Utilities ---

def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F ; N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested = CrEaTe_ProTo(value)
            packet.extend(EnC_Vr((field << 3) | 2) + EnC_Vr(len(nested)) + nested)
        elif isinstance(value, int):
            packet.extend(EnC_Vr((field << 3) | 0) + EnC_Vr(value))           
        elif isinstance(value, (str, bytes)):
            enc = value.encode() if isinstance(value, str) else value
            packet.extend(EnC_Vr((field << 3) | 2) + EnC_Vr(len(enc)) + enc)           
    return packet

def E_AEs(Pc):
    Z = bytes.fromhex(Pc)
    K = AES.new(b'Yg&tc%DEuh6%Zc^8' , AES.MODE_CBC , b'6oyZDr22E3ychjM%')
    return K.encrypt(pad(Z , AES.block_size))

def encrypt_api(plain_text):
    Z = bytes.fromhex(plain_text)
    K = AES.new(b'Yg&tc%DEuh6%Zc^8' , AES.MODE_CBC , b'6oyZDr22E3ychjM%')
    return K.encrypt(pad(Z , AES.block_size)).hex()

# --- API Functions ---

def generate_random_name(custom_prefix=None, region=None):
    superscript_digits = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
    base = custom_prefix if custom_prefix else "1shot"
    return f"{base}{''.join(random.choice(superscript_digits) for _ in range(4))}"

def create_acc(region, custom_prefix=None, max_retries=3):
    u_agents = ["GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)", "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;IN;)", "GarenaMSDK/4.0.19P6(SM-G973F ;Android 11;en;US;)"]
    for i in range(max_retries):
        try:
            pw = f"1shot-{''.join(random.choices(string.ascii_uppercase + string.digits, k=9))}-X64"
            data = f"password={pw}&client_type=2&source=2&app_id=100067"
            sig = hmac.new(key, data.encode('utf-8'), hashlib.sha256).hexdigest()
            headers = {"User-Agent": u_agents[i % 3], "Authorization": "Signature " + sig, "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip", "Connection": "Keep-Alive"}
            res = requests.post("https://100067.connect.garena.com/oauth/guest/register", headers=headers, data=data, timeout=30)
            if res.status_code == 200:
                uid = res.json().get('uid')
                if uid: return token_step(uid, pw, region, custom_prefix)
            print(f"{Fore.RED}[!] Register failed: {res.status_code} - {res.text}")
            time.sleep(1)
        except Exception as e: print(f"Register ex: {e}")
    return "Error: Registro fallido"

def token_step(uid, pw, region, custom_prefix=None):
    try:
        data = {"uid": uid, "password": pw, "response_type": "token", "client_type": "2", "client_secret": client_secret, "client_id": "100067"}
        headers = {"Host": "100067.connect.garena.com", "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;IN;)", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip, deflate, br", "Connection": "close"}
        res = requests.post("https://100067.connect.garena.com/oauth/guest/token/grant", headers=headers, data=data, timeout=30)
        if res.status_code == 200:
            json_res = res.json() ; acc_t = json_res['access_token'] ; o_id = json_res['open_id']
            ks = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30] * 4
            enc = "".join(chr(ord(o_id[i]) ^ ks[i % 32]) for i in range(len(o_id)))
            field = codecs.decode(''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in enc), 'unicode_escape').encode('latin1')
            return Major_Regsiter(acc_t, o_id, field, uid, pw, region, custom_prefix)
    except Exception as e: print(f"Token ex: {e}")
    return "Error en Token"

def Major_Regsiter(acc_t, o_id, field, uid, pw, region, custom_prefix=None):
    try:
        name = generate_random_name(custom_prefix, region)
        headers = {"Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded", "Expect": "100-continue", "Host": "loginbp.ggblueshark.com", "ReleaseVersion": "OB52", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)", "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"}
        payload = {1: name, 2: acc_t, 3: o_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field, 15: "en", 16: 1, 17: 1}
        body = E_AEs(CrEaTe_ProTo(payload).hex())
        res = requests.post("https://loginbp.ggblueshark.com/MajorRegister", headers=headers, data=body, verify=False, timeout=30)
        if res.status_code == 200: return login_step(uid, pw, acc_t, o_id, name, region)
    except Exception as e: print(f"Reg ex: {e}")
    return "Error en Register"

def login_step(uid, pw, acc_t, o_id, name, region):
    try:
        lang = REGION_LANG.get(region, "en") ; lang_b = lang.encode("ascii")
        headers = {"Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded", "Expect": "100-continue", "Host": "loginbp.ggblueshark.com", "ReleaseVersion": "OB52", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)", "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"}
        p = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang_b+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        data = p.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', acc_t.encode()).replace(b'1d8ec0240ede109973f3321b9354b44d', o_id.encode())
        body = bytes.fromhex(encrypt_api(data.hex()))
        url = "https://loginbp.common.ggbluefox.com/MajorLogin" if region.lower() == "me" else "https://loginbp.ggblueshark.com/MajorLogin"
        resp = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        if resp.status_code == 200:
            if lang.lower() not in ["ar", "en"]:
                jt = json.loads(get_available_room(resp.content.hex()))['8']['data']
                f = bytes.fromhex(encrypt_api(CrEaTe_ProTo({1: "RU" if region.lower() == "cis" else region}).hex()))
                r_cr = requests.post("https://loginbp.ggblueshark.com/ChooseRegion", data=f, headers={"Authorization": f"Bearer {jt}", "ReleaseVersion": "OB52"}, verify=False)
                if r_cr.status_code == 200: return login_server_step(uid, pw, acc_t, o_id, name, region)
            jt = resp.text[resp.text.find("eyJhbGciOiJIUzI1NiIsInN2ciIj"):-1]
            if not jt: jt = resp.text[resp.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6I"):-1]
            jt = jt[:jt.find(".", jt.find(".") + 1)+44]
            return GET_PAYLOAD_BY_DATA(jt, acc_t, name, region, uid, pw)
    except Exception as e: print(f"Login ex: {e}")
    return "Error en Login"

def login_server_step(uid, pw, acc_t, o_id, name, region):
    try:
        lang = REGION_LANG.get(region, "en") ; lang_b = lang.encode("ascii")
        headers = {"Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded", "Expect": "100-continue", "Host": "loginbp.ggblueshark.com", "ReleaseVersion": "OB52", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)", "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"}
        p = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang_b+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        data = p.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', acc_t.encode()).replace(b'1d8ec0240ede109973f3321b9354b44d', o_id.encode())
        body = bytes.fromhex(encrypt_api(data.hex()))
        url = "https://loginbp.common.ggbluefox.com/MajorLogin" if region.lower() == "me" else "https://loginbp.ggblueshark.com/MajorLogin"
        resp = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        if resp.status_code == 200:
            jt = json.loads(get_available_room(resp.content.hex()))['8']['data']
            jt = jt[:jt.find(".", jt.find(".") + 1)+44]
            return GET_PAYLOAD_BY_DATA(jt, acc_t, name, region, uid, pw)
    except Exception as e: print(f"LoginS ex: {e}")
    return "Error en LoginServer"

def GET_PAYLOAD_BY_DATA(jt, acc_t, nickname, region, u, p):
    try:
        t_p = jt.split('.')[1] ; t_p += '=' * ((4 - len(t_p) % 4) % 4)
        dec = json.loads(base64.urlsafe_b64decode(t_p).decode('utf-8'))
        ext_id = dec['external_id'] ; sig_md5 = dec['signature_md5']
        p_bytes = b':\x071.111.2\xaa\x01\x02ar\xb2\x01 55ed759fcf94f85813e57b2ec8492f5c\xba\x01\x014\xea\x01@6fb7fdef8658fd03174ed551e82b71b21db8187fa0612c8eaf1b63aa687f1eae\x9a\x06\x014\xa2\x06\x014'
        p_bytes = p_bytes.replace(b"15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6", acc_t.encode()).replace(b"4666ecda0003f1809655a7a8698573d0", ext_id.encode()).replace(b"7428b253defc164018c604a1ebbfebdf", sig_md5.encode())
        _ = GET_LOGIN_DATA(jt, bytes.fromhex(encrypt_api(p_bytes.hex())), region)
        return {"status_code": 200, "name": nickname, "uid": str(u), "password": str(p), "region": region, "account_id": str(dec.get('account_id')), "server": str(dec.get('lock_region'))}
    except Exception as e: print(f"Payload error: {e}")
    return "Error en Payload"

def GET_LOGIN_DATA(jt, body, region):
    url = f"{REGION_URLS.get(region, 'https://clientbp.ggblueshark.com/')}GetLoginData"
    if region.lower() == "me": url = 'https://clientbp.common.ggbluefox.com/GetLoginData'
    headers = {'Authorization': f'Bearer {jt}', 'X-Unity-Version': '2018.4.11f1', 'X-GA': 'v1 1', 'ReleaseVersion': 'OB52', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; G011A Build/PI)', 'Connection': 'close'}
    try: res = requests.post(url, headers=headers, data=body, verify=False, timeout=30) ; return json.loads(get_available_room(res.content.hex()))
    except: return None

def get_available_room(txt):
    try: results = Parser().parse(txt) ; return json.dumps(parse_results(results.results))
    except: return None

def parse_results(results):
    res = {}
    for r in results:
        if r.wire_type == "varint": res[r.field] = {"wire": "varint", "data": r.data}
        elif r.wire_type in ["string", "bytes"]: res[r.field] = {"wire": "bytes", "data": r.data if isinstance(r.data, str) else r.data.decode(errors='ignore')}
        elif r.wire_type == 'length_delimited': res[r.field] = {"wire": "length", "data": parse_results(r.data.results)}
    return res

# --- DB & Bot ---

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

def is_paid(u_id):
    if u_id == OWNER_ID: return True, "∞"
    db = load_db() ; c = db.get("clients", {}) ; u_s = str(u_id)
    if u_s in c:
        exp = c[u_s].get("expiry")
        if exp:
            try:
                if dt.datetime.now() < dt.datetime.fromisoformat(exp): return True, (dt.datetime.fromisoformat(exp) - dt.datetime.now()).days
            except: pass
    return False, 0

class ZENIHTBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default() ; intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
    async def setup_hook(self): await self.tree.sync()
    async def on_ready(self): 
        print(f"\n{Fore.CYAN}======================================")
        print(f"{Fore.GREEN} ZENIHT BOT ONLINE: {self.user}")
        print(f"{Fore.YELLOW} VERSION: 2.1 (Hardened)")
        print(f"{Fore.CYAN}======================================\n")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Fire Gen"))

bot = ZENIHTBot()

@bot.tree.command(name="crear", description="Gen FF")
async def crear(interaction: discord.Interaction, region: str, prefijo: str = "ZENIHT", cantidad: int = 1):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except Exception as e:
        print(f"Defer error in crear: {e}")
        return
    u_id = interaction.user.id ; paid, _ = is_paid(u_id)
    if not paid and u_id != OWNER_ID:
        if load_db().get("clients", {}).get(str(u_id), {}).get("used_free"):
            await interaction.followup.send("❌ Prueba gratuita ya utilizada.", ephemeral=True) ; return

    msg = await interaction.followup.send(embed=discord.Embed(title="⚡ ZENIHT", description="Iniciando...", color=0x00FFFF))
    succ = [] ; last_err = ""
    for _ in range(min(cantidad, 10)):
        r = await asyncio.to_thread(create_acc, region.upper(), prefijo)
        if isinstance(r, dict):
            succ.append(r)
            emb = discord.Embed(title=f"✅ #{len(succ)}", color=0x8A2BE2)
            emb.add_field(name="🆔 UID", value=f"`{r['uid']}`") ; emb.add_field(name="🔑 PASS", value=f"`{r['password']}`")
            await interaction.channel.send(embed=emb)
            await asyncio.sleep(2)
        else: last_err = str(r)

    if succ:
        db = load_db() ; db["stats"]["total_created"] = db["stats"].get("total_created", 0) + len(succ)
        if not paid:
            if str(u_id) not in db["clients"]: db["clients"][str(u_id)] = {}
            db["clients"][str(u_id)]["used_free"] = True
        save_db(db)
        
        # Prepare files to send (guest100067.dat if only 1 account)
        files = []
        if len(succ) == 1:
            acc = succ[0]
            dat_json = {"guest_account_info": {"com.garena.msdk.guest_uid": str(acc['uid']), "com.garena.msdk.guest_password": str(acc['password'])}}
            dat_content = json.dumps(dat_json)
            dat_file = io.BytesIO(dat_content.encode('utf-8'))
            files.append(discord.File(dat_file, filename="guest100067.dat"))
        
        await interaction.channel.send(content=f"<@{u_id}>", embed=discord.Embed(title="🏁 LISTO", description=f"Cuentas: {len(succ)}", color=0x00FF7F), files=files)
    else: await interaction.followup.send(f"❌ Fallo.\n📌 Detalle: `{last_err}`")

@bot.tree.command(name="info")
async def info(interaction: discord.Interaction):
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except Exception as e:
        print(f"Defer error in info: {e}")
        return
    paid, tl = is_paid(interaction.user.id)
    emb = discord.Embed(title="� PERFIL", color=0x3498DB)
    emb.add_field(name="� Estado", value="`PREMIUM`" if paid else "`FREE`")
    emb.add_field(name="⏳ Días", value=f"`{tl}`")
    await interaction.followup.send(embed=emb)

if __name__ == "__main__":
    if not TOKEN: print("TOKEN missing") ; sys.exit(1)
    bot.run(TOKEN)
