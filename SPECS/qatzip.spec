# SPDX-License-Identifier: MIT

%global githubname QATzip
%global libqatzip_soversion 3

Name:           qatzip
Version:        1.1.2
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology (QAT) QATzip Library
License:        BSD
URL:            https://github.com/intel/%{githubname}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc >= 4.8.5
BuildRequires:  zlib-devel >= 1.2.7
BuildRequires:  qatlib-devel >= 22.07.0
BuildRequires:  autoconf automake libtool make lz4-devel
# The purpose of the package is to support hardware that only exists on x86_64 platforms
# https://bugzilla.redhat.com/show_bug.cgi?id=1987280
ExclusiveArch:  x86_64

%description
QATzip is a user space library which builds on top of the Intel
QuickAssist Technology user space library, to provide extended
accelerated compression and decompression services by offloading the
actual compression and decompression request(s) to the Intel Chipset
Series. QATzip produces data using the standard gzip* format
(RFC1952) with extended headers. The data can be decompressed with a
compliant gzip* implementation. QATzip is designed to take full
advantage of the performance provided by Intel QuickAssist
Technology.

%package        libs
Summary:        Libraries for the qatzip package

%description    libs
This package contains libraries for applications to use
the QATzip APIs.

%package        devel
Summary:        Development components for the libqatzip package
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build
applications that use the QATzip APIs.

%prep
%autosetup -p0 -n %{githubname}-%{version}

%build
%set_build_flags

autoreconf -vif
./configure \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix} \
    --enable-symbol

%make_build

%install
%make_install
rm %{buildroot}/%{_libdir}/libqatzip.a
rm %{buildroot}/%{_libdir}/libqatzip.la
rm -vf %{buildroot}%{_mandir}/*.pdf

# Check section is not available for these functional and performance tests require special hardware.

%files
%license LICENSE*
%{_mandir}/man1/qzip.1*
%{_bindir}/qzip

%files libs
%license LICENSE*
%{_libdir}/libqatzip.so.%{libqatzip_soversion}*

%files devel
%doc docs/QATzip-man.pdf
%{_includedir}/qatzip.h
%{_libdir}/libqatzip.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Mar 29 2023 Vladis Dronov <vdronov@redhat.com> - 1.1.2-1
- Update to qatzip 1.1.2 (bz 2178631)
- Update README, update driver configure files
- Fix some bugs
- Add support for pkgconfig

* Mon Aug 08 2022 Vladis Dronov <vdronov@redhat.com> - 1.0.9-1
- Rebuild for qatzip v1.0.9 (bz 2047744)
- Update to require qatlib-devel >= 22.07.0 due to soversion bump

* Wed Feb 09 2022 Vladis Dronov <vdronov@redhat.com> - 1.0.7-1
- Rebuild for qatzip v1.0.7
- Fix snprintf truncation check (bz 2046925)
- Add -fstack-protector-strong build option (bz 2044889)

* Wed Oct 20 2021 Vladis Dronov <vdronov@redhat.com> - 1.0.6-5
- Add OSCI testing harness (bz 1874207)

* Mon Sep 13 2021 zm627 <zheng.ma@intel.com> - 1.0.6-3
- Rebuild for qatzip v1.0.6

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.6-2
- Upload new qatzip source package and rebuild

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.6-1
- Update to latest qatlib and qatzip upstream release

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.5-3
- Add ExcludeArch ticket number

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.5-2
- Rebuilt for qatlib v21.08

* Tue Jul 13 2021 Ma Zheng <zheng.ma@intel.com> - 1.0.5-1
- Initial version of RPM Package
