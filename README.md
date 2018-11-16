# promfilesd-cli
Add and remove targets and labels to file_sd file for your prometheus configuration directly from the cli

- Should be written in python2 to run by ansible

```
usage: (currently `$ python main.py` instread of prom-fsd)
$ python main.py sample_targets.json targets=["gitlab0d.fsf.org"] labels={'job': 'mysql', 'category':'xyz'}
$ python main.py sample_targets.json --remove-targets '["gitlab0d.fsf.org"]'
$ python main.py sample_targets.json --remove-labels '{"job":"job1", "category":"cat2"}'
```
