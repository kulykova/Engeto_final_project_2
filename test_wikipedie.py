import pytest
import re
from playwright.sync_api import Page


# Overeni viditelnosti titulu stranky
def test_viditelnost_title(page: Page):
    page.goto('https://www.wikipedia.org/')
    page.get_by_role('link', name='Čeština').click()
    assert (page.get_by_text('Vítejte ve Wikipedii')).is_visible()


home_URL = 'https://cs.wikipedia.org/wiki/Hlavn%C3%AD_strana'
validni_uzivatelske_jmeno = 'validnijmeno'
validni_heslo = 'validniheslo'
nevalidni_uzivatelske_jmeno = 'nenijmeno'
nevalidni_heslo = 'neniheslo'
search_input_selector = 'input[name="search"]'
text_input = 'Python'

# Overeni ze na strance je text 'Wikipedie:Článek týdne'
def test_text_title(page: Page):
    page.goto(home_URL)
    page.get_by_role('link', name='Článek týdne').click()
    assert (page.get_by_text('Wikipedie:Článek týdne'))


# Overeni neuspěšné přihlášení
def test_neuspesne_prihlaseni(page):
    page.goto(home_URL)
    page.get_by_role("link", name='Přihlášení').click()
    page.locator("#wpName1").fill(nevalidni_uzivatelske_jmeno)
    page.locator("#wpPassword1").fill(nevalidni_heslo)
    page.get_by_role("button", name='Přihlásit se').click()  
    assert(page.get_by_text('Bylo zadáno nesprávné uživatelské jméno nebo heslo.Zkuste to znovu.'))

# Úspěšné přihlášení
def test_uspesne_prihlaseni(page):
    page.goto(home_URL)
    page.get_by_role("link", name='Přihlášení').click()
    page.fill("#wpName1", validni_uzivatelske_jmeno)
    page.fill("#wpPassword1", validni_heslo)
    page.get_by_role("button", name='Přihlásit se').click() 
    assert(page.get_by_text('Vítejte ve Wikipedii.'))

# Overeni vyhledavani
def test_search(page):
    page.goto(home_URL)
    page.fill('input[name="search"]', text_input)
    page.press('input[name="search"]', "Enter")
    page.wait_for_load_state("load")
    assert (page.get_by_title(text_input))
    