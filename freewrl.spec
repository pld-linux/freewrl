%include	/usr/lib/rpm/macros.perl
Summary:	FreeWRL - VRML browser
Summary(pl):	FreeWRL - przegl±darka VRML
Name:		freewrl
Version:	0.37
Release:	0.1
License:	LGPL
Group:		X11/Applications/Graphics
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/freewrl/FreeWRL-%{version}.tar.gz
Patch0:		%{name}-config.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-mozilla.patch
Patch3:		%{name}-gcc3.patch
Patch4:		%{name}-system-js.patch
URL:		http://freewrl.sourceforge.net/
BuildRequires:	ImageMagick
BuildRequires:	gtk+-devel
BuildRequires:	jdk
BuildRequires:	js-devel
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
BuildRequires:	saxon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozilladir	/usr/X11R6/lib/mozilla
%define		netscapedir	/usr/X11R6/lib/netscape

%description
FreeWRL - VRML browser.

%description -l pl
FreeWRL - przegl±darka VRML.

%package -n mozilla-plugin-freewrl
Summary:	VRML plugin for Mozilla WWW browser
Summary(pl):	Wtyczka VRML dla przegl±darki WWW Mozilla
Group:		Libraries

%description -n mozilla-plugin-freewrl
VRML plugin for Mozilla WWW browser.

%description -n mozilla-plugin-freewrl -l pl
Wtyczka VRML dla przegl±darki WWW Mozilla.

%package -n netscape-plugin-freewrl
Summary:	VRML plugin for Netscape WWW browser
Summary(pl):	Wtyczka VRML dla przegl±darki WWW Netscape
Group:		Libraries

%description -n netscape-plugin-freewrl
VRML plugin for Netscape WWW browser.

%description -n netscape-plugin-freewrl -l pl
Wtyczka VRML dla przegl±darki WWW Netscape.

%prep
%setup -q -n FreeWRL-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CFLAGS="%{rpmcflags} -I/usr/X11R6/include/mozilla"
CXXFLAGS="$CFLAGS"
MOZILLA_INC="-I/usr/X11R6/include/mozilla"
export CFLAGS CXXFLAGS MOZILLA_INC
perl Makefile.PL
%{__make}
%{__make} -C Plugin/netscape

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
