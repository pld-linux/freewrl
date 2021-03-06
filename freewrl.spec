# TODO:
# - install fonts system-wide (subpackage?)
# - install one copy of vrml.jar
%define		pdir	VRML
%define		pnam	VRMLFunc
Summary:	FreeWRL - VRML/X3D browser
Summary(pl.UTF-8):	FreeWRL - przeglądarka VRM/X3D
Name:		freewrl
Version:	1.19.8
Release:	4
License:	LGPL v2
Group:		X11/Applications/Graphics
Source0:	http://dl.sourceforge.net/freewrl/%{name}-%{version}.tar.gz
# Source0-md5:	c193a1eb6e88c4253b6aec02098a9d3c
Patch0:		%{name}-config.patch
Patch1:		%{name}-makefile.patch
Patch2:		%{name}-system-js.patch
Patch3:		%{name}-optimize.patch
URL:		http://freewrl.sourceforge.net/
BuildRequires:	ImageMagick-devel
BuildRequires:	OpenGL-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	jdk
BuildRequires:	js-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	motif-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	saxon
BuildRequires:	xorg-lib-libXaw-devel
%ifarch %{x8664} ia64 ppc64 s390x sparc64
Provides:	libFreeWRLFunc.so()(64-bit)
%else
Provides:	libFreeWRLFunc.so
%endif
# jdk only these platforms
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
# false positives found by perlreq from rpm 4.1
%define		_noautoreq	'perl(VRML::Events)' 'perl(VRML::VRMLCU)' 'perl(VRML::VRMLFields)' 'perl(VRML::VRMLNodes)' 'perl(VRMLFields)' 'perl(VRMLNodes)' 'perl(VRMLRend)'

%define		_specflags_x86_64	 -fPIC

%description
FreeWRL - VRML/X3D browser.

%description -l pl.UTF-8
FreeWRL - przeglądarka VRM/X3D.

%package -n browser-plugin-%{name}
Summary:	VRML/X3D plugin for WWW browser
Summary(pl.UTF-8):	Wtyczka VRML/X3D dla przeglądarki WWW
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Obsoletes:	konqueror-plugin-freewrl
Obsoletes:	mozilla-firefox-plugin-freewrl
Obsoletes:	mozilla-plugin-freewrl
Obsoletes:	netscape-plugin-freewrl

%description -n browser-plugin-%{name}
VRML and X3D plugin for WWW browser.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka VRML i X3D dla przeglądarki WW.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# avoid using included js
rm -rf JS

%{__sed} -i -e 's#\(NETSCAPE_\(INST\|CLASSES\|PLUGINS\)\) =>.*#\1 => "%{_browserpluginsdir}",#' vrml.conf*

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} -j1 \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}" \
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
	PLUGDIR=%{_browserpluginsdir} \
	CHCON=true

# specified in java/classes/Makefile.PL, but finally not installed
install java/classes/vrml.jar $RPM_BUILD_ROOT%{perl_vendorlib}/VRML
install java/classes/java.policy $RPM_BUILD_ROOT%{perl_vendorlib}/VRML

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/fonts/{COPYRIGHT,README,RELEASENOTES}.TXT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.html
%attr(755,root,root) %{_bindir}/FreeWRL_Message
%attr(755,root,root) %{_bindir}/FreeWRL_SoundServer
%attr(755,root,root) %{_bindir}/freewrl
%attr(755,root,root) %{_libdir}/libFreeWRLFunc.so
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
%attr(755,root,root) %{_browserpluginsdir}/npfreewrl.so
%{_browserpluginsdir}/vrml.jar
