import pandas as pd
import folium
from haversine import haversine, Unit
import os
import geocoder
import requests
from io import StringIO
import os
import leafmap.foliumap as leafmap
from openai import OpenAI
from dotenv import load_dotenv



load_dotenv()
client =  OpenAI()

crime_color_mapping = {
    'theft/other': 'lightgray',
    'robbery': 'darkred',
    'motor vehicle theft': 'cadetblue',
    'theft f/auto': 'lightblue',
    'assault w/dangerous weapon': 'darkpurple',
    'burglary': 'gray',
    'sex abuse': 'purple',
    'homicide': 'black',
    'arson': 'orange'
}

try:
    crime_data = pd.read_csv("dc-crimes-search-results.csv")
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error loading CSV file: {e}")


def split_coordinates(coord):
    lat_str, lon_str = coord.split(",")
    return float(lat_str), float(lon_str)

crime_data[['latitude', 'longitude']] = crime_data['location'].apply(split_coordinates).apply(pd.Series)

# Set the map center and radius
map_center = [38.8951, -77.0364]
mile_radius = 1609.34


# Define the legend's HTML
legend_html = '''
<div style="position: fixed; 
     bottom: 20px; left: 1rem; width: 2rem; height: auto; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.85; padding: 10px;">
     <b>Legend</b> <br>
     Theft (Other): <i class="fa fa-circle" style="color:lightgray"></i><br>
     Robbery: <i class="fa fa-circle" style="color:darkred"></i><br>
     Motor Vehicle Theft: <i class="fa fa-circle" style="color:cadetblue"></i><br>
     Theft from Auto: <i class="fa fa-circle" style="color:lightblue"></i><br>
     Assault with Dangerous Weapon: <i class="fa fa-circle" style="color:indigo"></i><br>
     Burglary: <i class="fa fa-circle" style="color:gray"></i><br>
     Sex Abuse: <i class="fa fa-circle" style="color:purple"></i><br>
     Homicide: <i class="fa fa-circle" style="color:black"></i><br>
     Arson: <i class="fa fa-circle" style="color:orange"></i><br>
</div>
'''

# Create the initial map
my_map = folium.Map(location=map_center, max_zoom=12, width='100%', height='500px')

# Create the circle
circle = folium.Circle(
    location=map_center,
    radius=mile_radius * 5,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.1,
    popup='5 Mile Radius'
).add_to(my_map)

# Function to update the circle and add markers
def update_circle(curx, cury ,miles,report):
    

    latitude, longitude = curx,cury 
    
    my_map = folium.Map(location=[latitude, longitude], zoom_start=12, attributionControl=False)  
    my_map.get_root().html.add_child(folium.Element(legend_html))


    circle = folium.Circle(
    location=[latitude, longitude],
    radius=mile_radius * miles,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.1,
    popup='5 Mile Radius'
    ).add_to(my_map)
    r = 0
    folium.Marker(location=[latitude, longitude], popup="me").add_to(my_map)
    lst = []
    
    for index, row in crime_data.iterrows():
        x = row['latitude']
        y = row['longitude']
        crime_committed = row["OFFENSE"]
        point = (x, y)
        center = (curx, cury)
        distance = haversine(center, point, unit=Unit.METERS) #determines the great-circle distance between two points on a sphere
        if distance < mile_radius * miles:  # Check against the radius
             if  r < 500: # at 25 because any more reach input limit with pipeline
                lst.append(index)
                folium.Marker(location=[x, y], popup=f"{crime_committed}",icon=folium.Icon(icon="glyphicon-star", color= crime_color_mapping[crime_committed])
).add_to(my_map)
                r += 1  
               # print(f"Added marker at {x}, {y}. Total markers: {r}")  # Print marker info
    

    filtered_crime_data = crime_data.iloc[lst]
    filtered_crime_data["START_DATE"] = pd.to_datetime(filtered_crime_data["START_DATE"], format="%m/%d/%Y, %I:%M:%S %p")
    filtered_crime_data["MONTH"] = filtered_crime_data['START_DATE'].dt.month_name()
    filtered_crime_data["DAY_NUMBER"] = filtered_crime_data['START_DATE'].dt.days_in_month
    numerical_desc = filtered_crime_data.groupby("OFFENSE")[['DAY_NUMBER']].describe()
    categorical_desc = filtered_crime_data.groupby("OFFENSE")[['METHOD', 'SHIFT', 'BLOCK',"MONTH"]].describe(include='all')

    df_describe = pd.concat([numerical_desc, categorical_desc], axis=1)
    df_describe.columns = ['_'.join(col).strip() for col in df_describe.columns.values]
    #df_describe.to_csv("/Users/terrelldavis/Desktop/Personal Projects/SafeRadiusDC/infotest.csv")
    input_string = StringIO()
    # df_describe.to_csv(input_string, index=False)
    csv_output = input_string.getvalue()

    if report :
        reportInfo = gptRequest(csv_output)
    else:
        reportInfo =""

    # Save the updated map

    return (my_map._repr_html_(),reportInfo)
#create_report(csv_output)
    

def gptRequest(text):
    # Create the response using OpenAI's API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate crime reports for users based on provided crime data. These reports should be personalized, "
                    "engaging, and focused on helping users understand crime trends in their specific area. Start with a "
                    "conversational introduction that acknowledges the user's location and highlights the most relevant or "
                    "concerning crime trends. Include actionable advice and a summary of the top crimes nearby. Transition "
                    "smoothly into detailed insights for each crime type. Use a friendly but serious tone to keep the report "
                    "both relatable and informative."
                )
            },
            {
                "role": "user",
                "content": f"{text}"
            }
        ],
        temperature=0.7,
    )
    summary_text = response.choices[0].message.content
    return summary_text
