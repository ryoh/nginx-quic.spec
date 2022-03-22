srpm:
	dnf install -y rpkg rpm-build rpmdevtools
	spectool -g -R $(spec)
	cp -p SOURCES/* $(outdir)
	rpkg srpm --outdir $(outdir) --spec $(spec)
