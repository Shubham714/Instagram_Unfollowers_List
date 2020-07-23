from selenium import webdriver
from time import sleep
import secret as secret

class Instabot:
    # constructor of class
    def __init__(self, username, password):
        # start of webdriver
        self.driver = webdriver.Chrome()

        # open chrome browser and open tab with url https://www.instagram.com
        self.driver.get("https://www.instagram.com")

        # get username and password
        self.username = username
        self.password = password
        sleep(5)

        #enter username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)

        #enter password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)

        # click to submit
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(6)

        #click on not now button of save login info
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(5)

        #click on not now button of turn on notifications
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(5)

    #fuction to get unfollowers list
    def get_unfollower(self):
        # click on username
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(5)

        # click on following link
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self.get_names()

        # click on followers link
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self.get_names()

        # list comprehension to get unfollowers
        not_following_back = [user for user in following if user not in followers]
        return not_following_back

    def get_names(self):
        sleep(2)
        try:
            sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
            print(sugs)
        except:
            print("No suggestions found")

        # scrollbox ( copy xpath of just before the ul element)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        # here is the logic to scrolling it uses javascript for scrolling
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
            sleep(2)

        # find all a tags from the scroll_box
        links = scroll_box.find_elements_by_tag_name('a')

        # find all the names from the links
        names = [name.text for name in links if name.text != '']

        #click on close button
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()

        return names

My_bot = Instabot(secret.username, secret.password)
unfollowerList = My_bot.get_unfollower()
for user in unfollowerList:
    print(user)