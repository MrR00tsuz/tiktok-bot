import os
import sys
import subprocess
import tkinter as tk
import json
import pygame
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from loguru import logger
from threading import Thread


process = None

def save_url():
    url = url_entry.get()
    if url:
        url_path = os.path.join("config", "data", "url.json")
        with open(url_path, 'w') as json_file:
            json.dump({"url": url}, json_file)
        print(f"URL kaydedildi: {url}")

def run_log_cpython():
    try:
        log_path = os.path.join("config", "data", "log.cpython-312.py")
        if os.path.isfile(log_path):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(['python', log_path], startupinfo=startupinfo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"{log_path} dosyası bulunamadı.")
            sys.exit()
    except Exception as e:
        print(f"Hata oluştu: {e}")
        sys.exit()

def start_script():
    global process
    save_url()
    
    # Seçilen dosyaları çalıştır
    selected_scripts = []
    if zefoy_var.get():
        selected_scripts.append(os.path.join("config", "data", "views", 'zefoy.py'))
    if favorites_var.get():
        selected_scripts.append(os.path.join("config", "data", "favorites", 'favorites.py'))
    if comments_var.get():
        selected_scripts.append(os.path.join("config", "data", "comments", 'comments.py'))

    # subprocess ayarları
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    # Seçilen her dosyayı çalıştır
    for script_path in selected_scripts:
        process = subprocess.Popen(
            ['python', script_path],
            startupinfo=startupinfo, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )

def stop_script():
    global process
    if process:
        process.terminate()
        process = None
        print("Script durduruldu")

def anti_captcha():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    
    service = Service(os.path.join("config", "data", "chromedriver.exe"))
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://zefoy.com")
        for i in range(10):   
            time.sleep(7)  
            
            
            cookies = driver.get_cookies()
            formatted_cookies = []
            for cookie in cookies:
                formatted_cookie = {
                    "domain": cookie["domain"],
                    "hostOnly": cookie.get("hostOnly", False),
                    "httpOnly": cookie.get("httpOnly", False),
                    "name": cookie["name"],
                    "path": cookie["path"],
                    "sameSite": cookie.get("sameSite", None),
                    "secure": cookie.get("secure", False),
                    "session": cookie.get("expiry") is None,  
                    "storeId": cookie.get("storeId", None),
                    "value": cookie["value"]
                }
                
                if "expiry" in cookie:
                    formatted_cookie["expirationDate"] = cookie["expiry"]
                
                formatted_cookies.append(formatted_cookie)

            
            with open(os.path.join("config", "data", "cookies", f"cookies{i}.json"), 'w') as f:
                json.dump(formatted_cookies, f, indent=4)
            print(f"Cookies kaydedildi: cookies{i}.json")
            driver.delete_all_cookies()   
            driver.refresh()  
            time.sleep(5)  
    finally:
        driver.quit()   

def start_anti_captcha():
    thread = Thread(target=anti_captcha)
    thread.start()

def run_main_process():
    try:
        run_log_cpython()
        print("Ana işlem çalışıyor...")
    except KeyboardInterrupt:
        logger.warning('Ctrl + C basıldı')
        if process:
            process.kill()
        sys.exit()
    except Exception as e:
        logger.error(e)
        sys.exit()

def play_song():
    pygame.mixer.init()
    song_path = os.path.join("config", "data", "song.mp3")
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def toggle_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

current_language = "TR"

def update_language():
    global current_language
    if current_language == "TR":
        current_language = "ENG"
        url_entry.delete(0, tk.END)
        url_entry.insert(0, "Enter URL")
        start_button.config(text="Start")
        stop_button.config(text="Stop")
        sound_button.config(text="Toggle Sound")
        footer_label.config(text="2024|Code by MrR00tsuz")
        language_button.config(text="TR")
        anti_captcha_button.config(text="Anti-Captcha")
    else:
        current_language = "TR"
        url_entry.delete(0, tk.END)
        url_entry.insert(0, "URL Girin")
        start_button.config(text="Başlat")
        stop_button.config(text="Durdur")
        sound_button.config(text="Sesi Aç/Kapat")
        footer_label.config(text="MrR00tsuz Tarafından Kodlanmıştır")
        language_button.config(text="ENG")
        anti_captcha_button.config(text="Anti-Captcha")

def clear_url_placeholder(event):
    if url_entry.get() == ("Enter URL" if current_language == "ENG" else "URL Girin"):
        url_entry.delete(0, tk.END)
        url_entry.config(fg="#ffffff")
    url_entry.bind("<FocusOut>", restore_url_placeholder)

def restore_url_placeholder(event):
    if url_entry.get() == "":
        url_entry.insert(0, "Enter URL" if current_language == "ENG" else "URL Girin")
        url_entry.config(fg="#777")

def run_gui():
    root = tk.Tk()
    root.iconbitmap("config/data/logo.ico")
    root.title("Zefoy.me Otomasyonu")
    root.geometry("600x500")
    root.maxsize(600, 500)
    root.configure(bg="#282c35")

    ascii_art = """\
  __  __      _____   ___   ___  _                 
 |  \/  |    |  __ \ / _ \ / _ \| |                
 | \  / |_ __| |__) | | | | | | | |_ ___ _   _ ____ 
 | |\/| | '__|  _  /| | | | | | | __/ __| | | |_  /
 | |  | | |  | | \ \| |_| | |_| | |_\__ \ |_| |/ / 
 |_|  |_|_|  |_|  \_\\___/ \___/ \__|___/\__,_/___| 
"""

    ascii_label = tk.Label(root, text=ascii_art, font=("Courier New", 10), justify="center", anchor="center", bg="#282c35", fg="#ffffff")
    ascii_label.pack(padx=10, pady=10)

    url_frame = tk.Frame(root, bg="#282c35", bd=1, relief="solid", highlightbackground="#6f2558", highlightcolor="#6f2558", highlightthickness=1)
    url_frame.pack(pady=10, padx=10)

    global url_entry
    url_entry = tk.Entry(url_frame, width=30, font=("Helvetica", 12), fg="#777", bg="#282c35", bd=0)
    url_entry.insert(0, "URL Girin")
    url_entry.bind("<FocusIn>", clear_url_placeholder)
    url_entry.pack(padx=10, pady=10)

    
    global zefoy_var, favorites_var, comments_var
    zefoy_var = tk.BooleanVar()
    favorites_var = tk.BooleanVar()
    comments_var = tk.BooleanVar()

    
    zefoy_check = tk.Checkbutton(root, text="İzlenme", variable=zefoy_var, bg="#282c35", fg="#ffffff", selectcolor="#6f2558", font=("Helvetica", 10))
    zefoy_check.pack(pady=5)

    favorites_check = tk.Checkbutton(root, text="Favori", variable=favorites_var, bg="#282c35", fg="#ffffff", selectcolor="#6f2558", font=("Helvetica", 10))
    favorites_check.pack(pady=5)

    comments_check = tk.Checkbutton(root, text="Yorum Beğeni", variable=comments_var, bg="#282c35", fg="#ffffff", selectcolor="#6f2558", font=("Helvetica", 10))
    comments_check.pack(pady=5)

    button_style = {
        "font": ("Helvetica", 10),
        "fg": "#ffffff",
        "bg": "#6f2558",
        "relief": "flat",
        "width": 20,
        "bd": 0,
    }

    global start_button, stop_button, sound_button, anti_captcha_button
    start_button = tk.Button(root, text="Başlat", command=start_script, **button_style)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Durdur", command=stop_script, **button_style)
    stop_button.pack(pady=10)

    sound_button = tk.Button(root, text="Sesi Aç/Kapat", command=toggle_music, **button_style)
    sound_button.pack(pady=10)

    anti_captcha_button = tk.Button(root, text="Anti-Captcha", command=start_anti_captcha, **button_style)
    anti_captcha_button.pack(pady=10)

    global footer_label
    footer_label = tk.Label(root, text="2024|Code by MrR00tsuz", font=("Helvetica", 10), fg="#777", bg="#282c35")
    footer_label.pack(side="bottom", pady=10)

    global language_button
    language_button = tk.Button(root, text="ENG", command=update_language, font=("Helvetica", 10), bg="#6f2558", fg="#ffffff", relief="flat", bd=0)
    language_button.place(x=550, y=470)

    play_song()
    root.mainloop()

def run():
    run_main_process()
    run_gui()

if __name__ == '__main__':
    run()
