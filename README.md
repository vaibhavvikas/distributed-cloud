# DistributedCloud
Cloud Storage Object with End to End Encryption

Design and Implement a distributed cloud storage.
Similar to Google drive, where user can store and retrieve any Objects.

## Basic Functionalities: ##
* One Web Server
* REST API
* Config File
  ```
  {
    
    "storage_directory":"\home\<username>\uploads",
    "node_count":4,
    "size_per_slice":1024,
    "redundancy_count":1,
    "peers":[
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5001",
        "http://127.0.0.1-lt:5002",
        "http://127.0.0.1-lt:5003"
    ]
  }
  ```
 ### Methods ###
 * #### PUT ####
    * Store an incoming file and return the ID of the resource
    * PUT: http://localhost:5000/files
 * #### GET ####
    * Download the file for a given <ID>
    * GET: http://localhost:5000/files/{id}
 * #### LIST ####
    * List the files stored in the server
    * GET: http://localhost:5000/files/list
 * #### DELETE ####
    * Delete the file for a given <ID>
    * DELETE: http://localhost:5000/files/{id}



How to run:

```
$ python3 main.py
```

After that go to POSTMAN and execute the commands


## MILESTONES ##

### MILESTONE 1 (Completed) ###
Goal: Basic API Implementation
* Ability to Upload a file to the server
* Download the file
* List all the files on the server
* Delete a file

### MILESTONE 2 (Completed) ###
Goal: Encryption + Load Balancing
* Uploaded file must be broken down in to chunks as mentioned on the config
* Nodes ( folders ) must be created as per the node count on config
* Nodes must be named as node_<number> Eg. node_1
* File chunks must be moved to the nodes with API Server uploads load balancing. Node with the least number of files must be filled first
* Metadata file(s) must be created to save information on the file chunks and their location
  
### MILESTONE 3 (In Progress)  ###
Goal: Rendundancy: Files must be accessed even if one or more node goes down.
* When one or more nodes go down, the file must still be retrievable
* Redundancy_count = 1 value in config means, file must be retrievable when 1 node goes down.
* Redundancy level must increase as per the value specified on the config
