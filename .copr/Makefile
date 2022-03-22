srpm:
	dnf install -y rpkg rpm-build rpmdevtools
	spectool -g -C $(outdir) $(spec)
	cp -p SOURCES/* $(outdir)
	rpkg srpm --outdir $(outdir) --spec $(spec)
