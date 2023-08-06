<p align="left" >
<a href="https://github.com/RoberWare/wifiConf/graphs/contributors"><img src="https://img.shields.io/github/contributors/RoberWare/wifiConf" alt="Github contributors"/></a>
  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  
## Description
Google sheets API, easy to use

## Example of usage
```Python
from easy_googlesheets import GSheets

myGSheets = GSheets(secret_filename='credentials.json', 
                    spreadsheet_id='',
                    data_tab_name='Page 1',
                    control_id='user1')

# Example of filter output
filter_list=["lat>0", "lng<0"]
print(myGSheets.filter_by(filter_list))

# Example of insert row
myGSheets.insert({'name': '100 Montaditos ', 
                  'lat': float(37.3812499), 
                  'lng': float(-6.0085387), 
                  'url': 'https://spain.100montaditos.com/es/la-carta/', 
                  'vicinity': 'Calle San Jacinto, 89, 41010 Sevilla', 
                  'ref': 2999389465, 
                  'uploader': 'user1'})

#print(myGSheets.remove("ROWS",6,9))

# Always close at the end
myGSheets.close()
```
<img src="https://github.com/RoberWare/easy_googlesheets/blob/main/static/screenshot.png" alt="example01"/> 
