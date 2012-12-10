;; -*- Mode: Emacs-Lisp -*-
; Copyright (C) 2000 by Chmouel Boudjnah, MandrakeSoft.
; 
; Redistribution of this file is permitted under the terms of the GNU 
; Public License (GPL)
;

(if (string-match "GNU Emacs" (version))
    (progn
      (add-to-list 'load-path "/usr/share/emacs/site-lisp/gnus")
      (add-to-list 'Info-default-directory-list "/usr/share/info/packages/gnus"))
  )
