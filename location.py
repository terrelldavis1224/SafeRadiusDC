import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()
api_key = os.getenv("GEOAPIFY_API_KEY")




def getLocations(text):

    encoded_text = quote(text)  

    url = (
    "https://api.geoapify.com/v1/geocode/search?"
    f"text={encoded_text}"
    "&filter=circle:-77.03460987083406,38.89380923044945,120000"
    "&format=json"
    f"&apiKey={api_key}"
    )

    response = requests.get(url)

    # Handle the response
    if response.status_code == 200:
        data = response.json()

        if data['results'] == []:
            print("is empty")
            return None
        else:
            print(data['results'])
            for results in data['results']:
                print(results["formatted"])
                print(results["lon"])
                print(results["lat"])
                pass
            return data['results']
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
