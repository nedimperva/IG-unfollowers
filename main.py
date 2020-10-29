from selenium import webdriver
from time import sleep
import random

# enter your username and pasword here
# two factor authentication must be disabled
username = ""
pw = ""


class InstaBot:
    def __init__(self, username, pw):
        #log in
        self.username = username
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com/?hl=hr")
        sleep(2)
        self.driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[1]/div/label/input").send_keys(username)
        self.driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[2]/div/label/input").send_keys(pw)
        self.driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[3]/button/div").click()
        sleep(4)
        self.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div/div/div/button").click()
        sleep(4)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        sleep(4)

    def get_followers(self):
        #go to the profile page and click on followers
        self.driver.get(f"https://www.instagram.com/{username}/")
        self.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/ul/li[2]/a/span").click()
        sleep(5)
        #followers page scroll
        js_command = """
        followers = document.querySelector('.isgrP');
        followers.scrollTo(0, followers.scrollHeight);
        var lenOfPage = followers.scrollHeight;
        return lenOfPage;
        """
        lenOfPage = self.driver.execute_script(js_command)
        match     = False
        while(match == False):
            lastCount = lenOfPage
            sleep(3)
            lenOfPage = self.driver.execute_script(js_command)
            if lastCount == lenOfPage:
                match = True
        sleep(5)
        # get followers
        followersList = []
        followers = self.driver.find_elements_by_css_selector('.FPmhX.notranslate')
        for follower in followers:
            followersList.append(follower.text)
        return followersList
    
    def get_following(self):
        # go to the profile page agan and get following list
        self.driver.get(f"https://www.instagram.com/{username}/")
        self.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/ul/li[3]/a").click()
        sleep(3)
        #followers page scroll
        js_command = """
        followers = document.querySelector('.isgrP');
        followers.scrollTo(0, followers.scrollHeight);
        var lenOfPage = followers.scrollHeight;
        return lenOfPage;
        """
        lenOfPage = self.driver.execute_script(js_command)
        match     = False
        while(match == False):
            lastCount = lenOfPage
            sleep(3)
            lenOfPage = self.driver.execute_script(js_command)
            if lastCount == lenOfPage:
                match = True
        sleep(3)
        # get followers
        followingList = []
        following = self.driver.find_elements_by_css_selector('.FPmhX.notranslate')
        for follower in following:
            followingList.append(follower.text)
        return followingList
                    
    
my_bot = InstaBot(username, pw)
followers = my_bot.get_followers()
following = my_bot.get_following()
not_following_back = [user for user in following if user not in followers]
print("Number of people not following you back: " + str(len(not_following_back)))
print(*not_following_back, sep="\n")
