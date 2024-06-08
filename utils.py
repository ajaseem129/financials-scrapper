from datetime import time
import requests
from bs4 import BeautifulSoup
from downloader import download_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import os
import logging
from config import LOG_FILE_PATH,REPORT_TYPES

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def find_investor_page(base_url, driver):
    urls_to_try = [f'https://{base_url}', f'http://{base_url}']
    for url in urls_to_try:
        try:
            driver.get(url)
            time.sleep(3)
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            
            potential_links = soup.find_all('a', href=True)
            for link in potential_links:
                href = link['href'].lower()
                if any(keyword in href for keyword in ['investor', 'reports', 'financials']):
                    if not href.startswith('http'):
                        href = urljoin(url, href)
                    return href
        except Exception as e:
            logging.error(f"Error accessing {url}: {e}")
    return None

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_reports(investor_page, company_name, report_type, driver, download_dir):
    report_dir = os.path.join(download_dir, company_name, report_type)
    create_directory(report_dir)
    
    driver.get(investor_page)
    time.sleep(3)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')

    report_links = soup.find_all('a', href=True)
    for link in report_links:
        if any(report_type in link['href'].lower() for report_type in REPORT_TYPES):
            report_url = link['href']
            if not report_url.startswith('http'):
                report_url = urljoin(investor_page, report_url)
            try:
                download_file(report_url, report_dir)
            except Exception as e:
                logging.error(f"Error downloading report from {report_url} for {company_name}: {e}")
