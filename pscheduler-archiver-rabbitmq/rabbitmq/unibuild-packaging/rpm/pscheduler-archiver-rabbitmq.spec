#
# RPM Spec for pScheduler RabbitMQ Archiver
#

%define short	rabbitmq
%define perfsonar_auto_version 5.2.1
%define perfsonar_auto_relnum 1

Name:		pscheduler-archiver-%{short}
Version:	%{perfsonar_auto_version}
Release:	%{perfsonar_auto_relnum}%{?dist}

Summary:	RabbitMQ archiver class for pScheduler
BuildArch:	noarch
License:	ASL 2.0
Vendor:	perfSONAR
Group:		Unspecified

Source0:	%{short}-%{version}.tar.gz

Provides:	%{name} = %{version}-%{release}

Requires:	pscheduler-server >= 1.1.6
Requires:	%{_pscheduler_python}-pscheduler >= 1.3.7.3
Requires:	%{_pscheduler_python}-py-amqp >= 5.0.6
Requires:	%{_pscheduler_python}-vine >= 5.0.0
Requires:	rpm-post-wrapper

BuildRequires:	pscheduler-rpm


%description
This archiver sends JSON test results to RabbitMQ


%prep
%setup -q -n %{short}-%{version}


%define dest %{_pscheduler_archiver_libexec}/%{short}

%build
make \
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
