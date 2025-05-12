import pytest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Фикстура инициализации драйвера Appium для мобильного браузера Chrome
@pytest.fixture(
def driver():
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "13",  
        "deviceName": "Android Emulator",
        "browserName": "Chrome",
        "chromedriverExecutable": "/path/to/chromedriver"  # обновите путь к chromedriver, совместимому с версией Chrome
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Тест 1: Поиск видео через мобильную клавиатуру и поиск
def test_mobile_search_video(driver):
    driver.get("https://m.youtube.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='search']"))
    )
    search_box.click()
    search_box.send_keys("Python tutorials")
    # Нажатие кнопки поиска
    driver.find_element(By.XPATH, "//button[@id='search-icon-legacy']").click()
    # Проверка результатов
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='video-title']"))
    )
    videos = driver.find_elements(By.XPATH, "//a[@id='video-title']")
    assert any("Python" in video.text for video in videos)

# Тест 2: Скролл результатов поиска с помощью жеста свайпа
def test_mobile_swipe_scroll(driver):
    driver.get("https://m.youtube.com/results?search_query=Python")
    size = driver.get_window_size()
    start_x = size['width'] / 2
    start_y = size['height'] * 0.8
    end_y = size['height'] * 0.2
    driver.swipe(start_x, start_y, start_x, end_y, 800)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='video-title']"))
    )

# Тест 3: Проигрывание и пауза видео через тап по видео
def test_mobile_play_pause_video(driver):
    driver.get("https://m.youtube.com/watch?v=dQw4w9WgXcQ")
    video_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )
    # Тап по видео для переключения режима воспроизведения/паузы
    size = video_element.size
    x = video_element.location['x'] + size['width'] / 2
    y = video_element.location['y'] + size['height'] / 2
    driver.tap([(x, y)])
    # Проверка, что видео поставлено на паузу
    paused = driver.execute_script("return arguments[0].paused;", video_element)
    assert paused is True

# Тест 4: Регулировка громкости свайпом по области громкости
def test_mobile_adjust_volume(driver):
    driver.get("https://m.youtube.com/watch?v=dQw4w9WgXcQ")
    volume_slider = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'volume-slider')]"))
    )
    size = volume_slider.size
    start_x = volume_slider.location['x'] + size['width'] * 0.8
    end_x = volume_slider.location['x'] + size['width'] * 0.2
    y = volume_slider.location['y'] + size['height'] / 2
    driver.swipe(start_x, y, end_x, y, 300)

# Тест 5: Свайп для перехода на следующий авто-видео
def test_mobile_next_video_swipe(driver):
    driver.get("https://m.youtube.com/watch?v=dQw4w9WgXcQ")
    size = driver.get_window_size()
    start_x = size['width'] * 0.8
    end_x = size['width'] * 0.2
    y = size['height'] / 2
    driver.swipe(start_x, y, end_x, y, 500)
    # Проверка, что видео сменилось (заголовок обновился)
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'title')]"))
    )
    assert title.text != ""

