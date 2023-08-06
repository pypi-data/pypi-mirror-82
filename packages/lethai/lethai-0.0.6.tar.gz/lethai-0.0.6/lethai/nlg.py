import os
import webbrowser

import json
import requests


class config:
    def __init__(self, username, api_token):
        self.__username = username
        self.__headers = {
            'Content-Type': 'application/json',
            'Auth-Key': api_token,
            'Auth-username': self.__username
        }
        self.__dataset_api_url = 'https://api.lethical.ai/v1/discrimination/nlg/dataset'
        self.__detect_api_url = 'https://api.lethical.ai/v1/discrimination/nlg/detect-bias'
        self.__dataset = None

    def check_discrimination(self, generator, model_name):
        print(generator, model_name)
        print(json.dumps(self.__headers))
        # Gets the dataset from the backend if not already available in the frontend
        if self.__dataset is None:
            self.__dataset = self.__get_dataset(self.__dataset_api_url, self.__headers)
            if self.__dataset is None:
                return None

        # Generated predictions with their ML model's generator function
        results = config.__generate_output(generator, self.__dataset)

        # Now results has the generated text from the NLG model for various categories
        # We need to sync this output with the backend and process the biases (if any) in this model
        json_data = dict()
        if model_name:
            json_data['model_name'] = model_name
        json_data["data"] = results
        response = requests.post(self.__detect_api_url, headers=self.__headers, json=json_data)
        if response.status_code >= 500:
            print('[!] [{0}] Server Error'.format(response.status_code))
            return None
        elif response.status_code == 404:
            print('[!] [{0}] URL not found: [{1}]'.format(response.status_code, self.__detect_api_url))
            return None
        elif response.status_code == 401:
            print('[!] [{0}] Authentication Failed'.format(response.status_code))
            return None
        elif response.status_code >= 400:
            print('[!] [{0}] Bad Request'.format(response.status_code))
            print(response.content)
            return None
        elif response.status_code >= 300:
            print('[!] [{0}] Unexpected redirect.'.format(response.status_code))
            return None
        elif response.status_code != 200:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
            return None
        bias_results = json.loads(response.content)
        if bias_results['success']:
            config.__open_browser(bias_results["result"])
        else:
            print(bias_results["message"])

    @staticmethod
    def __open_browser(results):
        # Update the json file which is used by the html file
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'public', 'nlg_json.js'), mode='w') as f:
            f.write('var data = {}'.format(json.dumps(results, indent=2)))

        # Change path to reflect file location
        html_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'public', 'nlg.html')
        webbrowser.open_new_tab(html_file_path)

    @staticmethod
    def __get_dataset(url, headers):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()["result"]
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None

    @staticmethod
    def __generate_output(generator, categories):
        # Create an empty dictionary and fill it in the required format
        data = dict()
        for category in categories:
            data[category] = {}
            for datapoint in categories[category]:
                data[category][datapoint] = {}
                for text in categories[category][datapoint]:
                    data[category][datapoint][text] = []
                    for i in range(1):
                        data[category][datapoint][text].append(generator(text))

        return data
