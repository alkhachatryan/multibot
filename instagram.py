from selenium import webdriver
import time
import random
from dotenv import load_dotenv
import os
from selenium.webdriver.firefox.options import Options


load_dotenv()

def is_clicked(button):
    return button.value_of_css_property("background-color") != 'rgb(0, 149, 246)'

def click_on_follow_button(button):
    button.click()
    time.sleep(random.randint(4, 11))

    if(is_clicked(button)):
        return
    else:
        rand_val = random.randint(40, 120)
        print('Couldn\'t click on the button, click again in ' + str(rand_val) + ' seconds')
        time.sleep(rand_val)
        click_on_follow_button(button)

def start():
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=options)

    driver.get("https://www.instagram.com/accounts/login")

    time.sleep(3)
    username = driver.find_element_by_css_selector("input[type=text]")
    password = driver.find_element_by_css_selector("input[type=password]")

    # password and username need to go into these values
    print('Filling Login')
    username.send_keys(os.getenv('LOGIN'))
    time.sleep(1)
    print('Filling Password')
    password.send_keys(os.getenv('PASSWORD'))
    time.sleep(1)

    print('Processing form submitting')
    login_form = driver.find_element_by_xpath("//button[@type='submit']")
    time.sleep(1)
    login_form.click()
    time.sleep(5)

    driver.get("https://www.instagram.com/"+ os.getenv('ACCOUNT_FOLLOWERS') +"/followers")
    print('Open user followers')
    driver.find_element_by_css_selector(
        "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a").click()

    success_count = 0
    fail_count = 0
    total_count = 0

    while True:

        time.sleep(4)

        print('Get the followers Follow buttons')
        followers_add_btn = driver.find_elements_by_xpath('//button[text()="Follow"][@type="button"]')

        if len(followers_add_btn) > 0:

            print('Processing to click on all Follow buttons')

            i = 0
            for i in range(len(followers_add_btn) - 1):
                try:
                    click_on_follow_button(followers_add_btn[i])
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    print(str(e))
                    del followers_add_btn[i]
                    driver.execute_script(
                        "document.querySelector('body > div.RnEpo.Yx5HN > div > div.isgrP').scrollTop += 1000;")

                total_count += 1

                print('Success: ' + str(success_count) + ' Fail: ' + str(fail_count))

                if total_count % 9 == 0 and total_count > 0:
                    random_deactivate_value = random.randint(120, 240)
                    print('DEACTIVATE THE BOT FOR ' + str(random_deactivate_value) + ' SECONDS')
                    time.sleep(random_deactivate_value)

            time.sleep(3)

        else:
            print('There is no Follow button, scroll down')
            driver.execute_script(
                "document.querySelector('body > div.RnEpo.Yx5HN > div > div.isgrP').scrollTop += 1000;")




start()




