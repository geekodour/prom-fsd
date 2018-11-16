import argparse
import json

"""
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

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

class promfsd:
    """ prom-fsd class """
    def __init__(self, filepath, pj, rtargets, rlabels):
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
            """ add the new shit """
            targets_obj = {}
            targets_obj['targets'] = self.pj['targets']
            targets_obj['labels'] = self.pj['labels']
            self.file_data.append(targets_obj)
            print self.file_data
            # write to disk
        else:
            """ modify old shit """
            print 'index is %s' % indexCheck
            # add the targets to the existing (merge) use set
            # merge the labels dicts
            # else add the new stuff

    def checkifjobexists(self):
        """ ugly! """
        job = self.pj['labels']['job']
        alljobs = [i['labels']['job'] for i in self.file_data]
        if job not in alljobs:
            return False
        return alljobs.index(job)

    def removetargets(self):
        pass

    def removelabels(self):
        pass

    def processfile(self):
        if not (self.rtargets or self.rlabels):
            print "this happened"
            self.addtargets()
        elif self.rtargets:
            print "remove targets happened"
            self.removetargets()
        elif self.rlabels:
            print "remove labels happened"
            self.removelabels()

if __name__ == '__main__':
    args = parser.parse_args()
    parsed_json = json.loads(args.jsoninput)
    rtargets = args.remove_targets
    rlabels = args.remove_labels
    validate_input(parsed_json, rtargets, rlabels)
    cli = promfsd(args.filepath, parsed_json, rtargets, rlabels)
    cli.processfile()
