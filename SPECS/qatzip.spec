# SPDX-License-Identifier: MIT

%global githubname QATzip
%global libqatzip_soversion 3

Name:           qatzip
Version:        1.3.1
Release:        1%{?dist}
Summary:        Intel QuickAssist Technology (QAT) QATzip Library
License:        BSD-3-Clause
URL:            https://github.com/intel/%{githubname}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc >= 4.8.5
BuildRequires:  zlib-devel >= 1.2.7
BuildRequires:  qatlib-devel >= 23.08.0
BuildRequires:  autoconf automake libtool make lz4-devel numactl-devel
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
%autosetup -n %{githubname}-%{version}

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
%{_bindir}/qatzip-test

%files libs
%license LICENSE*
%{_libdir}/libqatzip.so.%{libqatzip_soversion}*

%files devel
%doc docs/QATzip-man.pdf
%{_includedir}/qatzip.h
%{_libdir}/libqatzip.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Apr 29 2025 Vladis Dronov <vdronov@redhat.com> - 1.3.1-1
- Update to qatzip 1.3.1 @ 10dbadba (RHEL-73092, RHEL-50462)
- Fix qatzip docker file build broken issue
- Support Latency sensitive mode for qatzip
- Add a suit of comp/decomp API to support Async offloading
- Support zlib format and end of stream flag
- Fix some bugs

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 1.2.0-4
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Wed Jun 26 2024 Vladis Dronov <vdronov@redhat.com> - 1.2.0-3
- Add self-tests and an OSCI harness (RHEL-20179)

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 1.2.0-2
- Bump release for June 2024 mass rebuild

* Fri Mar 22 2024 Vladis Dronov <vdronov@redhat.com> - 1.2.0-1
- Update to qatzip v1.2.0 (RHEL-20179)
- Add qatzip-test tool
- SW fallback
- Fix some bugs

* Fri Jan 26 2024 Vladis Dronov <vdronov@redhat.com> - 1.1.2-5
- Initial import from Fedora 40
