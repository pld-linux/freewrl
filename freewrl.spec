Summary:	-
Summary(pl):	-
Name:		freewrl
Version:	0.34
Release:	0.1
License:	LGPL
Group:		-
Source0:	FreeWRL-%{version}.tar.gz
#Source1:	-
Patch0:		%{name}-config.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-mozilla.patch
URL:		http://freewrl.sourceforge.net/
#BuildRequires:	-
#PreReq:		-
BuildRequires:	perl
BuildRequires:	saxon
BuildRequires:	ImageMagick
BuildRequires:	perl-devel
BuildRequires:	gtk+-devel
BuildRequires:	binutils-static
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
/usr/lib/perl5/site_perl/i686-pld-linux/5.6.1/VRML
/usr/lib/perl5/site_perl/i686-pld-linux/5.6.1/auto/VRML

%files -n mozilla-plugin-freewrl
%defattr(644,root,root,755)
/usr/X11R6/lib/mozilla/java/classes/*
/usr/X11R6/lib/mozilla/plugins/*

%files -n netscape-plugin-freewrl
%defattr(644,root,root,755)
/usr/X11R6/lib/netscape/java/classes/*
/usr/X11R6/lib/netscape/plugins/*
