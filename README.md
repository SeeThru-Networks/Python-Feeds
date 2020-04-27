# Python-Feed
A monitoring framework to report the status of anything to users of the SeeThru Networks platform.

# Code Map

## Library/
The library stores all of the components and services that you have. To acces these components and services in your executor script, you must import using the directory tree, e.g. `import Library.Components.HTTP.HTTPBase`.  
### - Components/
Any routines you find yourself using often in your services should be abstracted out to a component, this will simplify your codebase, moving common components into the components tree. These components can be imported in your services by using `from Library.Components.YourComponent.YourComponent import ComponentName`.  
All components should be implemented as a class which inherits from the ComponentBase in Model, this component base can be imported with `from Model.ComponentBase import ComponentBase`. 
This component class should override the `run` function in componentBase, this is the way in which your component should run its functionality.  
#### -- YourComponent/
###### --- YourComponent.py
#### -- HTTP/
###### --- HTTPBase.py
###### --- HTTPGet.py
###### --- HTTPPost.py
#### -- SNMP/
###### --- SNMP.py
#### -- Sockets/
###### -- Socket.py
### - Services/
A service is the script that executes your test. Each independent test should be implemented as a separate service.  
Each service that you create should be implemented as a class which inherits from the serviceBase in model, this service base can be imported with: `from Model.ServiceBase import ServiceBase `.  
This service should override the `run`, `evaluate` and `__init__` functions. The service should be executed using the `run` function, this function should call `evaluate` to determine the status and message of the test, the status should be stored in `self.status` and must be `red`, `amber` or `green`, the message should be stored in `self.message` and can be a maximum of 256 characters.  
The initialiser `__init__` can take as many arguments as you would like however the last argument **must** be `**kwargs`, this will stores any extra arguments passed into the initialiser of the service. The first line of the initialiser **must** also be `super().__init__("Service_Name", **kwargs)`, this will initialise the super class (serviceBase) of the service, the first argument **must** be your services name and the second argument **must** be `**kwargs` passed into the initialiser of the service. Overall the initialiser will pass any extra arguments that it recieves to the super class to deal with.  
An example of this is `output='path_to_output'`, when this is passed into the initialiser of the service, the output path of the service is set to that path which means that upon calling `service_instance.export()`, the service result will be output as json to the file defined.  
`service_instance.dump()` will print the status and message of the service to the terminal.  
`service_instance.get_result()` will return a string containing the json of the service in the format `{"color:"", message:"", time:"""}`.  
`service_instance.export()` will export the service result to the file path defined in the `output` argument in the service initialiser.  
#### -- YourService/
###### --- Service.py
#### -- Accedian/
###### -- AccedianCCAlert.py
#### -- Generic/
###### -- GenericHangouts.py
###### -- GenericTeams.py
###### -- GenericZoom.py
#### -- Zabbix
###### -- ZabbixService.py
## Model/
### - ComponentBase.py
### - ServiceBase.py
## executor.py
This is a file that you can execute your services from, it must be at the top level in the directory tree.  
