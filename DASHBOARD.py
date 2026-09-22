from xmlrpc import client

from rich import print
from rich.console import Console
from rich.theme import Theme
import asyncio 
from open_meteo import OpenMeteo 
from open_meteo.models import DailyParameters, HourlyParameters

custom_theme = Theme({
    "hot": "orange", 
    "sunny" : "yellow",
    "cloudy" : "grey",
    "cold" : "blue"
})
console = Console(theme = custom_theme)

async def main():
    async with OpenMeteo() as client:
        forecast = await client.forecast(
            latitude=45.4339,
            longitude=4.39,
            current_weather=True,
            #daily=[DailyParameters.SUNRISE, DailyParameters.SUNSET],
            #hourly=[HourlyParameters.TEMPERATURE_2M, HourlyParameters.RELATIVE_HUMIDITY_2M],
        )
        if forecast.current_weather.temperature >30 :
            console.print(":hot: It's a hot day!",style="hot") # temperature is above 30°C
        elif forecast.current_weather.temperature > 20 : 
            console.print(":sunny: It's a warm day!",style="sunny") #temperature is above 20°C
        elif forecast.current_weather.temperature >10 : 
            console.print(":cloud: It's a cool day! ",style="cloudy")#temperature is above 10°C
        else : 
            console.print(":cold: It's a cold day!",style="cold")# temperature is under 10°C
        #print(forecast) # print the result of the request with API

if __name__ == "__main__":
    asyncio.run(main())

#print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
#console.print("Hello World!", style="bold magenta", emoji=True)

