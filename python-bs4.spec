#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	bs4
Summary:	beautifulsoup4 - Screen-scraping library
Summary(pl.UTF-8):	beautifulsoup4 - biblioteka przechwytująca wyjście
Name:		python-%{module}
# keep 4.9.x here for python2 support
Version:	4.9.3
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/beautifulsoup4/
Source0:	https://files.pythonhosted.org/packages/source/b/beautifulsoup4/beautifulsoup4-%{version}.tar.gz
# Source0-md5:	57fd468ae3eb055f6871106e8f7813e2
Patch0:		test_suite.patch
Patch2:		%{name}-smart_quotes.patch
URL:		https://www.crummy.com/software/BeautifulSoup/
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-soupsieve >= 1.2
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Beautiful Soup sits atop an HTML or XML parser, providing Pythonic
idioms for iterating, searching, and modifying the parse tree.

%description -l pl.UTF-8
Beautiful Soup rezyduje powyżej parsera HTML lub XML, zapewniając
pythonowe idiomy do iterowania, wyszukiwania i modyfikowania drzewa
analizy.

%package apidocs
Summary:	API documentation for Python beautifulsoup4 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona beautifulsoup4
Group:		Documentation

%description apidocs
API documentation for Python beautifulsoup4 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona beautifulsoup4.

%prep
%setup -q -n beautifulsoup4-%{version}
%patch -P 0 -p1
%patch -P 2 -p1

# no longer supported by setuptools
%{__sed} -i -e '/use_2to3/d' setup.py

%build
%py_build

%if %{with tests}
%{__python} -m unittest discover -s bs4
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/bs4/tests
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING.txt NEWS.txt README.md TODO.txt
%{py_sitescriptdir}/bs4
%{py_sitescriptdir}/beautifulsoup4-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_images,_static,*.html,*.js}
%endif
