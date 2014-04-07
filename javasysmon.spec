%{?_javapackages_macros:%_javapackages_macros}
%global commit 61ce4b8c6fdd1a2496fc907d9763cf4b7f9fc4c7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20130319

Name:           javasysmon
Version:        0.3.4
Release:        4.0%{?dist}
Summary:        Java system monitor

License:        BSD
URL:            https://github.com/jezhumble/%{name}
# Upstream doesn't provide tarballs, so we take a git snapshot from the last
# commit that went into the release.
Source0:        https://github.com/jezhumble/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
# The tests cannot find the resource files.  Fix this for openjdk-1.7.0.
Patch0:         %{name}-test.patch
# Fix the test for CPU frequency.  Submitted upstream 5 Nov 2013.
Patch1:         %{name}-cpufreq.patch
BuildArch:      noarch

BuildRequires:  ant-junit
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  java-javadoc >= 1:1.6.0
BuildRequires:  jpackage-utils

Requires:       java-headless
Requires:       jpackage-utils

%description
JavaSysMon is designed to provide an OS-independent way to manage OS
processes and get live system performance information such as CPU and
memory usage, distributed as a single jar file.

%package javadoc
Summary:        Javadoc documentation for javasysmon
Requires:       %{name} = %{version}-%{release}

%description javadoc
The javadoc documentation for javasysmon.

%prep
%setup -q -n %{name}-%{commit}
%patch0
%patch1

# Remove prebuilt objects
rm -f lib/java/* lib/native/*

# Use the system junit instead of the bundled version.
# build-jar-repository gives us a link named "[junit].jar"!
ln -s %{_javadir}/junit.jar lib/java/junit.jar
sed -i 's/junit-3.8.2/junit/' build.xml

# Link to the offline javadocs
sed -i '\@</javadoc>@i\      <link href="file://%{_javadocdir}/java/" />' build.xml

%build
ant package javadoc

%install
# Install the JAR
mkdir -p %{buildroot}%{_javadir}
cp -p target/%{name}.jar %{buildroot}%{_javadir}

# Install the javadoc
mkdir -p %{buildroot}%{_javadocdir}
cp -a target/javadoc %{buildroot}%{_javadocdir}/%{name}

%check
ant test

%files
%doc LICENSE README.md
%{_javadir}/%{name}.jar

%files javadoc
%{_javadocdir}/%{name}/

%changelog
* Fri Feb 21 2014 Jerry James <loganjerry@gmail.com> - 0.3.4-4
- Require java-headless instead of java (bz 1068194)
- Link to offline javadocs

* Wed Nov  6 2013 Jerry James <loganjerry@gmail.com> - 0.3.4-3
- Update -cpufreq patch so that tests also pass

* Tue Nov  5 2013 Jerry James <loganjerry@gmail.com> - 0.3.4-2
- Fix -javadoc Requires
- Add -cpufreq patch to fix upstream issue 21

* Wed Oct 30 2013 Jerry James <loganjerry@gmail.com> - 0.3.4-1
- Initial RPM
