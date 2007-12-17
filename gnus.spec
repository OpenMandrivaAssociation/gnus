%define cvs    0
%define sname	ngnus-0.3

%define rel 1
%define release %mkrel %{rel}

%define infodir %_infodir/packages/%{name}
%define _install_info()	%{__install_info} %{infodir}/%{1}%{_extension} --dir=%{infodir}/dir\;
%define _remove_install_info() if [ "$1" = "0" ]; then %{__install_info} %{infodir}/%{1}%{_extension} --dir=%{infodir}/dir --remove ; fi %{nil}

%{expand:%%define emacs_version %(rpm -q emacs|sed 's/emacs-\([0-9].*\)-.*$/\1/')}
%{expand:%%define xemacs_version %(rpm -q xemacs|sed 's/xemacs-\([0-9].*\)-.*$/\1/')}

Summary:	Gnus Newsreader for Emacs
Name:	gnus
Epoch:	1
Version:	5.10.8
Release:	%release
%if %cvs
Source0:	http://www.gnus.com/dist/%sname.tar.bz2
%else
Source0:	http://www.gnus.com/dist/%name-%version.tar.bz2
%endif
Source1: 	gnus-emacs.el
#Source2: 	gnus-xemacs.el
URL: 		http://www.gnus.org/
License: 	GPL
Group: 		Networking/News
BuildArchitectures: noarch
BuildRequires: emacs-bin

%description
You can read news (and mail) from within Emacs by using Gnus. The news can be
gotten by any nefarious means you can think of -- NNTP, local spool or your
mbox file. All at the same time, if you want to push your luck.

%package doc
Summary: 	Gnus Newsreader for XEmacs
Group: 		Networking/News

%description doc
You can read news (and mail) from within Emacs by using Gnus. The news can be
gotten by any nefarious means you can think of -- NNTP, local spool or your
mbox file. All at the same time, if you want to push your luck.

This package is the documentation info files for GNUS version %{version}.

%package emacs
Summary: 	Gnus Newsreader for Emacs
Group: 		Networking/News
Requires: 	emacs
Obsoletes: 	gnus
Provides:	gnus = %version

%description emacs
You can read news (and mail) from within Emacs by using Gnus. The news can be
gotten by any nefarious means you can think of -- NNTP, local spool or your
mbox file. All at the same time, if you want to push your luck.

This version is compiled for GNU/Emacs %{emacs_version}

#%package xemacs
#Summary: Gnus Newsreader for XEmacs
#Copyright: GPL
#Group: Networking/News
#Requires: xemacs = %{xemacs_version}
#
#%description xemacs
#You can read news (and mail) from within Emacs by using Gnus. The news can be
#gotten by any nefarious means you can think of -- NNTP, local spool or your
#mbox file. All at the same time, if you want to push your luck.
#
#This version is compiled for XEmacs %{xemacs_version}

%prep
%if %cvs
%setup -q -n %sname
%else
%setup -q
%endif

%build
# We don't build it since even in the %%install gnus want always to do it.
install -d BUILD
mv [a-z]* Makefile* BUILD

for i in emacs ; do
  cp -a BUILD $i-build
  (cd $i-build ; EMACS=/usr/bin/$i %configure --with-lispdir=%{_datadir}/$i/site-lisp/%{name})
done

%install
rm -rf $RPM_BUILD_ROOT

for i in emacs ; do
  make -C $i-build install infodir=%buildroot%{infodir} lispdir=%buildroot%{_datadir}/$i/site-lisp/%{name} EMACS=/usr/bin/$i
done

install -d %buildroot%{_sysconfdir}/emacs/site-start.d
cat << EOF > %buildroot%{_sysconfdir}/emacs/site-start.d/%{name}-emacs.el
%{expand:%(%__cat %{SOURCE1})}
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%post doc 
%_install_info %{name}
%_install_info message
%_install_info emacs-mime

%preun doc
%_remove_install_info %{name}

%_remove_install_info message

%_remove_install_info emacs-mime

%files doc
%defattr(-,root,root)
%{infodir}/*

%files emacs
%defattr(-,root,root)
%doc GNUS-NEWS BUILD/lisp/ChangeLog
%dir %_datadir/emacs/site-lisp/%{name}
%_datadir/emacs/site-lisp/%{name}/*
%dir %_datadir/emacs/etc/images/%{name}
%_datadir/emacs/etc/images/%{name}/*
%_datadir/emacs/etc/images/smilies/*
%_datadir/emacs/etc/%{name}-tut.txt

%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}-emacs*

#%files xemacs
#%defattr(-,root,root)
#%doc GNUS-NEWS README
#%{_datadir}/xemacs/site-lisp/%{name}
#%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}-xemacs*

