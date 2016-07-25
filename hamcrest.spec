%global pkg_name hamcrest
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define with()          %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%define without()       %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%define bcond_with()    %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}

# This option controls integration which requires easymock2 and jmock
%bcond_without integration

# This option controls jarjar on qdox
# Since bundling the qdox classes prevents upgrades, we disable it by default
%bcond_with jarjar

# This option controls tests which requires ant-junit and testng
%bcond_with tests

# If integration is disabled, then tests are disabled
%if %without integration
%bcond_with tests
%endif

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.3
Release:        6.7%{?dist}
Epoch:          0
Summary:        Library of matchers for building test expressions
License:        BSD
URL:            http://code.google.com/p/hamcrest/
Source0:        http://%{pkg_name}.googlecode.com/files/%{pkg_name}-1.3.tgz
Source1:        http://repo1.maven.org/maven2/org/%{pkg_name}/%{pkg_name}-parent/%{version}/%{pkg_name}-parent-%{version}.pom
Source2:        http://repo1.maven.org/maven2/org/%{pkg_name}/%{pkg_name}-library/%{version}/%{pkg_name}-library-%{version}.pom
Source3:        http://repo1.maven.org/maven2/org/%{pkg_name}/%{pkg_name}-integration/%{version}/%{pkg_name}-integration-%{version}.pom
Source4:        http://repo1.maven.org/maven2/org/%{pkg_name}/%{pkg_name}-generator/%{version}/%{pkg_name}-generator-%{version}.pom
Source5:        http://repo1.maven.org/maven2/org/%{pkg_name}/%{pkg_name}-core/%{version}/%{pkg_name}-core-%{version}.pom
Source6:        http://repo1.maven.org/maven2/org/%{pkg_name}/%{pkg_name}-all/%{version}/%{pkg_name}-all-%{version}.pom

Source8:        hamcrest-core-MANIFEST.MF
Source9:        hamcrest-library-MANIFEST.MF
Source11:       hamcrest-integration-MANIFEST.MF
Source12:       hamcrest-generator-MANIFEST.MF

Patch0:         %{pkg_name}-%{version}-build.patch
Patch1:         %{pkg_name}-%{version}-no-jarjar.patch
Patch2:         %{pkg_name}-%{version}-no-integration.patch
Patch3:         %{pkg_name}-%{version}-javadoc.patch

Requires:       %{?scl_prefix}qdox
%if %with integration
Requires:       %{?scl_prefix}easymock2
#Requires:       %{?scl_prefix}jmock
%endif

BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}ant >= 0:1.6.5
BuildRequires:  %{?scl_prefix}ant-junit
BuildRequires:  zip
%if %with integration
BuildRequires:  %{?scl_prefix}easymock2
%endif
%if %with jarjar
BuildRequires:  %{?scl_prefix}jarjar
%endif
BuildRequires:  %{?scl_prefix}junit
BuildRequires:  %{?scl_prefix}qdox
%if %with tests
BuildRequires:  %{?scl_prefix}testng
%endif

BuildArch:      noarch

%description
Provides a library of matcher objects (also known as constraints or predicates)
allowing 'match' rules to be defined declaratively, to be used in other
frameworks. Typical scenarios include testing frameworks, mocking libraries and
UI validation rules.

%package javadoc
Summary:        Javadoc for %{pkg_name}
BuildArch:      noarch

%description javadoc
Javadoc for %{pkg_name}.

%package demo
Summary:        Demos for %{pkg_name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{?scl_prefix}junit
%if %with tests
Requires:       %{?scl_prefix}testng
%endif

%description demo
Demonstrations and samples for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
find . -type f -name "*.jar" | xargs -t rm
rm -fr hamcrest-integration/src/main/java/org/hamcrest/integration/JMock1Adapter.java
rm -fr hamcrest-integration/src/main/java/org/hamcrest/JMock1Matchers.java
rm -fr hamcrest-unit-test/src/main/java/org/hamcrest/integration/JMock1AdapterTest.java
# BUILD/hamcrest-%{version}/lib/generator/jarjar-1.0rc3.jar.no
%if %with jarjar
ln -sf $(build-classpath jarjar) lib/generator/
%endif
# BUILD/hamcrest-1.1/lib/generator/qdox-1.6.1.jar.no
ln -sf $(build-classpath qdox) lib/generator/
# BUILD/hamcrest-1.1/lib/integration/easymock-2.2.jar.no
%if %with integration
# easymock2 is now compat package
ln -sf $(build-classpath easymock2-2.4) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/jmock-1.10RC1.jar.no
ln -sf $(build-classpath jmock) lib/integration/
%endif
# BUILD/hamcrest-1.1/lib/integration/testng-4.6-jdk15.jar.no
%if %with tests
ln -sf $(build-classpath testng-jdk15) lib/integration/
%endif
%patch0 -p1
%if %without jarjar
%patch1 -p1
%endif
%if %without integration
%patch2 -p1
%endif
%patch3 -p1

perl -pi -e 's/\r$//g' LICENSE.txt
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath qdox)
export OPT_JAR_LIST="junit ant/ant-junit"
# The unit-test goal is switched off as some tests fail with JDK 7
# see https://github.com/hamcrest/JavaHamcrest/issues/30
ant -Dant.build.javac.source=1.5 -Dversion=%{version} -Dbuild.sysclasspath=last clean core generator library bigjar javadoc

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE8} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{pkg_name}-core-%{version}.jar META-INF/MANIFEST.MF

rm -fr META-INF
mkdir -p META-INF
cp -p %{SOURCE9} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{pkg_name}-library-%{version}.jar META-INF/MANIFEST.MF

rm -fr META-INF
mkdir -p META-INF
cp -p %{SOURCE11} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{pkg_name}-integration-%{version}.jar META-INF/MANIFEST.MF

rm -fr META-INF
mkdir -p META-INF
cp -p %{SOURCE12} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{pkg_name}-generator-%{version}.jar META-INF/MANIFEST.MF
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-parent.pom
%add_maven_depmap JPP.%{pkg_name}-parent.pom

install -m 644 build/%{pkg_name}-all-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/all.jar
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-all.pom
%add_maven_depmap JPP.%{pkg_name}-all.pom %{pkg_name}/all.jar

install -m 644 build/%{pkg_name}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/core.jar
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-core.pom
%add_maven_depmap JPP.%{pkg_name}-core.pom %{pkg_name}/core.jar

install -m 644 build/%{pkg_name}-generator-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/generator.jar
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-generator.pom
%add_maven_depmap JPP.%{pkg_name}-generator.pom %{pkg_name}/generator.jar

install -m 644 build/%{pkg_name}-library-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/library.jar
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-library.pom
%add_maven_depmap JPP.%{pkg_name}-library.pom %{pkg_name}/library.jar

%if %with integration
install -m 644 build/%{pkg_name}-integration-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/integration.jar
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-integration.pom
%add_maven_depmap JPP.%{pkg_name}-integration.pom %{pkg_name}/integration.jar
%endif

%if %with tests
install -m 644 build/%{pkg_name}-unit-test-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}/unit-test.jar
%endif

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/temp/hamcrest-all-1.3-javadoc.jar.contents/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}
cp -pr %{pkg_name}-examples $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}/
%{?scl:EOF}

%files
%doc LICENSE.txt
%dir %{_javadir}/%{pkg_name}
%{_javadir}/%{pkg_name}/all.jar
%{_javadir}/%{pkg_name}/core.jar
%{_javadir}/%{pkg_name}/generator.jar
%if %with integration
%{_javadir}/%{pkg_name}/integration.jar
%endif
%{_javadir}/%{pkg_name}/library.jar
%if %with tests
%{_javadir}/%{pkg_name}/unit-test.jar
%endif
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{pkg_name}

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-6.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.3-6
- Mass rebuild 2013-12-27

* Wed Jul 31 2013 Michal Srb <msrb@redhat.com> - 0:1.3-5
- Fix R: easymock3 -> easymock2

* Wed Jul 31 2013 Michal Srb <msrb@redhat.com> - 0:1.3-4
- Remove org.hamcrest:hamcrest-text artifact (it's no longer available in 1.3)

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 0:1.3-2
- Add easymock2 to classpath (Resolves: #979501)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Mar 21 2013 Tomas Radej <tradej@redhat.com> - 0:1.3-1
- Updated to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1-21
- Fix core manifest typo ";" -> ","

* Tue Aug 14 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:1.1-20
- Remove attributes in Export-Package header of hamcrest-core
  manifest.

* Wed Aug 1 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-19
- Add OSGi metadata to hamcrest-generator.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-18
- Actually build integration.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-17
- Add OSGi metadata to hamcrest-integration.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-16
- Remove checksums from manifest.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-15
- Add OSGi metadata to hamcrest-text.

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-14
- Add OSGi metadata for hamcrest-library.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-11
- Do not BR/R openjdk6 but java >= 1:1.6.0
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Mat Booth <fedora@matbooth.co.uk> 0:1.1-9.4
- Fix FTBFS due to zip BR - RHBZ #661011.

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-9.3
- Drop gcj support.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-9.2
- Add OSGi manifest for hamcrest-core.
- Make javadoc package noarch.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-7.1
- Fedora-specific: enable GCJ support
- Fedora-specific: build with java 1.6.0
- Fedora-specific: disable integration and tests

* Mon Nov 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-7
- update summary and description

* Tue Oct 28 2008 David Walluck <dwalluck@redhat.com> 0:1.1-6
- make demo dependency on testng conditional

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-5
- fix GCJ file list
- simplify build by always setting OPT_JAR_LIST

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-4
- add epoch to demo Requires

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-3
- set -Dant.build.javac.source=1.5

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-2
- add options to build without integration, jarjar, and tests
- allow build with java-devel >= 1.5.0
- remove javadoc scriptlets
- use more strict file list
- fix maven directory ownership
- add non-versioned symlink for demo
- fix GCJ requires
- fix eol in LICENSE.txt
- remove Vendor and Distribution

* Tue Feb 19 2008 Ralph Apel <r.apel@r-apel.de> - 0:1.1-1jpp
- 1.1

* Mon Feb 11 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-4jpp
- Fix versioned jar name, was junit-4.3.1
- Restore Epoch

* Fri Jan 25 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-3jpp
- build and upload noarch packages
- Add pom and depmap frag
- BR java-devel = 1.5.0
- Restore Vendor, Distribution from macros

* Tue Aug 07 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-2jpp
- Set gcj_support to 0 to work around problems with GCJ.
- Fix buglet with the gcj post/postun if statement.
- Fix tab / space problems.
- Fix buildroot.
- Update Summary.
- Convert html files to Unix file endings.
- Disable aot-compile-rpm because it's not working ATM.

* Mon Jul 09 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-1jpp
- 4.3.1.

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Thu Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Fri Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2
* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
