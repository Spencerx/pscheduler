#
# Makefile for any tool class
#

NAME=tracemtu

FILES=\
	can-run \
	duration \
	enumerate \
	merged-results \
	participant-data \
	run \
	common.py

install: $(FILES)
ifndef DESTDIR
	@echo No DESTDIR specified for installation
	@false

endif
	mkdir -p $(DESTDIR)
	install -m 555 $(FILES) $(DESTDIR)

clean:
	rm -f $(TO_CLEAN) *~
