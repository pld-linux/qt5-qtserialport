# TODO:
# - cleanup

%define		orgname		qtserialport
Summary:	The Qt5 Serialport
Name:		qt5-%{orgname}
Version:	5.2.0
Release:	0.1
License:	LGPL v2.1 or GPL v3.0
Group:		Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	7b90e0707b698331226e662bd39945e9
URL:		http://qt-project.org/
BuildRequires:	qt5-qtbase-devel = %{version}
BuildRequires:	qt5-qttools-devel = %{version}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_noautostrip	'.*_debug\\.so*'

%define		specflags	-fno-strict-aliasing
%define		_qtdir		%{_libdir}/qt5

%description
Qt5 Serial Port library.

%package devel
Summary:	The Qt5 Serial Port - development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Qt5 Serial Port - development files.

%package doc
Summary:	The Qt5 Serial Port - docs
Group:		Documentation

%description doc
Qt5 Serial Port - documentation.

%package examples
Summary:	Qt5 Serial Port examples
Group:		Development/Libraries

%description examples
Qt5 Serial Port - examples.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libQt5SerialPort.so.?
%attr(755,root,root) %{_libdir}/libQt5SerialPort.so.*.*
#%attr(755,root,root) %{_qtdir}/plugins

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5SerialPort.so
%{_libdir}/libQt5SerialPort.la
%{_libdir}/libQt5SerialPort.prl
%{_libdir}/cmake/Qt5SerialPort
%{_includedir}/qt5/QtSerialPort
%{_pkgconfigdir}/*.pc
%{_qtdir}/mkspecs

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc

#%files examples -f examples.files
