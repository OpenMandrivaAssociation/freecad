%define _disable_lto 1

%define sname FreeCAD
%define name %(echo %sname | tr [:upper:] [:lower:])

%global plugins Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui
#global plugins Complete DraftUtils Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part PartDesign Path Points QtUnit Raytracing ReverseEngineering Robot Sketcher Spreadsheet Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui area

# Setup python target for shiboken so the right cmake file is imported.
%global py_suffix %(%{__python3} -c "import sysconfig; print(sysconfig.get_config_var('SOABI'))")

%define __noautoreq /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d

%bcond_without	shiboken
%bcond_with	pycxx
%bcond_with	zipios
# (mandian) use bundled SMESH (upstream use an old version)
%bcond_with	smesh

#define snapshot 20220205

Summary:	FreeCAD is a general purpose 3D CAD modeler
Name:		%{name}
Version:	1.0.0
Release:	%{?snapshot:0.%{snapshot}.}1
License:	GPL and LGPL
Group: 		Graphics
Url:		https://freecadweb.org
Source0:	https://github.com/FreeCAD/FreeCAD/archive/%{?snapshot:master}%{!?snapshot:%{version}}/%{sname}-%{?snapshot:master}%{!?snapshot:%{version}}.tar.gz
Source1:	freecad.desktop
Source2: 	freecad.1
Source3:	%{name}.rpmlintrc

Patch0:		freecad-0.19.2-zipios++.patch
Patch1:		freecad-0.14-Version_h.patch
Patch2:		freecad-0.21.0-GL-linkage.patch
Patch3:		freecad-0.19.2-coin_doc.patch
#Patch4:		freecad-0.21.0-vtk-9.3.patch
#Patch5:		freecad-0.21.2-boost-1.85.patch
# (fedora)
#Patch6:		freecad-unbundled-pycxx.patch
# (upstream)
# https://github.com/FreeCAD/FreeCAD/commit/9a41845a417189776741297c50a3827ce292bc4f.patch
#Patch100:	freecad-0.19.3-opencascade_7_6_3.patch
#Patch101:	https://github.com/FreeCAD/FreeCAD/commit/f91ad00ed23e92c81fff2bd0073c662291efad32.patch
#Patch102:	https://github.com/FreeCAD/FreeCAD/commit/c0fa37cfa90f2e3d7b08d538c99d9b624d0950b9.patch
#Patch103:	https://github.com/FreeCAD/FreeCAD/commit/988ec4c4fbd8729cb4bc42623eba76a75b31c028.patch

BuildRequires: 	cmake
BuildRequires: 	ninja
#BuildRequires:	dos2unix
BuildRequires:	doxygen
#BuildRequires: gcc-gfortran
#BuildRequires:	graphviz
BuildRequires:	swig

BuildRequires:	boost-devel
#BuildRequires:	boost-static-devel
BuildRequires:	coin-doc
BuildRequires:	cmake(coin)
BuildRequires:	cmake(double-conversion)
#BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freeglut)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(MEDFile) 
BuildRequires:	cmake(ogg)
BuildRequires:	cmake(pegtl)
BuildRequires:	cmake(pybind11)
BuildRequires:	cmake(Qt5Concurrent)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Help)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5OpenGL)
BuildRequires:	cmake(Qt5PrintSupport)
BuildRequires:	cmake(Qt5Svg)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5UiTools)
#BuildRequires:	cmake(Qt5WebKitWidgets) # not more used?
BuildRequires:	cmake(Qt5WebEngineWidgets)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Xml)
BuildRequires:	cmake(Qt5XmlPatterns)
BuildRequires:	cmake(Qt5X11Extras)
BuildRequires:	cmake(utf8cpp)
BuildRequires:	freeimage-devel
BuildRequires:	gl2ps-devel
BuildRequires:	glibc-devel
BuildRequires:	hdf5-devel
BuildRequires:	java-devel
BuildRequires:	libharu-devel
BuildRequires:	opencascade-devel
#BuildRequires:	opencv-devel
BuildRequires:	python-vtk
BuildRequires:	python-vtk-qt
BuildRequires:	cmake(Verdict)
#BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires: 	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ompi-cxx)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(liblz4)
BuildRequires: 	pkgconfig(liblzma)
BuildRequires: 	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(python3)
%if %{with shiboken}
BuildRequires:	pkgconfig(pyside2)
BuildRequires:	pkgconfig(shiboken2)
%endif
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires: 	pkgconfig(xext)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python3dist(pivy)
%if %{with pycxx}
BuildRequires:	python3dist(cxx)
BuildRequires:	python-cxx-devel
%endif
BuildRequires:	python3dist(matplotlib)
%if %{with smesh}
BuildRequires:	smesh-devel
%endif
BuildRequires: 	spnav-devel
BuildRequires:	vtk-devel
%if %{with zipios}
BuildRequires:	zipios++-devel
%endif

Requires:	python3dist(pivy)
Requires:	python-matplotlib-qt5
Requires:	python3dist(matplotlib)
#Requires:	python3dist(pycollada)
%if %{with shiboken}
Requires:	pyside2
Requires:	python3dist(shiboken2)
%endif
#Requires:	openscad
Requires:	qt5-assistant

%description
FreeCAD is a general purpose feature-based, parametric 3D modeler for
CAD, MCAD, CAx, CAE and PLM, aimed directly at mechanical engineering
and product design but also fits a wider range of uses in engineering,
such as architecture or other engineering specialties. It is 100% Open
Source (LGPL2+ license) and extremely modular, allowing for very
advanced extension and customization.

FreeCAD is based on OpenCASCADE, a powerful geometry kernel, features an
Open Inventor-compliant 3D scene representation model provided by the
Coin 3D library, and a broad Python API. The interface is built with Qt.
FreeCAD runs exactly the same way on Windows, Mac OSX, BSD and Linux
platforms.

%files
%doc README.md SECURITY.md
%{_docdir}/%{name}/LICENSE.html
%{_docdir}/%{name}/ThirdPartyLibraries.html
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/share
%{_libdir}/%{name}/include
%{_libdir}/%{name}/lib/
%{_libdir}/%{name}/Mod/
%{_libdir}/%{name}/Ext/
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{sname}-%{?snapshot:master}%{!?snapshot:%{version}}

#rm -rf src/3rdParty
%if %{with zipios}
rm -rf src/zipios++
%endif
%if %{with pycxx}
rm -rf src/CXX
%endif

find . -type f -name "*.cpp" -o -name "*.h" |xargs sed -i -e 's,boost::mt19937,std::mt19937,g'

#rm -rf src/3rdParty/{boost,Pivy*}
#sed -i 's!-python2.7!!g' CMakeLists.txt

%build
%cmake_qt5 \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	-DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/lib \
	-DBUILD_ENABLE_CXX_STD="C++17" \
	-DBUILD_QT5:BOOL=ON \
	-DRESOURCEDIR=%{_datadir}/freecad \
	-DFREECAD_USE_EXTERNAL_ZIPIOS:BOOL=%{?with_zipios:ON}%{!?with_zipios:OFF} \
%if %{with smesh}
	-DFREECAD_USE_EXTERNAL_SMESH:BOOL=%{?with_smesh:ON}%{!?with_smesh:OFF} \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh/SMESH \
%endif
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DPYTHON_EXECUTABLE=%{__python} \
%if %{with pycxx}
	-DPYCXX_INCLUDE_DIR:PATH=%{_includedir}/python%{python3_version} \
	-DPYCXX_SOURCE_DIR:PATH=%{_datadir}/python%{python3_version}/CXX \
%endif
%if %{with shiboken}
	-DPYSIDE_INCLUDE_DIR=%{_includedir}/PySide2 \
	-DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken2 \
	-DSHIBOKEN_LIBRARY=%{_libdir}/libshiboken2.cpython-%{python3_version_nodots}-%{_arch}-linux-gnu.so \
	-DPYSIDE_INCLUDE_DIR=%{_includedir}/PySide2/ \
	-DPYSIDE_LIBRARY=%{_libdir}/libpyside2.%{py_suffix}.so \
%endif
	-DUSE_BOOST_PYTHON:BOOL=ON \
	-DENABLE_DEVELOPER_TESTS:BOOL=OFF \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# Symlink binaries to /usr/bin
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s ../%{_lib}/freecad/bin/FreeCAD .
ln -s ../%{_lib}/freecad/bin/FreeCADCmd .
popd

# Install desktop file
desktop-file-install \
	--dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

sed -i 's,@lib@,%{_lib},g' %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install desktop icon
install -pD -m 0644 src/Gui/Icons/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Install man page
install -pD -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/%{name}.1
