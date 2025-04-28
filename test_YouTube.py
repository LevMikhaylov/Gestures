import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка фикстуры браузера
@pytest.fixture(scope="module")
def driver():
    service = Service('path_to_chromedriver')  # укажите путь к chrome driver
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Тест 1: Поиск видео по ключевому слову (жест поиска)
def test_search_video(driver):
    driver.get("https://www.youtube.com")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Python tutorials")
    search_box.send_keys(Keys.RETURN)
    # Проверка, что результат поиска содержит нужное видео
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video-title"))
    )
    videos = driver.find_elements(By.ID, "video-title")
    assert any("Python" in video.text for video in videos)

# Тест 2: Увеличить громкость (жест регулировки громкости)
def test_increase_volume(driver):
    driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # Ожидание отображения плеера
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ytp-volume-panel"))
    )
    # Эмуляция жеста увеличения громкости (например, через JavaScript)
    driver.execute_script("""
        var video = document.querySelector('video');
        if (video) {
            video.volume = Math.min(1, video.volume + 0.1);
        }
    """)
    # Проверка, что громкость увеличилась
    # В реальной ситуации нужно получать текущий уровень громкости, если есть API или через JavaScript

# Тест 3: Переключение на следующую видео
def test_next_video(driver):
    driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ytp-next-button"))
    )
    next_button.click()
    # Проверка, что новое видео началось (например, обновление заголовка)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title"))
    )
    title = driver.find_element(By.CSS_SELECTOR, "h1.title")
    assert title.text != ""

# Тест 4: Воспроизведение и пауза (жест воспроизведения)
def test_play_pause(driver):
    driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # Найти кнопку воспроизведения/паузу
    play_pause_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ytp-play-button"))
    )
    play_pause_button.click()  # поставим на паузу
    # Проверка, что видео поставлено на паузу
    state = driver.execute_script(
        "return document.querySelector('video').paused"
    )
    assert state is True
    # Возобновление воспроизведения
    play_pause_button.click()


# Тест 5: Ползунок громкости (жест регулировки)
def test_adjust_volume_slider(driver):
    driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    volume_slider = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ytp-volume-area .ytp-volume-slider"))
    )
    # Можно эмулировать перемещение с помощью ActionChains или JavaScript
    driver.execute_script("arguments[0].value = 0.5;", volume_slider)
    # Проверить, что уровень изменился (может потребовать более сложных методов)
