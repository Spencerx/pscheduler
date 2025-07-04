#
# RPM Spec for pScheduler Ping Tool
#

#TODO: Requires pscheduler version >= 5.0 for ping parsing

%define short	ping
%define perfsonar_auto_version 5.2.1
%define perfsonar_auto_relnum 1

Name:		pscheduler-tool-%{short}
Version:	%{perfsonar_auto_version}
Release:	%{perfsonar_auto_relnum}%{?dist}

Summary:	pScheduler Ping Tool
BuildArch:	noarch
License:	ASL 2.0
Vendor:	perfSONAR
Group:		Unspecified

Source0:	%{short}-%{version}.tar.gz

Provides:	%{name} = %{version}-%{release}

Requires:	pscheduler-server >= 4.3.0
Requires:	pscheduler-account
Requires:	%{_pscheduler_python}-pscheduler >= 4.3.0
Requires:	pscheduler-test-rtt
Requires:	%{_pscheduler_python}-icmperror
# This supplies ping.
Requires:	iputils
# For setcap
Requires:	libcap
Requires:	sudo
Requires:	rpm-post-wrapper

BuildRequires:	pscheduler-account
BuildRequires:	pscheduler-rpm
BuildRequires:	iputils


%description
pScheduler Ping Tool


%prep
%setup -q -n %{short}-%{version}


%define dest %{_pscheduler_tool_libexec}/%{short}

%install
make \
     DESTDIR=$RPM_BUILD_ROOT/%{dest} \
     install


# Enable sudo for ping

PING=$(command -v ping)

mkdir -p $RPM_BUILD_ROOT/%{_pscheduler_sudoersdir}
cat > $RPM_BUILD_ROOT/%{_pscheduler_sudoersdir}/%{name} <<EOF
#
# %{name}
#
Cmnd_Alias PSCHEDULER_TOOL_PING = ${PING}
%{_pscheduler_user} ALL = (root) NOPASSWD: ${PING}
Defaults!PSCHEDULER_TOOL_PING !requiretty


EOF


%post
rpm-post-wrapper '%{name}' "$@" <<'POST-WRAPPER-EOF'

# Make sure whatever ping is authorized in sudoers.d can send raw
# packets without being root.

PING=$(awk '$1 == "Cmnd_Alias" && $2 == "PSCHEDULER_TOOL_PING" { print $4 }' \
	   %{_pscheduler_sudoersdir}/%{name})

if [ -x "${PING}" ]
then
    setcap cap_net_raw+p "${PING}"
else
    echo "Can't find executable ping '${PING}'"
    exit 1
fi


pscheduler internal warmboot
POST-WRAPPER-EOF

%postun
pscheduler internal warmboot


%files
%defattr(-,root,root,-)
%license LICENSE
%{dest}
%attr(440,root,root) %{_pscheduler_sudoersdir}/*
