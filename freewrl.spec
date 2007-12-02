# TODO:
# - install fonts system-wide (subpackage?)
# - CC not always honoured
# - ?? add more to optimize.patch
%include	/usr/lib/rpm/macros.perl
%define		pdir	VRML
%define		pnam	VRMLFunc
Summary:	FreeWRL - VRML/X3D browser
Summary(pl.UTF-8):	FreeWRL - przeglądarka VRM/X3D
Name:		freewrl
Version:	1.19.8
Release:	0.1
License:	LGPL
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/freewrl/%{name}-%{version}.tar.gz
# Source0-md5:	c193a1eb6e88c4253b6aec02098a9d3c
Patch0:		%{name}-config.patch
Patch1:		%{name}-makefile.patch
#Patch2:		%{name}-system-js.patch
#Patch3:		%{name}-optimize.patch
URL:		http://freewrl.sourceforge.net/
BuildRequires:	ImageMagick-devel
BuildRequires:	OpenGL-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	java-sun
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	openmotif-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.236
BuildRequires:	saxon
BuildRequires:	xorg-lib-libXaw-devel
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Provides:	libFreeWRLFunc.so()(64-bit)
%else
Provides:	libFreeWRLFunc.so
%endif
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		browsers mozilla, mozilla-firefox, konqueror, seamonkey

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
# false positives found by perlreq from rpm 4.1
%define		_noautoreq	'perl(VRML::Events)' 'perl(VRML::VRMLCU)' 'perl(VRML::VRMLFields)' 'perl(VRML::VRMLNodes)' 'perl(VRMLFields)' 'perl(VRMLNodes)' 'perl(VRMLRend)'

%description
FreeWRL - VRML/X3D browser.

%description -l pl.UTF-8
FreeWRL - przeglądarka VRM/X3D.

%package -n browser-plugin-%{name}
Summary:	VRML/X3D plugin for WWW browser
Summary(pl.UTF-8):	Wtyczka VRML/X3D dla przeglądarki WWW
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins(%{_target_base_arch})
Obsoletes:	konqueror-plugin-freewrl
Obsoletes:	mozilla-firefox-plugin-freewrl
Obsoletes:	mozilla-plugin-freewrl
Obsoletes:	netscape-plugin-freewrl

%description -n browser-plugin-%{name}
VRML and X3D plugin for WWW browser.

Supported browsers: %{browsers}.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka VRML i X3D dla przeglądarki WW.

Obsługiwane przeglądarki: %{browsers}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#%patch2 -p1
#%patch3 -p1

# this file causes unnecessary/unwanted rebuilds of JS module
rm -f JS/Makefile.aqua.PL
%{__sed} -i -e 's#\(NETSCAPE_\(INST\|CLASSES\|PLUGINS\)\) =>.*#\1 => "%{_browserpluginsdir}",#' vrml.conf*

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_browserpluginsdir},%{perl_vendorlib}/VRML}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SITEARCHEXP=$RPM_BUILD_ROOT%{perl_vendorarch} \
	DESTINSTALLPRIVLIB=$RPM_BUILD_ROOT%{perl_vendorlib} \
	PLUGDIR=%{_browserpluginsdir}

# specified in java/classes/Makefile.PL, but finally not installed
install java/classes/vrml.jar $RPM_BUILD_ROOT%{perl_vendorlib}/VRML
install java/classes/java.policy $RPM_BUILD_ROOT%{perl_vendorlib}/VRML

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/fonts/{COPYRIGHT,README,RELEASENOTES}.TXT

%clean
rm -rf $RPM_BUILD_ROOT

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc README.html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libFreeWRLFunc.so
%attr(755,root,root) %{_libdir}/libFreeWRLjs.so
%dir %{perl_vendorlib}/VRML
%{perl_vendorlib}/VRML/java.policy
%{perl_vendorlib}/VRML/vrml.jar
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/fonts
%{_datadir}/%{name}/fonts/*.ttf
%{_datadir}/%{name}/fonts/*.conf
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/*.so
%attr(755,root,root) %{_browserpluginsdir}/vrml.jar
