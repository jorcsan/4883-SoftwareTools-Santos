## A08 - Fast Api with Covid Data
### Jorge Santos
### Description:

This code will create an API with multiple routes. This API has access to a csv file containing data on covid cases and deaths. 
These routes can be used to find the amount of deaths, or cases a country has. 
The country with the most or least deahts and more.


### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | [data.csv]()| csv file containin covid data     |
|   2   |  [main.py]() | python code to generate dot code    |



### instructions

make sure to install uvicorn and fastapi.
uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="debug", reload=True)  # host="127.0.0.1"
have a line similair to the one above in main
Once you run the program, click the link that will take you to the api.
There you can click on the routes and than click on the "try it out"  button for each one

### routes and comments

@app.get("/deaths/")
async def deaths(country:str = None,year:int = None):
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


    @app.get("/deaths/{region}/{year}")
async def region_deaths(region: str ,year:int = None):
    """
    This method will return a regions death count or can be filtered by region and year.
    - **Params:**
      - country (str) : A region name
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


    @app.get("/cases/")
async def cases(country:str = None,year:int = None):
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

    @app.get("/max_deaths/")
async def max_deaths():
    """
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
