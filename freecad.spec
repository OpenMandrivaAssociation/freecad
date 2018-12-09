%define _disable_ld_no_undefined 1
%global plugins Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui

%define __noautoreq /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d
%define _disable_lto 1
Name:		freecad
Summary:	FreeCAD is a general purpose 3D CAD modeler
Version:	0.17
Release:	1
License:	GPL and LGPL
Group: 		Graphics
Url:		http://free-cad.sourceforge.net/
Source0:	https://github.com/FreeCAD/FreeCAD/archive/%{version}.tar.gz
Source1:      	freecad.desktop
Source2:      	freecad.1
Source3:	%{name}.rpmlintrc
#Patch0:		disable_memory_check.patch
#Patch1:		do_not_install_binary_examples.patch
#Patch2:		fix_armel_FTBFS.patch
#Patch3:		remove_doc-files.patch
# cb - breaks the gui
#Patch4:		use_share.patch
Patch0:		freecad-smesh_header.patch
#Patch1:		freecad-0.17-external_smesh.patch
BuildRequires:	doxygen
BuildRequires: 	qt5-devel
BuildRequires: 	libxerces-c-devel
BuildRequires: 	opencv-devel
BuildRequires: 	python-devel
BuildRequires: 	libode-devel
# disabled for armv7 in 3.0 till
# https://issues.openmandriva.org/show_bug.cgi?id=1825
%ifnarch %arm
BuildRequires: 	python2-matplotlib
%endif
BuildRequires: 	eigen3
BuildRequires: 	spnav-devel
BuildRequires: 	pkgconfig(shiboken2)
BuildRequires: 	pkgconfig(pyside2)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:  pyside2-tools
BuildRequires: 	cmake
BuildRequires: 	gcc-gfortran
BuildRequires: 	opencascade-devel
BuildRequires: 	coin-devel
BuildRequires: 	boost-devel >= 1.34.0
BuildRequires:	vtk-devel
BuildRequires:	med-devel

Requires:	python-pivy
Requires:	python2-pyside2

%description
FreeCAD will be a general purpose 3D CAD modeler.
The development will be completely Open Source.
As with many modern 3D CAD modelers it will
have a 2D component in order to extract design detail
from the 3D model to create 2D production drawings,
although 2D (e.g. AutoCAD LT) is not the focus,
neither are animation and organic shapes
(e.g. Maya, 3D StudioMAX and Cinema 4D).

%package devel
Group: Development/C++
Summary: Devel package for %{name}
Requires: %{name} = %{version}

%description devel
FreeCAD will be a general purpose 3D CAD modeler.
The development will be completely Open Source.
As with many modern 3D CAD modelers it will
have a 2D component in order to extract design detail
from the 3D model to create 2D production drawings,
although 2D (e.g. AutoCAD LT) is not the focus,
neither are animation and organic shapes
(e.g. Maya, 3D StudioMAX and Cinema 4D).

%prep
%setup -qn FreeCAD-%{version}
rm -rf src/3rdParty/{boost,Pivy*}
%apply_patches
sed -i 's!-python2.7!!g' CMakeLists.txt

%build
%define Werror_cflags %nil
export CC=gcc
export CXX=g++
%cmake_qt5 -DBUILD_QT5=ON -DMEDFILE_INCLUDE_DIRS=%{_includedir}/med \
	 -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	    -DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
            -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
            -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	    -DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/lib \
	    -DPYTHON_SUFFIX="-python2.7" \
            -DRESOURCEDIR=%{_datadir}/freecad
%make

%install
%makeinstall_std -C build

# Symlink binaries to /usr/bin
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s ../%{_lib}/freecad/bin/FreeCAD .
ln -s ../%{_lib}/freecad/bin/FreeCADCmd .
popd

# Install desktop file
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications  %{SOURCE1}

sed -i 's,@lib@,%{_lib},g' %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install desktop icon
install -pD -m 0644 src/Gui/Icons/%{name}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Install man page
install -pD -m 0644 %{SOURCE2} \
    %{buildroot}%{_mandir}/man1/%{name}.1

# Symlink manpage to other binary names
pushd %{buildroot}%{_mandir}/man1
ln -sf %{name}.1.gz FreeCAD.1.gz.
ln -sf %{name}.1.gz FreeCADCmd.1.gz
popd

%files
%doc ChangeLog.txt data/License.txt
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/lib/
%{_libdir}/%{name}/Mod/
%{_libdir}/%{name}/Ext/
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*

%files devel
#{_libdir}/%{name}/include/*
