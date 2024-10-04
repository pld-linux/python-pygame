#
# Conditional build:
%bcond_with	apidocs	# Sphinx documentation (encoding errors as of 1.9.6 / Sphinx 1.8)
%bcond_with	sdl1	# SDL 1.2 instead of 2.0

%define		module	pygame

Summary:	Python modules designed for writing games
Summary(pl.UTF-8):	Moduły Pythona dla piszących gry
Name:		python-%{module}
# keep 2.0.x here for python2 support
Version:	2.0.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/pygame/pygame-%{version}.tar.gz
# Source0-md5:	04e082d216b3b771b8d52769597b2fb2
Patch0:		pygame-py2-types.patch
Patch1:		pygame-portmidi.patch
Patch2:		x32.patch
URL:		https://www.pygame.org/
%if %{with sdl1}
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
%else
BuildRequires:	SDL2-devel >= 2.0
BuildRequires:	SDL2_image-devel >= 2.0
BuildRequires:	SDL2_mixer-devel >= 2.0
%endif
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	portmidi-devel >= 217
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-numpy-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with apidocs}
BuildRequires:	sphinx-pdg-2
%endif
BuildRequires:	xorg-lib-libX11-devel
Requires:	python-modules >= 1:2.7
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
Requires:	%{name} = %{version}-%{release}
Requires:	python-devel >= 1:2.7
BuildArch:	noarch

%description devel
C header files for pygame modules.

%description devel -l pl.UTF-8
Pliki nagłówkowe języka C modułów pygame.

%package examples
Summary:	Examples for Python pygame modules
Summary(pl.UTF-8):	Przykłady do modułów Pythona pygame
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description examples
Examples for Python pygame modules.

%description examples -l pl.UTF-8
Przykłady do modułów Pythona pygame.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# missing file, required for py2
touch docs/reST/ext/__init__.py

# encoding marker required for py2
%{__sed} -i -e '1i # -*- coding: utf-8 -*-' \
	docs/reST/ext/boilerplate.py

%build
export PORTMIDI_INC_PORTTIME=1
%py_build \
	%{?with_sdl1:-sdl1}

%if %{with apidocs}
LC_ALL=C.UTF-8 \
PYTHONIOENCODING=utf-8 \
sphinx-build-2 -b html docs/reST docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_install

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/%{module}/{docs,examples,tests}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{module}/pygame.ico
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{module}/pygame_icon.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.ttf
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py[cio]
%{py_sitedir}/%{module}/py.typed
%dir %{py_sitedir}/%{module}/__pyinstaller
%{py_sitedir}/%{module}/__pyinstaller/*.py[co]
%dir %{py_sitedir}/%{module}/_sdl2
%if %{without sdl1}
%attr(755,root,root) %{py_sitedir}/%{module}/_sdl2/*.so
%endif
%{py_sitedir}/%{module}/_sdl2/*.py[cio]
%dir %{py_sitedir}/%{module}/threads
%{py_sitedir}/%{module}/threads/*.py[co]
%{py_sitedir}/pygame-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{py_incdir}/%{module}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
