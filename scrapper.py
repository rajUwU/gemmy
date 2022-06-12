from statistics import mode
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from infinite_scroll import scroll
from mapper import format, xls1_2, xls3_12, xls13_14
import os
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
dirname = os.getcwd()
def selenium_initiation():
    
    PREFPATH = os.path.join(dirname, "files/")
    prefs = {"download.default_directory" : PREFPATH, "directory_upgrade": True, "download.prompt_for_download": False}
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install())

    url = f"https://gem.gov.in/view_contracts"
    driver.get(url)

    element=driver.find_element(By.ID,"select2-buyer_category-container")
    element.click()

    return driver

def main(driver, keyword, speed):

    logging.info(f'Item being Searched : {keyword}')


    items = driver.find_elements_by_xpath(f"//*[text()='{keyword}']")
    items[0].click()

    element=driver.find_element(By.ID, "searchlocation1")
    element.click()

    logging.info('Started Scrolling')
    logging.info(f'Scrolling Speed : {speed} seconds')

    scroll(driver, speed)

    logging.info('Scrolling Finished')

    element=driver.find_elements(By.ID, "pagi_content")

    def bidnum_allocator(content, contract_list):
        result={}
        bidnum = content[0].find_elements_by_xpath("//*[text()='Bid Number: ']")
        for bid in bidnum:
            bid = bid.find_element_by_xpath("..")
            parent_entry = bid.find_element_by_xpath("..")
            parent_entry = parent_entry.find_element_by_xpath("..")
            parent_entry = parent_entry.find_element_by_xpath("..")
            if parent_entry.text[:33] in contract_list:
                result[f'{parent_entry.text[:33]}'] = bid.text
        return result

    def detail_extractor(content, keyword):
        result = []
        entries = content[0].find_elements_by_xpath(f"//*[text()='{keyword}']")
        for entry in entries:
            parent_entry = entry.find_element_by_xpath("..")
            result.append(parent_entry.text)
        return result

    logging.info("Started Detail Extraction..")
    contract_list = detail_extractor(element,'Contract NO: ')
    logging.info(f"Contract Number Finished - {len(contract_list)}")
    status_list = detail_extractor(element,'Status of the Contract: ')
    logging.info(f"Status of the Contract Finished - {len(status_list)}")
    orgtype_list = detail_extractor(element,'Organization Type: ')
    logging.info(f"Organization Type Finished - {len(orgtype_list)}")
    ministry_list = detail_extractor(element,'Ministry: ')
    logging.info(f"Ministry Finished - {len(ministry_list)}")
    department_list = detail_extractor(element,'Department: ')
    logging.info(f"Department Finished - {len(department_list)}")
    organization_list = detail_extractor(element,'Organization Name: ')
    logging.info(f"Organization Name Finished - {len(organization_list)}")
    office_list = detail_extractor(element,'Office Zone: ')
    logging.info(f"Office Zone Finished - {len(office_list)}")
    designation_list = detail_extractor(element,'Buyer Designation: ')
    logging.info(f"Buyer Designation Finished - {len(designation_list)}")
    mode_list = detail_extractor(element,'Buying Mode: ')
    logging.info(f"Buying Mode Finished - {len(mode_list)}")
    contractdate_list = detail_extractor(element,'Contract Date: ')
    logging.info(f"Contract Date Finished - {len(contractdate_list)}")
    total_list = detail_extractor(element,'Total: ')
    logging.info(f"Total Value Finished - {len(total_list)}")
    bidnum_dict = bidnum_allocator(element, contract_list)
    logging.info(f"Bid Number Finished - {len(bidnum_dict)}")

    entries = driver.find_elements_by_class_name('ajxtag_item_title')
    product_list = []
    for i in range(0, len(entries), 3):
        product_list.append(entries[i].text)
    logging.info(f"Products Finished - {len(product_list)}" )
        
    entries = driver.find_elements_by_class_name('ajxtag_quantity')
    quantity_list=[]
    for entry in entries:
        quantity_list.append(entry.text)
        
    logging.info(f"Quantity Finished - {len(quantity_list)}")
        
    logging.info('Detail Extraction Done !')

    logging.info('Mapping the details...')
    
    format()

    xls1_2(contract_list,bidnum_dict)

    xls3_12(status_list, orgtype_list, ministry_list,
        department_list, organization_list, office_list, designation_list,
        mode_list, contractdate_list, total_list)


    xls13_14(product_list,quantity_list)
    # logging.info(bidnum_dict)
    output_path = dirname + '/Output.xls'
    item_path = dirname + f'/{keyword}.xls'
    os.rename(output_path, item_path)
    
    logging.info(f'File saved at {item_path}')
    
    logging.info('Closing driver...')
    
    driver.close()
    

def exec(item,speed):
    try:
        logging.info('Opening Driver ....')
        driver = selenium_initiation()
        main(driver, item, speed)
    except UnexpectedAlertPresentException:
        driver.close()
        exec(item, speed)


if __name__ == '__main__':
    items = ['All in One PC','Desktop Computers','Laptop-Notebook',
            'Multifunction Machines MFM', 'Server']
    
    for item in items:
        exec(item)
        

logging.info('EOL')


