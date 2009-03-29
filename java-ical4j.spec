%bcond_without  javadoc         # don't build javadoc
%if "%{pld_release}" == "ti"
%define	with_java_sun	1
%endif
#
%include	/usr/lib/rpm/macros.java
#
%define 	srcname	ical4j
%define 	_rc	rc1

Summary:	Java API that provides support for the iCalendar
Summary(pl.UTF-8):	Java API dodające wsparcie dla iCalendar
Name:		java-%{srcname}
Version:	1.0
Release:	0.%{_rc}.2
License:	BSD-like
Group:		Libraries/Java
Source0:	http://dl.sourceforge.net/ical4j/%{srcname}-%{version}-%{_rc}-src.tar.bz2
# Source0-md5:	1d07fbdf05cfad34354603b25d2ef8ea
URL:		http://ical4j.sourceforge.net/
BuildRequires:	java-commons-codec
BuildRequires:	java-commons-io
BuildRequires:	java-commons-lang
BuildRequires:	java-commons-logging
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
iCal4j is a Java API that provides support for the iCalendar
specification as defined in RFC2445. This support includes a Parser,
Object Model and Generator for iCalendar data streams.

%package javadoc
Summary:	Online manual for ical4j
Summary(pl.UTF-8):	Dokumentacja online do ical4j
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for ical4j.

%description javadoc -l pl.UTF-8
Dokumentacja do ical4j.

%description javadoc -l fr.UTF-8
Javadoc pour ical4j.

%prep
%setup -q -n %{srcname}-%{version}-%{_rc}

%build
CLASSPATH=$(build-classpath commons-codec commons-lang commons-logging commons-io)

install -d build
%javac -classpath $CLASSPATH -source 1.4 -target 1.4 -d build $(find source -name '*.java')

%if %{with javadoc}
%javadoc -d apidocs \
	%{?with_java_sun:net.fortuna.ical4j} \
	$(find source/net/fortuna/ical4j -name '*.java')
%endif

%jar -cf %{srcname}-%{version}.jar -C build .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
