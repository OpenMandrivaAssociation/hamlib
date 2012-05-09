%define name	hamlib
%define version	1.2.15
%define rel	2

%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define major_cxx	2
%define libname_cxx	%mklibname %{name}++ %{major_cxx}
%define devname_cxx	%mklibname -d %{name}++

Summary:	Control radio transceivers and receivers
Name:		%{name}
Version:	%{version}
Release:	%{rel}
License:	LGPLv2+
Group:		Communications
Url:		http://hamlib.sourceforge.net
Source0:	http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	libxml2-devel 
BuildRequires:	libusb-devel 
BuildRequires:	tirpc-devel
BuildRequires:	gd-devel
#BuildRequires:	usrp-devel
BuildRequires:	gnuradio-devel
BuildRequires:	boost-devel
BuildRequires:	libtool-devel

%description
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

%package -n %{libname}
Summary:	Run-time library to control radio transceivers and receivers
Group:		Communications
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}

%description -n %{libname}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

%package utils
Summary:	Utilities to support the hamlib radio control library
Group:		Communications

%description utils
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package provides a command-line utility to test the hamlib library and
to control transceivers if you're short of anything more sophisticated. 

%package -n %{devname}
Summary:	Development library to control radio transcievers and receivers
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}

%description -n %{devname}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package provides the development files and headers.

%package -n %{libname_cxx}
Summary:	Hamlib radio control library C++ binding
Group:		Communications

%description -n %{libname_cxx}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package contains Hamlib radio control library C++ language binding.

%package -n %{devname_cxx}
Summary:	Hamlib radio control library C++ binding development headers and libraries
Group:		Development/C++
Requires:	%{libname_cxx} = %{version}-%{release}
Provides:	%{name}++-devel = %{version}-%{release}
Provides:	lib%{name}++-devel = %{version}-%{release}

%description -n %{devname_cxx}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package contains Hamlib radio control library C++ binding development
headers and libraries for building C++ applications with Hamlib.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--with-rigmatrix \
	--with-usrp \
	--without-perl-binding \
	--without-kylix-binding \
	--without-tcl-binding \
	--without-python-binding
%make 

%install
%makeinstall_std

#we don't want these
find %{buildroot} -name "*.la" -exec rm {} \;

%files -n %{libname}
%doc AUTHORS ChangeLog PLAN README THANKS TODO
%{_libdir}/libhamlib.so.%{major}*
%{_libdir}/hamlib/hamlib-*.so

%files -n %{libname_cxx}
%{_libdir}/libhamlib++.so.%{major_cxx}*

%files utils
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_bindir}/*
%{_sbindir}/*

%files -n %{devname}
%doc README.developer
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/rig.h
%{_includedir}/%{name}/riglist.h
%{_includedir}/%{name}/rig_dll.h
%{_includedir}/%{name}/rotator.h
%{_includedir}/%{name}/rotlist.h
%{_datadir}/aclocal/hamlib.m4
%{_libdir}/pkgconfig/hamlib.pc
%{_libdir}/libhamlib.so

%files -n %{devname_cxx}
%doc README.developer
%{_libdir}/libhamlib++.so
%{_includedir}/%{name}/rigclass.h
%{_includedir}/%{name}/rotclass.h
