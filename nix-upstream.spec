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
Source2:        nix.conf
Source3:        LICENSE

ExclusiveArch:  x86_64
Requires:       expect

%description
Package the upstream nix binary tarball.


%prep
%setup -q -n nix-%{version}-x86_64-linux
cp %{SOURCE3} .


%build
rm -rf ~/.local/state/nix
./install
source ~/.nix-profile/etc/profile.d/nix.sh
nix-shell -p busybox -p bash --run 'echo "hi from nix-shell"'


%install
if [ -h ~/.local/state/nix/profiles/profile-1-link ]; then
    profile=profile-1-link
else
    profile=profile
fi

%global user_profile ~/.local/state/nix/profiles/${profile}

nix_profile=`readlink -f %{user_profile}`

echo ${nix_profile}

mkdir -p %{buildroot}%{_bindir}
(
    cd %{user_profile}/bin
    for i in *; do
        ln -s ${nix_profile}/bin/$i %{buildroot}%{_bindir}/
    done
)

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
(
    cd %{user_profile}%{_sysconfdir}/profile.d
    for i in *; do
        ln -s ${nix_profile}%{_sysconfdir}/profile.d/$i %{buildroot}%{_sysconfdir}/profile.d
    done
)

mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
(
    cd %{user_profile}/lib/systemd/system
    for i in *; do
        ln -s ${nix_profile}/lib/systemd/system/$i %{buildroot}%{_prefix}/lib/systemd/system/
    done
)
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
ln -s ${nix_profile}/lib/tmpfiles.d/* %{buildroot}%{_prefix}/lib/tmpfiles.d/

mkdir -p %{buildroot}%{_libexecdir}
ln -s ${nix_profile}%{_libexecdir}/nix %{buildroot}%{_libexecdir}

mkdir -p %{buildroot}%{bash_completions_dir}
ln -s ${nix_profile}/share/bash-completion/completions/nix %{buildroot}%{bash_completions_dir}

mkdir -p %{buildroot}%{fish_completions_dir}
ln -s ${nix_profile}/share/fish/vendor_completions.d/nix.fish %{buildroot}%{fish_completions_dir}

mkdir -p %{buildroot}%{zsh_completions_dir}
ln -s ${nix_profile}/share/zsh/vendor_completions.d/_nix %{buildroot}%{zsh_completions_dir}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/nix-daemon.conf
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/nix/nix.conf

sudo mkdir -p /nix/var/nix/profiles/default/bin
sudo ln -sf /usr/bin/expect /nix/var/nix/profiles/default/bin

sudo mv /nix %{buildroot}


%files
%license LICENSE
/nix
%{_sysconfdir}/nix/nix.conf
%{_sysconfdir}/profile.d/*
%{_sysusersdir}/nix-daemon.conf
%{_bindir}/*
%{_prefix}/lib/systemd/system/nix-daemon.service
%{_prefix}/lib/systemd/system/nix-daemon.socket
%{_libexecdir}/*
%{_datadir}/bash-completion/completions/nix
%{_datadir}/fish/vendor_completions.d/nix.fish
%{_datadir}/zsh/site-functions/*


%changelog
* Mon Jul 07 2025 Jens Petersen <petersen@redhat.com> - 2.29.1-1
- initial working packaging for singleuser at least
