# 🦠COVID-19 Tracker (India) 
> This is a simple RESTful API for accessing daily cases with state-wise breakdown in India. The average response 
> time of the API is ~400ms. Please link to this repository if you use it for your project

______                _   _                            _   _          _    ______                _   _          _ 
| ___ \              | | | |                          | | | |        | |   | ___ \              | | | |        | |
| |_/ /_ __ ___  __ _| |_| |__   ___    __ _ _ __   __| | | |     ___| |_  | |_/ /_ __ ___  __ _| |_| |__   ___| |
| ___ \ '__/ _ \/ _` | __| '_ \ / _ \  / _` | '_ \ / _` | | |    / _ \ __| | ___ \ '__/ _ \/ _` | __| '_ \ / _ \ |
| |_/ / | |  __/ (_| | |_| | | |  __/ | (_| | | | | (_| | | |___|  __/ |_  | |_/ / | |  __/ (_| | |_| | | |  __/_|
\____/|_|  \___|\__,_|\__|_| |_|\___|  \__,_|_| |_|\__,_| \_____/\___|\__| \____/|_|  \___|\__,_|\__|_| |_|\___(_)
                                                                                                                  
                                                                                                                  

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