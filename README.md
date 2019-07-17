# zanup

# Language Translation
pygettext -v
pygettext --version
pygettext3 --version
rm messages.pot
pygettext -d base -o base.pot ui.py
vi base.pot
msgfmt -o base.mo base

msgmerge base.pot.cklee base.pot > base.pot
