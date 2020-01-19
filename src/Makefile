PREFIX ?= /

PKGNAME = subscription-manager-migration-data
VERSION = $(shell echo `grep ^Version: $(PKGNAME).spec | awk '{ print $$2 }'`)
RHSMDIR = usr/share/rhsm

# Must be specified by the user
RHEL_VER =

build:
	python sanity-check.py RHEL

check_env:
ifndef RHEL_VER
	@echo 1>&2 "RHEL_VER must be set"
	false
endif

install: check_env build
	install -d ${PREFIX}/${RHSMDIR}/product
	install -d ${PREFIX}/${RHSMDIR}/product/RHEL-${RHEL_VER}
	install -m 644 RHEL/*.pem ${PREFIX}/${RHSMDIR}/product/RHEL-${RHEL_VER}
	install -m 644 RHEL/channel-cert-mapping.txt ${PREFIX}/${RHSMDIR}/product/RHEL-${RHEL_VER}/channel-cert-mapping.txt
	
clean:
	rm -f *~ *.bak *.tar.gz
	for d in ${SUBDIRS}; do make -C $$d clean ; done

archive: clean
	@rm -rf ${PKGNAME}-%{VERSION}.tar.gz
	@rm -rf /tmp/${PKGNAME}-${VERSION} /tmp/${PKGNAME}
	@dir=$$PWD; cd /tmp; cp -a $$dir ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-${VERSION}
	@dir=$$PWD; cd /tmp; tar cvzf $$dir/${PKGNAME}-$(VERSION).tar.gz --exclude \.git ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

rpm: archive
	rpmbuild -ta ${PKGNAME}-$(VERSION).tar.gz
