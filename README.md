# nginx-quic.spec

[![Copr build status](https://copr.fedorainfracloud.org/coprs/ryoh/nginx-quic/package/nginx-quic/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/ryoh/nginx-quic/package/nginx-quic/)

nginx quic preview package.

- Enable QUIC and HTTP/3
- SSL library uses quictls (Support kernel TLS)
- Use cloudflare zlib
- Use jemalloc
- Enable debug option
- Enable FastTCP option
- And some optimize (Disable LTO)

## Build

Requirement

- epel repository
- scl repository [reference](https://wiki.centos.org/AdditionalResources/Repositories/SCL)

enable other repository

```
sudo yum install -y epel-release
sudo yum install -y centos-release-scl
```

install tools

```
sudo yum install -y rpmlint rpm-build rpmdevtools yum-utils 
```

prepare

```
git clone https://github.com/ryoh/nginx-quic.spec.git
cd nginx-quic
cp -p .rpmmacros $HOME/

# Install build dependent packages
yum-builddep -y SPECS/nginx-quic.spec

# Download SOURCES files
./prepare.sh
```

build

```
rpmbuild -ba SPECS/nginx-quic.spec
```
