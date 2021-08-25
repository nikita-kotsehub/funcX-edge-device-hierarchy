Refer to [funcx-endpoint][1] documentation for setting up your endpoint. 

Alternatively, this snippet of code should set up an endpoint named `my_endpoint` on your machine:
```
$ python3 -m pip install funcx_endpoint

$ funcx-endpoint configure my_endpoint

$ funcx-endpoint start my_endpoint
```

The `facial_CNN_funcx_registratrion.py` registers the funcX function that runs facial prediction. Other files already use this function (`face_uuid`), so no need to run it and get another UUID. However, if you wish to modify the function, then you can make changes in this file and get a new funcX UUID.

[1]: https://funcx.readthedocs.io/en/latest/endpoints.html
