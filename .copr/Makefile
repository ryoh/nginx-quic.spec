srpm:
	dnf install -y rpkg
	cp -p SOURCES/* $(outdir)
	rpkg srpm --outdir $(outdir) --spec $(spec)
