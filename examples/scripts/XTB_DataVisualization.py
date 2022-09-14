import logging
import datetime
import pandas as pd
from stockbee.external_lib.xAPIConnector import APIClient, loginCommand
from login_data import userId, password

# set to true on debug environment only
DEBUG = True

# logger properties
logger = logging.getLogger("jsonSocket")
FORMAT = '[%(asctime)-15s][%(funcName)s:%(lineno)d] %(message)s'
logging.basicConfig(format=FORMAT)

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.CRITICAL)

def main():
    # create & connect to RR socket
    client = APIClient()
    
    # connect to RR socket, login
    loginResponse = client.execute(loginCommand(userId=userId, password=password))
    logger.info(str(loginResponse)) 

    # check if user logged in correctly
    if(loginResponse['status'] == False):
        print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
        return

    # get ssId from login response
    ssid = loginResponse['streamSessionId']
    
    date_start = int(datetime.datetime(year=2020, month=1, day=1).timestamp() * 1000)
    date_end = int(datetime.datetime(year=2022, month=9, day=13).timestamp() * 1000)

    myCommand = {
        "command": "getChartRangeRequest",
        "arguments": {
            "info": {
                "end": date_end,
	            "period": 1440,
	            "start": date_start,
	            "symbol": "DE30",
	            "ticks": 0
	        }
        }
    }

    de_data = client.execute(myCommand)
    de_data_df = pd.DataFrame(de_data['returnData']['rateInfos'])
    de_data_df.to_excel('de_data.xlsx')
    # gracefully close RR socket
    client.disconnect()
    
if __name__ == "__main__":
    main()	