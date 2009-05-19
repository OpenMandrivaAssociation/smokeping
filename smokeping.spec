%define name	smokeping
%define version 2.4.2
%define release %mkrel 3

%define _requires_exceptions perl(\\(Authen::.*\\|Smokeping.*\\))
%define _provides_exceptions perl(.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Network latency tracker
License:	GPL
Group:		Networking/WWW
URL:		http://oss.oetiker.ch/smokeping/
Source:     http://oss.oetiker.ch/smokeping/pub/%{name}-%{version}.tar.gz
Patch0:     %{name}-2.4.2-fhs.patch
requires:   rrdtool
requires:   fping
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16
Requires(postun):	rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
SmokePing keeps track of your network latency:

    * Best of breed latency visualisation.
    * Interactive graph exlorer.
    * Wide range of latency measurment plugins.
    * Master/Slave System for distributed measurement.
    * Highly configurable alerting system.
    * Live Latency Charts with the most 'interesting' graphs.
    * Free and OpenSource Software written in Perl written by Tobi Oetiker, the
      creator of MRTG and RRDtool

%prep
%setup -q
%patch0 -p 1

find lib -name *.pm | xargs chmod 644

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_bindir}
install -m 755 bin/smokeping.dist %{buildroot}%{_bindir}/smokeping
install -m 755 bin/tSmoke.dist %{buildroot}%{_bindir}/tSmoke

install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -m 755 htdocs/smokeping.cgi.dist \
    %{buildroot}%{_var}/www/%{name}/smokeping.cgi
install -m 755 htdocs/tr.cgi.dist \
    %{buildroot}%{_var}/www/%{name}/tr.cgi
install -m 644 htdocs/tr.html \
    %{buildroot}%{_var}/www/%{name}/tr.html
cp -pr htdocs/cropper %{buildroot}%{_var}/www/%{name}
cp -pr htdocs/resource %{buildroot}%{_var}/www/%{name}
cp -pr htdocs/script %{buildroot}%{_var}/www/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr lib %{buildroot}%{_datadir}/%{name}

# drop private libraries
rm -rf %{buildroot}%{_datadir}/%{name}/lib/BER.pm
rm -rf %{buildroot}%{_datadir}/%{name}/lib/CGI
rm -rf %{buildroot}%{_datadir}/%{name}/lib/Config
rm -rf %{buildroot}%{_datadir}/%{name}/lib/Digest
rm -rf %{buildroot}%{_datadir}/%{name}/lib/JSON*
rm -rf %{buildroot}%{_datadir}/%{name}/lib/SNMP_*

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/basepage.html.dist \
    %{buildroot}%{_sysconfdir}/%{name}/basepage.html
install -m 644 etc/config.dist \
    %{buildroot}%{_sysconfdir}/%{name}/config
install -m 644 etc/smokemail.dist \
    %{buildroot}%{_sysconfdir}/%{name}/smokemail
install -m 640 etc/smokeping_secrets.dist \
    %{buildroot}%{_sysconfdir}/%{name}/smokeping_secrets
install -m 644 etc/tmail.dist \
    %{buildroot}%{_sysconfdir}/%{name}/tmail

install -d -m 755 %{buildroot}%{_var}/cache/%{name}
install -d -m 755 %{buildroot}%{_var}/lib/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
    Options ExecCGI
    DirectoryIndex smokeping.cgi
    Allow from all
</Directory>
EOF

%clean
rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%doc README TODO CHANGES CONTRIBUTORS COPYING COPYRIGHT doc
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_var}/www/%{name}
%{_bindir}/%{name}
%{_bindir}/tSmoke
%{_datadir}/%{name}
%{_var}/cache/%{name}
%{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/basepage.html
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/smokemail
%config(noreplace) %{_sysconfdir}/%{name}/tmail
%config(noreplace) %attr(-,root,apache) %{_sysconfdir}/%{name}/smokeping_secrets

