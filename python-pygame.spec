#
# TODO: - unpackaged files:
#		_site-packages/pygame/docs/*
#		_site-packages/pygame/examples/*
#		_site-packages/pygame/gp2x/*
#		_site-packages/pygame/tests/*
#

%define		module	pygame

Summary:	Python modules designed for writing games
Summary(pl.UTF-8):	Moduły Pythona dla piszących gry
Name:		python-%{module}
Version:	1.9.1
Release:	16
License:	LGPL v2.1+
Group:		Libraries/Python
Source0:	http://www.pygame.org/ftp/pygame-%{version}release.tar.gz
# Source0-md5:	1c4cdc708d17c8250a2d78ef997222fc
Patch0:		%{name}-porttime.patch
Patch1:		%{name}-remove-v4l.patch
Patch2:		x32.patch
URL:		http://www.pygame.org/
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	portmidi-devel >= 217
BuildRequires:	python-numpy-devel
BuildRequires:	python-devel >= 2.2.1
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	smpeg-devel
%pyrequires_eq	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pygame is a set of Python modules designed for writing games. It is
written on top of the excellent SDL library. This allows you to create
fully featured games and multimedia programs in the python language.
The package is highly portable, with games running on Windows, NT4,
MacOS, OSX, BeOS, FreeBSD, IRIX, and Linux.

%description -l pl.UTF-8
Pygame jest zbiorem modułów Pythona zaprojektowanych do pisania gier.
Moduły te zostały napisane na bazie wspaniałej biblioteki SDL. Dzięki
temu możliwe jest tworzenie bogatych w multimedia gier w języku
Python.

%package devel
Summary:	C header files for pygame modules
Summary(pl.UTF-8):	Pliki nagłówkowe języka C modułów pygame
Group:		Development/Languages/Python
%pyrequires_eq	python
Requires:	%{name} = %{version}-%{release}

%description devel
C header files for pygame modules.

%description devel -l pl.UTF-8
Pliki nagłówkowe języka C modułów pygame.

%prep
%setup -q -n %{module}-%{version}release
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="%{rpmcflags} -I/usr/include/smpeg"; export CFLAGS
%py_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_install

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc WHATSNEW docs/*
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.ttf
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py[co]
%dir %{py_sitedir}/%{module}/threads/
%{py_sitedir}/%{module}/threads/*.py[co]

%files devel
%defattr(644,root,root,755)
%{py_incdir}/%{module}
%{_examplesdir}/%{name}-%{version}
