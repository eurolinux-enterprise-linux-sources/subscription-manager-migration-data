#!/usr/bin/python
#
# The JSON mapping file and directory of product certs are available in
# the git://git.app.eng.bos.redhat.com/rcm/rhn-definitions.git repository.
#
# The JSON file is cdn/product-baseline.json and the cert directory is
# under product_ids.

import glob
import os
import re
import sys
import simplejson as json
from optparse import OptionParser

JBEAP_PRODUCT_ID = "183"

class MappingCreator(object):
    def __init__(self, json_file, certdirs, outfile):
        f = open(json_file)
        self._data = json.load(f)
        self._certdirs = certdirs
        self._outfile = outfile

    def _find_arch(self, channel):
        tokens = channel.split('-')
        for token in tokens:
            if re.search("x86_64|i386|ppc|ppc64|s390x|ia64", token):
                return token

    def generate_jbeap_mapping(self, product_id, channels, mapping):
        dir_map = (
                ("jbappplatform-4.3.0-.*-server-5-rpm", "jbappplatform-4.3.0"),
                ("jbappplatform-5-.*-server-(5|6)-rpm", "jbappplatform-5.0"),
                ("jbappplatform-6-.*-server-6-rpm", "jbappplatform-6.0")
                )

        for channel in channels:
            # Map the channel to the correct directory
            for dir_mapping in dir_map:
                if re.match(dir_mapping[0], channel):
                    jboss_dir = dir_mapping[1]

            arch = self._find_arch(channel)
            if not arch:
                fatal_error("Could not detect arch for %s" % channel)

            fileglob = ''.join(('*', arch, '-*-', product_id, '*.pem'))
            for certdir in self._certdirs:
                # If the certdir matches the correct JBoss directory
                if re.search("%s$" % jboss_dir, certdir):
                    certs = glob.glob(os.path.join(certdir, fileglob))
                    if len(certs) > 1:
                        fatal_error("Found more than one cert matching %s" % fileglob)
                    if mapping.has_key(channel) and mapping[channel] != "none" and certs:
                        fatal_error("%s was found in more than one cert directory or %s is " \
                            "mapped twice" % (mapping[channel], channel))
                    if certs:
                        mapping[channel] = os.path.basename(certs[0])
                    elif mapping.has_key(channel):
                        pass
                    else:
                        mapping[channel] = "none"

    def generate_mapping(self):
        mapping = {}
        for product in self._data:
            product_id = product['Product ID']
            channels = product['RHN Channels']

            if product_id == JBEAP_PRODUCT_ID:
                self.generate_jbeap_mapping(product_id, channels, mapping)
                continue

            for channel in channels:
                if re.search("-5$|-5-", channel) and not re.search("jb", channel) \
                    or re.search("-htb$|-htb-", channel):
                    error("Skipping %s" % channel)
                    continue

                arch = self._find_arch(channel)
                if not arch:
                    fatal_error("Could not detect arch for %s" % channel)

                fileglob = ''.join(('*', arch, '-*-', product_id, '*.pem'))
                for certdir in self._certdirs:
                    certs = glob.glob(os.path.join(certdir, fileglob))
                    if len(certs) > 1:
                        fatal_error("Found more than one cert matching %s" % fileglob)

                    if mapping.has_key(channel) and mapping[channel] != "none" and certs:
                        # Special hack for 17{6|7|8|9}.pem and
                        # 180.pem which are mapped to the same
                        # channel.  We want to map to 180.pem.
                        if re.match("rhel-.*?-(client|server|hpc-node|workstation)-dts-6", channel):
                            first_cert = os.path.basename(certs[0])
                            if re.search("180.pem", first_cert):
                                mapping[channel] = first_cert
                            else:
                                continue
                        else:
                            fatal_error("%s was found in more than one cert directory or %s is " \
                                "mapped twice" % (mapping[channel], channel))
                    if certs:
                        mapping[channel] = os.path.basename(certs[0])
                    elif mapping.has_key(channel):
                        pass
                    else:
                        mapping[channel] = "none"

        if self._outfile:
            f = open(self._outfile, "w")

        for k, v in sorted(mapping.items()):
            line = "%s: %s" % (k, v)
            if self._outfile:
                f.write(line + "\n")
            else:
                print line


def error(msg):
    sys.stderr.write(msg)
    sys.stderr.write("\n")

def fatal_error(msg):
    error(msg)
    sys.exit(-1)

def parse_command_line():
    parser = OptionParser()
    parser.add_option("-c", "--certdir", action="append", help="Directory containing product certs.  " +
            "Can be provided more than once.", dest="certdirs")
    parser.add_option("-o", "--out", help="File to write mapping to.")
    parser.add_option("-j", "--json", help="JSON file containing mapping information.")

    (ops, args) = parser.parse_args()

    if not ops.certdirs:
        parser.error("Please provide one or more cert directories.")
    if False in map(os.path.isdir, ops.certdirs):
        parser.error("Could not find directory '%s'." % ops.certdirs)
    if not ops.json:
        parser.error("Please provide a JSON file.")
    if not os.path.isfile(ops.json):
        parser.error("Could not find file '%s'." % ops.json)

    return (ops, args)

def main():
    (ops, args) = parse_command_line()
    creator = MappingCreator(ops.json, ops.certdirs, ops.out)
    creator.generate_mapping()

if __name__ == "__main__":
    main()
