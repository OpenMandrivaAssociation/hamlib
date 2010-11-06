%define version	1.2.12
%define rel	1

Summary:	Run-time library to control radio transceivers and receivers
Name:		hamlib
Version:	%{version}
Release:	%mkrel %{rel}
License:	LGPL
Group:		Development/Other
Url:		http://hamlib.sourceforge.net
Source:		http://hamlib.sourceforge.net/%{name}-%{version}.tar.gz
BuildRequires:		glibc-devel  
BuildRequires:		textutils 
BuildRequires:		fileutils 
BuildRequires:		libxml2-devel 
BuildRequires:		libusb-devel 


%description
 Most recent amateur radio transceivers allow external control of their
 functions through a computer interface. Unfortunately, control commands are
 not always consistent across a manufacturer's product line and each
 manufacturer's product line differs greatly from its competitors.
 .
 This library addresses that issue by providing a standardised programming
 interface that applications can talk to and translating that into the
 appropriate commands required by the radio in use.
 .
 This package provides the run-time form of the library. If you wish to
 develop software using this library you need the 'hamlib-devel' package.
 .
 Also included in the package is a simple radio control program 'rigctl',
 which let one control a radio transceiver or receiver, either from
 command line interface or in a text-oriented interactive interface.

%package devel
Summary: Development library to control radio transcievers and receivers
Group: Development/Other
Requires: hamlib

%description devel
 Most recent amateur radio transceivers allow external control of their
 functions through a computer interface. Unfortunately, control commands are
 not always consistent across a manufacturer's product line and each
 manufacturer's product line differs greatly from its competitors.
 .
 This library addresses that issue by providing a standardised programming
 interface that applications can talk to and translating that into the
 appropriate commands required by the radio in use.
 .
 This package provides the development library. If you wish to run applications
 developed using this library you'll need the 'hamlib' package.

%prep
%setup

%build
autoreconf -fi

LIBS="-lpthread" CFLAGS="-pthread" %configure --without-cxx-binding   \
	   --without-perl-binding  \
	   --without-kylix-binding \
	   --without-tcl-binding   \
	   --without-python-binding
%make 


%install
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644, root, root, 755)
%doc COPYING

%{_mandir}/man1/*
%{_mandir}/man8/*

%defattr(755, root, root, 755)
%{_libdir}/libhamlib.so.*
%{_libdir}/hamlib-*.so

%{_bindir}/*
%{_sbindir}/*

%files devel
%defattr(644, root, root, 755)
%dir %{_includedir}/hamlib
%{_includedir}/hamlib/*.h
%{_datadir}/aclocal/hamlib.m4
%{_libdir}/pkgconfig/hamlib.pc
%{_libdir}/libhamlib.so
%{_libdir}/*.la
%{_libdir}/*.a


