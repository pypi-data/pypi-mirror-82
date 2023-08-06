# PynamoLogger
> log information into a dynamodb, with dax support


## Install

`pip install pynamologger`<br>
# view [Documentation](https://thanakijwanavit.github.io/pynamoLogger/)

# Usage

## class meta definition

```
from pynamoLogger.logger import PynamoLogger
class Logger(PynamoLogger):
  class Meta:
    table_name = 'member-database-log-dev-manual'
    region = 'ap-southeast-1'
    billing_mode = 'PAY_PER_REQUEST'
    
```

```
# Logger.create_table()
```

```
Logger.log(appName = 'test', message = "this is crazy", responseObject = {'response': 'null response'})
```




    {'logId': 1603075789.054751,
     'saveResult': {'ConsumedCapacity': {'CapacityUnits': 1.0,
       'TableName': 'member-database-log-dev-manual'}}}



```
Logger.checkLog(appName = 'test', logId = '1603074235.103042')
```




    [{'appName': None,
      'timestamp': 1603074235.103042,
      'logMessage': 'this is crazy',
      'requestObject': {'noValue': 'noValue'},
      'responseObject': {'response': 'null response'}}]


