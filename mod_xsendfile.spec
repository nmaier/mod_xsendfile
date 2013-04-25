Name: mod_xsendfile
Version: 1.0b1
Summary: Apache2 module that processes X-SENDFILE headers
Release: 1%{?dist}
License: Apache License, Version 2.0
Group: System Environment/Daemons
URL: http://tn123.ath.cx/mod_xsendfile/
Source: http://tn123.ath.cx/mod_xsendfile/mod_xsendfile-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: httpd-devel
BuildRequires: apr-devel
Requires: httpd

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE headers
registered by the original output handler.

If it encounters the presence of such header it will discard all output and
send the file specified by that header instead using Apache internals
including all optimizations like caching-headers and sendfile or mmap if
configured.

It is useful for processing script-output of e.g. php, perl or any cgi.


%prep
%setup

%{__cat} <<EOF >mod_xsendfile.conf
### Load the module
LoadModule xsendfile_module         modules/mod_xsendfile.so

### Enables or disables header processing, default is disabled
XSendFile on

EOF

%build
%{_sbindir}/apxs -c mod_xsendfile.c

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 .libs/mod_xsendfile.so %{buildroot}%{_libdir}/httpd/modules/mod_xsendfile.so
%{__install} -Dp -m0644 mod_xsendfile.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/mod_xsendfile.conf

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc docs/Readme.html
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_xsendfile.conf
%{_libdir}/httpd/modules/mod_xsendfile.so

%changelog
* Thu Apr 25 2013 Yukinari Toyota <xxseyxx@gmail.com> - 0.1.0b1
- Initial spec file creation.
