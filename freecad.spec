%define _disable_ld_no_undefined 1
%global plugins Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui

# Setup python target for shiboken so the right cmake file is imported.
%global py_suffix %(%{__python3} -c "import sysconfig; print(sysconfig.get_config_var('SOABI'))")

%define __noautoreq /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d
%define _disable_lto 1
%bcond_with	shiboken

Name:		freecad
Summary:	FreeCAD is a general purpose 3D CAD modeler
Version:	0.18.4
Release:	2
License:	GPL and LGPL
Group: 		Graphics
Url:		https://freecadweb.org
Source0:	https://github.com/FreeCAD/FreeCAD/archive/%{version}.tar.gz
Source1:      	freecad.desktop
Source2:      	freecad.1
Source3:	%{name}.rpmlintrc

Patch0:         freecad-0.15-zipios.patch
Patch1:         freecad-0.14-Version_h.patch
Patch2:         freecad-0.18-py38.patch
Patch3:         freecad-iostream_scope.patch

BuildRequires:	doxygen
BuildRequires: 	qt5-devel
BuildRequires: 	libxerces-c-devel
BuildRequires: 	opencv-devel
# disabled for armv7 in 3.0 till
# https://issues.openmandriva.org/show_bug.cgi?id=1825
%ifnarch %arm
BuildRequires: 	python-matplotlib
%endif
BuildRequires: 	eigen3
BuildRequires:	hdf5-devel
BuildRequires:	smesh-devel
BuildRequires: 	spnav-devel
BuildRequires: 	double-conversion-devel
BuildRequires: 	pkgconfig(liblzma)
BuildRequires:	boost-static-devel
BuildRequires: 	cmake(Qt5X11Extras)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(glew)
BuildRequires: 	pkgconfig(xext)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(liblz4)
BuildRequires: 	pkgconfig(shiboken2)
BuildRequires:	pkgconfig(sm)
BuildRequires: 	pkgconfig(pyside2)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(python)
BuildRequires: 	python-matplotlib
BuildRequires: 	cmake
BuildRequires: 	gcc-gfortran
BuildRequires: 	opencascade-devel
BuildRequires: 	pkgconfig(Coin4)
BuildRequires: 	boost-devel >= 1.34.0
BuildRequires:	python-vtk
BuildRequires:	python-vtk-qt
BuildRequires:	vtk-devel
BuildRequires:	med-devel
BuildRequires:	swig
BuildRequires:	pybind11-devel

Requires:	python-pivy
%if %{with shiboken}
Requires:	pyside2-core
%endif

%description
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
%autopatch -p1
sed -i 's!-python2.7!!g' CMakeLists.txt

%build
%define Werror_cflags %nil
#export CC=gcc
#export CXX=g++


%cmake_qt5 -DBUILD_QT5=ON \
            -DMEDFILE_INCLUDE_DIRS=%{_includedir}/med \
	    -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	    -DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
            -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
            -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	    -DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/lib \
            -DRESOURCEDIR=%{_datadir}/freecad \
            -DPYTHON_EXECUTABLE=%{__python3} \
%if %{with shiboken}
            -DPYSIDE_INCLUDE_DIR=%{_includedir}/PySide2 \
            -DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken2 \
            -DPYSIDE_LIBRARY=%{_libdir}/libpyside2.%{py_suffix}.so \
%endif
            -DFREECAD_USE_EXTERNAL_SMESH=FALSE \
            -DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
            -DOpenGL_GL_PREFERENCE=LEGACY \
            -DBUILD_QT5=ON \
            -DUSE_BOOST_PYTHON=OFF    
%make_build VERBOSE=1

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
%{_docdir}/%{name}/freecad.q*
%{_docdir}/%{name}/ThirdPartyLibraries.html
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/share
%{_libdir}/%{name}/lib/
%{_libdir}/%{name}/Mod/
%{_libdir}/%{name}/Ext/
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*
