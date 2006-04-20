
%define		module	pygame

Summary:	Python modules designed for writing games
Summary(pl):	Modu³y Pythona dla pisz±cych gry
Name:		python-%{module}
Version:	1.7.1
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:	http://www.pygame.org/ftp/pygame-%{version}release.tar.gz
# Source0-md5:	05d86d1af446f79411359400951053b7
URL:		http://www.pygame.org/
BuildRequires:	python-devel >= 2.2.1
BuildRequires:	python-numpy-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel >= 2.0
BuildRequires:	smpeg-devel
%pyrequires_eq	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pygame is a set of Python modules designed for writing games. It is
written on top of the excellent SDL library. This allows you to create
fully featured games and multimedia programs in the python language.
The package is highly portable, with games running on Windows, NT4,
MacOS, OSX, BeOS, FreeBSD, IRIX, and Linux.

%description -l pl
Pygame jest zbiorem modu³ów Pythona zaprojektowanych do pisania gier.
Modu³y te zosta³y napisane na bazie wspania³ej biblioteki SDL. Dziêki
temu mo¿liwe jest tworzenie bogatych w multimedia gier w jêzyku
Python.

%package devel
Summary:	C header files for pygame modules
Summary(pl):	Pliki nag³ówkowe jêzyka C modu³ów pygame
Group:		Development/Languages/Python
%pyrequires_eq	python
Requires:	%{name} = %{version}

%description devel
C header files for pygame modules.

%description devel -l pl
Pliki nag³ówkowe jêzyka C modu³ów pygame.

%prep
%setup -q -n %{module}-%{version}release

%build
CFLAGS="%{rpmcflags} -I%{_prefix}/X11R6/include/smpeg"; export CFLAGS
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

python setup.py install \
	--root=$RPM_BUILD_ROOT

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc WHATSNEW docs/*
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.ttf
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py[co]

%files devel
%defattr(644,root,root,755)
%{py_incdir}/%{module}
%{_examplesdir}/%{name}-%{version}
