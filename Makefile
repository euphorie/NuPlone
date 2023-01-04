PYTHON		?= python2.7

POT		= plonetheme/nuplone/locales/nuplone.pot
PO_FILES	= $(wildcard plonetheme/nuplone/locales/*/LC_MESSAGES/nuplone.po)
MO_FILES	= $(PO_FILES:.po=.mo)

TARGETS		= $(MO_FILES)
BINDIR      ?= .bundle/bin
BUNDLE      ?= $(BINDIR)/bundle
YARN		?= npx yarn

all: ${TARGETS}

bundle bundle.js bundles/oira.cms.js: stamp-yarn
	npm run build


.PHONY: clean
clean::
	-rm ${TARGETS}
	rm -rf stamp-yarn node_modules bundles/*


##
# PATTERNSLIB
##


# Install patternslib
stamp-yarn:
	$(YARN) install
	touch stamp-yarn


# Build JavaScript bundle
.PHONY: bundle
bundle: stamp-yarn

	-$(YARN) unlink @patternslib/pat-redactor
	-$(YARN) unlink @patternslib/patternslib
	$(YARN) install --force
	$(YARN) build


.PHONY: bundledev
bundledev: stamp-yarn

	$(YARN) builddev


# Watch JavaScript for changes
.PHONY: watch
watch: stamp-yarn
	$(YARN) watch


.PHONY: devln
devln:
	$(YARN) link "@patternslib/patternslib"


.PHONY: undevln
undevln:
	$(YARN) unlink "@patternslib/patternslib"


# OTHER


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
		--charset=utf-8 \
		plonetheme > $(POT)~
	mv $(POT)~ $(POT)
	$(MAKE) $(MFLAGS) $(PO_FILES)

$(PO_FILES): $(POT)
	msgmerge --update $@ $<

.po.mo:
	msgfmt -c --statistics -o $@~ $< && mv $@~ $@

.PHONY: all docs jenkins pot
.SUFFIXES:
.SUFFIXES: .po .mo .css .min.css
