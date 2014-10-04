%define __noautoreq 'perl\\(Authen::.*|perl\\(Smokeping.*'
%define __noautoprov perl(.*)

Summary:          Latency Logging and Graphing System
Name:             smokeping
Version:          2.6.9
Release:          1
License:          GPLv2+
Group:            Networking/WWW
URL:              http://oss.oetiker.ch/smokeping/
Source0:          http://oss.oetiker.ch/smokeping/pub/smokeping-%{version}.tar.gz
Source1:          smokeping.service
Source3:          http://oss.oetiker.ch/smokeping-demo/img/smokeping.png
Source4:          http://oss.oetiker.ch/smokeping-demo/img/rrdtool.png
Source5:          README.urpmi
Source6:          smokeping-tmpfs.conf
Source7:          smokeping-httpd24.conf.d
Patch0:           smokeping-2.6.7-path.patch
Patch1:           smokeping-2.6.7-config.patch
Patch2:           smokeping-2.6.7-silence.patch
Patch3:           smokeping-2.6.7-datadir.patch
Patch4:           smokeping-2.6.8-Escape-solidus-in-POD-link.patch
Patch5:           smokeping-2.6.9-remove-date.patch
BuildRequires:    systemd-units
BuildRequires:    perl(CGI)
BuildRequires:    perl(CGI::Fast)
BuildRequires:    perl(Config::Grammar)
BuildRequires:    perl(Digest::HMAC_MD5)
BuildRequires:    perl(FCGI)
BuildRequires:    perl(File::Basename)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(LWP)
BuildRequires:    perl(Pod::Usage)
BuildRequires:    perl(POSIX)
BuildRequires:    perl(RRDs)
BuildRequires:    perl(SNMP_Session)
BuildRequires:    perl(SNMP_util) >= 1.13
BuildRequires:    perl(strict) 
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Sys::Syslog)
BuildRequires:    perl(URI::Escape)
BuildRequires:    perl(vars)
#BuildRequires:    pod2man
BuildRequires:    automake
BuildRequires:    autoconf
Requires:         perl >= 5.6.1
Requires:         rrdtool >= 1.0.33
Requires:         fping >= 2.4b2
Requires:         traceroute
# Not picked up for some reason
Requires:         perl(Config::Grammar)
Requires:         perl(SNMP_util) >= 1.13
# only httpd supported without config changes
Requires:         apache
Requires:         apache-mod_fcgid
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
BuildArch:        noarch

%description
SmokePing is a latency logging and graphing system. It consists of a
daemon process which organizes the latency measurements and a CGI
which presents the graphs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

install -p -m 0644 %{SOURCE5} . 
iconv -f ISO-8859-1 -t utf-8 -o CHANGES.utf8 CHANGES
touch -r CHANGES CHANGES.utf8 
mv CHANGES.utf8 CHANGES

# remove some external modules
rm -f lib/{SNMP_Session,SNMP_util,BER}.pm

%build
autoreconf -fi
automake
autoconf
%configure --with-htdocs-dir=%{_datadir}/%{name}/htdocs \
           --disable-silent-rules

%install
%make install DESTDIR=%{buildroot}

# Some additional dirs and files
install -d %{buildroot}%{_localstatedir}/lib/%{name}/{rrd,images} \
                %{buildroot}%{_localstatedir}/run/%{name} \
                %{buildroot}%{_datadir}/%{name}/cgi
install -Dp -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -Dp -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install  -p -m 0644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_datadir}/%{name}/htdocs
install -Dp -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

# Fix some files
for f in config basepage.html smokemail tmail smokeping_secrets ; do
    mv %{buildroot}%{_sysconfdir}/%{name}/$f.dist \
            %{buildroot}%{_sysconfdir}/%{name}/$f
done
mv %{buildroot}%{_sysconfdir}/%{name}/examples __examples
mv %{buildroot}%{_bindir}/%{name}_cgi %{buildroot}%{_datadir}/%{name}/cgi
ln -s %{name}_cgi %{buildroot}%{_datadir}/%{name}/cgi/%{name}.fcgi
rm -f %{buildroot}%{_datadir}/%{name}/htdocs/smokeping.fcgi.dist

%post
%systemd_post smokeping.service

%preun
%systemd_preun smokeping.service

%postun
%systemd_postun_with_restart smokeping.service

%files
%doc CHANGES CONTRIBUTORS COPYRIGHT LICENSE README TODO README.urpmi
%doc __examples/*
%{_sbindir}/%{name}
%{_bindir}/smokeinfo
%{_bindir}/tSmoke
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%attr(0640, root, apache) %config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/basepage.html
%config(noreplace) %{_sysconfdir}/%{name}/smokemail
%attr(0640, root, root) %config(noreplace) %{_sysconfdir}/%{name}/smokeping_secrets
%config(noreplace) %{_sysconfdir}/%{name}/tmail
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/rrd
%{_localstatedir}/run/%{name}
%attr(0755, apache, root) %{_localstatedir}/lib/%{name}/images
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man1/tSmoke.1*
%{_mandir}/man3/Smokeping_*.3*
%{_mandir}/man5/%{name}_*.5*
%{_mandir}/man7/%{name}_*.7*

