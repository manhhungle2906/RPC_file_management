To run the script, install these three dependencies grpcio, grpcio-tools, and protobuf by command: <br>
`$ py -m pip install grpcio grpcio-tools protobuf ` <br>
(Make sure py and pip is available on your local machine)<br>

First run the file `auth_service.py` file to start the server:<br>
`$ py .\{path_to_your_code}\auth_service.py`<br>
Run the `file_storage_service.py` file will create a test.txt in folder file_storage.
Run the `client.py` file to upload the previous created test.txt file to the server.

