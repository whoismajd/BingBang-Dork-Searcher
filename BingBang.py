from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import concurrent.futures

class DorkSearcher:
    def __init__(self, dorks_path, num_threads):
        self.dorks_path = dorks_path
        self.num_threads = num_threads
        self.dorks = self.read_dorks()
    
    def read_dorks(self):
        with open(self.dorks_path, 'r', encoding='utf-8') as file:
            dorks = file.readlines()
        return [dork.strip() for dork in dorks]
    
    def search_dork(self, dork):
        driver = webdriver.Chrome()
        driver.get('https://www.bing.com')
        
        search_box = driver.find_element(By.XPATH, "//input[@type='search']")
        search_box.send_keys(dork + Keys.RETURN)
        time.sleep(5)  # Wait for the page to load
        
        while True:
            script = """
            var linkElements = document.querySelectorAll('a.tilk');
            var urls = [];
            linkElements.forEach(function(linkElement) {
                var url = linkElement.getAttribute('href');
                urls.push(url);
            });
            return urls;
            """
            urls = driver.execute_script(script)
            
            with open('Grabbed_URLS.txt', 'a') as file:
                for url in urls:
                    file.write(url + '\n')
                    print(url)
            
            script = """
            var buttonElement = document.querySelector('a.sb_pagN');
            if (buttonElement) {
                return "The Next button exists.";
            } else {
                return "The Next button does not exist.";
            }
            """
            result = driver.execute_script(script)
            
            if result == "The Next button exists.":
                driver.execute_script("document.querySelector('a.sb_pagN').click()")
            else:
                break
        
        driver.quit()

    def start_search(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            executor.map(self.search_dork, self.dorks)
    
if __name__ == '__main__':
    banner = """   
    ██████╗░██╗███╗░░██╗░██████╗░██████╗░░█████╗░███╗░░██╗░██████╗░
    ██╔══██╗██║████╗░██║██╔════╝░██╔══██╗██╔══██╗████╗░██║██╔════╝░
    ██████╦╝██║██╔██╗██║██║░░██╗░██████╦╝███████║██╔██╗██║██║░░██╗░
    ██╔══██╗██║██║╚████║██║░░╚██╗██╔══██╗██╔══██║██║╚████║██║░░╚██╗
    ██████╦╝██║██║░╚███║╚██████╔╝██████╦╝██║░░██║██║░╚███║╚██████╔╝
    ╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░
    Creator: Majdeddine Ben Hadj Brahim
    Github : github.com/whoismajd
    """
    print(banner)
    
    dorks_path = input("Dorks File: ")
    num_threads = int(input("Threads: "))

    dork_searcher = DorkSearcher(dorks_path, num_threads)
    dork_searcher.start_search()
