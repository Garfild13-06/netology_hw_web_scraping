import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def wait_element(driver, delay_seconds=1, by=By.TAG_NAME, value=None):
    """
    Иногда элементы на странице не пргружаются сразу
    Функция ждёт delay_seconds если элемент не пргрузился
    Если за отведённое время элемент не прогружается выбрасывается timeoutException
    :param driver: driver
    :param delay_seconds: маскимальное время ожидания
    :param by: поле поиска
    :param value: значение поиска
    :return: найденный элемент
    """

    return WebDriverWait(driver, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


KEYWORDS = ['Гейм', 'дизайн', 'фото', 'web', 'python']

driver = webdriver.Chrome()
driver.get("https://habr.com/ru/all/")
articles = driver.find_element(By.CLASS_NAME, 'tm-articles-list')

parsed_data = []
result_data = []
all_element = articles.find_elements(By.TAG_NAME, 'article')
for article in all_element:
    h2_element = article.find_element(By.TAG_NAME, 'h2')
    a_element = h2_element.find_element(By.TAG_NAME, 'a')
    span_element = a_element.find_element(By.TAG_NAME, 'span')
    preview_element = article.find_element(By.CLASS_NAME, 'article-formatted-body')

    time_element = wait_element(driver, by=By.TAG_NAME, value='time')

    title = span_element.text
    link = a_element.get_attribute('href')
    date_time = time_element.get_attribute('datetime')
    preview_text = preview_element.text

    parsed_data.append({
        'title': title,
        'link': link,
        'datetime': date_time,
        'preview_text': preview_text
    })

# поиск ключевых слов по заголовку и preview-тексту на общей странице
# for _ in KEYWORDS:
#     if re.search(_, title, re.IGNORECASE) != None or re.search(_, preview_text, re.IGNORECASE) != None:
#         parsed_data.append({
#             'title': title,
#             'link': link,
#             'datetime': date_time
#         })
#         break
# получаем полный текст статьи
for item in parsed_data:
    driver.get(item['link'])
    article = wait_element(driver, by=By.ID, value='post-content-body')
    item['text'] = article.text

# ищем ключевые слова по загловку, preview-тексту на общей странице и всему тексту статьи
for item in parsed_data:
    for _ in KEYWORDS:
        if re.search(_, item['title'], re.IGNORECASE) != None or re.search(_, item['preview_text'],
                                                                           re.IGNORECASE) != None or re.search(_, item[
            'text'], re.IGNORECASE):
            result_data.append(item)
            break

for _ in result_data:
    print(f"{_['datetime']} - {_['title']} - {_['link']}")
