# RPM package of the upstream nix tarball

Probably one of my worst hacks: note this probably needs to be built
inside a throw-away VM or maybe a rootful container, since it uses `sudo`.
I used a Fedora 42 WS Live 8GB instance with increased /run:

    sudo mount -o remount,size=4G /run

!!NB DO NOT BUILD ON YOUR OWN SYSTEM WITH nix INSTALLED!!
WARNING: `/nix` and `~/.local/state/nix` will be removed during rpmbuild!!

Use at your own risk.

<https://github.com/juhp/nix-upstream-rpm>

(This is not intended as a replacement for <https://github.com/juhp/nix-fedora>
which is built from source of course.)
