from xmlrpc import client

from rich import print #import rich library 
from rich.console import Console #import console from rich library 
from rich.theme import Theme #import theme from rich library 
from rich.table import Table #import possiblity to create Table
import asyncio 
from open_meteo import OpenMeteo #import OpenMeteo to get the local weather
from open_meteo.models import DailyParameters, HourlyParameters #import previsions daily and hourly parameters
custom_theme = Theme({
    "hot": " bold red", 
    "sunny" : "yellow",
    "cloudy" : "black",
    "cold" : " cyan",
    "rain" : "bold blue",
    "snow" : "white"
}) #only use primary and secondary colors for customing theme
console = Console(theme = custom_theme) #use to add a theme at the terminal

async def main():
    async with OpenMeteo() as client:
        forecast = await client.forecast(
            latitude=45.4339,
            longitude=4.39, #Saint-Etienne location
            current_weather=True,
            #daily=True,
            hourly=[HourlyParameters.PRECIPITATION,HourlyParameters.SNOW_DEPTH],#useful for rain and snow 
        )
        nom_ville = "Saint-Etienne"
        ville_latitude = str(forecast.latitude)
        ville_longitude = str(forecast.longitude)
        precipitation_hourly = sum(forecast.hourly.precipitation)
        snow_hourly = sum(forecast.hourly.snow_depth)
        current_temperature = forecast.current_weather.temperature
        if precipitation_hourly> 5.0:
            console.print(":umbrella: Bring your umbrella today !", style="rain")#condition with rain
        elif snow_hourly > 0.02 :
            console.print(":snow: Bring a scarf and boots !", style="snow") #condition with snow 
        elif current_temperature >=30 :
            console.print(":hot: It's a hot day!",style="hot") # temperature is above 30°C
        elif current_temperature >= 20 : 
            console.print(":sunny: It's a warm day!",style="sunny") #temperature is above 20°C
        elif current_temperature >=10 : 
            console.print(":cloud: It's a cool day! ",style="cloudy")#temperature is above 10°C
        else : 
            console.print(":cold: It's a cold day!",style="cold")# temperature is under 10°C
        #print(forecast) # print the result of the request with API
        table = Table(title ="Bulletin meteo")
        table.add_column("Ville")
        table.add_column("Latitude")
        table.add_column("Longitude")
        table.add_column("Précipitations")
        table.add_column("Neige")
        table.add_column("Température")
        table.add_row(nom_ville,ville_latitude,ville_longitude,str(precipitation_hourly),str(snow_hourly),str(current_temperature))
        console.print(table)
        
if __name__ == "__main__":
    asyncio.run(main())





