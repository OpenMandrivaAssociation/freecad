Name: freecad
Summary: FreeCAD is a general purpose 3D CAD modeler
Version: 0.10.3247
Release: %mkrel 1
License: GPL and LGPL
Group: Graphics
URL: http://free-cad.sourceforge.net/
Source0: http://dfn.dl.sourceforge.net/sourceforge/free-cad/freecad-%{version}.tar.gz
Patch0: freecad-0.10.3247-fix-link.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gstreamer0.10-devel
BuildRequires: qt4-devel
BuildRequires: libxerces-c-devel
BuildRequires: opencv-devel
BuildRequires: python-devel
BuildRequires: libode-devel
BuildRequires: eigen2
BuildRequires: opencascade-devel
BuildRequires: coin-devel
BuildRequires: soqt-devel
BuildRequires: boost-devel >= 1.34.0

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
Group: Development/Libraries/C and C++
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
%setup -q -n FreeCAD-%{version}
%patch0 -p0

%build
%define Werror_cflags %nil
%cmake_qt4
%make

%install
rm -fr %buildroot
%makeinstall_std -C build

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc ChangeLog.txt copying.lib README.Linux
%{_prefix}/lib/%{name}
