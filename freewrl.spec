# TODO:
# - install fonts system-wide (subpackage?)
# - why not having the plugin in single dir, /usr/lib/nsplugins, and
#   all the browsers symlink there?
#Warning: prerequisite HTML::Parser 2.25 not found.
#Warning: prerequisite LWP 5.47 not found.
#Warning: prerequisite URI 1.04 not found.
%include	/usr/lib/rpm/macros.perl
Summary:	FreeWRL - VRML browser
Summary(pl):	FreeWRL - przegl±darka VRML
Name:		freewrl
Version:	1.03
Release:	3.1
License:	LGPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/freewrl/FreeWRL-%{version}.tar.gz
# Source0-md5:	cb4435f5f64cebd6b0cc5cf831fb186f
Patch0:		%{name}-config.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-mozilla.patch
Patch3:		%{name}-gcc3.patch
Patch4:		%{name}-system-js.patch
URL:		http://freewrl.sourceforge.net/
BuildRequires:	ImageMagick
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	freetype-devel
BuildRequires:	gtk+2-devel
BuildRequires:	jar
BuildRequires:	jdk
BuildRequires:	js-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	mozilla-devel
BuildRequires:	mozilla-embedded(gtk2)
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	saxon
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozilladir	/usr/%{_lib}/mozilla
%define		netscapedir	/usr/%{_lib}/netscape

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
# false positives found by perlreq from rpm 4.1
%define		_noautoreq	'perl(VRML::Events)' 'perl(VRML::VRMLCU)' 'perl(VRML::VRMLFields)' 'perl(VRML::VRMLNodes)' 'perl(VRMLFields)' 'perl(VRMLNodes)' 'perl(VRMLRend)'

%description
FreeWRL - VRML browser.

%description -l pl
FreeWRL - przegl±darka VRML.

%package -n mozilla-plugin-%{name}
Summary:	VRML plugin for Mozilla WWW browser
Summary(pl):	Wtyczka VRML dla przegl±darki WWW Mozilla
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mozilla-embedded(gtk2)

%description -n mozilla-plugin-%{name}
VRML plugin for Mozilla WWW browser.

%description -n mozilla-plugin-%{name} -l pl
Wtyczka VRML dla przegl±darki WWW Mozilla.

%package -n netscape-plugin-%{name}
Summary:	VRML plugin for Netscape WWW browser
Summary(pl):	Wtyczka VRML dla przegl±darki WWW Netscape
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n netscape-plugin-%{name}
VRML plugin for Netscape WWW browser.

%description -n netscape-plugin-%{name} -l pl
Wtyczka VRML dla przegl±darki WWW Netscape.

%package -n mozilla-firefox-plugin-%{name}
Summary:	VRML plugin for Mozilla Firefox browser
Summary(pl):	Wtyczka VRML dla przegl±darki Mozilla Firefox
Group:		Libraries
PreReq:		mozilla-firefox
Requires:	%{name} = %{version}-%{release}

%description -n mozilla-firefox-plugin-%{name}
VRML plugin for Mozilla Firefox browser.

%description -n mozilla-firefox-plugin-%{name} -l pl
Wtyczka VRML dla przegl±darki Mozilla Firefox.

%package -n konqueror-plugin-%{name}
Summary:	VRML plugin for Konqueror browser
Summary(pl):	Wtyczka VRML dla przegl±darki Konqueror
Group:		Libraries
PreReq:		konqueror >= 3.0.8-2.3
Requires:	%{name} = %{version}-%{release}

%description -n konqueror-plugin-%{name}
VRML plugin for Konqueror browser.

%description -n konqueror-plugin-%{name} -l pl
Wtyczka VRML dla przegl±darki Konqueror.

%prep
%setup -q -n FreeWRL-%{version}
%patch0 -p1
%patch1 -p1
# for mozilla plugin - removed intentionaly?
#%patch2 -p1
#%patch3 -p1
%patch4 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}" \
	OPTIMIZER="%{rpmcflags}"
#	MOZILLA_INC="/usr/include/mozilla" \
#	GTK_CONFIG="pkg-config gtk+-2.0"

%{__make} -C Plugin/netscape \
	OPTIMIZER="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{mozilladir}/{plugins,java/classes},%{netscapedir}/plugins} \
	$RPM_BUILD_ROOT%{_libdir}/{mozilla-firefox/plugins,/kde3/plugins/konqueror}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SITEARCHEXP=$RPM_BUILD_ROOT%{perl_vendorarch}

#install Plugin/mozilla/_lib/npFreeWRL.so $RPM_BUILD_ROOT%{mozilladir}/plugins

install Plugin/netscape/_lib/npfreewrl.so $RPM_BUILD_ROOT%{mozilladir}/plugins
install Plugin/netscape/_lib/npfreewrl.so $RPM_BUILD_ROOT%{netscapedir}/plugins

install Plugin/netscape/_lib/*.so $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/plugins
install Plugin/netscape/_lib/*.so $RPM_BUILD_ROOT%{_libdir}/kde3/plugins/konqueror

# no such directory, don't know how to make mozilla+java load this jar
# without placing it in /usr/lib/java/jre/lib/ext :/
#install java/classes/vrml.jar $RPM_BUILD_ROOT%{mozilladir}/java/classes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.html
%attr(755,root,root) %{_bindir}/*
%{perl_vendorarch}/VRML
%dir %{perl_vendorarch}/auto/VRML
%dir %{perl_vendorarch}/auto/VRML/*
%{perl_vendorarch}/auto/VRML/*/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/VRML/*/*.so
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%files -n mozilla-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{mozilladir}/plugins/*.so

%files -n netscape-plugin-%{name}
%defattr(644,root,root,755)
%{netscapedir}/java/classes/*.jar
%attr(755,root,root) %{netscapedir}/plugins/*.so

%files -n mozilla-firefox-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mozilla-firefox/plugins/*.so

%files -n konqueror-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/plugins/konqueror/*.so
