%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name XStatic-Json2yaml

Name:           python-%{pypi_name}
Version:        0.1.1.0
Release:        1%{?dist}
Provides:       python2-%{pypi_name} = %{version}-%{release}
Summary:        Json2yaml (XStatic packaging standard)

License:        MIT
URL:            https://github.com/jeffsu/json2yaml
Source0:        https://files.pythonhosted.org/packages/source/X/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-XStatic
Requires:       xstatic-json2yaml-common


%description
Json2yaml JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.


%package -n xstatic-json2yaml-common
Summary:        %{summary}

BuildRequires:  web-assets-devel
Requires:       web-assets-filesystem

%description -n xstatic-json2yaml-common
Json2yaml JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.

This package contains the JavaScript files.


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-XStatic
Requires:       xstatic-json2yaml-common

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Json2yaml JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.

This package provides Python 3 build of %{pypi_name}.
%endif


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Patch to use webassets directory
sed -i "s|^BASE_DIR = .*|BASE_DIR = '%{_jsdir}/json2yaml'|" xstatic/pkg/json2yaml/__init__.py


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif


%install
%py2_install
mkdir -p %{buildroot}/%{_jsdir}/json2yaml
mv %{buildroot}/%{python2_sitelib}/xstatic/pkg/json2yaml/data/json2yaml.js %{buildroot}/%{_jsdir}/json2yaml
rmdir %{buildroot}%{python2_sitelib}/xstatic/pkg/json2yaml/data/

%if 0%{?with_python3}
%py3_install
# Remove static files, already created by the python2 subpkg
rm -rf %{buildroot}%{python3_sitelib}/xstatic/pkg/json2yaml/data/
%endif


%files -n python-%{pypi_name}
%doc README.txt
%{python2_sitelib}/xstatic/pkg/json2yaml
%{python2_sitelib}/XStatic_Json2yaml-%{version}-py%{python_version}.egg-info
%{python2_sitelib}/XStatic_Json2yaml-%{version}-py%{python_version}-nspkg.pth

%files -n xstatic-json2yaml-common
%doc README.txt
%{_jsdir}/json2yaml

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%{python3_sitelib}/xstatic/pkg/json2yaml
%{python3_sitelib}/XStatic_Json2yaml-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/XStatic_Json2yaml-%{version}-py%{python3_version}-nspkg.pth
%endif


%changelog
* Thu Jul 12 2018 Radomir Dopieralski <rdopiera@redhat.com) - 0.1.1.0-1
- Initial package
