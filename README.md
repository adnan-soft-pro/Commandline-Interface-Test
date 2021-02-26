# Commandline-Interface-Test-App
This app is to check the python programming skill as well as experience with managing APIs

# Installation & Run
- Make sure you set up Python3 on your system (note: I assumed that your OS is a Linux OS)
- Clone this app from the github: [app](https://github.com/adnan-soft-pro/Commandline-Interface-Test)
- Create a virtualenv and activate it like so (only one time):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary packages in the requirements.txt
    ```bash
    pip install -r requirements.txt
    ```
- Run this app like so:
    ```bash
    python main.py
    ```
# How does this app work?
- When you run the script, you can see the output in the terminal like so:
![first_screen](./screenshots/first_screen.png)
- After you entering the api key, you are asked to enter a keyword to search for matching symbols through API
![second_screen](./screenshots/second_screen.png)
- Once you enter a keyword and press Enter in the terminal, you can see a list of symbols with company names and are asked to select a company:
![third_screen](./screenshots/third_screen.png)
- There, you input an id of a company and press Enter. Then, you are asked to input another selection number to display different data for a chosen company:
![forth_screen](./screenshots/forth_screen.png)
- Finally, you can see different data for a chosen company by entering different options in the terminal:
![fifth_screen](./screenshots/fifth_screen.png)
![fifth_screen_1](./screenshots/fifth_screen_1.png)
![fifth_screen_2](./screenshots/fifth_screen_2.png)
![fifth_screen_3](./screenshots/fifth_screen_3.png)
![sixth_screen](./screenshots/sixth_screen.png)
![seventh_screen](./screenshots/seventh_screen.png)
![seventh_screen_1](./screenshots/seventh_screen_1.png)
![seventh_screen_2](./screenshots/seventh_screen_2.png)
- Additionally, if you enter nothing for a keyword and an api key, you will get out from the app like so:
![eighth_screen](./screenshots/eighth_screen.png)
