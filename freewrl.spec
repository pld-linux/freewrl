%include	/usr/lib/rpm/macros.perl
Summary:	FreeWRL - VRML browser
Summary(pl):	FreeWRL - przeglądarka VRML
Name:		freewrl
Version:	0.37
Release:	1
License:	LGPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/freewrl/FreeWRL-%{version}.tar.gz
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
BuildRequires:	gtk+-devel
BuildRequires:	jdk
BuildRequires:	js-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
BuildRequires:	saxon
# not found by perlprov from rpm 4.1
Provides:	perl(VRML::Config)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozilladir	/usr/X11R6/lib/mozilla
%define		netscapedir	/usr/X11R6/lib/netscape

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
# false positives found by perlreq from rpm 4.1
%define		_noautoreq	'perl(VRML::Events)' 'perl(VRML::VRMLCU)' 'perl(VRML::VRMLFields)' 'perl(VRML::VRMLNodes)' 'perl(VRMLFields)' 'perl(VRMLNodes)' 'perl(VRMLRend)'

%description
FreeWRL - VRML browser.

%description -l pl
FreeWRL - przeglądarka VRML.

%package -n mozilla-plugin-freewrl
Summary:	VRML plugin for Mozilla WWW browser
Summary(pl):	Wtyczka VRML dla przeglądarki WWW Mozilla
Group:		Libraries

%description -n mozilla-plugin-freewrl
VRML plugin for Mozilla WWW browser.

%description -n mozilla-plugin-freewrl -l pl
Wtyczka VRML dla przeglądarki WWW Mozilla.

%package -n netscape-plugin-freewrl
Summary:	VRML plugin for Netscape WWW browser
Summary(pl):	Wtyczka VRML dla przeglądarki WWW Netscape
Group:		Libraries

%description -n netscape-plugin-freewrl
VRML plugin for Netscape WWW browser.

%description -n netscape-plugin-freewrl -l pl
Wtyczka VRML dla przeglądarki WWW Netscape.

%prep
%setup -q -n FreeWRL-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
perl Makefile.PL
%{__make} \
	OPTIMIZE="%{rpmcflags}" \
	OPTIMIZER="%{rpmcflags}" \
	MOZILLA_INC="/usr/X11R6/include/mozilla"

%{__make} -C Plugin/netscape \
	OPTIMIZER="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{mozilladir}/{plugins,java/classes},%{netscapedir}/plugins}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install Plugin/mozilla/_lib/npFreeWRL.so $RPM_BUILD_ROOT%{mozilladir}/plugins
install Plugin/netscape/_lib/npfreewrl.so $RPM_BUILD_ROOT%{netscapedir}/plugins

install java/classes/vrml.jar $RPM_BUILD_ROOT%{mozilladir}/java/classes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* TODO* ARCHITECTURE* CONFORMANCE*
%attr(755,root,root) %{_bindir}/*
%{perl_sitearch}/VRML
%dir %{perl_sitearch}/auto/VRML
%dir %{perl_sitearch}/auto/VRML/*
%{perl_sitearch}/auto/VRML/*/*.bs
%attr(755,root,root) %{perl_sitearch}/auto/VRML/*/*.so
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%files -n mozilla-plugin-freewrl
%defattr(644,root,root,755)
%{mozilladir}/java/classes/*
%{mozilladir}/plugins/*

%files -n netscape-plugin-freewrl
%defattr(644,root,root,755)
%{netscapedir}/java/classes/*
%{netscapedir}/plugins/*
