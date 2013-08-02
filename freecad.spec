Name: 	freecad
Summary: FreeCAD is a general purpose 3D CAD modeler
Version: 0.13.1830
Release: 1
License: GPL and LGPL
Group: 		Graphics
Url:		http://free-cad.sourceforge.net/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/free-cad/freecad-%{version}.tar.gz
Source1:      	freecad.desktop
Source2:      	freecad.1
Source3:	%{name}.rpmlintrc
BuildRequires: 	gstreamer0.10-devel
BuildRequires: 	qt4-devel
BuildRequires: 	libxerces-c-devel
BuildRequires: 	opencv-devel
BuildRequires: 	python-devel
BuildRequires: 	libode-devel
BuildRequires: 	python-matplotlib
BuildRequires: 	eigen3
BuildRequires: 	cmake
BuildRequires: 	gcc-gfortran
BuildRequires: 	opencascade-devel
BuildRequires: 	coin-devel
BuildRequires: 	soqt-devel
BuildRequires: 	boost-devel >= 1.34.0

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
%setup -q 

%build
%define Werror_cflags %nil
%cmake_qt4 -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	    -DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
            -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
            -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
            -DRESOURCEDIR=%{_libdir}/freecad
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
%doc ChangeLog.txt copying.lib data/License.txt build/doc/*
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/lib/
%{_libdir}/%{name}/Mod/
%{_datadir}/%{name}/
%{_mandir}/man1/*.1*

%files devel
%{_libdir}/%{name}/include/*
