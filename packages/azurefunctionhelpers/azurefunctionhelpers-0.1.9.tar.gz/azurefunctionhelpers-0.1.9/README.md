## Python helpers for Azure Functions

### Modules

#### observability
Wrapper for logging handler and event tracing

##### Functions
###### Log
 For use as a decorator at Azure Function entry point. 
Requires the setting of the environment variable ```OBSERVABILITY_SCHEME``` 


Currently only logging with the variable setting ```elastic_apm``` is supported which will require the additional environment variables
```ELASTIC_APM_SERVICE_NAME``` and ```ELASTIC_APM_SERVER_URL```
as defined in APM documentation https://www.elastic.co/guide/en/apm/agent/python/current/api.html

Example usage

```
import azure.functions as func
from azurefunctionhelpers import observability

@observability.log('transaction_category')
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Here is my message')
    raise Exception('Unhandled exceptions will log')
    
    return func.HttpResponse(
         "Ok",
         status_code=200
    )
```

