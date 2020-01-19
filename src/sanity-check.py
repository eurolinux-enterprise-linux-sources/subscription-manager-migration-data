#!/usr/bin/python

import os
import re
import sys
import glob


def error(msg):
    sys.stderr.write(msg)
    sys.stderr.write("\n")


def fatal_error(msg):
    error(msg)
    sys.exit(-1)


class MappingValidator(object):
    def __init__(self, path):
        self._path = path
        self._mapping = {}
        self._dupes = set()
        self.successful = True

    def load_mapping(self):
        mapping_file = os.path.join(self._path, "channel-cert-mapping.txt")

        # copypasta'd from rhn-migrate-classic-to-rhsm. here's hoping it won't
        # change!
        f = open(mapping_file)
        lines = f.readlines()
        for line in lines:
            if re.match("^[a-zA-Z]", line):
                line = line.replace("\n", "")
                key, val = line.split(": ")
                if key not in self._mapping.keys():
                    self._mapping[key] = val
                else:
                    self._dupes.add(key)

    def check_for_dupes(self):
        for dupe in self._dupes:
            error("Duplicate channel mapping found: %s" % dupe)
            self.successful = False

    def filter_out_none_mappings(self):
        # remove any channels that map to none from further tests.
        # NB: the value must be _EXACTLY_ "none" to be filtered,
        # just as the migrate script does.
        for key in self._mapping.keys():
            if self._mapping[key] == "none":
                del self._mapping[key]

    def check_for_valid_pem_files(self):
        for key, val in self._mapping.items():
            pem_path = os.path.join(self._path, val)
            if not os.path.exists(pem_path):
                error('Missing pem file: "%s: %s"' % (key, val))
                self.successful = False
            else:
                f = open(pem_path, 'r')
                line = f.readline()
                if not line.startswith("-----BEGIN CERTIFICATE-----"):
                    error('Does not appear to be a PEM file: "%s: %s"'
                            % (key, val))
                    self.successful = False

    def check_for_extra_pem_files(self):
        pem_files = glob.glob(os.path.join(self._path, "*.pem"))
        pem_files = map(os.path.basename, pem_files)
        for pem_file in pem_files:
            if not pem_file in self._mapping.values():
                error("%s is unused." % pem_file)
                self.successful = False


def main():
    if len(sys.argv) == 1:
        fatal_error("Please provide a directory to validate")

    validator = MappingValidator(sys.argv[1])

    validator.load_mapping()
    validator.check_for_dupes()
    validator.filter_out_none_mappings()
    validator.check_for_valid_pem_files()
    validator.check_for_extra_pem_files()

    if not validator.successful:
        fatal_error("Errors found!")

if __name__ == "__main__":
    main()
