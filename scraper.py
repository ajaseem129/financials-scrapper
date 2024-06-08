import pandas as pd
from utils import init_driver, find_investor_page, download_reports
from config import REPORT_TYPES, DOWNLOAD_DIR, DELAY_BETWEEN_REPORTS
import time

def load_websites(file_path):
    df = pd.read_csv(file_path)
    return df[['name', 'internet']].values.tolist()

def process_companies(file_path):
    company_data = load_websites(file_path)
    driver = init_driver()
    
    for company_name, website in company_data:
        print(f'Processing: {company_name} - {website}')
        try:
            investor_page = find_investor_page(website, driver)
            if investor_page:
                print(f'Found investor page: {investor_page}')
                for report_type in REPORT_TYPES:
                    download_reports(investor_page, company_name, report_type, driver, DOWNLOAD_DIR)
                    time.sleep(DELAY_BETWEEN_REPORTS)  # Delay between report type downloads
            else:
                print(f'Investor page not found for: {company_name}')
        except Exception as e:
            print(f"Error processing {company_name}: {e}")
    
    driver.quit()
