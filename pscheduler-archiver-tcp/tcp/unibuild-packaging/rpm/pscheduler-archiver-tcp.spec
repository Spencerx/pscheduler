#
# RPM Spec for pScheduler tcp archiver
#

%define short	tcp
%define perfsonar_auto_version 5.2.1
%define perfsonar_auto_relnum 1

Name:		pscheduler-archiver-%{short}
Version:	%{perfsonar_auto_version}
Release:	%{perfsonar_auto_relnum}%{?dist}

Summary:	HTTP archiver class for pScheduler
BuildArch:	noarch
License:	ASL 2.0
Vendor:		perfSONAR
Group:		Unspecified

Source0:	%{short}-%{version}.tar.gz

Provides:	%{name} = %{version}-%{release}

Requires:	pscheduler-server >= 1.1.6.1
Requires:	%{_pscheduler_python}-pscheduler >= 4.4.0
Requires:	rpm-post-wrapper

BuildRequires:	pscheduler-rpm
BuildRequires:  %{_pscheduler_python}
BuildRequires:	%{_pscheduler_python}-nose

%define directory %{_includedir}/make

%description
This archiver sends JSON test results to a TCP socket


%prep
%setup -q -n %{short}-%{version}


%define dest %{_pscheduler_archiver_libexec}/%{short}

%build
make \
     DESTDIR=$RPM_BUILD_ROOT/%{dest} \
     DOCDIR=$RPM_BUILD_ROOT/%{_pscheduler_archiver_doc} \
     install

%post
rpm-post-wrapper '%{name}' "$@" <<'POST-WRAPPER-EOF'
pscheduler internal warmboot
POST-WRAPPER-EOF

%postun
pscheduler internal warmboot

%files
%defattr(-,root,root,-)
%license LICENSE
%{dest}
%{_pscheduler_archiver_doc}/*
