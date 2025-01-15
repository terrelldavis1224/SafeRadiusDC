import pandas as pd

crime_data = pd.read_csv("/Users/terrelldavis/Desktop/Personal Projects/SafeRadiusDC/dc-crimes-search-results.csv")

shifts = ['midnight', 'day', 'evening']
offenses = ['theft/other', 'robbery', 'motor vehicle theft', 'theft f/auto',
       'assault w/dangerous weapon', 'burglary', 'sex abuse', 'homicide',
       'arson']
offensegrouplst = ['property', 'violent']
def processCrimedata(offense,offensegroup,shift):
    df = crime_data
    if shift in shifts:
        df =df[df["SHIFT"] == shift]
    if offense in offenses:
        df =df[df["OFFENSE"] == offense]
    if  offensegroup in offensegrouplst:
        df=df[df["offensegroup"] == offensegroup]

    return df

