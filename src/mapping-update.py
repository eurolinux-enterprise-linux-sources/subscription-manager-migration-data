#!/usr/bin/python

import os
import sys
import re
import glob

def error(msg):
    sys.stderr.write(msg)
    sys.stderr.write("\n")

def fatal_error(msg):
    error(msg)
    sys.exit(-1)

class MappingUpdater(object):
    def __init__(self, mapping_path, cert_path):
        self._mapping_path = mapping_path
        self._cert_path = cert_path

    def update_mapping(self):
        old_mapping_file = os.path.join(self._mapping_path, \
                "channel-cert-mapping.txt")
        f = open(old_mapping_file)

        new_mapping_file = os.path.join(self._mapping_path, \
                "channel-cert-mapping.new")
        out = open(new_mapping_file, "w")

        lines = f.readlines()
        for line in lines:
            if re.match("^[a-zA-Z]", line):
                line = line.replace("\n", "")
                key, val = line.split(": ")
                if val == "none":
                    out.write("%s: %s\n" % (key, val))
                else:
                    # This will, of course, break horribly if there isn't
                    # a one to one mapping between the old certs and the new.
                    # The only thing that can change is the hash value after
                    # the cert name.  E.g. 
                    # Client-Client-x86_64-efe91c1c-78d7-4d19-b2fb-3c88cfc2da35-68.pem
                    # changed to Client-Client-x86_64-6587edcf1c03-68.pem 
                    prefix = re.match("(\w+-\w+-\w+-)", val)
                    paths = glob.glob(
                            os.path.join(self._cert_path, prefix.group(1)) + \
                            "*.pem")
                    out.write("%s: %s\n" % (key, os.path.basename(paths[0])))

def main():
    if len(sys.argv) != 3:
        fatal_error("Usage: %s <directory with mapping file> <directory with new certs>" \
                % sys.argv[0])

    updater = MappingUpdater(sys.argv[1], sys.argv[2])
    updater.update_mapping()

if __name__ == "__main__":
    main()
