PREFIX ?= /

PKGNAME = subscription-manager-migration-data
VERSION = $(shell echo `grep ^Version: $(PKGNAME).spec | awk '{ print $$2 }'`)

RHSMDIR = usr/share/rhsm

build:
	./sanity-check.py RHEL-7

install: build
	install -d ${PREFIX}/${RHSMDIR}/product
	install -d ${PREFIX}/${RHSMDIR}/product/RHEL-7
	#install -m 644 RHEL-7/*.pem ${PREFIX}/${RHSMDIR}/product/RHEL-7
	install -m 644 RHEL-7/channel-cert-mapping.txt ${PREFIX}/${RHSMDIR}/product/RHEL-7/channel-cert-mapping.txt
	
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
