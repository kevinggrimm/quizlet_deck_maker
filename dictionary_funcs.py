# https://dictionaryapi.com/

# API Keys
dictionary_key = "YOUR_DICTIONARY_API_KEY_HERE"

# Pass a word to the dictionary API
def send_request(word, sleep=.2):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?"    
    headers = {
    'Content-Type': 'application/json'
    }
    params = {
        'key': dictionary_key
    }
    
    response = requests.get(url, headers=headers, params=params)
    time.sleep(sleep)
    response.raise_for_status()
    return response.json()

# Extract first response
def get_definition(response):
    definition = response[0]['shortdef'][0]
    return definition