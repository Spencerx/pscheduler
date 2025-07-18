#
# RPM Spec for Python pScheduler Module
#

%define perfsonar_auto_version 5.2.1
%define perfsonar_auto_relnum 1

%define short	pscheduler
Name:		%{_pscheduler_python}-%{short}
Version:	%{perfsonar_auto_version}
Release:	%{perfsonar_auto_relnum}%{?dist}
Summary:	Utility functions for pScheduler
BuildArch:	noarch
License:        ASL 2.0	
Group:		Development/Libraries

Provides:	%{name} = %{version}-%{release}
Prefix:		%{_prefix}

Vendor:		perfSONAR
Url:		http://www.perfsonar.net

Source0:	%{short}-%{version}.tar.gz

# NOTE: The runtime Python module requirements must be duplicated in
# BuildRequires because they're required to run the tests.

Requires:	iputils

Requires:	%{_pscheduler_python}-attrs
Requires:	%{_pscheduler_python}-dateutil
Requires:	%{_pscheduler_python}-dns
Requires:	%{_pscheduler_python}-isodate
Requires:	%{_pscheduler_python}-jinja2
Requires:	%{_pscheduler_python}-jsonschema >= 3.0
Requires:	%{_pscheduler_python}-netaddr
Requires:	%{_pscheduler_python}-netifaces
Requires:	%{_pscheduler_python}-ntplib
Requires:	%{_pscheduler_python}-psutil
Requires:	%{_pscheduler_python}-psycopg2 >= 2.6.1
Requires:	%{_pscheduler_python}-py-radix
# The limit system uses this.
Requires:	pscheduler-jq-library
Requires:	%{_pscheduler_python}-pycurl
Requires:	%{_pscheduler_python}-pyjq >= 2.2.0
Requires:	%{_pscheduler_python}-tzlocal
Requires:	%{_pscheduler_python}-pytz
Requires:	rsyslog
Requires:	logrotate
Requires:       numactl
Requires:	traceroute
Requires:	rpm-post-wrapper

BuildRequires:	pscheduler-rpm
BuildRequires:  %{_pscheduler_python}
BuildRequires:	%{_pscheduler_python}-coverage
BuildRequires:	%{_pscheduler_python}-nose
BuildRequires:	%{_pscheduler_python}-setuptools
# NOTE:  Cloned from above.
BuildRequires:	iputils
BuildRequires:	%{_pscheduler_python}-attrs
BuildRequires:	%{_pscheduler_python}-dateutil
BuildRequires:	%{_pscheduler_python}-dns
BuildRequires:	%{_pscheduler_python}-isodate
BuildRequires:	%{_pscheduler_python}-jsonschema
BuildRequires:	%{_pscheduler_python}-netaddr
BuildRequires:	%{_pscheduler_python}-netifaces
BuildRequires:	%{_pscheduler_python}-ntplib
BuildRequires:	%{_pscheduler_python}-psutil
BuildRequires:	%{_pscheduler_python}-psycopg2 >= 2.2.0
BuildRequires:	%{_pscheduler_python}-py-radix
# The limit system uses this.
BuildRequires:	pscheduler-jq-library
BuildRequires:	%{_pscheduler_python}-pycurl
BuildRequires:	%{_pscheduler_python}-pyjq >= 2.2.0
BuildRequires:	%{_pscheduler_python}-tzlocal
BuildRequires:	%{_pscheduler_python}-pytz
BuildRequires:  numactl
BuildRequires:  traceroute

%define limit_config %{_pscheduler_sysconfdir}/limits.conf
%define logdir %{_var}/log/pscheduler
%define logfile pscheduler.log
%define logrotate_d %{_sysconfdir}/logrotate.d
%define syslog_d %{_sysconfdir}/rsyslog.d

%define macros %{_pscheduler_rpmmacroprefix}%{name}


%description
Utility functions for pScheduler


# Don't do automagic post-build things.
%global              __os_install_post %{nil}


%prep
%setup -q -n %{short}-%{version}


%build

make CLASSES="%{_pscheduler_classes}"


%install
%{_pscheduler_python} setup.py install --root=$RPM_BUILD_ROOT -O1  --record=INSTALLED_FILES

mkdir -p $RPM_BUILD_ROOT/%{logrotate_d}
cat > $RPM_BUILD_ROOT/%{logrotate_d}/%{name} <<EOF
# Rotation for logs produced by pScheduler

%{logdir}/%{logfile}
{
    missingok
    sharedscripts
    postrotate
        /bin/kill -HUP \`cat %{_rundir}/syslogd.pid 2> /dev/null\` 2> /dev/null || true
    endscript
}
EOF

mkdir -p $RPM_BUILD_ROOT/%{syslog_d}
cat > $RPM_BUILD_ROOT/%{syslog_d}/%{name}.conf <<EOF
# Syslog configuration for pScheduler

local4.*  %{logdir}/%{logfile}
EOF

mkdir -p $RPM_BUILD_ROOT/%{_pscheduler_rpmmacrodir}
cat > $RPM_BUILD_ROOT/%{macros} <<EOF
#
# RPM Macros for %{name} Version %{version}
#

%%_pscheduler_limit_config %{limit_config}

%%_pscheduler_log_dir %{logdir}
%%_pscheduler_log_file %{logfile}
EOF



%clean
rm -rf $RPM_BUILD_ROOT

%post
rpm-post-wrapper '%{name}' "$@" <<'POST-WRAPPER-EOF'

# This removes a duplicate entry leftover from the Python 2 version.
# TODO: Remove this after we stop supporting 4.2.x.
OLD_LOGROTATE="%{logrotate_d}/python-pscheduler"
if [ -e "${OLD_LOGROTATE}" ]
then
    cat > "${OLD_LOGROTATE}" <<EOF
# Rotation for logs produced by pScheduler

### Removed forcibly by %{name} %{version} to avoid duplicate
### log file names.
EOF
fi

systemctl enable rsyslog
systemctl reload-or-restart rsyslog
POST-WRAPPER-EOF


%postun
systemctl reload-or-restart rsyslog


%files -f INSTALLED_FILES
%defattr(-,root,root)
%license LICENSE
%config(noreplace) %{logrotate_d}/*
%config(noreplace) %{syslog_d}/*
%attr(444,root,root) %{_pscheduler_rpmmacroprefix}*
