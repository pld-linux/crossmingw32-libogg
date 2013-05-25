%define		realname	libogg
Summary:	Ogg Bitstream Library - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka obsługi strumieni bitowych Ogg - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.3.1
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	http://downloads.xiph.org/releases/ogg/%{realname}-%{version}.tar.xz
# Source0-md5:	ca25d8da0ddfc8c6cbbf78d847a209fe
Patch0:		%{realname}-ac_fixes.patch
URL:		http://www.xiph.org/ogg/
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.6
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
Libogg is a library for manipulating Ogg bitstreams. It handles both
making Ogg bitstreams and getting packets from Ogg bitstreams.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Libogg jest biblioteką do manipulacji strumieniami bitowymi Ogg.
Obsługuje ona zarówno tworzenie strumieni jak i uzyskiwanie pakietów
ze strumieni.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libogg library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libogg (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libogg library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libogg (wersja skrośna MinGW32).

%package dll
Summary:	DLL libogg library for Windows
Summary(pl.UTF-8):	Biblioteka DLL libogg dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
DLL libogg library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL libogg dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--host=%{target} \
	--target=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{aclocal,doc}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/libogg.dll.a
%{_libdir}/libogg.la
%{_includedir}/ogg
%{_pkgconfigdir}/ogg.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libogg.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libogg-*.dll
