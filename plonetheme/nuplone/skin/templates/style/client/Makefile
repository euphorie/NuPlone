PACK		= yuicompressor --charset utf-8 --nomunge

TARGETS		= screen.min.css

all: ${TARGETS}

clean:
	-rm ${TARGETS}

%.min.css: %.css
	set -e ; $(PACK) $< > $@~ ; mv $@~ $@

.PHONY: all clean
