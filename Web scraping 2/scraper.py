from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from config import BASE_URL, OUTPUT_CSV

def solve_captcha():
    # You can implement CAPTCHA solving here, e.g., using DeathByCaptcha
    captcha_answer = input("Enter the CAPTCHA answer: ")  # Manually input or solve via service
    return captcha_answer

def scrape_data():
    driver = webdriver.Chrome()  # Initialize WebDriver
    driver.get(BASE_URL)  # Navigate to the URL
    wait = WebDriverWait(driver, 10)

    # Step 1: Select Case Type from dropdown
    case_type_dropdown = Select(driver.find_element(By.ID, "case_type"))  # Replace with actual ID
    case_type_dropdown.select_by_visible_text("Case Type")  # Select the appropriate case type

    # Wait for 10 seconds before proceeding (alternative to WebDriverWait)
    time.sleep(10)  # You can replace this with WebDriverWait if necessary

    # Step 2: Select Diary Year from dropdown
    diary_year_dropdown = Select(driver.find_element(By.ID, "select2-year-container"))  # Replace with actual ID
    diary_year_dropdown.select_by_visible_text("2022")  # Replace with the correct year

    # Wait for 10 seconds before proceeding (alternative to WebDriverWait)
    time.sleep(10)  # You can replace this with WebDriverWait if necessary

    # Step 3: Enter Case Number
    case_number_input = driver.find_element(By.ID, "case_no")  # Replace with actual ID
    case_number_input.send_keys("12")  # Replace with actual case number

    # Wait for 10 seconds before proceeding (alternative to WebDriverWait)
    time.sleep(10)  # You can replace this with WebDriverWait if necessary

    # Step 4: Handle CAPTCHA
    captcha_question = driver.find_element(By.CLASS_NAME, "siwp-captcha-cntr").text  # Replace with actual class
    print("CAPTCHA Question:", captcha_question)

    captcha_answer = solve_captcha()  # Call the CAPTCHA solver function

    captcha_input = driver.find_element(By.ID, "siwp_captcha_value_0")  # Replace with the actual CAPTCHA input ID
    captcha_input.send_keys(captcha_answer)  # Enter CAPTCHA answer

    # Wait for 10 seconds before proceeding (alternative to WebDriverWait)
    time.sleep(10)  # You can replace this with WebDriverWait if necessary

    # Step 5: Wait for form submission or page reload after CAPTCHA solving
    submit_button = driver.find_element(By.ID, "siwp_captcha_value_0")  # Replace with the submit button's ID
    submit_button.click()  # Submit the form

    # Wait for 10 seconds before proceeding (alternative to WebDriverWait)
    time.sleep(10)  # You can replace this with WebDriverWait if necessary

    # Extract case details after submitting the form
    cases = []
    try:
        for _ in range(10):  # Adjust number of pages to scrape
            time.sleep(2)  # Wait for content to load

            # Wait for case elements to load before extracting data
            case_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "case-class"))  # Adjust class name as needed
            )

            for case in case_elements:
                title = case.find_element(By.CLASS_NAME, "title-class").text  # Replace with actual class name
                date = case.find_element(By.CLASS_NAME, "date-class").text  # Replace with actual class name
                summary = case.find_element(By.CLASS_NAME, "summary-class").text  # Replace with actual class name
                cases.append({"Title": title, "Date": date, "Summary": summary})

            # Handle pagination if present
            try:
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Next")))  # Adjust as needed
                next_button.click()
            except Exception as e:
                print("No more pages or error:", e)
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

    # Save extracted data to CSV
    df = pd.DataFrame(cases)
    df.to_csv(OUTPUT_CSV, index=False)

if __name__ == "__main__":
    scrape_data()
