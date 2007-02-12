# TODO:
# - install fonts system-wide (subpackage?)
# - CC not always honoured
# - ?? add more to optimize.patch
%include	/usr/lib/rpm/macros.perl
%define		pdir	VRML
%define		pnam	VRMLFunc
Summary:	FreeWRL - VRML browser
Summary(pl.UTF-8):   FreeWRL - przeglądarka VRML
Name:		freewrl
Version:	1.17.4
Release:	0.2
License:	LGPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/freewrl/%{name}-%{version}.tar.gz
# Source0-md5:	0c4e7d91b51c593d37ca190d112c869e
Patch0:		%{name}-config.patch
Patch1:		%{name}-make.patch
Patch2:		%{name}-system-js.patch
Patch3:		%{name}-optimize.patch
URL:		http://freewrl.sourceforge.net/
BuildRequires:	ImageMagick
BuildRequires:	OpenGL-devel
BuildRequires:	X11-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	jar
BuildRequires:	jdk
BuildRequires:	js-devel
BuildRequires:	lesstif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	mozilla-devel
BuildRequires:	mozilla-embedded(gtk2)
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.236
BuildRequires:	saxon
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Provides:	libFreeWRLFunc.so()(64-bit)
%else
Provides:	libFreeWRLFunc.so
%endif
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins
%define		browsers mozilla, mozilla-firefox, konqueror, seamonkey

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
# false positives found by perlreq from rpm 4.1
%define		_noautoreq	'perl(VRML::Events)' 'perl(VRML::VRMLCU)' 'perl(VRML::VRMLFields)' 'perl(VRML::VRMLNodes)' 'perl(VRMLFields)' 'perl(VRMLNodes)' 'perl(VRMLRend)'

%description
FreeWRL - VRML browser.

%description -l pl.UTF-8
FreeWRL - przeglądarka VRML.

%package -n browser-plugin-%{name}
Summary:	VRML plugin for WWW browser
Summary(pl.UTF-8):   Wtyczka VRML dla przeglądarki WWW
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins(%{_target_base_arch})
Obsoletes:	konqueror-plugin-freewrl
Obsoletes:	mozilla-firefox-plugin-freewrl
Obsoletes:	mozilla-plugin-freewrl
Obsoletes:	netscape-plugin-freewrl

%description -n browser-plugin-%{name}
VRML plugin for Mozilla WWW browser.

Supported browsers: %{browsers}.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka VRML dla przeglądarki WWW Mozilla.

Obsługiwane przeglądarki: %{browsers}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# this file causes unnecessary/unwanted rebuilds of JS module
rm -f JS/Makefile.aqua.PL
%{__sed} -i -e 's#\(NETSCAPE_\(INST\|CLASSES\|PLUGINS\)\) =>.*#\1 => "%{_plugindir}",#' vrml.conf*

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} -j1 \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
	OPTIMIZER="%{rpmcflags}" \
	DESTINSTALLPRIVLIB=%{perl_vendorlib}

%{__make} -C Plugin \
	CC="%{__cc}" \
	OPTIMIZER="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_plugindir},%{perl_vendorlib}/VRML}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SITEARCHEXP=$RPM_BUILD_ROOT%{perl_vendorarch} \
	DESTINSTALLPRIVLIB=$RPM_BUILD_ROOT%{perl_vendorlib} \
	PLUGDIR=%{_plugindir}

# specified in java/classes/Makefile.PL, but finally not installed
install java/classes/vrml.jar $RPM_BUILD_ROOT%{perl_vendorlib}/VRML
install java/classes/java.policy $RPM_BUILD_ROOT%{perl_vendorlib}/VRML

# remove copy, make a symlink
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/VRML/VRMLFunc/libFreeWRLFunc.so
ln -sf %{perl_vendorarch}/auto/VRML/VRMLFunc/VRMLFunc.so $RPM_BUILD_ROOT%{_libdir}/libFreeWRLFunc.so

rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/VRML/fonts/{COPYRIGHT,README,RELEASENOTES}.TXT

%clean
rm -rf $RPM_BUILD_ROOT

%triggerun -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins %{name}.so %{name}.xpi

%triggerin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins %{name}.so %{name}.xpi

%triggerun -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins %{name}.so %{name}.xpi

%triggerin -- konqueror
%nsplugin_install -d %{_libdir}/kde3/plugins/konqueror %{name}.so %{name}.xpi

%triggerun -- konqueror
%nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror %{name}.so %{name}.xpi

%triggerin -- seamonkey
%nsplugin_install -d %{_libdir}/seamonkey/plugins %{name}.so %{name}.xpi

%triggerun -- seamonkey
%nsplugin_uninstall -d %{_libdir}/seamonkey/plugins %{name}.so %{name}.xpi

%files
%defattr(644,root,root,755)
%doc README.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libFreeWRLFunc.so
%attr(755,root,root) %{_libdir}/libFreeWRLjs.so

%dir %{perl_vendorlib}/VRML
%attr(755,root,root) %{perl_vendorlib}/VRML/fw2init.pl
%{perl_vendorlib}/VRML/java.policy
%{perl_vendorlib}/VRML/vrml.jar
%dir %{perl_vendorlib}/VRML/fonts
# Bitstream Amerigo, BauerBodni, Futura fonts
%{perl_vendorlib}/VRML/fonts/*.ttf
%{perl_vendorarch}/VRML
%dir %{perl_vendorarch}/auto/VRML
%dir %{perl_vendorarch}/auto/VRML/*
%{perl_vendorarch}/auto/VRML/*/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/VRML/*/*.so
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/*.so
