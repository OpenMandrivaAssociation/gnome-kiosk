%global tarball_version %%(echo %{version} | tr '~' '.')
%global major_version %(echo -n %{tarball_version} | sed 's/[.].*//')

%global gettext_version                         0.19.6
%global gnome_desktop_version                   40~rc
%global glib2_version                           2.68.0
%global gtk4_version                            3.24.27
%global mutter_version                          40.0
%global gsettings_desktop_schemas_version       40~rc
%global ibus_version                            1.5.24
%global gnome_settings_daemon_version           40~rc

Name:           gnome-kiosk
Version:        40~alpha
Release:        7%{?dist}
Summary:        Window management and application launching for GNOME

License:        GPLv2+
URL:            https://gitlab.gnome.org/halfline/gnome-kiosk
Source0:        https://download.gnome.org/sources/%{name}/%{major_version}/%{name}-%{tarball_version}.tar.xz

Provides:       firstboot(windowmanager) = %{name}

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext >= %{gettext_version}
BuildRequires:  git
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-3.0) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(ibus-1.0) >= %{ibus_version}
BuildRequires:  pkgconfig(libmutter-8) >= %{mutter_version}
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson

Requires:       gnome-settings-daemon%{?_isa} >= %{gnome_settings_daemon_version}
Requires:       gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}

# https://gitlab.gnome.org/halfline/gnome-kiosk/-/merge_requests/1
Patch10001: 0001-compositor-Be-less-aggressive-about-full-screening-w.patch

# https://gitlab.gnome.org/halfline/gnome-kiosk/-/merge_requests/2
Patch20001: 0001-gobject-utils-Log-when-executing-deferred-tasks.patch
Patch20002: 0002-input-sources-manager-Fix-overzealous-rename-mistake.patch
Patch20003: 0003-compositor-Add-signal-for-reporting-X-server-events.patch
Patch20004: 0004-input-sources-manager-Support-libxklavier-managed-ke.patch

# https://gitlab.gnome.org/halfline/gnome-kiosk/-/merge_requests/3
Patch30001: 0001-Make-the-desktop-file-valid.patch

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

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Kiosk.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop

%files
%license COPYING
%doc README.md
%{_bindir}/gnome-kiosk
%{_datadir}/applications/org.gnome.Kiosk.desktop

%files -n gnome-kiosk-search-appliance
%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop
%{_datadir}/gnome-session/sessions/org.gnome.Kiosk.SearchApp.session
%{_datadir}/xsessions/org.gnome.Kiosk.SearchApp.Session.desktop
%{_datadir}/wayland-sessions/org.gnome.Kiosk.SearchApp.Session.desktop

%changelog
* Tue Apr 27 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-7
- Fix desktop file
  Resolves: #1954285

* Fri Apr 23 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-6
- Add vprovides so initial-setup can use this

* Wed Apr 21 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-5
- Fix keyboard layouts getting out of sync in anaconda

* Tue Apr 20 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-4
- Fix infinite loop

* Mon Apr 19 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-3
- Fix crash

* Sun Apr 18 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-2
- Work with 3rd party keyboard layout selectors
- Be less aggressive about fullscreening windows

* Mon Apr 12 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-1
- Initial import
