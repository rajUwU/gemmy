import time

def scroll(driver, timeout):
    scroll_pause_time = timeout

    last_height = driver.execute_script("return document.body.scrollHeight")
    

    while True:
       
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-900);")
        time.sleep(scroll_pause_time)
        driver.execute_script("window.scrollTo(0, 0);")
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height