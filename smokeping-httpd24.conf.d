<Directory "/usr/share/smokeping" >
  Require local
  # Require ip 2.5.6.8
  # Require host example.org
</Directory>

<Directory "/var/lib/smokeping" >
  Require local
  # Require ip 2.5.6.8
  # Require host example.org
</Directory>

# .fcgi : smokeping by mod_fcgid aka fastcgi
# _cgi  : plain old fashion cgi
ScriptAlias /smokeping/sm.cgi  /usr/share/smokeping/cgi/smokeping.fcgi
#ScriptAlias /smokeping/sm.cgi  /usr/share/smokeping/cgi/smokeping_cgi

Alias       /smokeping/images  /var/lib/smokeping/images
Alias       /smokeping         /usr/share/smokeping/htdocs
