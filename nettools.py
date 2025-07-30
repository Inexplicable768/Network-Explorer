# imports 
import requests, time, os, re, socket
import tkinter as tk

import yt_dlp
import sqlite3
import shutil
from bs4 import BeautifulSoup

# config and constants
WIDTH = 800
HEIGHT = 600
FRAME_LIMIT = 60
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',  # Save file as the video title
    'cookiefile': 'cookies.txt'
}
headers = {'User-Agent': 'Mozilla/5.0'}

# === internet utilities ===
def find_html(website: str, log: bool = False):
    try:
        if "https://" not in website:
            website = "https://" + website
        print(f"Fetching {website} html information...")
        response = requests.get(website)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            html_content = response.text
            print(html_content)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return 1
        soup = BeautifulSoup(response.text, 'html.parser')
        if not log:
            print(soup.prettify())
        t = time.strftime("%m-%d-%Y")
        with open(f"logs/{t}.txt", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
            f.close()
        print("File written to logs directory")
    except Exception as e:
        return e
    return html_content
def download_video(url: str, cookiefile: str, autogetcookies:False):
    if not cookiefile:
        del ydl_opts['cookiefile']
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception() as e:
        return e

def export_edge_cookies_to_txt(output_file, domain_filter=None):
    # Path to Edge cookies DB
    cookie_db = os.path.expanduser(
        r"~\AppData\Local\Microsoft\Edge\User Data\Default\Cookies"
    )

    temp_db = "temp_cookies.db"
    shutil.copy2(cookie_db, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("SELECT host_key, name, value, path, expires_utc, is_secure FROM cookies")
    cookies = cursor.fetchall()

    with open(output_file, "w") as f:
        for host, name, value, path, expires, is_secure in cookies:
            if domain_filter and domain_filter not in host:
                continue
            line = f"{host}\tTRUE\t{path}\t{'TRUE' if is_secure else 'FALSE'}\t{expires}\t{name}\t{value}\n"
            f.write(line)

    conn.close()
    os.remove(temp_db)
    print(f"Cookies saved to {output_file}")



def download_multiple(urls: list):
    for url in urls:
        download_video(url)

def spotify_download(url: str):
    pass

def get_whois_server(domain: str): # first identify a valid whois server on a socket at port 43 via TPS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("whois.iana.org", 43)) # connect to server
            s.send((domain.split('.')[-1] + "\r\n").encode()) # send a request
            response = b"" # response from server
        except Exception() as e:
            print(e)
            raise Exception("Err: Failed to fetch response from the server")
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
    for line in response.decode(encoding="utf-8",errors="strict").splitlines(): # decode bytes
        if line.lower().startswith("whois:"): 
            return line.split(":")[1].strip() #return information
    return None

def ip_lookup():
    pass

def whois(url: str, noterms=True):
    if bool(re.search(r'\d', url)):
       url = get_url(url)
    server = get_whois_server(url)
    if not server:
        raise ValueError("WHOIS server not found for domain.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # make a socket endpoint with ipv4 adress family (AF_INET)
        sock.connect((server, 43)) # connect to server at port 43
        sock.send((url + "\r\n").encode()) # send request
        response = b"" # binary response
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
    try:
        return response.decode(encoding="utf-8",errors='ignore').split(">>> Last update of whois database")[0]
    except Exception as e:
        print(e)
        return response.decode(encoding="utf-8",errors='ignore')

def get_ip_adress(url: str):
    pass
def get_url(ip: str):
    pass
# === network utilities ===




# === entry point & app ===
def funlist(): # word salad readability im sorry
    return [name for name, obj in globals().items() if callable(obj) and obj.__module__ == __name__ and obj is not funlist]

