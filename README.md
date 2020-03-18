# Covid-19 Tracker (India)
> This is a simple RESTful API for accessing daily cases with state-wise breakdown in India. The average response 
> time of the API is ~400ms. Please link to this repository if you use it for your project :)

### Usage [v1]:
1. `GET https://covid19indiaapi.herokuapp.com/v1/states`

```json
{
    "state" : {
        "date" : ["confirmed (Indian Nationals)", "confirmed (Foreign Nationals)", "Recovered", "Death"]
    }
}
```

1. `GET https://covid19indiaapi.herokuapp.com/v1/overall`

```json
{
    "confirmed": ..., "recovered": ..., "death": ...
}
```

### Data Source:
[Ministry of Health & Family Walefare](https://www.mohfw.gov.in/)

### ToDo:
- Scrape websites to add specific info like # being monitored, age of new cases etc.