#!/usr/bin/python

import os
import re
import shutil
import sys
import simplejson as json
from optparse import OptionParser


class MappingCreator(object):
    def __init__(self, json_file, outfile):
        f = open(json_file)
        self.data = json.load(f)
        self.outfile = outfile

    def invalid_channel(self, channel):
        return bool(re.search("-(htb$|htb-)", channel))

    def generate_mapping(self):
        mapping = {}

        for channel, details in self.data.items():
            if self.invalid_channel(channel):
                error("Skipping invalid channel: %s" % channel)
                continue
            if channel in mapping:
                fatal_error("%s is in the JSON more than once." % channel)
            mapping[channel] = os.path.basename(details['Product Cert file'])

        if self.outfile:
            f = open(self.outfile, "w")

        for k, v in sorted(mapping.items()):
            line = "%s: %s" % (k, v)
            if self.outfile:
                f.write(line + "\n")
            else:
                print line

    def copy_certs(self, certdir, certdest):
        if not os.path.exists(certdest):
            os.mkdir(certdest)
        for channel, details in self.data.items():
            if self.invalid_channel(channel):
                continue
            src = details['Product Cert file']
            if src[0] == "/":
                src = src[1:]
            src = os.path.join(certdir, src)
            try:
                shutil.copy(src, certdest)
            except IOError as e:
                error("Couldn't copy file: %s" % e)


def error(msg):
    sys.stderr.write(msg)
    sys.stderr.write("\n")


def fatal_error(msg):
    error(msg)
    sys.exit(-1)


def parse_command_line():
    parser = OptionParser()
    parser.add_option("-c", "--cert-directory", dest="certdir",
            help="Directory containing product certs.")
    parser.add_option("-o", "--out",
            help="File to write mapping to.")
    parser.add_option("-j", "--json",
            help="JSON file containing mapping information.")
    parser.add_option("-d", "--cert-destination", dest="certdest",
            help="Directory to copy certs to")
    (ops, args) = parser.parse_args()

    if ops.certdest:
        if not ops.certdir:
            parser.error("Please provide a cert directory to read the product certs from.")
        if not os.path.isdir(ops.certdir):
            parser.error("Could not find directory '%s'." % ops.certdir)
    if ops.certdir and not ops.certdest:
        parser.error("Please provide a destination to copy the certs to.")
    if not ops.json:
        parser.error("Please provide a JSON file.")
    if not os.path.isfile(ops.json):
        parser.error("Could not find file '%s'." % ops.json)

    return (ops, args)


def main():
    (ops, args) = parse_command_line()
    creator = MappingCreator(ops.json, ops.out)
    creator.generate_mapping()
    if ops.certdir and ops.certdest:
        creator.copy_certs(ops.certdir, ops.certdest)

if __name__ == "__main__":
    main()
