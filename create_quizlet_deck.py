'''
Quizlet Deck Maker (Part I)

Overview:
- Creates a quizlet deck from a list of terms enterd by the user by pulling definitions from the 
Merriam Webster API. User must also enter their birth information, username, email, and password.

Notes: 
- Can add in functionality so that returning users can simply pass in credentials, though that 
would reuqire users to trust that the App isn't saving their info :) so sticking to new users for now.

- Currently, this only pulls definitions from one data source, and assumes that the pulled definition
is in fact correct. Can add functionality for synonyms, adjectics, antonyms, alternative definitions, etc.

- UI will be delivered via a Flask App which is a WIP.

- Add in error catching for invalid birth info, email address, username, password, word

- Look into Selenium ActionChains for future improvements
'''
import json
import pandas as pd 
import requests 
import time

from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from dictionary_funcs import send_request, get_definition
from quizlet_funcs import enter_birth_info, enter_account_info, enter_set_details, create_card

# Birth info
month = 'July'
day = '24'
year = '1993'

# Account info
username = 'autoRobotBeepBoop'
email = 'qubolerobot@gmail.com' 
password = 'TestPassword!'

# Set info
title = 'random words'
description = 'random words that we are adding to Quizlet'

# Navitage to homepage
driver = webdriver.Firefox()
driver.get("https://quizlet.com/")

# Add more robut wait time (WebDriverWait) between screen change
time.sleep(5)

# Find `Create` button on homepage
create = driver.find_element_by_class_name("SiteHeader-createInner")

# Click create
create.click()

# Add more robut wait time (WebDriverWait) between screen change
time.sleep(5)

# Enter personal, account info
enter_birth_info(driver, month, day, year)
enter_account_info(driver, username, email, password)

# Create account
sign_up = driver.find_element_by_class_name("UILoadingButton")
sign_up.click()

# Add more robut wait time (WebDriverWait) between screen change
time.sleep(5)

# Continue through to main page (popup appears after signup)
continue_link = driver.find_element_by_link_text('Or continue to free Quizlet')
continue_link.click()

# Check for popup, close if found
# If not found, catch error and continue
# Review `3.5: Popup dialogs` in documentation
try: 
    close_button = driver.find_element_by_class_name("UIModal-closeButton")
    close_button.click()
except NoSuchElementException as e:
    pass    

# Add more robut wait time (WebDriverWait) between screen change
time.sleep(5)

# Enter set title, description
enter_set_details(driver, title, description)

# List of words passed into the Dictionary API
# This will be replaced with a textbox when the UI is built
word_set = ['programming', 'engineering', 'computer', 'python', 'kindle', 'marathon', 'software', 'quarantine',
        'block', 'leaf', 'sample', 'tomahawk', 'cactus', 'air', 'throne', 'dirt', 'cherry', 'crunchy', 'sticky', 
         'frame', 'dog', 'chip', 'corner', 'bagel', 'fruit', 'general', 'plane', 'plain', 'flower']

# List of confirmed words, definitions
all_words = []
all_definitions = []

# Cycle through each word to get definition
for word in word_set:
    response = send_request(word)
    definition = get_definition(response)
    # Skip if definition returns blank
    if len(definition) == 0:
        continue
    all_words.append(word)
    all_definitions.append(definition)


# First five terms, definitions for 5 visible cards
first_five_words = all_words[:5]
first_five_definitions = all_definitions[:5]

# Remaining terms, definitions for added cards
remaining_words = all_words[5:]
remaining_definitions = all_definitions[5:]

# Select term row class
# By default, six cards are shown on the page
all_card_rows = driver.find_element_by_class_name("TermRows")
all_cards = all_card_rows.find_elements_by_class_name("TermRows-termRowWrap")

first_five_cards = all_cards[:5]
add_card = all_cards[-1]

# Enter first 5 terms and definitions into the cards 
i=0
for card in first_five_cards:
    create_card(card, first_five_words[i], first_five_definitions[i])
    i+=1
    
# Add a new card 
add_row = add_card.find_element_by_id("addRow").find_element_by_tag_name("button")
add_row.click()

for i in range(len(remaining_words)):
    # Get the final two terms rows; one is the new card, the other is the add row
    # Need to reset due to the Javascript event
    term_rows = driver.find_element_by_class_name("TermRows")
    new_card = term_rows.find_elements_by_class_name("TermRows-termRowWrap")[-2]
    add_card = term_rows.find_elements_by_class_name("TermRows-termRowWrap")[-1]
    
    # Create new card
    create_card(new_card, remaining_words[i], remaining_definitions[i])
        
    # Don't add a new card if final term
    if i+1 == len(remaining_words):
        break
    
    # Add a new card
    new_card = add_card.find_element_by_id("addRow").find_element_by_tag_name("button")
    new_card.click()

# Create list
create_set = driver.find_element_by_class_name("CreateSetPage-publishButton")
create = create_set.find_element_by_tag_name("button")
create.click()

# Add more robut wait time (WebDriverWait) between screen change
time.sleep(5)

# Search for popup; try to close
share_popup = driver.find_element_by_class_name("UIModalHeader-closeIconButton")
share_button = share_popup.find_element_by_tag_name("button")
share_button.click()