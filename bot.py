# =============================================================
#  ZENIHT FF PREMIUM - Free Fire Guest Account Generator
#  Developed by ZENIHT
# -------------------------------------------------------------
#  Professional tool for generating Free Fire guest accounts.
#  Features:
#    - Multi-region support
#    - Custom account names and superscript uniqueness
#    - Batch account creation
#    - Premium Discord UI
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

colorama.init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import io
import datetime as dt
from datetime import timedelta

# Configuration
hex_key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
key = bytes.fromhex(hex_key)
default_key = b'Yg&tc%DEuh6%Zc^8'
default_iv = b'6oyZDr22E3ychjM%'
freefire_version = "OB52"
client_secret = key

# Discord Config
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

# --- Utility Functions ---

def get_region(language_code: str) -> str:
    return REGION_LANG.get(language_code)

def get_region_url(region_code: str) -> str:
    return REGION_URLS.get(region_code, None)

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

# --- API Logic ---

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
                if uid:
                    return token(uid, password, region, custom_prefix)
            time.sleep(1)
        except: continue
    return None

def token(uid , password , region, custom_prefix=None):
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        data = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": client_secret,
            "client_id": "100067",
        }
        response = requests.post(url, data=data, timeout=30)
        if response.status_code == 200:
            json_response = response.json()
            access_token = json_response['access_token']
            open_id = json_response['open_id']
            encoded = ""
            keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30] * 4
            for i in range(len(open_id)):
                encoded += chr(ord(open_id[i]) ^ keystream[i % len(keystream)])
            field = ''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in encoded)
            field = codecs.decode(field, 'unicode_escape').encode('latin1')
            return Major_Register(access_token, open_id, field, uid, password, region, custom_prefix)
    except: return None

def Major_Register(access_token , open_id , field , uid , password, region, custom_prefix=None):
    try:
        url = "https://loginbp.ggblueshark.com/MajorRegister"
        name = generate_random_name(custom_prefix=custom_prefix, region=region)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1"
        }
        payload_fields = {1: name, 2: access_token, 3: open_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field, 15: "en", 16: 1, 17: 1}
        payload = CrEaTe_ProTo(payload_fields).hex()
        body = bytes.fromhex(E_AEs(payload).hex())
        response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
        if response.status_code == 200:
            return login(uid , password, access_token , open_id, name , region)
    except: return None

def login(uid , password, access_token , open_id, name , region):
    lang = get_region(region).encode("ascii")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "ReleaseVersion": "OB52",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)"
    }    
    payload = b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02'+lang+b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
    data = payload.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode())
    data = data.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
    
    # Encrypt and send
    key_login = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv_login = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key_login, AES.MODE_CBC, iv_login)
    body = cipher.encrypt(pad(bytes.fromhex(data.hex()), AES.block_size))
    
    url = "https://loginbp.common.ggbluefox.com/MajorLogin" if region.lower() == "me" else "https://loginbp.ggblueshark.com/MajorLogin"
    response = requests.post(url, headers=headers, data=body, verify=False, timeout=30)
    
    if response.status_code == 200:
        return {
            "status_code": 200, 
            "name": name, 
            "uid": str(uid), 
            "password": str(password),
            "region": region
        }
    return None

# --- Database Management ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "db_clients.json")

def load_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "clients" not in data: data = {"clients": data, "partners": [], "stats": {"total_created": 0}}
                return data
        except: return {"clients": {}, "partners": [], "stats": {"total_created": 0}}
    return {"clients": {}, "partners": [], "stats": {"total_created": 0}}

def save_db(db):
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)
    except: pass

def is_admin(user_id):
    if user_id == OWNER_ID: return True
    db = load_db()
    return str(user_id) in db.get("partners", [])

def is_paid(user_id):
    if user_id == OWNER_ID: return True, "∞"
    db = load_db()
    clients = db.get("clients", {})
    user_str = str(user_id)
    if user_str in clients:
        expiry_str = clients[user_str].get("expiry")
        if not expiry_str: return False, 0
        try:
            expiry_dt = dt.datetime.fromisoformat(expiry_str)
            now = dt.datetime.now()
            if now < expiry_dt:
                days = (expiry_dt - now).days
                return True, days if days > 0 else "Hoy"
        except: pass
    return False, 0

# --- Discord Bot Setup ---

class ZENIHTBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"\n{Fore.CYAN}{bold}======================================")
        print(f"{Fore.GREEN} ZENIHT FF GEN ONLINE")
        print(f"{Fore.WHITE} Bot: {self.user}")
        print(f"{Fore.CYAN}{bold}======================================\n")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Fire Generator"))

bot = ZENIHTBot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    try:
        if interaction.response.is_done():
            await interaction.followup.send(f"❌ **Error:** `{error}`", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ **Error:** `{error}`", ephemeral=True)
    except: pass

# --- Slash Commands ---

@bot.tree.command(name="crear", description="Generar cuentas de Free Fire")
@app_commands.describe(region="Región", prefijo="Prefijo", cantidad="Máximo 10")
@app_commands.choices(region=[
    app_commands.Choice(name="Middle East (ME)", value="ME"),
    app_commands.Choice(name="India (IND)", value="IND"),
    app_commands.Choice(name="Indonesia (ID)", value="ID"),
    app_commands.Choice(name="Brazil (BR)", value="BR"),
    app_commands.Choice(name="USA (SAC)", value="SAC"),
    app_commands.Choice(name="Europe (EU)", value="EU")
])
async def crear(interaction: discord.Interaction, region: str, prefijo: str = "ZENIHT", cantidad: int = 1):
    await interaction.response.defer()
    
    user_id = interaction.user.id
    paid, time_left = is_paid(user_id)
    
    # Trial check
    if not paid and user_id != OWNER_ID:
        db = load_db()
        if db["clients"].get(str(user_id), {}).get("used_free"):
            embed = discord.Embed(title="🚫 Acceso Denegado", description="Prueba gratuita ya utilizada. Contacta al dueño.", color=0xFF0000)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

    embed_init = discord.Embed(title="⚡ ZENIHT FF GENERATOR", description="🔄 Iniciando procesos maestros...", color=0x00FFFF)
    embed_init.set_footer(text="Tecnología ZENIHT X64")
    msg = await interaction.followup.send(embed=embed_init)

    successful = []
    for i in range(min(cantidad, 10)):
        try:
            r = await asyncio.to_thread(create_acc, region, prefijo)
            if r:
                successful.append(r)
                embed_acc = discord.Embed(title=f"✅ CUENTA #{len(successful)}", color=0x8A2BE2)
                embed_acc.add_field(name="🆔 UID", value=f"`{r['uid']}`", inline=True)
                embed_acc.add_field(name="🔑 PASS", value=f"`{r['password']}`", inline=True)
                embed_acc.add_field(name="🌍 REGIÓN", value=f"`{region}`", inline=True)
                await interaction.channel.send(embed=embed_acc)
                await asyncio.sleep(1)
        except: continue

    if successful:
        db = load_db()
        db["stats"]["total_created"] = db["stats"].get("total_created", 0) + len(successful)
        if not paid and user_id != OWNER_ID:
            if str(user_id) not in db["clients"]: db["clients"][str(user_id)] = {}
            db["clients"][str(user_id)]["used_free"] = True
        save_db(db)
        
        embed_final = discord.Embed(title="🏁 PROCESO COMPLETADO", description=f"Se entregaron **{len(successful)}** cuentas con éxito.", color=0x00FF7F)
        await interaction.channel.send(content=f"<@{user_id}>", embed=embed_final)
    else:
        await interaction.followup.send("❌ Error Crítico: No se pudo generar la cuenta.")

@bot.tree.command(name="info", description="Ver tu perfil ZENIHT")
async def info(interaction: discord.Interaction):
    await interaction.response.defer()
    paid, time_left = is_paid(interaction.user.id)
    embed = discord.Embed(title="👤 PERFIL ZENIHT FF", color=0x3498DB)
    embed.add_field(name="💼 Estado", value="`PREMIUM`" if paid else "`GRATUITO`", inline=True)
    embed.add_field(name="⏳ Validez", value=f"`{time_left} días`" if isinstance(time_left, int) else f"`{time_left}`", inline=True)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"ID: {interaction.user.id}")
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="add_client", description="Añadir cliente premium (Socio/Dueño)")
async def add_client(interaction: discord.Interaction, user_id: str, tiempo: str):
    await interaction.response.defer()
    if not is_admin(interaction.user.id):
        await interaction.followup.send("❌ No autorizado.", ephemeral=True)
        return
    
    try:
        now = dt.datetime.now()
        days = int(tiempo[:-1])
        expiry = now + timedelta(days=days) if tiempo.endswith('d') else now + timedelta(days=days*30)
        db = load_db()
        db["clients"][str(user_id)] = {"expiry": expiry.isoformat(), "used_free": True}
        save_db(db)
        await interaction.followup.send(f"✅ <@{user_id}> activado hasta `{expiry.strftime('%d/%m/%Y')}`")
    except:
        await interaction.followup.send("❌ Formato incorrecto. Usa `7d` o `1m`.")

@bot.tree.command(name="stats", description="Estadísticas Globales")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer()
    db = load_db()
    embed = discord.Embed(title="📊 ESTADÍSTICAS GLOBALES", color=0xF1C40F)
    embed.add_field(name="🔥 Cuentas Creadas", value=f"`{db['stats'].get('total_created', 0)}`", inline=True)
    embed.add_field(name="👑 Clientes Premium", value=f"`{len(db['clients'])}`", inline=True)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="announce", description="📢 Enviar anuncio oficial (Solo Dueño)")
async def announce(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.user.id != OWNER_ID:
        await interaction.followup.send("❌ Solo accesible por el Dueño.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📢 AVISO OFICIAL ZENIHT",
        description=(
            "@everyone @here\n\n"
            "**EL BOT GENERADOR DE CUENTAS ESTÁ DISPONIBLE**\n"
            "Genera cuentas de Free Fire en segundos.\n\n"
            "💎 **Premium:** Acceso ilimitado y soporte prioritario.\n\n"
            "Dueño: **ZENIHT**"
        ),
        color=0xFF4500
    )
    await interaction.channel.send(content="@everyone @here", embed=embed)
    await interaction.followup.send("✅ Anuncio enviado.")

if __name__ == "__main__":
    if not TOKEN:
        print(f"{red}!! ERROR: DISCORD_TOKEN no configurado en entorno.")
        sys.exit(1)
    bot.run(TOKEN)
