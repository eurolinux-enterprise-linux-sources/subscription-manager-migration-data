Name: subscription-manager-migration-data
Summary: RHN Classic to RHSM migration data
Group: System Environment/Base
License: See Red Hat Enterprise Agreement 
Version: 1.13.0.2
Release: 1%{?dist}
URL: http://redhat.com
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: python-devel

%description
This package provides certificates for migrating a system from
RHN Classic to RHSM.

%prep
%setup -q

%build
make -f Makefile build VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_DIR

%install
rm -rf $RPM_BUILD_ROOT
make -f Makefile install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(755,root,root) %dir %{_datadir}/rhsm/product
%attr(755,root,root) %dir %{_datadir}/rhsm/product/RHEL-7
#%{_datadir}/rhsm/product/RHEL-7/*pem
%{_datadir}/rhsm/product/RHEL-7/channel-cert-mapping.txt

%changelog
* Wed Aug 07 2013 Alex Wood <awood@redhat.com> 1.13.0.2-1
- Add BuildRequires for python. (awood@redhat.com)

* Tue Jul 02 2013 Alex Wood <awood@redhat.com> 1.13.0.1-1
- Revising files for RHEL 7 (awood@redhat.com)

* Tue Nov 13 2012 Adrian Likins <alikins@redhat.com> 1.12.2.6-1
- 875760: Add Openshift channel mappings. (awood@redhat.com)

* Mon Nov 05 2012 Adrian Likins <alikins@redhat.com> 1.12.2.5-1
- 872959: Adding missing mappings and certificates. (awood@redhat.com)

* Fri Nov 02 2012 Adrian Likins <alikins@redhat.com> 1.12.2.4-1
- Adding OpenShift product certificates. (awood@redhat.com)

* Fri Oct 12 2012 Adrian Likins <alikins@redhat.com> 1.12.2.3-1
- rev subscription-manager-migration-data for 6.4 

* Mon Oct 08 2012 Adrian Likins <alikins@redhat.com> 1.12.2.2-1
- Updating tito releaser. (awood@redhat.com)

* Fri Oct 05 2012 Alex Wood <awood@redhat.com> 1.12.2.1-1
- New product migration data for RHEL 6.4. (awood@redhat.com)
- Updating mapping creation script for RHEL 6.4. (awood@redhat.com)
- Add check to see if more than one certificate exists for a product ID.
  (awood@redhat.com)

* Tue May 01 2012 Alex Wood <awood@redhat.com> 1.12.1.8-1
- 816364: Correcting mapping for Red Hat Enterprise Virtualization on i386.
  (awood@redhat.com)
- Adding product certs. (awood@redhat.com)

* Tue May 01 2012 Alex Wood <awood@redhat.com> 1.12.1.7-1
- 816364: Adding corrected product cert for Red Hat Enterprise Virtualization
  on i386. (awood@redhat.com)

* Tue May 01 2012 Alex Wood <awood@redhat.com> 1.12.1.6-1
- 816364: Adding missing product cert for Red Hat Enterprise Virtualization on
  i386. (awood@redhat.com)
- 816364: Adding missing mapping for Red Hat Enterprise Virtualization on i386.
  (awood@redhat.com)

* Tue Apr 24 2012 Michael Stead <mstead@redhat.com> 1.12.1.5-1
- 811779: Remove dependency on subscription-manager. (awood@redhat.com)

* Tue Apr 24 2012 Michael Stead <mstead@redhat.com> 1.12.1.4-1
- 815433: Add sam-rhel-x86_64-server-6 channel mapping. (awood@redhat.com)
- Dealt with certificate change for HPN. (awood@redhat.com)
- 811633: Adding mapping for product 167 "Red Hat CloudForms"
  (awood@redhat.com)

* Wed Apr 11 2012 Michael Stead <mstead@redhat.com> 1.12.1.3-1
- 799152: Adding missing product certificates and mappings. (awood@redhat.com)
- Updating create-mapping.py (awood@redhat.com)

* Fri Mar 23 2012 Alex Wood <awood@redhat.com> 1.12.1.2-1
- Altering version to reflect new branching strategy. (awood@redhat.com)
- Add s390x and cf channels. (awood@redhat.com)
- Moving RHEL 6 migration data to a separate branch. (awood@redhat.com)
- Updating version number. (mstead@redhat.com)
- Adding mapping file and certs for RHEL-6. (awood@redhat.com)
- Adding a script to generate mapping files from product data.
  (awood@redhat.com)

* Tue Feb 14 2012 Michael Stead <mstead@redhat.com> 1.12-1
- 773030: add subscription-manager-migration-data to RHEL 6.3
  (mstead@redhat.com)
- Adding a quick and dirty script to help with mapping file updates.
  (awood@redhat.com)

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

