#
# Conditional build:
%bcond_with	apidocs	# Sphinx documentation (encoding errors as of 1.9.6 / Sphinx 1.8)

%define		module	pygame

Summary:	Python modules designed for writing games
Summary(pl.UTF-8):	Moduły Pythona dla piszących gry
Name:		python-%{module}
Version:	1.9.6
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/pygame/pygame-%{version}.tar.gz
# Source0-md5:	36f8817874f9e63acdf12914340b60e9
Patch2:		x32.patch
URL:		https://www.pygame.org/
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
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
%patch2 -p1

%build
export PORTMIDI_INC_PORTTIME=1
%py_build

%if %{with apidocs}
LC_ALL=en.UTF-8 \
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
%{py_sitedir}/%{module}/*.py[co]
%dir %{py_sitedir}/%{module}/threads
%{py_sitedir}/%{module}/threads/*.py[co]
%{py_sitedir}/pygame-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{py_incdir}/%{module}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
