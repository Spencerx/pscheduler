#
# RPM Spec for pScheduler Latency Background Test
#

%define short	latencybg
%define perfsonar_auto_version 5.2.1
%define perfsonar_auto_relnum 1

Name:		pscheduler-test-%{short}
Version:	%{perfsonar_auto_version}
Release:	%{perfsonar_auto_relnum}%{?dist}

Summary:	Latency Background test class for pScheduler
BuildArch:	noarch
License:	ASL 2.0
Vendor:	perfSONAR
Group:		Unspecified

Source0:	%{short}-%{version}.tar.gz

Provides:	%{name} = %{version}-%{release}

Requires:	pscheduler-server
Requires:	%{_pscheduler_python}-pscheduler
Requires:	rpm-post-wrapper

BuildRequires:	pscheduler-rpm
BuildRequires:	%{_pscheduler_python}-pscheduler
BuildRequires:  %{_pscheduler_python}-nose

%description
Latency test class for pScheduler that runs in the background.


%prep
%setup -q -n %{short}-%{version}


%define dest %{_pscheduler_test_libexec}/%{short}

%build
make \
     PYTHON=%{_pscheduler_python} \
     DESTDIR=$RPM_BUILD_ROOT/%{dest} \
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

