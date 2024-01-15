import geocoder
import requests
from tkinter import *
from datetime import datetime


window = Tk()
window.config(padx=10, pady=10)
window.title("Weather")
window.iconbitmap("icons/sun.ico")

def refresh():

    g = geocoder.ip('me')

    weather_endpoint = "https://api.openweathermap.org/data/2.5/weather"
    forecast_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

    api_key = "139212597f13da5380ea494acf0705dd"
    lat = g.latlng[0]
    lon = g.latlng[1]

    weather_params = {
        "lat":lat,
        "lon":lon,
        "appid":api_key,
        "units":"metric"
    }

    response = requests.get(url=weather_endpoint, params=weather_params)
    forecast_response = requests.get(url=forecast_endpoint, params=weather_params)

    response.raise_for_status()
    global data
    data = response.json()

    forecast_response.raise_for_status()
    global forecast_data
    forecast_data = forecast_response.json()

    img = PhotoImage(file=f'icons/{data["weather"][0]["icon"]}.png')
    temp = round(data["main"]["temp"])
    feels_like_temp = round(data["main"]["feels_like"])
    description = data["weather"][0]["description"]
    sunrise_unix = data["sys"]["sunrise"]
    sunrise_time = datetime.fromtimestamp(sunrise_unix).strftime('%H:%M')
    sunset_unix = data["sys"]["sunset"]
    sunset_time = datetime.fromtimestamp(sunset_unix).strftime('%H:%M')
    min_temp = data["main"]["temp_min"]
    max_temp = data["main"]["temp_max"]
    wind_speed = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    location = f"{data['name']}, {data['sys']['country']}"

    forecast_labels = {
        "label0":Label(),
        "label1":Label(),
        "label2":Label(),
        "label3":Label(),
        "label4":Label(),
        "label5":Label(),
        "label6":Label(),
        "label7":Label(),
        "label8":Label(),
        "label9":Label(),

    }

    for hour in range(0, 7):
        weekday_unix = forecast_data["list"][hour]["dt"]
        weekday = datetime.fromtimestamp(weekday_unix).strftime("%d.%m.\n%H:%M")
        forecast_img = PhotoImage(file=f'resized_icons/{forecast_data["list"][hour]["weather"][0]["icon"]}.png')
        forecast_temp = round(forecast_data["list"][hour]["main"]["temp"])
        forecast_labels[f"label{hour}"].config(text=f"{weekday}\n{forecast_temp} °C", image=forecast_img, compound=TOP)
        forecast_labels[f"label{hour}"].grid(row=3, column=hour)
        forecast_labels[f"label{hour}"].image = forecast_img


    icon_label = Label(image=img)
    icon_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, columnspan=2)
    icon_label.image = img

    temp_label = Label(text=f"{temp}°C", font=("Arial", 40, "bold"))
    temp_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

    feels_like_temp_label = Label(text=f"Feels like: {feels_like_temp} °C\n{description}", font=("Arial", 10))
    feels_like_temp_label.grid(row=1, column=2, rowspan=2, padx=10, pady=10)

    sunrise_img = PhotoImage(file="icons/sunrise.png")
    sunrise_label = Label(image=sunrise_img, text=f"Sunrise:\n{sunrise_time}", compound=TOP)
    sunrise_label.grid(row=0, column=3, padx=10, pady=10)
    sunrise_label.image = sunrise_img

    sunset_img = PhotoImage(file="icons/sunset.png")
    sunset_label = Label(image=sunset_img, text=f"Sunset:\n{sunset_time}", compound=TOP)
    sunset_label.grid(row=0, column=4, padx=10, pady=10)
    sunset_label.image = sunset_img

    min_temp_image = PhotoImage(file="icons/min_temp.png")
    min_temp_label = Label(image=min_temp_image, text=f"Min. Temperature:\n{min_temp} °C", compound=TOP)
    min_temp_label.grid(row=1, column=3, padx=10, pady=10)
    min_temp_label.image = min_temp_image

    max_temp_image = PhotoImage(file="icons/max_temp.png")
    max_temp_label = Label(image=max_temp_image, text=f"Max. Temperature:\n{max_temp} °C", compound=TOP)
    max_temp_label.grid(row=1, column=4, padx=10, pady=10)
    max_temp_label.image = max_temp_image

    pressure_image = PhotoImage(file="icons/pressure.png")
    pressure_label = Label(image=pressure_image, text=f"Wind pressure:\n{pressure} mb", compound=TOP)
    pressure_label.grid(row=0, column=5, padx=10, pady=10)
    pressure_label.image = pressure_image

    speed_image = PhotoImage(file="icons/speed.png")
    speed_label = Label(image=speed_image, text=f"Wind speed:\n{wind_speed} km/h", compound=TOP)
    speed_label.grid(row=0, column=6, padx=10, pady=10)
    speed_label.image = speed_image

    humidity_image = PhotoImage(file="icons/humidity.png")
    humidity_label = Label(image=humidity_image, text=f"Humidity:\n{humidity} %", compound=TOP)
    humidity_label.grid(row=1, column=5, padx=10, pady=10)
    humidity_label.image = humidity_image

    refresh_image = PhotoImage(file="icons/refresh.png")
    refresh_button = Button(image=refresh_image, command=refresh)
    refresh_button.grid(row=1, column=6, padx=10, pady=10)
    refresh_image.image = refresh_image

    location_label = Label(text=f"Current location: {location}")
    location_label.grid(row=2, column=0, padx=10, pady=10)

    time_label = Label(text=f"Updated: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    time_label.grid(row=2, column=1)

refresh()


window.mainloop()