
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
import time, sys, datetime

try:
	output_file = sys.argv[1]
except:
	print("masukin output bego")
	exit()

def screenshot_el(el, tanggal):
	image = el.screenshot_as_png
	with open("./screenshot/{}.png".format(tanggal), 'wb') as out:
	    out.write(image)

profile = webdriver.FirefoxProfile()
profile.set_preference('dom.webnotifications.enabled', False)

binary = FirefoxBinary('/usr/bin/firefox')
binary.add_command_line_options('--headless')

driver = webdriver.Firefox(profile, firefox_binary=binary)

with open("./instagram_target.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

for instagram_username in content:
	driver.get('https://www.instagram.com/' + instagram_username)

	photos = driver.find_elements_by_css_selector('a[href*="/p/"]')
	photos_arr = []
	for photo in photos:
		photos_arr.append(photo.get_attribute('href'))

	with open(output_file, 'a') as the_file:
		for photo_url in photos_arr:
			driver.get(photo_url)
			time.sleep(2)
			publish_time = driver.find_element_by_css_selector('time[datetime]')
			publish_time = publish_time.get_attribute('datetime')
			now = datetime.datetime.now()
			now = str(now.strftime("%Y-%m-%d")) # 2018-09-21
			if now in publish_time:
				screenshot_el(driver.find_element_by_css_selector('article'), publish_time)
				the_file.write(photo_url+"\n")

driver.quit()