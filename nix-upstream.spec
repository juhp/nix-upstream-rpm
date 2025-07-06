%global debug_package %{nil}

%global __check_files %{nil}
%global __brp_strip %{nil}
%global __brp_strip_lto %{nil}
%global __brp_strip_comment_note %{nil}
%global __brp_strip_static_archive %{nil}
%global __brp_check_rpaths %{nil}
%global __brp_mangle_shebangs %{nil}
%global __brp_remove_la_files %{nil}
%global __os_install_post_build_reproducibility %{nil}

Name:           nix-upstream
Version:        2.29.1
Release:        1%{?dist}
Summary:        A purely functional package manager

License:        LGPL-2.1-or-later
URL:            https://nixos.org/download/
Source0:        nix-2.29.1-x86_64-linux.tar.xz
Source1:        sysusers.conf

ExclusiveArch:  x86_64
Requires:       expect

%description
Package the upstream nix binary tarball.


%prep
%setup -q -n nix-%{version}-x86_64-linux

%build
rm -rf ~/.local/state/nix
./install
source ~/.nix-profile/etc/profile.d/nix.sh
nix-shell -p busybox -p bash --run 'echo "hi from nix-shell"'


%install
%global sys_nix_dir %{_prefix}/nix

mkdir -p %{buildroot}%{_prefix}

if [ -h ~/.local/state/nix/profiles/profile-1-link ]; then
    profile=profile-1-link
else
    profile=profile
fi
mv ~/.local/state/nix/profiles/${profile} %{buildroot}%{sys_nix_dir}

if [ -h %{buildroot}%{_prefix}/nix/bin ]; then
    echo "found /usr/nix/bin"
else
    echo "no /usr/nix/bin"
    exit 1
fi
sudo mkdir -p /nix/var/nix/profiles/default/bin
sudo ln -s /usr/bin/expect /nix/var/nix/profiles/default/bin

sudo mv /nix %{buildroot}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/nix-daemon.conf


%files
#%%license add-license-file-here
#%%doc add-docs-here
%{_prefix}/nix
/nix


%changelog
* Sun Jul 06 2025 Jens Petersen <juhpetersen@gmail.com>
-
