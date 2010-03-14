#!/usr/bin/env python

# Copyright (C) 2008 Novell, Inc.
# Written by Brian G. Merrell <bgmerrell@novell.com>

# THIS FILE IS LICENSED UNDER THE MIT LICENSE

import replace as r
import re

# rename files first, REMEMBER to refer to them later as their new names
r.rename_file('chromium.spec', 'chromium-browser.spec');
r.rename_file('chromium.changes', 'chromium-browser.changes');

# change the master_preferences file to use SLEish settings instead of
# openSUSEish settings
r.replace_line('master_preferences',
               '     "http://www.opensuse.org",',
               '     "http://www.novell.com/linux",')
r.replace_line('master_preferences',
               '  "homepage": "http://www.opensuse.org",',
               '  "homepage": "http://www.novell.com/linux",')

# replace necessary lines in spec file
r.replace_line('chromium-browser.spec',
               'Name:           chromium',
               'Name:           chromium-browser')
r.remove_line('chromium-browser.spec',
              'Provides:       chromium-browser = %{version}')
r.remove_line('chromium-browser.spec',
              'Obsoletes:      chromium-browser < %{version}')

# fix patch
r.replace_line('chromium-master-prefs-path.patch',
               '+    master_prefs = FilePath("/etc/chromium");',
               '+    master_prefs = FilePath("/etc/chromium-browser");')

# rename the decompressed src directory from chromium to chromium-browser,
# also rename the tarball and compressed lzma
r.rename_src('chromium', 'chromium-browser')
