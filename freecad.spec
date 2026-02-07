#define _disable_lto 1

%define sname FreeCAD
%define name %(echo %sname | tr [:upper:] [:lower:])

%global plugins Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui
#global plugins Complete DraftUtils Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part PartDesign Path Points QtUnit Raytracing ReverseEngineering Robot Sketcher Spreadsheet Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui area

# Setup python target for shiboken so the right cmake file is imported.
%global py_suffix %(%{__python3} -c "import sysconfig; print(sysconfig.get_config_var('SOABI'))")

%define __noautoreq /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d

%bcond addonmgr		1
%bcond e57format	1
%bcond netgen		0
%bcond ondselsolver	0
%bcond pybind11		1
%bcond pycxx		1
%bcond shiboken		1
# (mandian) use bundled SMESH (upstream use an old version)
%bcond smesh		0
%bcond tests		0
%bcond zipios		0

Summary:	FreeCAD is a general purpose 3D CAD modeler
Name:		%{name}
Version:	1.1~rc2^1git8175e0633fd
Release:	2
License:	GPL and LGPL
Group: 		Graphics
Url:		https://freecadweb.org
Source0:        https://github.com/FreeCAD/FreeCAD/releases/tag/%{version}/%{sname}-%{version}.tar.gz
Source1:	freecad.desktop
Source2: 	freecad.1
Source3:	%{name}.rpmlintrc
Source4:	GSL-4.2.0.tar.gz

#Patch0:		freecad-0.19.2-zipios++.patch
#Patch1:		freecad-0.14-Version_h.patch
#Patch2:		freecad-0.21.0-GL-linkage.patch
#Patch3:		freecad-0.19.2-coin_doc.patch
# (fedora)
Patch4:		freecad-1.0.0-unbundled-pycxx.patch
#Patch5:		fix_vtk_include_path.patch
#Patch6:		fix_deprecated_vtk_function.patch
#Patch7:		boost-1.89.patch
# Patch5: 	freecad_limits.patch
# PATCH-FIX-UPSTREAM
#Patch50:        https://github.com/Ondsel-Development/OndselSolver/commit/2e3659c4bce3e6885269e0cb3d640261b2a91108.patch#/ondselsolver_fix_gcc_75_filesystem.patch

BuildRequires: 	cmake
BuildRequires: 	ninja
BuildRequires:	desktop-file-utils
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	swig
BuildRequires:	gnutar
BuildRequires:	boost-devel
BuildRequires:	coin-doc
BuildRequires:	cmake(coin)
BuildRequires:	cmake(double-conversion)
%if %{with e57format}
BuildRequires:	cmake(e57format)
%endif
#BuildRequires:	pkgconfig(egl)
BuildRequires:	cmake(expat)
BuildRequires:	pkgconfig(freeglut)
BuildRequires:	cmake(FastFloat)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(libjpeg-turbo)
BuildRequires:	cmake(MEDFile) 
BuildRequires:	cmake(ogg)
BuildRequires:	cmake(opencascade)
BuildRequires:	cmake(opencv)
BuildRequires:	cmake(pegtl)
%if %{with pybind11}
BuildRequires:	cmake(pybind11)
%endif
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6SvgWidgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6UiPlugin)
BuildRequires:	cmake(Qt6UiTools)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(utf8cpp)
BuildRequires:	cmake(yaml-cpp)
BuildRequires:	cmake(Verdict)
BuildRequires:	cmake(vtk)
%if %{with zipios}
BuildRequires:	cmake(zipios)
%endif
BuildRequires:	freeimage-devel
BuildRequires:	gl2ps-devel
BuildRequires:	glibc-devel
BuildRequires:	hdf5-devel
BuildRequires:	java-devel
BuildRequires:	libharu-devel
BuildRequires:	python-vtk
BuildRequires:	python-vtk-qt
#BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ompi-cxx)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(liblz4)
BuildRequires: 	pkgconfig(liblzma)
BuildRequires: 	pkgconfig(libtiff-4)
%if %{with ondselsolver}
BuildRequires:	pkgconfig(OndselSolver)
%endif
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(python3)
%if %{with shiboken}
BuildRequires:	pkgconfig(pyside6)
BuildRequires:	pkgconfig(shiboken6)
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
BuildRequires:	python%{pyver}dist(pivy)

%if %{with pycxx}
BuildRequires:	python%{pyver}dist(cxx)
BuildRequires:	python-cxx-devel
%endif
BuildRequires:	python%{pyver}dist(matplotlib)
%if %{with smesh}
BuildRequires:	smesh-devel
%endif
BuildRequires: 	spnav-devel
BuildRequires:	vtk-devel

Requires:	python%{pyver}dist(pivy)
#Requires:	python-matplotlib-qt6
Requires:	python%{pyver}dist(matplotlib)
#Requires:	python3dist(pycollada)
Requires:	python%{pyver}dist(six)
%if %{with shiboken}
Requires:	pyside6
#Requires:	python%{pyver}dist(shiboken6)
%endif
#Requires:	openscad
Requires:	qt6-qttools-assistant

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
%{_datadir}/mime/packages/org.freecad.FreeCAD.xml
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/share
%{_libdir}/%{name}/include
%{_libdir}/%{name}/lib/
%{_libdir}/%{name}/Mod/
%{_libdir}/%{name}/Ext/
%{_includedir}/OndselSolver/*.h
%{_datadir}/%{name}/
%{py_puresitedir}/%{name}
%{_mandir}/man1/*.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{sname}-%{version}
cd %{_builddir}/%{sname}-%{version}/src/3rdParty/GSL
gtar -xvf  %{_sourcedir}/GSL-4.2.0.tar.gz --strip=1 


# remove 3rd party
#rm -rf src/3rdParty
%if %{with pycxx}
rm -rf src/CXX
%endif
%if %{with ondselsolver}
rm -rf src/3rdParty/OndselSolver
%endif
%if %{with smesh}
rm -rf src/salomesmesh
%endif
%if %{with zipios}
rm -rf src/zipios++
%endif

%build
export CMAKE_GENERATOR=Ninja 
%cmake -Wno-dev \
	-DBUILD_ENABLE_CXX_STD:STRING="C++20" \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	-DCMAKE_INSTALL_LIBDIR=lib \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-DCMAKE_SKIP_INSTALL_RPATH:BOOL=OFF \
	-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
	-DRESOURCEDIR=%{_datadir}/freecad \
	-DFREECAD_QT_VERSION=6 \
	-DONDSELSOLVER_BUILD_EXE=TRUE \
 	-DFREECAD_USE_EXTERNAL_ZIPIOS:BOOL=%{?with_zipios:ON}%{!?with_zipios:OFF} \
	-DFREECAD_USE_EXTERNAL_ONDSELSOLVER=%{?with_ondselsolver:ON}%{!?with_ondselsolver:OFF} \
	-DFREECAD_USE_PYBIND11:BOOL=%{?with_pybind11:ON}%{!?with_pybind11:OFF} \
	-DENABLE_DEVELOPER_TESTS:BOOL=OFF \
	
%if %{with smesh}
	-DFREECAD_USE_EXTERNAL_SMESH:BOOL=%{?with_smesh:ON}%{!?with_smesh:OFF} \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh/SMESH \
%endif
#	-DOpenGL_GL_PREFERENCE=GLVND \
#	-DPYTHON_EXECUTABLE=%{_python3} \
%if %{with pycxx}
#	-DPYCXX_INCLUDE_DIR:PATH=%{_includedir}/python%{pyver} \
#	-DPYCXX_SOURCE_DIR:PATH=%{_datadir}/python%{pyver}/CXX \
%endif
%if %{with shiboken}
#	-DPYSIDE_INCLUDE_DIR=%{_includedir}/PySide6 \
#	-DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken6 \
#	-DPYSIDE_LIBRARY=%{_libdir}/libpyside6.abi3.so \
%endif
#	-DUSE_BOOST_PYTHON:BOOL=ON \
#	-DBUILD_FEM_NETGEN:BOOL=%{?with_netgen:ON}%{!?with_netgen:OFF} \
#	-DENABLE_DEVELOPER_TESTS:BOOL=%{?with_tests:ON}%{!?with_tests:OFF} \
#	-DBUILD_ADDONMGR:BOOL=%{?with_addonmgr:ON}%{!?with_addonmgr:OFF} \ 
#	-DCMAKE_VERBOSE_MAKEFILE=ON 
#	-DCMAKE_VERBOSE_MAKEFILE=ON -Bbuild -H

%ninja_build

%install
%ninja_install -C build

# symlink binaries to /usr/bin
mkdir -pm 0755 %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s ../%{_lib}/freecad/bin/FreeCAD %{name}
ln -s ../%{_lib}/freecad/bin/FreeCAD .
ln -s ../%{_lib}/freecad/bin/FreeCADCmd .
popd

# .desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

sed -i 's,@lib@,%{_lib},g' %{buildroot}%{_datadir}/applications/%{name}.desktop

# icon
install -Dpm 0644 src/Gui/Icons/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# appdata
install -dpm 0755 %{buildroot}%{_appdatadir}
mv %{buildroot}%{_libdir}/%{name}/share/metainfo/org.freecad.FreeCAD.metainfo.xml %{buildroot}%{_appdatadir}/

# mime
install -dpm 0755 %{buildroot}%{_datadir}/mime/packages
mv %{buildroot}%{_libdir}/%{name}/share/mime/packages/org.freecad.FreeCAD.xml %{buildroot}%{_datadir}/mime/packages/

# man pages
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/%{name}.1

# remove unwanted stuff
#rm -r %{buildroot}%{_libdir}/%{name}/include
#rm -r %{buildroot}%{_libdir}/%{name}/share/pkgconfig
#rm -r %{buildroot}%{_includedir}/OndselSolver

