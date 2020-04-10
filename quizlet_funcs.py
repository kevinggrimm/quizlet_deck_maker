'''
Select month, day, and year
- Same process; can be packaged in to a function
- Enter values submitted on form
'''

def enter_birth_info(driver, month, day, year):
    # Select, enter month
    birth_month = Select(driver.find_element_by_name("birth_month"))
    select = birth_month.select_by_visible_text(month)
    
    # Select, enter day
    birth_day = Select(driver.find_element_by_name("birth_day"))
    select = birth_day.select_by_visible_text(day)
    
    # Select, enter year
    birth_year = Select(driver.find_element_by_name("birth_year"))
    select = birth_year.select_by_visible_text(year)
    
def enter_account_info(driver, username, email, password):
    # Select, enter username
    page_username = driver.find_element_by_id("username")
    page_username.send_keys(username)
    
    # Select, enter email
    page_email = driver.find_element_by_id("email")
    page_email.send_keys(email)
    
    # Select, enter password
    page_password = driver.find_element_by_id("password1")
    page_password.send_keys(password)


# Function to enter set title, description
def enter_set_details(driver, title, description):
    fields = {"title": title,
              "description": description}
    header = driver.find_element_by_class_name("CreateSetHeader-headingContent")
    for key in fields.keys():
        set_field = header.find_element_by_class_name("CreateSetHeader-" + key)
        set_label = set_field.find_element_by_tag_name("label")
        set_area = set_label.find_element_by_tag_name("textarea")
        set_area.click()
        set_area.send_keys(fields[key])


# Function to add word, definition to card
def create_card(driver, word, definition):
    fields = {'word': word, 'definition': definition}
    for key in fields.keys():
        card_field = driver.find_element_by_class_name("TermContent-side--" + key)
        editor = card_field.find_element_by_class_name("ProseMirror")
        editor.send_keys(fields[key])

