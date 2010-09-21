Name:		mod_xsendfile
Version:	0.11.1
Release:	1%{?dist}
Summary:	A small Apache2 module that processes X-SENDFILE headers

Group:		System Environment/Daemons
License:	Apache
URL:		http://tn123.ath.cx/mod_xsendfile/
Source0:	http://tn123.ath.cx/mod_xsendfile/mod_xsendfile-0.11.1.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	httpd-devel
Requires:	httpd

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE
headers registered by the original output handler.

If it encounters the presence of such header it will discard all
output and send the file specified by that header instead using Apache
internals including all optimizations like caching-headers and
sendfile or mmap if configured.

It is useful for processing script-output of e.g. php, perl or any
cgi.

%prep
%setup -q


%build
apxs -c mod_xsendfile.c


%install
rm -rf $RPM_BUILD_ROOT
LEXEC=$(apxs -q LIBEXECDIR)
install -d -m 0755 "${RPM_BUILD_ROOT}${LEXEC}"
apxs -S LIBEXECDIR="${RPM_BUILD_ROOT}${LEXEC}" -i mod_xsendfile.la

install -d -m 0755 "${RPM_BUILD_ROOT}/%{_docdir}/%{name}-%{version}"
install -m 0644 docs/* "${RPM_BUILD_ROOT}/%{_docdir}/%{name}-%{version}"

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_xsendfile.so
%doc
%{_docdir}/%{name}-%{version}

%post
# add the module to the config file, but leave it commented out (if possible)
APXS=`which apxs 2>/dev/null`

if [ -n "$APXS" -a -x "$APXS" ]; then
   apxs -e -A -n xsendfile mod_xsendfile.so
fi

%preun
# comment out the module before we remove it.
APXS=`which apxs 2>/dev/null`

if [ -n "$APXS" -a -x "$APXS" ]; then
   apxs -e -A -n xsendfile mod_xsendfile.so
fi


%changelog
* Tue Sep 21 2010 Ben Walton <bwalton@artsci.utoronto.ca> - 0.11.1-1
- Initial spec file creation.
