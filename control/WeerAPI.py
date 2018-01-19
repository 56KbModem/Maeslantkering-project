from weather import Weather
weather = Weather()

# Zoek inlog via http://weather.yahoo.com.

lookup = weather.lookup(560743)
condition = lookup.condition()
print(condition.text())

# Vraag locatie aan

location = weather.lookup_by_location('amsterdam')
condition = location.condition()
print(condition.text())

# Laat de weersvoorspelling zien

forecasts = location.forecast()
for forecast in forecasts:
    print(forecast.text(), forecast.date(), forecast.high(), forecast.low())

