import pytest
import re
from playwright.async_api import Page, expect, input

# Overeni viditelnosti titulu stranky
def test_viditelnost_title(page: Page):
    page.goto('https://www.wikipedia.org/')
    page.get_by_role('link', name='Čeština').click()
    expect(page.get_by_text('Vítejte ve Wikipedii,')).to_be_visible()

# Overeni ze na strance je text 'Wikipedie:Článek týdne'
def test_text_title(page: Page):
    page.goto('https://www.wikipedia.org/')
    page.get_by_role('link', name='Čeština').click()
    page.get_by_role('link', name='Článek týdne').click()
    page.locator('#ca-talk').click()
    expect(page.locator('#firstHeading')).to_have_text('Wikipedie:Článek týdne')

# Overeni prihlaseni
def test_prihlaseni(page: Page, uzivateslke_jmeno, heslo, spravne_udaje):
    page.goto('https://www.wikipedia.org/')
    page.get_by_role('link', name='Čeština').click()
    page.get_by_role('link', name='Přihlášení').click()
    page.locator('input(#wpName1)').fill(uzivateslke_jmeno)
    page.locator('input(#wpPassword1)').fill(heslo)
    page.locator('#wpLoginAttempt').click()
    if (spravne_udaje):
        assert page.title() != 'Vítejte, uživateli (uzivateslke_jmeno)'
    else:
        assert page.title() == 'Vítejte, uživateli (uzivateslke_jmeno)'

# Overeni vyhledavani
def test_search(page: Page, text_input):
    page.goto('https://cs.wikipedia.org/wiki/Hlavn%C3%AD_strana')
    search_input_selector = 'input(#searchform)'
    text_input = 'Python'
    page.fill(search_input_selector, text_input)
    page.locator("button:has-text('Hledat')").click()
    page.wait_for_load_state("load")
    assert text_input in page.url.lower()
    #nebo
    assert (page).to_have_title(re.compile('text_input'))