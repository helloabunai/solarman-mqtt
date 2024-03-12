import json
from pydantic import BaseModel
import hashlib
import subprocess


class State(BaseModel):
    """
    My setup has two circuits of panels, DC1+2
    """
    inverter_power: int  # watts
    dc1_power: int # watts
    dc2_power: int # watts
    battery_soc: int  # percentage
    battery_power: int  # watts

class SolarmanAPI:
    login_request_url = ''
    data_request_url = ''
    request_type = "application/json"
    appid: str
    appsecret: str
    username: str
    password: str
    inverter: str
    access_token: str = None
    token_type: str = None
    refresh_token: str = None

    def __init__(self, appid: str, appsecret: str, username: str, password: str, inverter: str):
        self.appid = appid
        self.appsecret = appsecret
        self.username = username
        self.password = password
        self.inverter = inverter
        self.login_request_url = "https://globalapi.solarmanpv.com/account/v1.0/token?appId={}&language=en&=".format(self.appid)
        self.data_request_url = "https://globalapi.solarmanpv.com/device/v1.0/currentData?appId={}&language=en&=".format(self.appid)

    def login(self):
        """
        Get access token with app ID/secret credentials from API
        Example:
        curl --request POST \
            --url 'https://globalapi.solarmanpv.com/account/v1.0/token?appId=XXXXX&language=en&=' \
            --header 'Content-Type: application/json' \
            --data '{
	            "appSecret": "",
	            "email": "",
	            "password": ""
        }'
        """

        print("Attempting to get Solarman API access token with provided credentials")
        data = {
            "appSecret": self.appsecret,
            "email": self.username,
            "password": hashlib.sha256(self.password.encode()).hexdigest()
        }
        api_response = subprocess.check_output([
            'curl', '-s', '--request', 'POST',
            '--url', self.login_request_url,
            '--header', 'Content-Type: application/json',
            '--data', json.dumps(data)
            ])
        parsed_response = json.loads(api_response.decode('utf-8'))

        if parsed_response['success'] == True:
            print("Granted access token for Solarman API")
            self.access_token = parsed_response.get("access_token", "")
            self.refresh_token = parsed_response.get("refresh_token", "")
        else:
            print("Failed to get access token")
            print(json.dumps(api_response.json()))

    def get_state(self) -> State:
        """
        Use granted API access token in order to get current state of solar inverter
        Example:
        curl --request POST \
            --url 'https://globalapi.solarmanpv.com/device/v1.0/currentData?appId=XXXXXXX&language=en&=' \
            --header 'Authorization: bearer XXXXX' \
            --header 'Content-Type: application/json' \
            --data '{
                "deviceSn": "XXXXXX"
            }'
        """

        if not self.access_token:
            self.login()

        print("Attempting to get inverter data with granted Solarman API access tokens")
        data_response = None
        ## Grab data from API
        if self.access_token:
            data = {
                "deviceSn": self.inverter
            }
            api_response = subprocess.check_output([
                'curl', '-s', '--request', 'POST',
                '--url', self.data_request_url,
                '--header', 'Content-Type: application/json',
                '--header', 'Authorization: bearer {}'.format(self.access_token),
                '--data', json.dumps(data)
            ])

            parsed_response = json.loads(api_response.decode('utf-8'))
            if parsed_response['success'] == True:
                print("Acquired data from Solarman API")
                data_response = parsed_response['dataList']
            else:
                print("Failed to retrieve Solarman data")
        else:
            print("No access token. Attempt cancelled.")


        ## Pull out information we want from the response
        print("Attempting to parse API response...")

        ## DC1 Power: DP1
        ## DC2 Power: DP2
        ## Total AC Output: T_AC_OP
        desired_keys = ['PG_Pt1', 'DP1', 'DP2', 'T_AC_OP']
        circuit_one = [d for d in data_response if d['key'] == 'DP1']
        circuit_two = [d for d in data_response if d['key'] == 'DP2']
        total_power = [d for d in data_response if d['key'] == 'T_AC_OP']

        state = State(
            inverter_power=total_power['value'],
            dc1_power=circuit_one['value'],
            dc2_power=circuit_two['value'],
            battery_power=100,
            battery_soc=100, # i don't have batteries and there was no battery info in the API
        )
        return state