%define cvs    0
%define sname	ngnus-0.3

%define rel 3
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
License: 	GPLv2+
Group: 		Networking/News
BuildRoot: 	%{_tmppath}/%{name}-buildroot
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



%changelog
* Sat Jul 17 2010 Sandro Cazzaniga <kharec@mandriva.org> 1:5.10.8-3mdv2011.0
+ Revision: 554697
- fix license

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1:5.10.8-2mdv2010.0
+ Revision: 429284
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1:5.10.8-1mdv2009.0
+ Revision: 136456
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - import gnus


* Fri Jul 14 2006 Olivier Blin <blino@mandriva.com> 5.10.8-1mdv2007.0
- 5.10.8
- adapt to new lispdir and etcdir

* Fri May  6 2005 Pixel <pixel@mandriva.com> 5.10.6-6mdk
- no need to load info before setting Info-default-directory-list (this fixed bugzilla #9395)

* Mon May 02 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.6-5mdk
- no-gnus 0.3
- remove packager tag

* Thu Dec 23 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.6-4mdk
- fix info pages (anthill #1241)

* Tue May 04 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.6-3mdk
- no-gnus 0.2

* Fri Apr 23 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.6-2mdk
- no-gnus 0.1

* Mon Jan 05 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.6-1mdk
- new release

* Wed May 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.2-1mdk
- gnus-5.10.2

* Mon May 12 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.10.1-1mdk
- gnus-5.10.1

* Tue Apr 29 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-16mdk
- oort gnus-0.19

* Tue Apr 29 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-15mdk
- oort gnus-0.18

* Fri Apr 25 2003 Pixel <pixel@mandrakesoft.com> 6.0.0-14mdk
- replace BuildRequires emacs with emacs-bin

* Wed Apr 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-13mdk
- rebuild for new emacs

* Tue Apr 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-12mdk
- oort gnus-0.17

* Wed Mar 19 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-11mdk
- oort gnus-0.16

* Mon Feb 10 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-10mdk
- oort gnus-0.15

* Mon Jan 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-9mdk
- oort gnus-0.14

* Tue Jan 21 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-8mdk
- oort gnus-0.13

* Mon Jan 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-7mdk
- oort gnus-0.12

* Mon Jan 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-6mdk
- oort gnus-0.10

* Thu Nov 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-5mdk
- rebuild for current emacs

* Wed Oct 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-4mdk
- rebuild for current emacs

* Tue Oct 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-3mdk
- fix pre-un

* Tue Sep 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 6.0.0-1mdk
- Oort gnus v0.07

* Mon May 06 2002 Yves Duret <yduret@mandrakesoft.com> 6.0.0-1mdk
- Oort Gnus v0.06

* Tue Apr 30 2002 Yves Duret <yduret@mandrakesoft.com> 6.0.0-0.20020430.1mdk
- new cvs snapshot
- now good for mdk

* Wed Aug 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.9.0-0.20010808-1mdk
- cvs snapshot

* Wed Aug 01 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.9.0.oort_v0.0.3-0.1_oort_v0.0.3mdk
- cvs snapshot

* Thu Mar  8 2001 Pixel <pixel@mandrakesoft.com> 5.8.8-2mdk
- rebuild, removing xemacs-gnus

* Sat Jan  6 2001 Pixel <pixel@mandrakesoft.com> 5.8.8-1mdk
- fix chmouel's split (strange, he didn't use brute force? he shouldn't, he's not used to it ;p)
- cleanup and fix
- new version

* Tue Jan  2 2001 Pixel <pixel@mandrakesoft.com> 5.8.7-5mdk
- remove ugly require xemacs in gnus-doc (chmousux)

* Tue Nov 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.8.7-4mdk
- Move info files to %%infodir and add to lisp path in the .el files.

* Tue Nov 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.8.7-3mdk
- Fix %%preun.
- Split in different pacakge -emacs -xemacs and -doc, -emacs obsoletes
  now gnus-.

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 5.8.7-2mdk
- add packager tag

* Thu Aug 24 2000 Pixel <pixel@mandrakesoft.com> 5.8.7-1mdk
- first version
