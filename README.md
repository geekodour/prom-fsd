# promfilesd-cli
Add and remove targets and labels to file_sd file for your prometheus configuration directly from the cli

```
$ promfilesd-cli file=~/ss.json targets=["gitlab0d.fsf.org"] labels={'job': 'mysql', 'category':'xyz'}
$ promfilesd-cli --remove-targets file=~/ss.json targets=["gitlab0d.fsf.org"]
$ promfilesd-cli --remove-labels file=~/ss.json labels=['job','category']
```

If you want to mass add remove files you must do it separately for targents and labels

- for merging the labels, merge like object.assign in js

--
Steps for adding targets:
- job label is mandatory for all label objects, if job label not found throw error
- filter out targets that are already present and remove them from processing
    - already present --> A
        - merge labels for all the targets
    - remaining --> B
        - add the target object
            - add targets array and put in all the targets list
            - add labels object
    - if no targets arg is present at all, merge label with all the targets
--
Steps for removing targets
-

**TODO**
```
$ promfilesd-cli file=~/ss.json mergefile=~/mm.json
$ promfilesd-cli file=~/ss.json mergefile=~/mm.json
```
