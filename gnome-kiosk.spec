%global gettext_version                         0.19.6
%global gnome_desktop_version                   40~rc
%global glib2_version                           2.68.0
%global gtk4_version                            3.24.27
%global mutter_version                          42.0
%global gsettings_desktop_schemas_version       40~rc
%global ibus_version                            1.5.24
%global gnome_settings_daemon_version           40~rc

Name:           gnome-kiosk
Version:        44.0
Release:        1
Summary:        Window management and application launching for GNOME

License:        GPLv2+
URL:            https://gitlab.gnome.org/halfline/gnome-kiosk
Source0:        https://download.gnome.org/sources/%{name}/40/%{name}-%{version}.tar.xz
Patch0:         fix-usr-bin-sh.patch

# Mandriva patches:
#Patch1:         fix-compilation-with-meson-0.60.patch

Provides:       firstboot(windowmanager) = %{name}

BuildRequires:  gettext >= %{gettext_version}
BuildRequires:  git
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-3.0) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(ibus-1.0) >= %{ibus_version}
BuildRequires:  pkgconfig(libmutter-11) >= %{mutter_version}
BuildRequires:  egl-devel
BuildRequires:  pkgconfig(dri)
BuildRequires:  meson

Requires:       gnome-settings-daemon%{?_isa} >= %{gnome_settings_daemon_version}
Requires:       gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}

%description
GNOME Kiosk provides a desktop enviroment suitable for fixed purpose, or
single application deployments like wall displays and point-of-sale systems.

%package search-appliance
Summary:        Example search application application that uses GNOME Kiosk
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       firefox
Requires:       gnome-session
BuildArch:      noarch

%description search-appliance
This package provides a full screen firefox window pointed to google.

%package script-session            
Summary:        Basic session used for running kiosk application from shell script            
License:        GPLv2+            
Requires:       %{name} = %{version}-%{release}            
Recommends:     gedit      
Requires:       gnome-session

BuildArch:      noarch

%description script-session
This package generates a shell script and the necessary scaffolding to start that shell script within a kiosk session.

%prep
%autosetup -S git -n %{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_bindir}/gnome-kiosk
%{_datadir}/applications/org.gnome.Kiosk.desktop
%{_userunitdir}/org.gnome.Kiosk.target            
%{_userunitdir}/org.gnome.Kiosk@wayland.service            
%{_userunitdir}/org.gnome.Kiosk@x11.service

%files -n gnome-kiosk-search-appliance
%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop
%{_datadir}/gnome-session/sessions/org.gnome.Kiosk.SearchApp.session
%{_datadir}/xsessions/org.gnome.Kiosk.SearchApp.Session.desktop
%{_datadir}/wayland-sessions/org.gnome.Kiosk.SearchApp.Session.desktop

%files -n gnome-kiosk-script-session            
%{_bindir}/gnome-kiosk-script            
%{_userunitdir}/gnome-session@gnome-kiosk-script.target.d/session.conf            
%{_userunitdir}/org.gnome.Kiosk.Script.service            
%{_datadir}/applications/org.gnome.Kiosk.Script.desktop            
%{_datadir}/gnome-session/sessions/gnome-kiosk-script.session            
%{_datadir}/wayland-sessions/gnome-kiosk-script-wayland.desktop            
%{_datadir}/xsessions/gnome-kiosk-script-xorg.desktop
