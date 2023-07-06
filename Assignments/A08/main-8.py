from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import csv

description = """🚀
## Santos
### Where awesomeness happens
"""

app = FastAPI(

    description=description,

)

db = []

# Open the CSV file
# populates the `db` list with all the csv data
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    i = 0
    # Read each row in the CSV file
    for row in reader:
        if i == 0:
            i += 1
            continue
        db.append(row)


def getUniqueCountries():
    global db
    countries = {}

    for row in db:
        print(row)
        if not row[2] in countries:
            countries[row[2]] = 0

    return list(countries.keys())


def getUniqueWhos():
    global db
    whos = {}

    for row in db:
        print(row)
        if not row[3] in whos:
            whos[row[3]] = 0

    return list(whos.keys())


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/countries/")
async def countries():
    return {"countries": getUniqueCountries()}


@app.get("/whos/")
async def whos():
    return {"whos": getUniqueWhos()}


@app.get("/casesByRegion/")
async def casesByRegion(year: int = None):
    """
    Returns the number of cases by region

    """

    # create a dictionary as a container for our results
    # that will hold unique regions. Why, because there 
    # cannot be duplicate keys in a dictionary.
    cases = {}

    # return {'success':False,'message':'no database exists'}

    # loop through our db list
    for row in db:

        # If there is a year passed in and that year is not equal to this row
        # then skip the rest of code
        if year != None and year != int(row[0][:4]):
            continue

        # this line guarantees that the dictionary has the region as a key
        if not row[3] in cases:
            cases[row[3]] = 0

        # this line adds the case count to whatever is at that key location
        cases[row[3]] += int(row[4])

        # return cases

    return {"data": cases, "success": True, "message": "Cases by Region", "size": len(cases), "year": year}


my_list = ['apple', 'banana', 'cherry', 'date', 'elderberry']


@app.get("/get_values1/")
def get_values1(index1: int = None, index2: int = None):
    try:
        value1 = my_list[index1]
        value2 = my_list[index2]
        return [value1, value2]
    except IndexError:
        return {"error": "Invalid index provided."}


@app.get("/get_values2/{index1}/{index2}")
def get_values2(index1: int, index2: int):
    try:
        value1 = my_list[index1]
        value2 = my_list[index2]
        return [value1, value2]
    except IndexError:
        return {"error": "Invalid index provided."}


@app.get("/deaths/")
async def deaths(country: str = None, year: int = None):
    """
    This method will return a total death count or can be filtered by country and year.
    - **Params:**
      - country (str) : A country name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/deaths/](http://localhost:8080/deaths/)

    #### Response 1:

        {
            "total": 1000000,
            "params": {
                "country": null,
                "year": null
            }
            "success": true,
        }

    #### Example 2:

    [http://localhost:8080/deaths/?country=Brazil&year=2023](http://localhost:8080/deaths/?country=Brazil&year=2023)

    #### Response 2:

        {
            "total": 42,
            "params": {
                "country": "Brazil",
                "year": 2023
            }
            "success": true,
        }

    """
    total_deaths = 0

    for row in db:
        if country is not None and row[2] != country:
            continue
        if year is not None and int(row[0][:4]) != year:
            continue
        total_deaths += int(row[6])

    response = {
        "total": total_deaths,
        "params": {
            "country": country,
            "year": year
        },
        "success": True
    }

    return response


@app.get("/deaths/{region}/{year}")
async def region_deaths(region: str, year: int = None):
    """
    This method will return a regions death count or can be filtered by region and year.
    - **Params:**
      - region (str) : A region name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters

    #### Example 1:

    [http://localhost:8080/deaths/EMRO/2020](http://localhost:8080/deaths/)

    #### Response 1:

        {
            "total": 1000000,
            "params": {
                "region": EMRO,
                "year": 2020
            }
            "success": true,
        }

    #### Example 2:

    [http://localhost:8080/deaths/region/]

    #### Response 2:

        {
            "total": 42,
            "params": {
                "region": "EMRO",
                "year": NULL
            }
            "success": true,
        }

    """
    total_deaths = 0

    for row in db:
        if region is not None and row[3] != region:
            continue
        if year is not None and int(row[0][:4]) != year:
            continue
        total_deaths += int(row[6])

    response = {
        "total": total_deaths,
        "params": {
            "country": region,
            "year": year
        },
        "success": True
    }

    return response


@app.get("/cases/")
async def cases(country: str = None, year: int = None):
    """
    This method will return a total death count or can be filtered by country and year.
    - **Params:**
      - country (str) : A country name
      - year (int) : A 4 digit year
    - **Returns:**
      - (int) : The total sum based on filters (if any)

    #### Example 1:

    [http://localhost:8080/cases/](http://localhost:8080/cases/)

    #### Response 1:

        {
            "total": 1000000,
            "params": {
                "country": null,
                "year": null
            }
            "success": true,
        }

    #### Example 2:

    [http://localhost:8080/deaths/?country=Brazil&year=2023](http://localhost:8080/deaths/?country=Brazil&year=2023)

    #### Response 2:

        {
            "total": ,
            "params": {
                "country": "Brazil",
                "year": 2023
            }
            "success": true,
        }

    """
    total_cases = 0

    for row in db:
        if country is not None and row[2] != country:
            continue
        if year is not None and int(row[0][:4]) != year:
            continue
        total_cases += int(row[5])

    response = {
        "total": total_cases,
        "params": {
            "country": country,
            "year": year
        },
        "success": True
    }

    return response

@app.get("/max_deaths/")
async def max_deaths():
    """"
    this method will return the country with the most amount of deaths and its number of deaths
    - ** Params: **
    - country(str): a country name

    - year(int): A
    4
    digit
    year


- ** Returns: **
- (int): The biggest sum and the country that has it


#### Example 1:

[http: // localhost: 8080 / max_deaths)

#### Response 1:

{
    "total": 1000000,
    "params": {
        "country": Brazil,
        "year": 2020
    }
    "success": true,
}




"""
    country_deaths = {}

    for row in db:
        country = row[2]
        deaths = int(row[6])

    if country in country_deaths:
        country_deaths[country] += deaths
    else:
        country_deaths[country] = deaths

# Find the country with the most deaths
    country_max = max(country_deaths, key=country_deaths.get)
    total_deaths = country_deaths[country_max]

    response = {
    "country": country_max,
    "total_deaths": total_deaths
}

    return response


@app.get("/min_deaths/")
async def min_deaths():
    """"
    this method will return the country with the least amount of deaths and its number of deaths
    - ** Params: **
    - country(str): a country name

    - year(int): A
    4
    digit
    year


- ** Returns: **
- (int): The lowest sum and the country that has it


#### Example 1:

[http: // localhost: 8080 / min_deaths)

#### Response 1:

{
    "total": 100,
    "params": {
        "country": France,
        "year": 2022
    }
    "success": true,
}




"""
    country_deaths = {}

    for row in db:
        country = row[2]
        deaths = int(row[6])
    #find the a,ount of deaths for each country
    if country in country_deaths:
        country_deaths[country] += deaths
    else:
        country_deaths[country] = deaths

    # Find the country with the least amount of deaths and store it in country_min
    country_min = min(country_deaths, key=country_deaths.get)
    total_deaths = country_deaths[country_min]

    response = {
        "country": country_min,
        "total_deaths": total_deaths
    }

    return response

@app.get("/avg_deaths/")
async def avg_deaths():
    """"
    this method will return the country with the least amount of deaths and its number of deaths
    - ** Params: **
    - country(str): a country name

    - year(int): A
    4
    digit
    year


- ** Returns: **
- (int): The average deaths between all countries


#### Example 1:

[http: // localhost: 8080 / avg_deaths)

#### Response 1:

{
    "average": 10000000

}




"""
    country_deaths = {}
    total_deaths = 0
    countries = 0

    for row in db:
        country = row[2]
        deaths = int(row[6])

        if country in country_deaths:
            country_deaths[country] += deaths
        else:
            country_deaths[country] = deaths

    for deaths in country_deaths.values():
        total_deaths += deaths
        countries += 1

    average_deaths = total_deaths / countries

    return average_deaths


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="debug", reload=True)  # host="127.0.0.1"