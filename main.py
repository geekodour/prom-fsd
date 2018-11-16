import argparse
import os
import json

"""
usage: (currently `$ python main.py` instread of prom-fsd)
$ prom-fsd ss.json targets=["gitlab0d.fsf.org"] labels={'job': 'mysql', 'category':'xyz'}
$ prom-fsd ss.json --remove-targets '["gitlab0d.fsf.org"]'
$ prom-fsd ss.json --remove-labels '{"job":"job1", "category":"cat2"}'
"""

"""
Argument parser
"""
parser = argparse.ArgumentParser(description='Prometheus file service discovery cli tool')

parser.add_argument('filepath', type=str, help='relative path to the file')
parser.add_argument('jsoninput', type=str, help='JSON string')
parser.add_argument('--remove-targets', action='store_true', help='if set, will remove the targets. if the last target will remove the labels too')
parser.add_argument('--remove-labels', action='store_true', help='if set, will remove the lablels from all the targets')


"""
Functions to check for data validity
"""
def validate_input(pj, rtargets, rlabels):
    if rtargets and rlabels:
        raise ValueError('only set one of --remove-* flags')
    elif not (rtargets or rlabels):
        if not set(pj.keys()) == set([u'targets',u'labels']):
            raise ValueError('json object should contain targets and labels fields only')
        if not (type(pj) is dict and type(pj['targets']) is list and type(pj['labels']) is dict):
            raise ValueError('check if json data is correctly formatted')
        if not 'job' in pj['labels']:
            raise ValueError('labels json object must contain job field')
    elif rtargets:
        if not type(pj) is list:
            raise ValueError('json object should be a list of targets to remove')
    elif rlabels:
        if not type(pj) is list:
            raise ValueError('json object should be a list of labels to remove')

"""
Utility functions
"""
def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

"""
prom-fsd class
"""
class promfsd:
    """ prom-fsd class """
    def __init__(self, filepath, pj, rtargets, rlabels):
        self.file_path = filepath
        self.file_data = self.getfiledata(filepath)
        self.pj = pj
        self.rtargets = rtargets
        self.rlabels = rlabels

    @staticmethod
    def getfiledata(filepath):
        with open(filepath) as f:
            return json.load(f)

    def addtargets(self):
        indexCheck = self.checkifjobexists()
        if indexCheck is False:
            """ add the new stuff """
            targets_obj = {}
            targets_obj['targets'] = self.pj['targets']
            targets_obj['labels'] = self.pj['labels']
            self.file_data.append(targets_obj)
            self.write_to_disk()
        else:
            """ modify old stuff """
            temp_obj = self.file_data[indexCheck]
            temp_obj['targets'] = list(set(temp_obj['targets']+self.pj['targets']))
            temp_obj['labels'] = merge_dicts(temp_obj['labels'],self.pj['labels'])
            self.file_data[indexCheck] = temp_obj
            self.write_to_disk()

    def checkifjobexists(self):
        """ ugly! return False if not found, index if found """
        job = self.pj['labels']['job']
        alljobs = [i['labels']['job'] for i in self.file_data]
        if job not in alljobs:
            return False
        return alljobs.index(job)

    def removetargets(self):
        # scan through all of the targets in each target object, if target matches, remove target
        for target in self.pj:
            for target_obj in self.file_data:
                if target in target_obj['targets']:
                    target_obj['targets'].remove(target)
        self.write_to_disk()

    def removelabels(self):
        # scan through all of the labels keys in each target object, if label found, remove label
        for label in self.pj:
            for target_obj in self.file_data:
                if label in target_obj['labels'].keys():
                    target_obj['labels'].pop(label, None)
        self.write_to_disk()

    def processfile(self):
        if not (self.rtargets or self.rlabels):
            self.addtargets()
        elif self.rtargets:
            self.removetargets()
        elif self.rlabels:
            self.removelabels()

    def write_to_disk(self):
        with open('%s.new' % self.file_path , 'w') as f:
            json.dump(self.file_data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        os.rename('%s.new' % self.file_path, self.file_path)

if __name__ == '__main__':
    args = parser.parse_args()
    parsed_json = json.loads(args.jsoninput)
    rtargets = args.remove_targets
    rlabels = args.remove_labels
    validate_input(parsed_json, rtargets, rlabels)
    cli = promfsd(args.filepath, parsed_json, rtargets, rlabels)
    cli.processfile()
