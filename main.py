import inspect

from tabulate import tabulate
from handlers.api_handler import APIHandler


class AlphavantageMain:
    end_constant = '\033[0m'
    bold_constant = '\033[1m'
    api_handler = None

    def display_data(self, display_type, company_details):
        """
        Display data by a given display_type retrieved from API

        :param display_type: indicates what to display for a given company
        :param company_details: details information about a company
        """
        mapping_type = {
            '1': 'ADDITIONAL',
            '2': 'TIME_SERIES',
            '3': 'QUOTE',
            '4': 'INDICATORS'
        }

        if mapping_type[str(display_type)] == 'ADDITIONAL':
            print(tabulate([company_details.values()],
                           headers=company_details.keys(),
                           tablefmt='psql'))
        elif mapping_type[str(display_type)] == 'TIME_SERIES':
            functions = ['TIME_SERIES_WEEKLY', 'TIME_SERIES_MONTHLY']
            data_list = self.api_handler.get_time_series_by_symbol(
                company_details['symbol'], functions)

            for data in data_list:
                print(f"===== {data['title']} =====")
                print(tabulate(data['table'],
                               headers=data['columns'],
                               tablefmt='psql'))
        elif mapping_type[str(display_type)] == 'QUOTE':
            func = 'GLOBAL_QUOTE'
            quote_data = self.api_handler.get_quote_by_symbol(
                company_details['symbol'], func)
            print(tabulate([quote_data.values()],
                           headers=quote_data.keys(),
                           tablefmt='psql'))
        else:
            functions = ['SMA', 'EMA']
            indicators_list = self.api_handler.get_technical_indicators_by_symbol(
                company_details['symbol'], functions)

            for data in indicators_list:
                print(f"===== {data['title']} =====")
                print(tabulate(data['table'],
                               headers=data['columns'],
                               tablefmt='psql'))

    def start_search(self, api_key):
        """
        Search for some specific symbols or companies and display the data
        of a chosen company

        :param api_key: the free api key to be remembered for the session
        :return: boolean value
        """
        keyword_comment = '<-> Please input a keyword to search for: '
        company_comment = '<--> Please input a number to select a company: '
        details_comment = '<--> Please input a display option for the company: [\033[s ]\033[u'
        details_quote = inspect.cleandoc('''
            1. Display additional details
            2. Display historical prices on specific timeframes
            3. Display current quote
            4. Indicator results for the company
            5. Exit
            ''')

        self.api_handler = APIHandler(api_key)

        while True:
            try:
                keyword = input(f'{self.bold_constant}'
                                f'{keyword_comment}'
                                f'{self.end_constant}')

                if not keyword:
                    # Exit if nothing is entered.
                    break
                details_list = self.api_handler.get_details_by_keyword(keyword)

                if not details_list:
                    print('Can not find matching companies with the keyword. '
                          'Please input another keyword.')
                    continue

                for idx, item in enumerate(details_list):
                    print(f"{idx + 1}. {item['symbol']}\t{item['name']}")

                select_num = -1

                while True:
                    company_option = input(f'{self.bold_constant}'
                                           f'{company_comment}'
                                           f'{self.end_constant}')

                    try:
                        company_option = int(company_option)

                        if company_option not in range(1, len(details_list) + 1):
                            print('The section number is out of range')
                            continue
                        select_num = company_option - 1
                        break
                    except:
                        if company_option == 'x':
                            break
                        print('Please input a number. Or, '
                              'if you wanna exit, please enter "x"')

                if select_num < 0:
                    continue

                print(details_quote)

                while True:
                    details_option = input(f'{self.bold_constant}'
                                           f'{details_comment}'
                                           f'{self.end_constant}')
                    try:
                        details_option = int(details_option)

                        if details_option in range(1, 5):
                            self.display_data(details_option, details_list[select_num])
                        elif details_option == 5:
                            break
                        else:
                            print('Please input 1/2/3/4/5 to go forward!')
                    except:
                        print('Please only input a number!')
                        print(details_quote)
                        pass
            except Exception as error:
                # Retry when any error occurs
                pass

    def start(self):
        """
      This is the main method for a user to enter API key in the CMD line
      and search for a specific company.
      """
        api_key_comment = 'Please input an api key: '

        while True:
            api_key = input(f'{self.bold_constant}{api_key_comment}{self.end_constant}')

            if not api_key:
                print('API Key can not be empty! Thank you for your time!')
                break
            self.start_search(api_key)


if __name__ == '__main__':
    alphavantage = AlphavantageMain()
    alphavantage.start()
