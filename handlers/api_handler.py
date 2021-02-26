import re
import asyncio
import aiohttp
import requests


class APIHandler:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_query_url = 'https://www.alphavantage.co/query'

    async def fetch_data(self, session, url):
        """
        Retrieve json data from a given url through API

        :param session: aiohttp Client session
        :param url: a url where to request data
        :return: a response data in json format
        """
        result = None

        while not result:
            try:
                async with session.get(url) as res:
                    res.raise_for_status()
                    result = await res.json()
            except aiohttp.ClientError as error:
                print(f'Exceed max requests, so sleep a little '
                      f'and try again for {url}')
                print(error)
                # sleep a little and try again
                await asyncio.sleep(2)

        return result

    async def check_and_fetch_all(self, urls, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            results = await asyncio.gather(
                *[self.fetch_data(session, url)
                  for url in urls],
                return_exceptions=True)
            return results

    @staticmethod
    def clean_dict(data_dict):
        """
        Optimize the key name of each item in a given data_dict

        :param data_dict: a dict data to optimize
        :return: an optimized dict data
        """
        return {
            re.sub(r'\d+.', '', j).strip(): v for j, v in data_dict.items()
        }

    def get_details_by_keyword(self, keyword):
        """
        Get a list of symbols with additional details based on the given
        keyword from alphavantage through API

        :param keyword: a symbol to find matching data
        :return: a list of symbols with additional details
        """
        api_url = f"{self.base_query_url}?function=SYMBOL_SEARCH" \
                  f"&keywords={keyword}&apikey={self.api_key}"
        response = requests.get(api_url)

        if not response.ok:
            print('Failed to get matching symbols through API.')
            return []

        matches = [self.clean_dict(i) for i in response.json()['bestMatches']]

        return matches

    def get_time_series_by_symbol(self, symbol, functions):
        """
        Get time series of given functions through API

        :param symbol: a symbol name literally
        :param functions: a list of functions. e.x. TIME_SERIES_MONTHLY
        """
        api_urls = []
        response_list = []

        for func in functions:
            if func == 'TIME_SERIES_INTRADAY':
                interval = '15min'
                url = f"{self.base_query_url}?" \
                      f"function={func}" \
                      f"&symbol={symbol}" \
                      f"&interval={interval}" \
                      f"&apikey={self.api_key}"
            else:
                url = f"{self.base_query_url}?" \
                      f"function={func}" \
                      f"&symbol={symbol}" \
                      f"&apikey={self.api_key}"
            api_urls.append(url)

        loop = asyncio.get_event_loop()
        response_list += loop.run_until_complete(
            self.check_and_fetch_all(api_urls, loop))

        result_list = []

        for response in response_list:
            result = {'title': [*response.keys()][-1]}
            table = [
                [i, *v.values()]
                for i, v in response[result['title']].items()
            ]
            result['table'] = table
            result['columns'] = ['datetime', 'open', 'high',
                                 'low', 'close', 'volume']
            result_list.append(result)

        return result_list

    def get_quote_by_symbol(self, symbol, func):
        """
        Get the current quote of a given symbol

        :param symbol: a symbol name literally
        :param func: the name of the function. e.x. GLOBAL_QUOTE
        """
        api_url = f"{self.base_query_url}?function={func}" \
                  f"&symbol={symbol}&apikey={self.api_key}"

        response = requests.get(api_url)

        if not response.ok:
            print('Failed to get the current quote of a symbol through API.')
            return []

        data = self.clean_dict(response.json()['Global Quote'])

        return data

    def get_technical_indicators_by_symbol(self,
                                           symbol,
                                           functions,
                                           interval='weekly',
                                           time_period='10',
                                           series_type='open'):
        """
        Get technical indicators of given functions through API

        :param symbol: a symbol name literally
        :param functions: a list of functions. e.x. EMA, SMA
        :param interval: time interval between two consecutive data points
                         in the time series
        :param time_period: number of data points used to
                            calculate each moving average value
        :param series_type: the desired price type in the time series
        """
        api_urls = []
        response_list = []

        for func in functions:
            url = f"{self.base_query_url}?" \
                  f"function={func}" \
                  f"&symbol={symbol}" \
                  f"&interval={interval}" \
                  f"&time_period={time_period}" \
                  f"&series_type={series_type}" \
                  f"&apikey={self.api_key}"
            api_urls.append(url)

        loop = asyncio.get_event_loop()
        response_list += loop.run_until_complete(
            self.check_and_fetch_all(api_urls, loop))

        result_list = []

        try:
            for response in response_list:
                result = {'title': [*response.keys()][-1]}
                table = [
                    [i, *v.values()]
                    for i, v in response[result['title']].items()
                ]
                result['table'] = table
                result['columns'] = ['datetime', result['title'].split(':')[-1].strip()]
                result_list.append(result)
        except Exception as error:
            # Pass this exception error for now because the error comes up
            # due to the limited number of requests.
            pass
        return result_list
