%global         _performance_build  1
%undefine       _hardened_build

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

%global         nginx_quic_commit   c5ea341f705a 
%global         boringssl_commit    777e1ff3b1443788c5fdb982b3b822aac5448d9e

%global         pkg_name            nginx-quic
%global         main_version        1.19.3
%global         main_release        10%{?dist}.%{nginx_quic_commit}.%{boringssl_commit}

Name:           %{pkg_name}
Version:        %{main_version}
Release:        %{main_release}
Summary:        A high performance web server and reverse proxy
Group:          System Environment/Daemons 
License:        BSD
URL:            https://nginx.org/

Source0:        https://hg.nginx.org/nginx-quic/archive/%{nginx_quic_commit}.tar.gz#/nginx-quic-%{nginx_quic_commit}.tar.gz
Source1:        https://hg.nginx.org/njs/archive/0.4.4.tar.gz#/njs-0.4.4.tar.gz

Source10:       nginx.service
Source11:       nginx.sysconf
Source12:       nginx.logrotate
Source13:       nginx.conf
Source14:       nginx-http.conf
Source15:       nginx-http-log_format.conf
Source16:       nginx-http-client.conf
Source17:       nginx-http-proxy.conf
Source18:       nginx-http-gzip.conf
Source19:       nginx-http-ssl.conf
Source20:       nginx-http-security_headers.conf
Source21:       nginx-http-proxy_headers.conf
Source22:       nginx-http-brotli.conf
Source50:       00-default.conf

Source100:      https://boringssl.googlesource.com/boringssl/+archive/%{boringssl_commit}.tar.gz#/boringssl-%{boringssl_commit}.tar.gz

Source200:      https://github.com/google/ngx_brotli/archive/v1.0.0rc.tar.gz#/ngx_brotli-v1.0.0rc.tar.gz
Source201:      https://github.com/leev/ngx_http_geoip2_module/archive/3.3.tar.gz#/ngx_http_geoip2_module-3.3.tar.gz
Source202:      https://github.com/SpiderLabs/ModSecurity-nginx/archive/v1.0.1.tar.gz#/ModSecurity-nginx-v1.0.1.tar.gz
Source203:      https://github.com/vozlt/nginx-module-vts/archive/v0.1.18.tar.gz#/nginx-module-vts-v0.1.18.tar.gz
Source204:      https://github.com/openresty/echo-nginx-module/archive/v0.62.tar.gz#/echo-nginx-module-v0.62.tar.gz
Source205:      https://github.com/openresty/headers-more-nginx-module/archive/v0.33.tar.gz#/headers-more-nginx-module-v0.33.tar.gz

Requires:       jemalloc
Requires:       brotli
Requires(pre):  shadow-utils
Requires(post):   systemd 
Requires(preun):  systemd 
Requires(postun): systemd 
BuildRequires:    systemd

BuildRequires:  make gcc automake autoconf libtool
BuildRequires:  zlib-devel pcre-devel
BuildRequires:  jemalloc-devel
BuildRequires:  cmake3 ninja-build golang
BuildRequires:  libunwind-devel
BuildRequires:  libatomic_ops-devel
BuildRequires:  brotli-devel
BuildRequires:  openssl-devel
BuildRequires:  GeoIP-devel
BuildRequires:  libmaxminddb-devel
BuildRequires:  readline-devel
%if 0%{?rhel} == 7
BuildRequires:  libmodsecurity-devel
BuildRequires:  expect-devel
BuildRequires:  devtoolset-9
BuildRequires:  rh-git218
%endif
%if 0%{?rhel} == 8
BuildRequires:  gcc-toolset-9
%endif

%description
nginx [engine x] is an HTTP and reverse proxy server, a mail proxy server,
and a generic TCP/UDP proxy server, originally written by Igor Sysoev.

%prep
%setup -q -n %{name}-%{nginx_quic_commit}

pushd ..
%{__rm} -rf boringssl
%{__mkdir} boringssl
cd boringssl
%{__tar} -xf %{SOURCE100}
popd

pushd ..
MODULE="njs"
%{__rm} -rf ${MODULE}
%{__mkdir} ${MODULE}
cd ${MODULE}
%{__tar} -xf %{SOURCE1} --strip 1
popd

pushd ..
%{__rm} -rf ngx_brotli
%{__mkdir} ngx_brotli
cd ngx_brotli
%{__tar} -xf %{SOURCE200} --strip 1
popd

pushd ..
%{__rm} -rf ngx_http_geoip2_module
%{__mkdir} ngx_http_geoip2_module
cd ngx_http_geoip2_module
%{__tar} -xf %{SOURCE201} --strip 1
popd

pushd ..
MODULE="ModSecurity-nginx"
%{__rm} -rf ${MODULE}
%{__mkdir} ${MODULE}
cd ${MODULE}
%{__tar} -xf %{SOURCE202} --strip 1
popd

pushd ..
MODULE="nginx-module-vts"
%{__rm} -rf ${MODULE}
%{__mkdir} ${MODULE}
cd ${MODULE}
%{__tar} -xf %{SOURCE203} --strip 1
popd

pushd ..
MODULE="echo-nginx-module"
%{__rm} -rf ${MODULE}
%{__mkdir} ${MODULE}
cd ${MODULE}
%{__tar} -xf %{SOURCE204} --strip 1
popd

pushd ..
MODULE="headers-more-nginx-module"
%{__rm} -rf ${MODULE}
%{__mkdir} ${MODULE}
cd ${MODULE}
%{__tar} -xf %{SOURCE205} --strip 1
popd

%build
%if 0%{?rhel} == 7
source scl_source enable devtoolset-9 ||:
source scl_source enable rh-git218 ||:
%endif
%if 0%{?rhel} == 8
source scl_source enable gcc-toolset-9 ||:
%endif

# BoringSSL
pushd ../boringssl
mkdir build
cd build
cmake3 -GNinja ..
ninja
popd

EXCC_OPTS="-ftree-vectorize -flto=8 -ffat-lto-objects -fuse-ld=gold -fuse-linker-plugin -Wformat -Wno-strict-aliasing -Wno-stringop-truncation -gsplit-dwarf"
CFLAGS="$(echo %{optflags} $(pcre-config --cflags) | sed -e 's/-O2/-O3/')"
CFLAGS="${CFLAGS} ${EXCC_OPTS}"; export CFLAGS;
export CXXFLAGS="${CFLAGS}"
LDFLAGS="%{?__global_ldflags} -Wl,-E -lrt -ljemalloc -lpcre -flto=8 -fuse-ld=gold"; export LDFLAGS;

pushd ../njs
./configure
%make_build
popd

./auto/configure \
  --with-debug \
  --with-cc-opt="-I../boringssl/include ${CFLAGS}" \
  --with-ld-opt="-L../boringssl/build/ssl -L../boringssl/build/crypto ${LDFLAGS}" \
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
  --with-libatomic \
  --with-compat \
  --with-pcre \
  --with-pcre-jit \
  --with-http_ssl_module \
  --with-http_v2_module \
  --with-http_v3_module \
  --with-http_quic_module \
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
  --with-http_geoip_module=dynamic \
  --add-dynamic-module=../njs/nginx \
  --add-dynamic-module=../ngx_brotli \
  --add-dynamic-module=../ngx_http_geoip2_module \
  --add-dynamic-module=../nginx-module-vts \
  --add-dynamic-module=../echo-nginx-module \
  --add-dynamic-module=../headers-more-nginx-module \
%if 0%{?rhel} == 7
  --add-dynamic-module=../ModSecurity-nginx \
%endif


%make_build

%install
[[ -d %{buildroot} ]] && rm -rf "%{buildroot}"
%{__mkdir} -p "%{buildroot}"
%make_install INSTALLDIRS=vendor

# njs bin
%if 0%{?rhel} == 7
%{__install} -p -D -m 0755 %{_builddir}/njs/build/njs %{buildroot}%{_bindir}/njs
%endif

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

# Add systemd service unit file
%{__install} -p -D -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/nginx.service

# sysconfig
%{__install} -p -D -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/nginx

# logrotate
%{__install} -p -D -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/logrotate.d/nginx

# nginx config
unlink %{buildroot}%{nginx_confdir}/koi-utf
unlink %{buildroot}%{nginx_confdir}/koi-win
unlink %{buildroot}%{nginx_confdir}/win-utf
%{__install} -p -D -m 0640 %{SOURCE13} %{buildroot}%{nginx_confdir}/nginx.conf
%{__install} -p -D -m 0640 %{SOURCE14} %{buildroot}%{nginx_confdir}/conf.d/http.conf
%{__install} -p -D -m 0640 %{SOURCE15} %{buildroot}%{nginx_confdir}/conf.d/http/log_format.conf
%{__install} -p -D -m 0640 %{SOURCE16} %{buildroot}%{nginx_confdir}/conf.d/http/client.conf
%{__install} -p -D -m 0640 %{SOURCE17} %{buildroot}%{nginx_confdir}/conf.d/http/proxy.conf
%{__install} -p -D -m 0640 %{SOURCE18} %{buildroot}%{nginx_confdir}/conf.d/http/gzip.conf
%{__install} -p -D -m 0640 %{SOURCE19} %{buildroot}%{nginx_confdir}/conf.d/http/ssl.conf
%{__install} -p -D -m 0640 %{SOURCE20} %{buildroot}%{nginx_confdir}/conf.d/http/security_headers.conf
%{__install} -p -D -m 0640 %{SOURCE21} %{buildroot}%{nginx_confdir}/conf.d/http/proxy_headers.conf
%{__install} -p -D -m 0640 %{SOURCE22} %{buildroot}%{nginx_confdir}/conf.d/http/brotli.conf

%{__install} -p -D -m 0640 %{SOURCE50} %{buildroot}%{nginx_confdir}/vhost.d/http/00-default.conf

# nginx modules conf
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.modules.d/

# brotli module
cat <<__EOL__ > %{buildroot}%{nginx_confdir}/conf.modules.d/ngx_brotli.conf
load_module "%{nginx_moddir}/ngx_http_brotli_filter_module.so";
load_module "%{nginx_moddir}/ngx_http_brotli_static_module.so";
__EOL__

# nginx reset paths
%{__sed} -i \
  -e 's|${rundir}|%{_rundir}|g' \
  -e 's|${sbindir}|%{_sbindir}|g' \
  -e 's|${sysconfdir}|%{_sysconfdir}|g' \
  -e 's|${logdir}|%{nginx_logdir}|g' \
  -e 's|${pkg_name}|nginx|g' \
  %{buildroot}%{_unitdir}/nginx.service \
  %{buildroot}%{_sysconfdir}/sysconfig/nginx \
  %{buildroot}%{_sysconfdir}/logrotate.d/nginx \
  %{buildroot}%{nginx_confdir}/nginx.conf

%{__sed} -i \
  -e 's|${client_tempdir}|%{nginx_client_tempdir}|g' \
  %{buildroot}%{nginx_confdir}/conf.d/http/client.conf

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
%systemd_post nginx.service
case $1 in
  1)
  : install
  ;;
  2)
  : update
  ;;
esac

%preun
%systemd_pre nginx.service
case $1 in
  0)
  : uninstall
  ;;
  1)
  : update
  ;;
esac

%postun
%systemd_postun nginx.service
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
%config(noreplace) %{nginx_confdir}/conf.d/http.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/client.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/gzip.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/log_format.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/proxy.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/ssl.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/security_headers.conf
%config(noreplace) %{nginx_confdir}/conf.d/http/proxy_headers.conf
%config(noreplace) %{nginx_confdir}/vhost.d/http/00-default.conf

%dir %{nginx_home}
%dir %{nginx_webroot}
%{nginx_webroot}/50x.html
%{nginx_webroot}/index.html

%config(noreplace) %{_unitdir}/nginx.service
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%config(noreplace) %{_sysconfdir}/logrotate.d/nginx

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

# njs
%dir %{nginx_moddir}
%if 0%{?rhel} == 7
%{_bindir}/njs
%endif
%{nginx_moddir}/ngx_http_js_module.so

# Brotli
%config(noreplace) %{nginx_confdir}/conf.d/http/brotli.conf
%config(noreplace) %{nginx_confdir}/conf.modules.d/ngx_brotli.conf
%{nginx_moddir}/ngx_http_brotli_filter_module.so
%{nginx_moddir}/ngx_http_brotli_static_module.so

# GeoIP
%{nginx_moddir}/ngx_http_geoip_module.so

# GeoIP2
%{nginx_moddir}/ngx_http_geoip2_module.so

# ModSecurity
%if 0%{?rhel} == 7
%{nginx_moddir}/ngx_http_modsecurity_module.so
%endif

# VTS
%{nginx_moddir}/ngx_http_vhost_traffic_status_module.so

# util modules
%{nginx_moddir}/ngx_http_echo_module.so
%{nginx_moddir}/ngx_http_headers_more_filter_module.so


%changelog
* Tue Oct 27 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.3-10
- Change bumpup version nginx-quic, boringssl
- Add njs module
- Add GeoIP module
- Add GeoIP2 module
- Add ModSecurity module
- Add VTS module
- Add echo module
- Add headers more filter module
* Tue Aug 11 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-9
- Change bumpup version nginx-quic, boringssl
* Wed Jul 29 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-8
- Add h3 directive: http3_max_field_size, http3_max_table_capacity, http3_max_blocked_streams, http3_max_concurrent_pushes, http3_push, http3_push_preload
- Add "quic" listen parameter
- Add HTTP/3 Server Push
- Add support HTTP/3 $server_protocol variable
- Add QUIC support for stream module
- Change build options
* Sun Jul 19 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-7
- Add Brotli module
* Sun Jul 19 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-6
- Change build options
* Sun Jul 19 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-5
- Change nginx-quic and boringssl commit version master -> commit hash
- Change snapshot version
* Thu Jul 16 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-4
- Delete openssl11-libs, openssl11-devel
* Wed Jul 15 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-1
- Add Conf files
* Fri Jul 10 2020 Ryoh Kawai <kawairyoh@gmail.com> - 1.19.1-0
- Initial
