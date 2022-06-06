import os
import ctypes
import requests
import time
import random
import json
import threading
from colorama import Fore, init

init(autoreset=True)
if os.name == "nt":
	os.system("mode con: cols=138 lines=30")

locker = threading.Lock()
proxies_list = []

def title(text):
	if os.name == "nt":
		ctypes.windll.kernel32.SetConsoleTitleW(f"Bloody Spammer V2 | By Bloody | {text}")
	else:
		print(f"\33]0;Bloody Spammer V2 | By Bloody | {text}\a", end="", flush=True)

def logo():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

	print(f"""{Fore.LIGHTBLUE_EX}
                                 ██████╗ ██╗      ██████╗  ██████╗ ██████╗ ██╗   ██╗               
                                 ██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗╚██╗ ██╔╝               
                                 ██████╔╝██║     ██║   ██║██║   ██║██║  ██║ ╚████╔╝                
                                 ██╔══██╗██║     ██║   ██║██║   ██║██║  ██║  ╚██╔╝                 
                                 ██████╔╝███████╗╚██████╔╝╚██████╔╝██████╔╝   ██║                  
                                 ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝    ╚═╝                  
                                                                  
                                 ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗     
                                 ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗    
                                 ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝    
                                 ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗    
                                 ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║    
                                 ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝    
                                                                  
                                 ██╗   ██╗██████╗                                                  
                                 ██║   ██║╚════██╗                                                 
                                 ██║   ██║ █████╔╝                                                 
                                 ╚██╗ ██╔╝██╔═══╝                                                  
                                  ╚████╔╝ ███████╗                                                 
                                   ╚═══╝  ╚══════╝                                                 
                                                                                                         
                                 {Fore.LIGHTYELLOW_EX}Fucking webhooks has never been {Fore.LIGHTGREEN_EX}easier{Fore.LIGHTYELLOW_EX}.

{Fore.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n
	""")

def proxies_scraper():
	global proxies_list

	while True:
		response = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&simplified=true")
		proxies_list = response.text.splitlines()
		
		time.sleep(3)

def proxies_random():
	proxy = random.choice(proxies_list)

	proxies = {
		"http": f"socks4://{proxy}",
		"https": f"socks4://{proxy}"
	}
	
	return proxies

def spammer(use_proxies, url, username, avatar_url, message):
	while True:
		try:
			if use_proxies == "y":
				proxy = proxies_random()
			else:
				proxy = {
					"http": None,
					"https": None
				}
			
			response = requests.post(url, json={"username": username, "avatar_url": avatar_url, "content": message}, proxies=proxy)
			if response.status_code != 204:
				if response.status_code == 404:
					locker.acquire()
					print(f"{Fore.LIGHTRED_EX}[Invalid Webhook] {url.split('webhooks/')[1]}")
					locker.release()
					break
				elif response.status_code == 429:
					time.sleep(float(json.loads(response.content)['retry_after'] / 1000))
				else:
					locker.acquire()
					print(f"{Fore.LIGHTRED_EX}[Unknown Error - {response.status_code}] {url.split('webhooks/')[1]}")
					locker.release()
			else:
				locker.acquire()
				print(f"{Fore.LIGHTGREEN_EX}[Success] {url.split('webhooks/')[1]}")
				locker.release()
		except:
			pass

def deleter(use_proxies, url):
	global success, errors

	request_sent = False
	while not request_sent:
		try:
			if use_proxies == "y":
				proxy = proxies_random()
			else:
				proxy = {
					"http": None,
					"https": None
				}

			response = requests.delete(url, proxies=proxy, timeout=5)
			request_sent = True
			if response.status_code != 204:
				errors += 1
				if response.status_code == 404:
					locker.acquire()
					print(f"{Fore.LIGHTRED_EX}[Invalid Webhook] {url.split('webhooks/')[1]}")
					locker.release()
			else:
				success += 1
				locker.acquire()
				print(f"{Fore.LIGHTGREEN_EX}[Success] {url.split('webhooks/')[1]}")
				locker.release()

			if success + errors == total_url:
				title("Deleting - Finished")

				logo()
				print(f"{Fore.LIGHTGREEN_EX}{success} webhooks have been deleted with success.")
				print(f"{Fore.LIGHTRED_EX}{errors} webhooks encountered errors while deleting them.")

				time.sleep(5)
				init()
		except:
			pass

def init():
	global total_url, success, errors

	title("Initialization")

	logo()
	print(f"{Fore.LIGHTMAGENTA_EX}Do you want to spam webhook? (y/n if you want to delete)")
	spam_webhooks = input("\n~# ").lower()

	logo()
	print(f"{Fore.LIGHTMAGENTA_EX}Do you want to destroy multiple webhooks? (y/n)")
	multiple_webhooks = input("\n~# ").lower()
	if multiple_webhooks == "n":
		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}Enter Webhook URL you want to destroy.")
		url = input("\n~# ")
	else:
		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}Enter file name that contains webhooks. (with .txt)")
		webhooks_file = input("\n~# ")

	if spam_webhooks == "y":
		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}Enter webhook's username.")
		username = input("\n~# ")

		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}Enter webhook's avatar URL. (Empty for no avatar)")
		avatar_url = input("\n~# ")

		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}Enter message you want to spam.")
		message = input("\n~# ")

		logo()
		print(f"{Fore.LIGHTMAGENTA_EX}How many threads?")
		try:
			threads_count = int(input("\n~# "))
		except:
			logo()
			print(f"{Fore.LIGHTRED_EX}[Error] Invalid threads count.")
			time.sleep(5)
			init()

	logo()
	print(f"{Fore.LIGHTMAGENTA_EX}Do you want to use proxies? (Recommanded, y/n)")
	use_proxies = input("\n~# ").lower()

	if spam_webhooks == "y":
		title("Spamming")

		logo()
		if use_proxies == "y":
			threading.Thread(target=proxies_scraper).start()
			while len(proxies_list) == 0: 
				time.sleep(0.5)

		if multiple_webhooks == "n":
			for i in range(0, threads_count):
				threading.Thread(target=spammer, args=(use_proxies, url, username, avatar_url, message)).start()
		else:
			with open(webhooks_file) as file:
				for line in file:
					for i in range(0, threads_count):
						threading.Thread(target=spammer, args=(use_proxies, line.rstrip(), username, avatar_url, message)).start()

				file.close()
	else:
		title("Deleting")

		logo()

		if use_proxies == "y":
			threading.Thread(target=proxies_scraper).start()
			while len(proxies_list) == 0: 
				time.sleep(0.5)

		success = 0
		errors = 0
		if multiple_webhooks == "n":
			total_url = 1
			threading.Thread(target=deleter, args=(use_proxies, url,)).start()
		else:
			total_url = len(open(webhooks_file).readlines())
			with open(webhooks_file) as file:
				for line in file:
					threading.Thread(target=deleter, args=(use_proxies, line.rstrip(),)).start()

				file.close()

if __name__ == "__main__":
	try:
		init()
	except KeyboardInterrupt:
		exit()
