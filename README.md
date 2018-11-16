# promfilesd-cli
Add and remove targets and labels to file_sd file for your prometheus configuration directly from the cli

- Should be written in python2 to run by ansible

Content of `./sample_targets.json`
```json
[
    {
        "labels": {
            "datacenter": "east", 
            "job": "mysql"
        }, 
        "targets": [
            "10.11.150.1:7870", 
            "10.11.150.4:7870"
        ]
    }, 
    {
        "labels": {
            "job": "postgres"
        }, 
        "targets": [
            "10.11.122.11:6001", 
            "10.11.122.15:6002"
        ]
    }, 
    {
        "labels": {
            "job": "node_exporter"
        }, 
        "targets": ["somehostname"]
    }
]
```
### Usage
Add a **new target** with a **new job**:
```
$ python main.py sample_targets.json '{"targets":["gitlab42d.fsf.org"], "labels": {"job": "exim", "category":"mail"}}'
```

Add a **new target** to an **existing job**: (eg. for the `postgres` job)
```
$ python main.py sample_targets.json '{"targets":["newhost.fsf.org"], "labels": {"job": "postgres", "category":"database"}}'
```

Remove a target
```
$ python main.py sample_targets.json --remove-targets '["gitlab0d.fsf.org"]'
```

Remove a label from the whole file(all occurences will be removed
```
$ python main.py sample_targets.json --remove-labels '["node_exporter"]'
```
