%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define major_cxx 2
%define libname_cxx %mklibname %{name}++ %{major_cxx}
%define devname_cxx %mklibname -d %{name}++

Summary:	Control radio transceivers and receivers
Name:		hamlib
Version:	3.3
Release:	2
License:	LGPLv2+
Group:		Communications/Radio
Url:		http://hamlib.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libusb) >= 0.1
BuildRequires:	pkgconfig(gdlib)
BuildRequires:	libltdl-devel

%description
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

%package -n %{libname}
Summary:	Run-time library to control radio transceivers and receivers
Group:		Communications/Radio
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}

%description -n %{libname}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

%package utils
Summary:	Utilities to support the hamlib radio control library
Group:		Communications/Radio

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
Group:		Communications/Radio

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
sed -i 's|usrp|uhd|g' configure.ac
sed -i 's!AX_CFLAGS_WARN_ALL(\[AM_CFLAGS\])!!'g configure.ac
sed -i 's!AX_CXXFLAGS_WARN_ALL(\[AM_CXXFLAGS\])!!g' configure.ac
rm -f macros/ax_cflags_warn_all.m4
rm -f configure

%build
autoreconf -fiv
libtoolize --copy --force
%configure \
	--disable-static \
	--with-rigmatrix \
	--with-xml-support \
	--enable-uhd \
	--with-cxx-binding \
	--without-perl-binding \
	--without-python-binding

%make_build

%install
%make_install

#we don't want these
find %{buildroot} -name "*.la" -delete

%files -n %{libname}
%doc AUTHORS ChangeLog PLAN README THANKS TODO
%{_libdir}/libhamlib.so.%{major}{,.*}
%{_libdir}/libhamlib.so

%files -n %{libname_cxx}
%{_libdir}/libhamlib++.so.%{major_cxx}{,.*}

%files utils
%{_mandir}/man*/*
%{_bindir}/*

%files -n %{devname}
%doc README.developer
%{_defaultdocdir}/%{name}/*
%{_infodir}/hamlib.info.xz
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
