PYTHON		?= python2.7

POT		= plonetheme/nuplone/locales/nuplone.pot
PO_FILES	= $(wildcard plonetheme/nuplone/locales/*/LC_MESSAGES/nuplone.po)
MO_FILES	= $(PO_FILES:.po=.mo)

TARGETS		= $(MO_FILES)

all: ${TARGETS}

clean::
	-rm ${TARGETS}

bin/buildout: bootstrap.py
	$(PYTHON) bootstrap.py

bin/pybabel bin/test bin/sphinx-build: bin/buildout buildout.cfg versions.cfg setup.py
	bin/buildout -t 10
	touch bin/test
	touch bin/sphinx-build
	touch bin/pybabel

check:: bin/test ${MO_FILES}
	bin/test

jenkins: bin/test bin/sphinx-build $(MO_FILES)
	bin/test --xml

docs:: bin/sphinx-build
	make -C docs html

clean::
	rm -rf docs/.build

pot: bin/pybabel
	bin/pybabel extract -F babel.cfg \
		--copyright-holder='Simplon B.V. - Wichert Akkerman' \
		--msgid-bugs-address='euphorie@lists.wiggy.net' \
		--charset=utf-8 \
		plonetheme > $(POT)~
	mv $(POT)~ $(POT)	
	$(MAKE) $(MFLAGS) $(PO_FILES)

$(PO_FILES): $(POT)
	msgmerge --update $@ $<

.po.mo:
	msgfmt -c --statistics -o $@~ $< && mv $@~ $@

.PHONY: all clean docs jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
