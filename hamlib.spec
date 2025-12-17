%define major	4
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname -d %{name}

%define major_cxx 4
%define libname_cxx %mklibname %{name}++ %{major_cxx}
%define devname_cxx %mklibname -d %{name}++

%define oname Hamlib

Summary:	Control radio transceivers and receivers
Name:		hamlib
Version:	4.6.5
Release:	3
License:	GPL-2.0-or-later and LGPL-2.0-or-later
Group:		Communications/Radio
Url:		https://hamlib.github.io/
Source0:	https://github.com/Hamlib/Hamlib/archive/%{version}/%{name}-%{version}.tar.gz
# Fix perl install
Patch0:		hamlib-4.6.5-perl-install.patch

BuildRequires:	automake autoconf libtool
BuildRequires:	doxygen
BuildRequires:	cmake(boost)
BuildRequires:	perl-devel
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(gdlib)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(tcl)
BuildRequires:	rpm-build
BuildRequires:	source-highlight
BuildRequires:	swig

%description
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

%package -n %{libname}
Summary:	Run-time library to control radio transceivers and receivers
Group:		Communications/Radio
Provides:	%{name} = %{version}-%{release}
Provides:	%{name}%{?_isa} = %{version}-%{release}
Obsoletes:	%{name} < %{version}-%{release}
Recommends:	%{name}-doc = %{version}-%{release}

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
Provides:	lib%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Recommends:	%{name}-doc = %{version}-%{release}

%description -n %{devname}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package provides the development files and headers.

%package -n %{libname_cxx}
Summary:	Hamlib radio control library C++ binding
Group:		Communications/Radio
Provides:	%{libname_cxx} = %{version}-%{release}
Provides:	%{libname_cxx}%{?_isa} = %{version}-%{release}
Recommends:	%{name}-doc = %{version}-%{release}

%description -n %{libname_cxx}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package contains Hamlib radio control library C++ language binding.

%package -n %{devname_cxx}
Summary:	Hamlib radio control library C++ binding development headers and libraries
Group:		Development/C++
Requires:	%{libname_cxx} = %{version}-%{release}
Provides:	%{name}++-devel = %{version}-%{release}
Provides:	%{name}++-devel%{?_isa} = %{version}-%{release}
Provides:	lib%{name}++-devel = %{version}-%{release}
Recommends:	%{name}-doc = %{version}-%{release}

%description -n %{devname_cxx}
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

This package contains Hamlib radio control library C++ binding development
headers and libraries for building C++ applications with Hamlib.

%package -n lua-%{name}
Summary:        LUA bindings for Hamlib
Group:          Development/Libraries/Other

%description -n lua-%{name}
Hamlib LUA Language bindings to allow radio control from LUA scripts.

%package -n perl-%{name}
Summary:	Hamlib radio control library Perl binding
Group:		Development/Languages/Perl
Requires:	hamlib%{?_isa} = %{version}-%{release}
Provides:	hamlib-perl = %{version}-%{release}

%description -n perl-%{name}
Hamlib PERL Language bindings to allow radio control from PERL scripts.

%package -n python-%{name}
Summary:	Hamlib radio control library Python binding
Group:		Development/Libraries/Python
Requires:	hamlib%{?_isa} = %{version}-%{release}
Requires:	python >= 3

%description -n python-%{name}
Hamlib Python Language bindings to allow radio control from Python scripts.

%package -n tcl-%{name}
Summary:        Hamlib radio control library TCL binding
Requires:       hamlib%{?_isa} = %{version}-%{release}
Provides:       hamlib-tcl = %{version}-%{release}

%description -n tcl-%{name}
Hamlib TCL Language bindings to allow radio control from TCL scripts.

%package doc
Summary:        Documentation for the hamlib radio control library
BuildArch:      noarch

%description doc
This package provides the developers documentation and exmaples
for the hamlib radio control library API.

%prep
%autosetup -n %{oname}-%{version} -p1
sed -i 's|usrp|uhd|g' configure.ac
sed -i 's!AX_CFLAGS_WARN_ALL(\[AM_CFLAGS\])!!'g configure.ac
sed -i 's!AX_CXXFLAGS_WARN_ALL(\[AM_CXXFLAGS\])!!g' configure.ac
rm -f macros/ax_cflags_warn_all.m4
rm -f configure

%build
export PYTHON=%{__python}
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{optflags} -llua" # -lpython"
autoreconf -fiv
#libtoolize --copy --force
%configure \
	--disable-static \
	--with-rigmatrix \
	--with-xml-support \
	--enable-uhd \
	--with-cxx-binding \
	--with-lua-binding \
	--with-perl-binding \
	--with-python-binding PYTHON_VERSION=%{pyver} \
	--with-tcl-binding \
	--with-tcl=/usr/%{_lib}

%make_build

# Build Documentation
make -C doc doc

%install
%make_install

# Install documentation
mkdir -p %{buildroot}%{_docdir}/%{name}/html/search
for f in `find doc/html/ -type f -maxdepth 1`
	do install -D -m 0644 $f %{buildroot}%{_docdir}/%{name}/`echo $f | cut -d '/' -f2`
done
for f in `find doc/html/search -type f -maxdepth 1`
	do install -D -m 0644 $f %{buildroot}%{_docdir}/%{name}/html/`echo $f | cut -d '/' -f3`
done

# Move installed docs
#mkdir -p %{buildroot}%{_docdir}
#mv %{buildroot}/%{_datadir}/doc/%{name} %{buildroot}%{_docdir}

# Fix permissions
find %{buildroot} -type f -name Hamlib.so -exec chmod 0755 {} ';'

#we don't want these
find %{buildroot} -type f \( -name '*.a' -o -name '*.la' \) -delete -print
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name Hamlib.bs -exec rm -f {} ';'


%check
make V=1 check

%post -n %{libname} -p /sbin/ldconfig
%post -n %{libname_cxx} -p /sbin/ldconfig
%post -n tcl-%{name} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig
%postun -n %{libname_cxx} -p /sbin/ldconfig
%postun -n tcl-%{name} -p /sbin/ldconfig


%files -n %{libname}
%doc AUTHORS ChangeLog PLAN README THANKS
%{_libdir}/libhamlib.so.%{major}{,.*}
%{_libdir}/libhamlib.so

%files -n %{libname_cxx}
%{_libdir}/libhamlib++.so.%{major_cxx}{,.*}

%files utils
%{_mandir}/man*/*
%{_bindir}/*

%files -n %{devname}
%license COPYING COPYING.LIB
%doc README.developer
%{_defaultdocdir}/%{name}/*
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
%license COPYING COPYING.LIB
%doc README.developer
%{_libdir}/libhamlib++.so
%{_includedir}/%{name}/*.h

%files -n lua-%{name}
%license COPYING COPYING.LIB
%{_libdir}/lua

%files -n perl-%{name}
%license COPYING COPYING.LIB
%{perl_vendorarch}/*

%files -n python-%{name}
%license COPYING COPYING.LIB
%{python3_sitearch}/Hamlib.*
%{python3_sitearch}/_Hamlib.*
%{python3_sitearch}/__pycache__/Hamlib.cpython*.pyc

%files -n tcl-%{name}
%license COPYING COPYING.LIB
%dir %{_libdir}/tcl*/
%dir %{_libdir}/tcl*/Hamlib
%{_libdir}/tcl*/Hamlib/*

%files doc
%{_docdir}/hamlib
