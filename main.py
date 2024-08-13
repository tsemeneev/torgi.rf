import csv
import os
import requests
from drivers import main_driver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

def main():

    cats = {'Жилая недвижимость':'купить-жилую-недвижимость-с-торгов', 'Коммерческая недвижимость': 'купить-коммерческую-недвижимость-с-торгов', 
            'Гаражи и строения': 'купить-гаражи-строения-сооружения-с-торгов', 'Земельные участки': 'купить-земельные-участки-с-торгов',
            'СХ здания и сооружения': 'купить-сх-здания-и-сооружения-с-торгов'}
    domen = 'https://торги-россии.рф'
    driver = main_driver('')

    for cat_name, cat in cats.items():
        print(cats.items())
        create_file(f'{cat_name}.csv')
        driver.get(f'{domen}/{cat}')
        for page in range(1, 3):
            sleep(2)
            card_list = driver.find_elements(By.CLASS_NAME, 'card__desc')  
            links = [card.find_element(By.TAG_NAME, 'a').get_attribute('href') for card in card_list]
            driver_2 = main_driver('')
            for link in enumerate(links):
                driver_2.get(link[1])
                if link[0] == 0:
                    sleep(3)
                
                lot_id = link[1].split('/')[-1]
                name = driver_2.find_element(By.CLASS_NAME, 'page__title').text
                price = driver_2.find_element(By.CLASS_NAME, 'bid__value').text
                org_data = driver_2.find_elements(By.ID, 'trade-organizer')
                kadastr_number = driver_2.find_elements(By.CLASS_NAME, 'cadastral-item__title')
                if len(kadastr_number) > 0:
                    kadastr_number = kadastr_number[0].text
                else:
                    kadastr_number = 'Не указано'
                org_name = 'Не указано'
                org_email = 'Не указано'
                org_phone = 'Не указано'
                org_inn = 'Не указано'
                org_ogrn = 'Не указано'
                org_contact = 'Не указано'
                etp_url = 'Не указано'
                gis_url = 'Не указано'
                if len(org_data) > 0:
                    org_name = org_data[0].find_elements(By.XPATH, './/p/span[@class="text-grey" and contains(text(), "Наименование:")]//following-sibling::span[@class="js-share-search"]')
                    if len(org_name) > 0:
                        org_name = org_name[0].text
                    else:
                        org_name = 'Не указано'

                    org_email = org_data[0].find_elements(By.XPATH, './/p/span[@class="text-grey" and contains(text(), "E-mail:")]//following-sibling::span[@class="js-share-search"]')
                    if len(org_email) > 0:
                        org_email = org_email[0].text
                    else:
                        org_email = 'Не указано'
                    

                    org_phone = org_data[0].find_elements(By.XPATH, './/p/span[@class="text-grey" and contains(text(), "Телефон:")]//following-sibling::span[@class="js-share-search"]')
                    if len(org_phone) > 0:
                        org_phone = org_phone[0].text
                    else:
                        org_phone = 'Не указано'

                    org_inn = org_data[0].find_elements(By.XPATH, './/p/span[@class="text-grey" and contains(text(), "ИНН:")]//following-sibling::span[@class="js-share-search"]')
                    if len(org_inn) > 0:
                        org_inn = org_inn[0].text
                    else:
                        org_inn = 'Не указано'
                    

                    org_ogrn = org_data[0].find_elements(By.XPATH, './/p/span[@class="text-grey" and contains(text(), "ОГРН:")]//following-sibling::span[@class="js-share-search"]')
                    if len(org_ogrn) > 0:
                        org_ogrn = org_ogrn[0].text
                    else:
                        org_ogrn = 'Не указано'
                    

                    org_contact = org_data[0].find_elements(By.XPATH, './/p/span[@class="text-grey" and contains(text(), "ФИО")]//following-sibling::span[@class="js-share-search"]')
                    if len(org_contact) > 0:
                        org_contact = org_contact[0].text
                    else:
                        org_contact = 'Не указано'

                    lot_buttons = driver_2.find_elements(By.CLASS_NAME, 'lot-section__buttons')
                    
                    if len(lot_buttons) > 0:
                        lot_buttons = lot_buttons[0].find_elements(By.TAG_NAME, 'a')
                        if len(lot_buttons) > 0:
                            for button in lot_buttons:
                                if button.text == 'Торги на ЭТП':
                                    etp_url = button.get_attribute('href')
                                elif button.text == 'Лот на ГИС Торги':
                                    gis_url = button.get_attribute('href')

                    
                    
                write_to_file(f'{cat_name}.csv', [lot_id, name, price, kadastr_number, org_name, org_email, org_phone, org_inn, org_ogrn, org_contact, etp_url, gis_url, link[1]])

            driver_2.close()
            
            next_page = driver.find_elements(By.XPATH, '//a[@class="page-link" and @rel="next"]')
            action_chains = ActionChains(driver)
            if next_page:
                action_chains.move_to_element(next_page[0]).click().perform()
            else:
                break

            
        sleep(3)
    for title, i in cats.items():
        df = pd.read_csv(f'{title}.csv')
        df.to_excel(f'{title}.xlsx', index=False)
        os.remove(f'{title}.csv')
        


def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Лот', 'Нименование', 'Цена', 'Кадастровый номер', 'Наименование организации', 'Email', 'Телефон', 'ИНН', 'ОГРН', 
                         'ФИО контактного лица', 'Торги на ЭТП', 'Лот на ГИС Торги', 'Ссылка'])

def write_to_file(file_name, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    

if __name__ == '__main__':
    main()