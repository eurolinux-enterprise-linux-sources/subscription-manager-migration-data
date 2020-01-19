Name: subscription-manager-migration-data
Summary: RHN Classic to RHSM migration data
Group: System Environment/Base
License: See Red Hat Enterprise Agreement 
Version: 2.0.7
Release: 1%{?dist}
URL: http://redhat.com
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python

%description
This package provides certificates for migrating a system from
RHN Classic to RHSM.

%prep
%setup -q

%build
make -f Makefile build VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_DIR

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT RHEL_VER=%{?rhel}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(755,root,root) %dir %{_datadir}/rhsm/product
%attr(755,root,root) %dir %{_datadir}/rhsm/product/RHEL-%{?rhel}
%{_datadir}/rhsm/product/RHEL-%{?rhel}/*pem
%{_datadir}/rhsm/product/RHEL-%{?rhel}/channel-cert-mapping.txt

%changelog
* Tue Feb 18 2014 ckozak <ckozak@redhat.com> 2.0.7-1
- Invoke sanity-check.py with python and require python for build.
  (awood@redhat.com)

* Tue Feb 18 2014 ckozak <ckozak@redhat.com> 2.0.6-1
- Add RHEL 7 certs. (awood@redhat.com)

* Thu Oct 17 2013 Alex Wood <awood@redhat.com> 2.0.5-1
- 1009932: Add RHEL 4 mappings to migration data. (awood@redhat.com)

* Thu Sep 26 2013 Alex Wood <awood@redhat.com> 2.0.4-1
- Adding RHEL 6.5 certificates. (awood@redhat.com)
- Detect invalid channels more generally. (awood@redhat.com)

* Wed Sep 25 2013 Alex Wood <awood@redhat.com> 2.0.3-1
- 1011992: Skip high touch beta channels. (awood@redhat.com)

* Wed Sep 11 2013 Alex Wood <awood@redhat.com> 2.0.2-1
- Updating product cert mappings. (awood@redhat.com)
- Point to newest rcm-metadata (awood@redhat.com)
- Adding file explaining how to build on Fedora. (awood@redhat.com)

* Thu Jun 06 2013 Alex Wood <awood@redhat.com> 2.0.1-1
- new package built with tito

* Wed Jun 05 2013 Alex Wood <awood@redhat.com> 2.0.0-1
- Unifying all RHEL product certificates into one package

* Thu May 09 2013 Alex Wood <awood@redhat.com> 1.11.3.0-1
- Adding product certificates for RHEL 5.10

* Fri Oct 12 2012 Alex Wood <awood@redhat.com> 1.11.2.7-1
- 865566: Add mappings for RHEV debuginfo channels. (awood@redhat.com)

* Tue Oct 02 2012 Alex Wood <awood@redhat.com> 1.11.2.6-1
- Removing unused product certificate. (awood@redhat.com)

* Tue Oct 02 2012 Alex Wood <awood@redhat.com> 1.11.2.5-1
- 861420: Add mapping and certificates for RHEV 3.0. (awood@redhat.com)
- 861470: Add mapping and certificates for ELS-JBEAP. (awood@redhat.com)

* Wed Aug 29 2012 Alex Wood <awood@redhat.com> 1.11.2.4-1
- Adding product certificate for RHB i386. (awood@redhat.com)
- 820749: Correct mappings for i386 DTS. (awood@redhat.com)
- 849274, 849305: Update mappings for JBEAP and RHEV Agent. (awood@redhat.com)

* Thu Aug 09 2012 Alex Wood <awood@redhat.com> 1.11.2.3-1
- Correcting logic on special hack for 180.pem (awood@redhat.com)
- Adding additional product certs and mappings. (awood@redhat.com)
- Adding special hack for 17{6|8}.pem and 180.pem (awood@redhat.com)
- 840148: Adding cert and mapping for Server-EUCJP (awood@redhat.com)

* Thu Jun 28 2012 Alex Wood <awood@redhat.com> 1.11.2.2-1
- Product mappings for RHEL5.9 (awood@redhat.com)

* Tue Jan 17 2012 Alex Wood <awood@redhat.com> 1.11-1
- 782208: Use RHEL 5.8 certificates. (awood@redhat.com)

* Mon Jan 09 2012 Alex Wood <awood@redhat.com> 1.10-1
- 771615: Remove a dependency on the Linux 'file' command from the linting
  script. (awood@redhat.com)

* Mon Jan 09 2012 Alex Wood <awood@redhat.com> 1.9-1
- Remove a dependency on the Linux 'file' command from the linting script.
  (awood@redhat.com)

* Mon Jan 09 2012 Alex Wood <awood@redhat.com> 1.8-1
- 771615: fix mapping file syntax errors (jbowes@redhat.com)
- 771615: add sanity-check script for mappings (jbowes@redhat.com)
- update gitignore for swap files (jbowes@redhat.com)

* Thu Dec 15 2011 Alex Wood <awood@redhat.com> 1.7-1
- 767749: subscription-manager-migration-data should require subscription-
  manager-migration. (awood@redhat.com)

* Mon Nov 28 2011 Alex Wood <awood@redhat.com> 1.6-1
- 757829: Fixing license field. (awood@redhat.com)

* Mon Nov 28 2011 Alex Wood <awood@redhat.com> 1.5-1
- Changing text of license field. (awood@redhat.com)

* Mon Nov 21 2011 Alex Wood <awood@redhat.com> 1.4-1
- Adding CVS releaser. (awood@redhat.com)

* Mon Nov 21 2011 Alex Wood <awood@redhat.com> 1.3-1
- 755035: Genericize to RHEL-5 instead of just RHEL-5.7 (awood@redhat.com)

* Thu Nov 17 2011 Alex Wood <awood@redhat.com> 1.2-1
- Correcting incorrect date in the changelog. (awood@redhat.com)
- alter license per mkhusid (he is following up w/ legal to confirm)
  (cduryee@redhat.com)
- rpmlint fixes (cduryee@redhat.com)
- Removing .svn directory that was checked in accidentally. (awood@redhat.com)

* Wed Nov 02 2011 Alex Wood <awood@redhat.com> 1.1-1
- new package built with tito

* Tue Nov 01 2011 Alex Wood <awood@redhat.com> 1.0.0-1
- Initial packaging.

