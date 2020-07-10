%global         _performance_build  1
%global         _hardened_build     1

%global         nginx_user          nginx
%global         nginx_group         nginx
%global         nginx_uid           996
%global         nginx_gid           996
%global         nginx_moddir        %{_libdir}/nginx/modules
%global         nginx_confdir       %{_sysconfdir}/nginx
%global         nginx_tempdir       %{_var}/cache/nginx
%global         nginx_logdir        %{_localstatedir}/log/nginx
%global         nginx_rundir        %{_rundir}
%global         nginx_lockdir       %{_rundir}/lock/subsys/nginx
%global         nginx_home          %{_datadir}/nginx
%global         nginx_webroot       %{nginx_home}/html
%global         nginx_client_tempdir   %{nginx_tempdir}/client_body_temp
%global         nginx_proxy_tempdir    %{nginx_tempdir}/proxy_temp
%global         nginx_fastcgi_tempdir  %{nginx_tempdir}/fastcgi_temp
%global         nginx_uwsgi_tempdir    %{nginx_tempdir}/uwsgi_temp
%global         nginx_scgi_tempdir     %{nginx_tempdir}/scgi_temp
%global         nginx_proxy_cachedir   %{nginx_tempdir}/proxy_cache
%global         nginx_fastcgi_cachedir %{nginx_tempdir}/fastcgi_cache
%global         nginx_uwsgi_cachedir   %{nginx_tempdir}/uwsgi_cache
%global         nginx_scgi_cachedir    %{nginx_tempdir}/scgi_cache

%global         pkg_name            nginx-quic
%global         main_version        1.19.1
%global         main_release        0%{?dist}

Name:           %{pkg_name}
Version:        %{main_version}
Release:        %{main_release}
Summary:        A high performance web server and reverse proxy
Group:          System Environment/Daemons 
License:        BSD
URL:            https://nginx.org/

Source0:        https://hg.nginx.org/nginx-quic/archive/quic.tar.gz
Source100:      https://boringssl.googlesource.com/boringssl/+archive/refs/heads/master.tar.gz

Requires:       openssl11-libs
Requires:       jemalloc
Requires(pre):  shadow-utils
Requires(post):   systemd 
Requires(preun):  systemd 
Requires(postun): systemd 
BuildRequires:    systemd

BuildRequires:  make gcc automake autoconf libtool
BuildRequires:  zlib-devel pcre-devel
BuildRequires:  jemalloc-devel
BuildRequires:  cmake3 ninja-build golang
BuildRequires:  openssl11-devel
BuildRequires:  libunwind-devel

%description
nginx [engine x] is an HTTP and reverse proxy server, a mail proxy server,
and a generic TCP/UDP proxy server, originally written by Igor Sysoev.

%prep
%setup -q -n %{name}-quic

pushd ..
%{__rm} -rf boringssl
%{__mkdir} boringssl
cd boringssl
%{__tar} -xf %{SOURCE100}
popd


%build
pushd ../boringssl
mkdir build
cd build
cmake3 -GNinja ..
ninja

cd ..
mkdir -p .openssl/lib
cd .openssl
ln -s ../include .
cd ..
cp build/crypto/libcrypto.a build/ssl/libssl.a .openssl/lib
popd

source scl_source enable devtoolset-9 ||:

CFLAGS="${CFLAGS:-%{optflags} $(pcre-config --cflags)}"; export CFLAGS;
export CXXFLAGS="${CXXFLAGS:-${CFLAGS}}"
LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS} -Wl,-E -ljemalloc}"; export LDFLAGS;

./auto/configure \
  --with-debug \
  --with-cc-opt="-I../boringssl/include -DTCP_FASTOPEN=23" \
  --with-ld-opt="-L../boringssl/build/ssl -L../boringssl/build/crypto" \
  --prefix=%{nginx_home} \
  --sbin-path=%{_sbindir}/nginx \
  --modules-path=%{nginx_moddir} \
  --conf-path=%{nginx_confdir}/nginx.conf \
  --pid-path=%{nginx_rundir}/nginx.pid \
  --lock-path=%{nginx_lockdir} \
  --error-log-path=%{nginx_logdir}/error.log \
  --http-log-path=%{nginx_logdir}/access.log \
  --http-client-body-temp-path=%{nginx_client_tempdir} \
  --http-proxy-temp-path=%{nginx_proxy_tempdir} \
  --http-fastcgi-temp-path=%{nginx_fastcgi_tempdir} \
  --http-uwsgi-temp-path=%{nginx_uwsgi_tempdir} \
  --http-scgi-temp-path=%{nginx_scgi_tempdir} \
  --user=%{nginx_user} \
  --group=%{nginx_group} \
  --build=%{name}-%{version}-%{release} \
  --with-threads \
  --with-file-aio \
  --with-compat \
  --with-pcre \
  --with-pcre-jit \
  --with-http_ssl_module \
  --with-http_v2_module \
  --with-http_v3_module \
  --with-http_realip_module \
  --with-http_addition_module \
  --with-http_sub_module \
  --with-http_dav_module \
  --with-http_flv_module \
  --with-http_mp4_module \
  --with-http_gunzip_module \
  --with-http_gzip_static_module \
  --with-http_auth_request_module \
  --with-http_random_index_module \
  --with-http_secure_link_module \
  --with-http_degradation_module \
  --with-http_slice_module \
  --with-http_stub_status_module \

%make_build

%install
[[ -d %{buildroot} ]] && rm -rf "%{buildroot}"
%{__mkdir} -p "%{buildroot}"
%make_install INSTALLDIRS=vendor

# Deleting unused files
%{__rm} -f %{buildroot}%{nginx_confdir}/fastcgi.conf
%{__rm} -f %{buildroot}%{nginx_confdir}/*.default

# Create temporary directories
%{__install} -p -d -m 0755 %{buildroot}%{nginx_rundir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_lockdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_tempdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_client_tempdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_proxy_tempdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_fastcgi_tempdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_uwsgi_tempdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_scgi_tempdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_proxy_cachedir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_fastcgi_cachedir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_uwsgi_cachedir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_scgi_cachedir}

# nginx config
unlink %{buildroot}%{nginx_confdir}/koi-utf
unlink %{buildroot}%{nginx_confdir}/koi-win
unlink %{buildroot}%{nginx_confdir}/win-utf

%pre
case $1 in
  1)
  : install
  getent group %{nginx_group} >/dev/null 2>&1 \
    || groupadd -r -g %{nginx_gid} %{nginx_group} \
    || groupadd -r %{nginx_group}

  getent passwd %{nginx_user} >/dev/null 2>&1 \
    || useradd -r -g %{nginx_group} -u %{nginx_uid} %{nginx_user} \
    || useradd -r -g %{nginx_group} %{nginx_user}
  ;;
  2)
  : update
  ;;
esac

%post
#%systemd_post nginx.service
case $1 in
  1)
  : install
  ;;
  2)
  : update
  ;;
esac

%preun
#%systemd_pre nginx.service
case $1 in
  0)
  : uninstall
  ;;
  1)
  : update
  ;;
esac

%postun
#%systemd_postun nginx.service
case $1 in
  0)
  : uninstall
  getent passwd %{nginx_user} >/dev/null 2>&1 \
    && userdel %{nginx_user} >/dev/null 2>&1 ||:

  getent group %{nginx_group} >/dev/null 2>&1 \
    && groupdel %{nginx_group} >/dev/null 2>&1 ||:
  ;;
  1)
  : update
  ;;
esac


%files
%defattr(-,root,root)
%{_sbindir}/nginx

%config(noreplace) %{nginx_confdir}/nginx.conf
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params

%dir %{nginx_home}
%dir %{nginx_webroot}
%{nginx_webroot}/50x.html
%{nginx_webroot}/index.html

%dir %{nginx_rundir}
%dir %{nginx_lockdir}

%defattr(-,%{nginx_user},%{nginx_group})
%dir %{nginx_logdir}
%dir %{nginx_tempdir}
%dir %{nginx_client_tempdir}
%dir %{nginx_proxy_tempdir}
%dir %{nginx_fastcgi_tempdir}
%dir %{nginx_uwsgi_tempdir}
%dir %{nginx_scgi_tempdir}
%dir %{nginx_proxy_cachedir}
%dir %{nginx_fastcgi_cachedir}
%dir %{nginx_uwsgi_cachedir}
%dir %{nginx_scgi_cachedir}


%changelog
* Fri Jul 10 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-0
- Initial
