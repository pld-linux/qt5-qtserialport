#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtserialport
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 SerialPort library
Summary(pl.UTF-8):	Biblioteka Qt5 SerialPort
Name:		qt5-%{orgname}
Version:	5.15.17
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	48146c5b1b1096367dcf52a07f35b55a
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 SerialPort library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 SerialPort.

%package -n Qt5SerialPort
Summary:	The Qt5 SerialPort library
Summary(pl.UTF-8):	Biblioteka Qt5 SerialPort
Group:		Libraries
%requires_eq_to	Qt5Core Qt5Core-devel
Obsoletes:	qt5-qtserialport < 5.2.0-1

%description -n Qt5SerialPort
Qt5 SerialPort library provides classes that enable access to a serial
port.

%description -n Qt5SerialPort -l pl.UTF-8
Biblioteka Qt5 SerialPort udostępnia klasy pozwalające na dostęp do
portu szeregowego.

%package -n Qt5SerialPort-devel
Summary:	Qt5 SerialPort library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 SerialPort - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5SerialPort = %{version}-%{release}
Requires:	udev-devel
Obsoletes:	qt5-qtserialport-devel < 5.2.0-1

%description -n Qt5SerialPort-devel
Qt5 SerialPort library - development files.

%description -n Qt5SerialPort-devel -l pl.UTF-8
Biblioteka Qt5 SerialPort - pliki programistyczne.

%package doc
Summary:	Qt5 SerialPort documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 SerialPort w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 SerialPort documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 SerialPort w formacie HTML.

%package doc-qch
Summary:	Qt5 SerialPort documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 SerialPort w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 SerialPort documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 SerialPort w formacie QCH.

%package examples
Summary:	Qt5 SerialPort examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 SerialPort
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Qt5 SerialPort examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 SerialPort.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/serialport

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5SerialPort -p /sbin/ldconfig
%postun	-n Qt5SerialPort -p /sbin/ldconfig

%files -n Qt5SerialPort
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5SerialPort.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5SerialPort.so.5

%files -n Qt5SerialPort-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5SerialPort.so
%{_libdir}/libQt5SerialPort.prl
%{_includedir}/qt5/QtSerialPort
%{_pkgconfigdir}/Qt5SerialPort.pc
%{_libdir}/cmake/Qt5SerialPort
%{qt5dir}/mkspecs/modules/qt_lib_serialport.pri
%{qt5dir}/mkspecs/modules/qt_lib_serialport_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtserialport

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtserialport.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
