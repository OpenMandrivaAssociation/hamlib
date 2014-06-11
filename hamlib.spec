%define name	hamlib
%define version	1.2.15.3
%define rel	1

%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define major_cxx	2
%define libname_cxx	%mklibname %{name}++ %{major_cxx}
%define devname_cxx	%mklibname -d %{name}++
%define libname_tcl	%mklibname -d hamlibtcl1.0

Summary:	Control radio transceivers and receivers
Name:		%{name}
Version:	%{version}
Release:	%{rel}
License:	LGPLv2+
Group:		Communications
Url:		http://hamlib.sourceforge.net
Source0:	http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:         hamlib-1.2.15.3-bindings.patch
BuildRequires:	pkgconfig(libxml-2.0) 
BuildRequires:	pkgconfig(libusb-1.0) 
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	gd-devel
BuildRequires:	pkgconfig(gnuradio-core)
BuildRequires:	boost-devel
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(gnuradio-uhd)
BuildRequires:	pkgconfig(gruel)
BuildRequires:	pkgconfig(gnuradio-fcd)
BuildRequires:	pkgconfig(gnuradio-pager)
BuildRequires:	tcl-devel
BuildRequires:	doxygen
BuildRequires:	swig
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	glibc-devel


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



%package -n	perl-%{name}
Summary:	Hamlib radio control library Perl binding
Group:		Development/Perl
Requires:	hamlib = %{version}-%{release}

%description -n	perl-%{name}
Hamlib PERL Language bindings to allow radio control from PERL scripts.

%package -n	python-%{name}
Summary:	Hamlib radio control library Python binding
Group:		Development/Python
Requires:	hamlib = %{version}-%{release}

%description -n	python-%{name}
Hamlib Python Language bindings to allow radio control from Python scripts.

%package -n	%{libname_tcl}
Summary:	Hamlib radio control library TCL binding
Group:		System/Libraries
Requires:	hamlib = %{version}-%{release}
Provides:	%{name}-tcl-devel = %{version}-%{release}

%description -n %{libname_tcl}
Hamlib TCL Language bindings to allow radio control from TCL scripts.

%prep
%setup -q
%patch0 -p1 -b .bindings

%build
export LDFLAGS="$LDFLAGS -lm -ltirpc"
%configure2_5x \
        --with-ldtl-include=%{_includedir} \
        --with-ldtl-lib=%{_libdir} \
        --disable-static \
        --with-rigmatrix \
        --enable-tcl-binding \
        --with-perl-binding \
        --with-python-binding \
#	usrp depreciated
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# broken paralel build for libs, drivers, and programs

make 

make -C doc doc

%install
%makeinstall_std

find %{buildroot} -type f -name Hamlib.so -exec chmod 0755 {} ';'
find %{buildroot} -type f -name pkgIndex.tcl -exec rm -f {} ';'
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name Hamlib.bs -exec rm -f {} ';'
find %{buildroot} -type f -name perltest.pl -exec rm -f {} ';'

#we don't want these
find %{buildroot} -name "*.la" -exec rm {} \;

%files -n %{libname}
%doc AUTHORS ChangeLog PLAN README THANKS TODO
%{_libdir}/libhamlib.so.%{major}*
%{_libdir}/hamlib/hamlib-*.so

%files -n %{libname_cxx}
%doc AUTHORS ChangeLog
%{_libdir}/libhamlib++.so.%{major_cxx}*

%files utils
%doc AUTHORS ChangeLog
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


%files -n perl-%{name}
%doc COPYING.LIB
%{perl_vendorarch}/*

%files -n python-%{name}
%doc COPYING.LIB
%{py_puresitedir}/*.py*
%{py_puresitedir}/_Hamlib.so


%files -n %{libname_tcl}
%doc COPYING.LIB
%{_libdir}/hamlibtcl*


