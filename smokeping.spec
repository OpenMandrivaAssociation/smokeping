%define __noautoreq 'perl\\(Authen::.*|perl\\(Smokeping.*'
%define __noautoprov perl(.*)

Name:		smokeping
Version:	2.4.2
Release:	15
Summary:	Network latency tracker
License:	GPL
Group:		Networking/WWW
URL:		http://oss.oetiker.ch/smokeping/
Source0:    http://oss.oetiker.ch/smokeping/pub/%{name}-%{version}.tar.gz
Source1:    smokeping.init
Patch0:     %{name}-2.4.2-fhs.patch
Requires:   rrdtool
Requires:   fonts-ttf-dejavu
Requires:   fping
Requires:   perl(Qooxdoo::JSONRPC)
Requires:   perl(Config::Grammar)
Requires:   apache
# webapp macros and scriptlets
Requires(post):		rpm-helper >= 0.16
Requires(postun):	rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	rpm-mandriva-setup >= 1.23
BuildArch:	noarch

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

install -d -m 755 %{buildroot}%{_datadir}/%{name}/www
install -m 755 htdocs/smokeping.cgi.dist \
    %{buildroot}%{_datadir}/%{name}/www/smokeping.cgi
install -m 755 htdocs/tr.cgi.dist \
    %{buildroot}%{_datadir}/%{name}/www/tr.cgi
install -m 644 htdocs/tr.html \
    %{buildroot}%{_datadir}/%{name}/www/tr.html
cp -pr htdocs/cropper %{buildroot}%{_datadir}/%{name}/www
cp -pr htdocs/resource %{buildroot}%{_datadir}/%{name}/www
cp -pr htdocs/script %{buildroot}%{_datadir}/%{name}/www

install -d -m 755 %{buildroot}%{_datadir}/%{name}/lib
cp -pr lib/Smokeping* %{buildroot}%{_datadir}/%{name}/lib

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
Alias /%{name}/cache %{_localstatedir}/cache/%{name}
Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
    Options ExecCGI
    DirectoryIndex smokeping.cgi
    Require all granted
</Directory>

<Directory %{_localstatedir}/cache/%{name}>
    Require all granted
</Directory>
EOF

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/smokeping

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%doc README TODO CHANGES CONTRIBUTORS COPYING COPYRIGHT doc
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/tSmoke
%{_datadir}/%{name}
%attr(-,apache,apache) %{_var}/cache/%{name}
%{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/basepage.html
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/smokemail
%config(noreplace) %{_sysconfdir}/%{name}/tmail
%config(noreplace) %attr(-,root,apache) %{_sysconfdir}/%{name}/smokeping_secrets



%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-11mdv2011.0
+ Revision: 614926
- the mass rebuild of 2010.1 packages

* Tue Jan 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-10mdv2010.1
+ Revision: 493885
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Mon Oct 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-9mdv2010.0
+ Revision: 454033
- yet another dependency fix

* Tue Sep 29 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-8mdv2010.0
+ Revision: 450935
- requires apache

* Wed Sep 16 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-7mdv2010.0
+ Revision: 443524
- fix typo in apache configuration file

* Wed Sep 16 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-6mdv2010.0
+ Revision: 443522
- fix apache configuration for generated files
- font dependency
- ship init script
- proper perms on cache directory

* Wed Jul 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-4mdv2010.0
+ Revision: 396458
- move web files under %%{_datadir}/%%{name}/www
- drop last remaining private perl library, packaged separatly

* Wed May 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-3mdv2010.0
+ Revision: 377835
- really fix dependencies

* Mon May 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-2mdv2010.0
+ Revision: 371917
- drop private copies of perl modules

* Sun Oct 12 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-1mdv2009.1
+ Revision: 292954
- import smokeping


* Sun Oct 12 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.2-1mdv2009.1
- first mdv release 
