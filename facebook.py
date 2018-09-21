print("Pengaturan Bahasa pada akun harus bahasa inggris !")

import time, getpass, json, sys, os.path, math
from selenium import webdriver

try:
	output_file = sys.argv[1]
	total_post = sys.argv[2]
except:
	print("masukin output bego")
	exit()

if os.path.isfile(output_file):
	exit("Output File Exists !")

def screenshot_el(el, epoch):
	fname = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch)))
	image = el.screenshot_as_png
	with open("./screenshot/{}.png".format(fname), 'wb') as out:
	    out.write(image)

profile = webdriver.FirefoxProfile()
profile.set_preference('dom.webnotifications.enabled', False)

driver = webdriver.Firefox(profile)

driver.get('https://m.facebook.com/')

input_username = driver.find_elements_by_css_selector('input#m_login_email')
input_password = driver.find_elements_by_css_selector('input[type="password"]')
submit_btn = driver.find_elements_by_css_selector('input[name="login"]')

if len(input_username) > 0 and len(input_password) > 0 and len(submit_btn) > 0:
	print("Login")
	user_username = input("Username : ")
	user_password = getpass.getpass("Password : ")
	input_username[0].send_keys(user_username)
	input_password[0].send_keys(user_password)
	submit_btn[0].click()

page_url = input("Page Url (m.facebook) : ")

if "m.facebook" not in page_url:
	exit("Error")

saved_post = []
posts_arr = []

driver.get(page_url)

for i in range(0, int(math.ceil(int(total_post)/5))):
	show_more = driver.find_element_by_xpath("//*[contains(text(), 'Show more')]")
	time.sleep(2)
	posts = driver.find_elements_by_css_selector('div[role="article"]')
	for post in posts:
		posts_arr.append(json.loads(str(post.get_attribute('data-ft'))))
	show_more.click()

with open(output_file, 'a') as the_file:
	for post in posts_arr:
		get_url = 'https://www.facebook.com/story.php?story_fbid={}&id={}'.format(post["throwback_story_fbid"], post["page_id"])
		if get_url not in saved_post:
			driver.get(get_url)
			time.sleep(5)
			is_there_any_popup = driver.find_elements_by_css_selector('div#photos_snowlift a[href="#"][role="button"]')
			if len(is_there_any_popup) > 0:
				is_there_any_popup[0].click()
			time.sleep(2)
			screenshot_el(driver.find_element_by_css_selector('div[class*="userContent"]'), post["page_insights"][post["content_owner_id_new"]]["post_context"]["publish_time"])
			the_file.write(get_url+"\n")
			saved_post.append(get_url)

driver.quit()