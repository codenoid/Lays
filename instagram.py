import time, sys
from selenium import webdriver

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

driver = webdriver.Firefox(profile)

instagram_username = input("Instagram Username : ")

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
		screenshot_el(driver.find_element_by_css_selector('article'), publish_time)
		the_file.write(photo_url+"\n")

driver.quit()