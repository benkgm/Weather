from key import *
from datetime import datetime
import datetime as dt
import requests as requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


def kelvin_to_celsius_farhenheit(kelvin, unit):
    if unit == "celsius":
        celsius = kelvin - 273.15
        return celsius
    elif unit == "fahrenheit":
        fahrenheit = (kelvin - 273.15) * 9/5 + 32
        return fahrenheit
    else:
        raise ValueError("Unit must be celsius or fahrenheit")


def get_weather_icon(icon_code, size):
    icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
    icon_data = requests.get(icon_url).content
    with open("icon.png", "wb") as f:
        f.write(icon_data)
    icon_image = Image.open("icon.png")
    icon_image_resized = icon_image.resize((size, size), Image.LANCZOS)
    return ImageTk.PhotoImage(icon_image_resized)


def get_weather(city_name, unit):
    url = f"{BASE_URL}q={city_name}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    temperature = kelvin_to_celsius_farhenheit(data["main"]["temp"], unit)
    temperature_formatted = "{:.2f}".format(temperature)
    feels_like = kelvin_to_celsius_farhenheit(data["main"]["feels_like"], unit)
    feels_like_formatted = "{:.2f}".format(feels_like)
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_direction = data["wind"]["deg"]
    description = data["weather"][0]["description"]
    icon = get_weather_icon(data["weather"][0]["icon"], 100)
    return temperature_formatted, feels_like_formatted, humidity, pressure, wind_speed, wind_direction, description, icon


class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")
        self.master.geometry("400x400")
        # Set background color of root window
        self.master.configure(bg="#0077be")
        # Set background color of label
        self.city_label = tk.Label(
            self.master, text="Enter city name", bg="#0077be", fg="white")
        self.city_label.grid(row=0, column=1, padx=5, pady=5)
        self.city_entry = tk.Entry(self.master)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5,)
        self.unit_var = tk.StringVar(value="celsius")
        self.celsius_radio = tk.Radiobutton(
            self.master, text="Celsius", variable=self.unit_var, value="celsius", bg="#0077be", fg="white")  # Set background color of radio button
        self.celsius_radio.grid(row=2, column=0, padx=5, pady=5)
        self.fahrenheit_radio = tk.Radiobutton(
            self.master, text="Fahrenheit", variable=self.unit_var, value="fahrenheit", bg="#0077be", fg="white")  # Set background color of radio button
        self.fahrenheit_radio.grid(row=2, column=2, padx=5, pady=5)
        self.get_weather_button = tk.Button(
            self.master, text="Get Weather", command=self.display_weather, bg="#0077be", fg="black")  # Set background color of button
        self.get_weather_button.grid(
            row=3, column=0, columnspan=3, padx=5, pady=5)
        # Set background color of label
        self.result_label = tk.Label(
            self.master, text="", bg="#0077be", fg="white")
        self.result_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        # Set background color of label
        self.icon_label = tk.Label(self.master, bg="#0077be")
        self.icon_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        # Set background color of label
        self.feels_like_label = tk.Label(
            self.master, text="", bg="#0077be", fg="white")
        self.feels_like_label.grid(row=6, column=0, padx=5, pady=5)
        # Set background color of label
        self.humidity_label = tk.Label(
            self.master, text="", bg="#0077be", fg="white")
        self.humidity_label.grid(row=6, column=2, padx=5, pady=5)
        # Set background color of label
        self.pressure_label = tk.Label(
            self.master, text="", bg="#0077be", fg="white")
        self.pressure_label.grid(row=7, column=0, padx=5, pady=5)
        # Set background color of label
        self.wind_speed_label = tk.Label(
            self.master, text="", bg="#0077be", fg="white")
        self.wind_speed_label.grid(row=7, column=2, padx=5, pady=5)
        self.wind_direction_label = tk.Label(
            self.master, text="", bg="#0077be", fg="white")  # Set background color of label
        self.wind_direction_label.grid(row=8, column=0, padx=5, pady=5)

    def display_weather(self):
        city_name = self.city_entry.get()
        unit = self.unit_var.get()
        temperature, feels_like, humidity, pressure, wind_speed, wind_direction, description, icon = get_weather(
            city_name, unit)
        self.result_label.config(
            text=f"{temperature} {unit.capitalize()} - {description}")
        self.icon_label.config(image=icon)
        self.icon_label.image = icon
        self.feels_like_label.config(
            text=f"Feels like: {feels_like} {unit.capitalize()}")
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        self.pressure_label.config(text=f"Pressure: {pressure} hPa")
        self.wind_speed_label.config(text=f"Wind speed: {wind_speed} m/s")
        self.wind_direction_label.config(
            text=f"Wind direction: {wind_direction}°")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
