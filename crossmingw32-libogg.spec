%define		realname	libogg
Summary:	Ogg Bitstream Library - Mingw32 cross version
Summary(pl.UTF-8):	Biblioteka obsługi strumieni bitowych Ogg - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.1.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.xiph.org/releases/ogg/%{realname}-%{version}.tar.gz
# Source0-md5:	eaf7dc6ebbff30975de7527a80831585
Patch0:		%{realname}-ac_fixes.patch
URL:		http://www.xiph.org/ogg/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
Libogg is a library for manipulating Ogg bitstreams. It handles both
making Ogg bitstreams and getting packets from Ogg bitstreams.

%description -l pl.UTF-8
Libogg jest biblioteką do manipulacji strumieniami bitowymi Ogg.
Obsługuje ona zarówno tworzenie strumieni jak i uzyskiwanie pakietów
ze strumieni.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl.UTF-8):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

%configure \
	--host=%{_host} \
	--target=%{target}

# autoshit badly wants -lc, which is unavailable, so let's make something
# simpler

for i in bitwise.c framing.c
do
	%{__cc} %{rpmcflags} -c src/$i -Iinclude
done

rm -f libogg.a
$AR cru libogg.a *.o
$RANLIB libogg.a

%{__cc} --shared *.o -Wl,--enable-auto-image-base -o ogg.dll -Wl,--out-implib,libogg.dll.a

%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

sed -i	-e 's@libdir=/usr/lib@libdir=%{arch}/lib@' \
	-e 's@includedir=/usr/include@includedir=%{arch}/include@' \
	ogg.pc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/ogg,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

install include/ogg/*.h $RPM_BUILD_ROOT%{arch}/include/ogg
install libogg.a $RPM_BUILD_ROOT%{arch}/lib
install libogg.dll.a $RPM_BUILD_ROOT%{arch}/lib
install ogg.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install ogg.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/i386-mingw32-ogg.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/ogg
%{arch}/lib/*
%{_pkgconfigdir}/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
