# RPM package of the upstream nix tarball

Probably one of my worst hacks: note this probably needs to be built
inside a throw-away VM or something like this, since it used `sudo`.
I used a Fedora 42 WS Live 8GB instance with increased /run:

    sudo mount -o remount,size=4G /run

!!NB DO NOT BUILD ON YOUR SYSTEM WITH nix INSTALLED!!

WARNING: `/nix` and `~/.local/state/nix` will be removed!!

Use at your own risk.
