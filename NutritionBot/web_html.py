from selenium import webdriver

def search_on_google(html):
    driver = webdriver.Chrome(r'F:\AI\Line_Chatbot\NutritionBot\NutritionBot\chromedriver.exe')
    driver.get(html)

    # print(type(addr), type(name))
    #
    # driver = webdriver.Chrome(r'F:\AI\Line_Chatbot\NutritionBot\NutritionBot\chromedriver.exe')
    # driver.get("http://www.google.com")
    # element = driver.find_element_by_name("q")
    #
    # if 'NULL' not in name:
    #     element.send_keys(name)
    #     element.submit()
    # elif 'NULL' not in addr:
    #     element.send_keys(addr)
    #     element.submit()

    return driver.current_url
