import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--start-fullscreen')  # Start Chrome in fullscreen mode
driver = webdriver.Chrome(options=options)

# Step 2: Open the webpage
url = 'https://the.streameast.app/mlb-playoffs/houston-astros-detroit-tigers/26489504'
driver.get(url)

# Wait for the page to load
time.sleep(4)

def click_center_of_screen():
    # Get the screen resolution of the browser window
    window_size = driver.get_window_size()
    window_width = window_size['width']
    window_height = window_size['height']

    # Calculate the center coordinates relative to the window size
    center_x = window_width // 2
    center_y = window_height // 2

    # Move to the center of the screen and click
    actions = ActionChains(driver)
    body = driver.find_element(By.TAG_NAME, 'body')  # Move relative to the body element
    actions.move_to_element_with_offset(body, center_x, center_y).click().perform()
    print("Clicked the center of the screen.")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#Click the video player
def click_element_by_xpath(xpath):
    try:
        # Wait for the element to be clickable and then click it
        element = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        print(f"Clicked element with XPath: {xpath}")
    except Exception as e:
        print(f"Error clicking the element with XPath: {xpath}: {e}")

# Try to click the element and handle new tabs
try:
    original_window = driver.current_window_handle
    element_xpath = '/html/body/div[1]/div/main/div[2]/div/div/div/div[1]/fieldset/div/div[1]'

    while True:
        # Click the element by its XPath
        click_element_by_xpath(element_xpath)

        # Wait for a possible new tab to open (use a short timeout if no new tab opens)
        try:
            WebDriverWait(driver, 3).until(EC.number_of_windows_to_be(2))  # Wait until a second window is detected
        except:
            # No new tab opened, exit the loop
            print("No new tabs opened. Exiting the loop.")
            break

        # If a new tab opens, close it and switch back to the original window
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                driver.close()  # Close the new tab

        # Switch back to the original tab
        driver.switch_to.window(original_window)

        # Optionally, wait for a bit before trying to click again
        time.sleep(2)

except Exception as e:
    print(f"Error handling new tabs and clicks: {e}")

# Continue with other tasks
driver.fullscreen_window()

# Example of capturing the screen with ffmpeg (make sure ffmpeg is properly configured)
ffmpeg_command = [
    'ffmpeg',
    '-f', 'gdigrab',
    '-framerate', '30',
    '-i', 'desktop',
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-c:a', 'aac',
    '-f', 'hls',
    '-hls_time', '10',
    '-hls_list_size', '5',  # Limit the number of .ts files to 5
    '-hls_playlist_type', 'event',
    'output.m3u8'
]

print(f"Running ffmpeg command: {' '.join(ffmpeg_command)}")

try:
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"ffmpeg error: {stderr.decode('utf-8')}")
    else:
        print("ffmpeg started successfully")
except Exception as e:
    print(f"An error occurred while running ffmpeg: {e}")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    driver.quit()
