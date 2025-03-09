from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re

def track_view(request):
    if request.method == "POST":
        tracking_number = request.POST.get("tracking_number")
        tracking_info = track_package(tracking_number)
        return render(request, "tracking/tracking.html", {"tracking_info": tracking_info})
    
    return render(request, "tracking/tracking.html")

def track_package(tracking_number):
    url = f"https://www.chronopost.fr/tracking-no-cms/suivi-page?listeNumerosLT={tracking_number}"

    # Set up Selenium WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser pop-up)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Use WebDriver Manager to install and set up ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    tracking_info = []

    try:
        # Wait until the tracking table appears
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ch-block-suivi-tab"))
        )

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "lxml")

        # Locate the tracking table
        tracking_table = soup.find("table", class_="ch-block-suivi-tab")

        if tracking_table:
            rows = tracking_table.find_all("tr")
            for row in rows[1:]:  # Skip header row
                columns = row.find_all(["th", "td"])
                if len(columns) >= 2:
                    raw_date = columns[0].get_text(strip=True)

                    # Fixing date format (Ensuring two spaces before time)
                    match = re.match(r"(.+? \d{2}/\d{2}/\d{4})(\d{2}:\d{2})", raw_date)
                    if match:
                        formatted_date = f"{match.group(1)}  {match.group(2)}"  # Add two spaces before time
                    else:
                        formatted_date = raw_date  # Fallback if parsing fails

                    step = columns[1].get_text(strip=True)
                    complement = columns[2].get_text(strip=True) if len(columns) > 2 else ""

                    tracking_info.append([formatted_date, step, complement])
        else:
            tracking_info = [["No data found", "Tracking details not available", ""]]

    except Exception as e:
        tracking_info = [["Error", str(e), ""]]

    finally:
        driver.quit()  # Close the browser session

    return tracking_info
