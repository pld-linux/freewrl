%include	/usr/lib/rpm/macros.perl
Summary:	-
Summary(pl):	-
Name:		freewrl
# note: there is 0.35 on ftp
Version:	0.34
Release:	0.1
License:	LGPL
Group:		-
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/freewrl/FreeWRL-%{version}.tar.gz
Patch0:		%{name}-config.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-mozilla.patch
URL:		http://freewrl.sourceforge.net/
BuildRequires:	ImageMagick
BuildRequires:	binutils-static
BuildRequires:	gtk+-devel
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
BuildRequires:	saxon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozilladir	/usr/X11R6/lib/mozilla
%define		netscapedir	/usr/X11R6/lib/netscape

%description

%description -l pl

%package -n netscape-plugin-freewrl
Summary:	-
Summary(pl):	-
Group:		-

%description -n netscape-plugin-freewrl

%description -n netscape-plugin-freewrl -l pl

%package -n mozilla-plugin-freewrl
Summary:	-
Summary(pl):	-
Group:		-

%description -n mozilla-plugin-freewrl

%description -n mozilla-plugin-freewrl -l pl

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="%{rpmcflags} -I/usr/X11R6/include/mozilla"
CXXFLAGS="$CFLAGS"
MOZILLA_INC="-I/usr/X11R6/include/mozilla"
export CFLAGS CXXFLAGS MOZILLA_INC
perl Makefile.PL
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* TODO* ARCHITECTURE* CONFORMANCE*
%attr(755,root,root) %{_bindir}/*
%{perl_sitearch}/VRML
%{perl_sitearch}/auto/VRML

%files -n mozilla-plugin-freewrl
%defattr(644,root,root,755)
%{mozilladir}/java/classes/*
%{mozilladir}/plugins/*

%files -n netscape-plugin-freewrl
%defattr(644,root,root,755)
%{netscapedir}/java/classes/*
%{netscapedir}/plugins/*
