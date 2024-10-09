from json import dumps, loads
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_cards(url: str, timeout: int = 5) -> str:
    driver = webdriver.Chrome()
    driver.get(url)

    # Accept cookies
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
    )
    # Some chat window overlaps, click with JS instead
    accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    driver.execute_script("arguments[0].click();", accept_button)

    # Wait for cards to render from JS
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "uk-card")))
    sleep(1)

    # Parse cards
    result = []
    cards = driver.find_elements(By.CLASS_NAME, "uk-card")
    for card in cards:
        product_json = {
            "productName": "",
            "startingLetter": "",
            "description": "",
            "freeTrialUrl": "",
            "demoRequestUrl": "",
            "supportLinkUrl": "",
            "communityLinkUrl": "",
        }
        title = (
            card.find_element(By.CLASS_NAME, "uk-card-title")
            .find_element(By.CLASS_NAME, "block-header")
            .text
        )
        product_json["productName"] = title
        product_json["startingLetter"] = title[0].upper()
        product_json["description"] = card.find_element(By.CLASS_NAME, "description").text

        for link in card.find_elements(By.TAG_NAME, "a"):
            text, href = link.text, link.get_attribute("href")
            if text == "Get free trial" and href:
                product_json["freeTrialUrl"] = href
            elif text == "Request a demo" and href:
                product_json["demoRequestUrl"] = href
            elif text == "Community" and href:
                product_json["communityLinkUrl"] = href
            elif text == "Support" and href:
                product_json["supportLinkUrl"] = href
        result.append(product_json)

    return dumps(result)


if __name__ == "__main__":
    product_list = scrape_cards("https://www.microfocus.com/en-us/products?trial=true")
    print(product_list)
    with open("products.json", "w") as f:
        f.write(product_list)

    pretty_product_list = dumps(loads(product_list), indent=4)
    print(pretty_product_list)
    with open("pretty_products.json", "w") as f:
        f.write(pretty_product_list)
