#
# Makefile for pScheduler Core
#

#
# The following variables need to be specified when running this
# Makefile:
#
#   ARCHIVEDEFAULTDIR   Where default archivers live
#   BINDIR              Where binaries should be installed (e.g., /usr/bin)
#   COMMANDSDIR         Where command programs should be installed
#   COMMANDSINSTALLED   Where $(COMMANDSDIR) is when installed
#   INTERNALSDIR         Where internal programs should be installed
#   INTERNALSINSTALLED   Where $(INTERNALSDIR) is when installed
#   TOOLCONFIGDIR       Where tool configuration files live
#

PROGRAMS=

RAWPROGRAMS=\
	pscheduler

COMMANDS=\
	archiving-summary \
	batch \
	cancel \
	clock \
	env \
	metrics \
	monitor \
	ping \
	plot-schedule \
	plugins \
	result \
	schedule \
	task \
	troubleshoot \
	version \
	watch

RAWCOMMANDS=\
	diags \
	internal \
	validate-limits

INTERNALS=\
	nothing

RAWINTERNALS=\
	list

RAWBASHCOMPLETION=\
	bash_completion

ALLPROGRAMS=$(PROGRAMS) $(RAWPROGRAMS)
ALLCOMMANDS=$(COMMANDS) $(RAWCOMMANDS)
ALLINTERNALS=$(INTERNALS) $(RAWINTERNALS)

ALLRAW=$(RAWPROGRAMS) $(RAWCOMMANDS) $(RAWINTERNALS) $(RAWBASHCOMPLETION)
ALLRAW=$(ALLRAW:%=%.raw)

ALL=$(ALLPROGRAMS) $(ALLCOMMANDS) $(ALLINTERNALS) $(RAWBASHCOMPLETION)


default:  build

%: %.raw
ifndef ARCHIVEDEFAULTDIR
	@echo No ARCHIVEDEFAULTDIR specified for build of $@
	@false
endif
ifndef CLASSESINSTALLED
	@echo No CLASSESINSTALLED specified for build of $@
	@false
endif
ifndef COMMANDSINSTALLED
	@echo No COMMANDSINSTALLED specified for build of $@
	@false
endif
ifndef INTERNALSINSTALLED
	@echo No INTERNALSSINSTALLED specified for build of $@
	@false
endif
ifndef LIMITSFILE
	@echo No LIMITSFILE specified for build of $@
	@false
endif
ifndef TOOLCONFIGDIR
	@echo No TOOLCONFIGDIR specified for build of $@
	@false
endif
	sed \
		-e 's|__ARCHIVE_DEFAULT__|$(ARCHIVEDEFAULTDIR)|g' \
		-e 's|__COMMANDS__|$(COMMANDSINSTALLED)|g' \
		-e 's|__CLASSES__|$(CLASSESINSTALLED)|g' \
		-e 's|__INTERNALS__|$(INTERNALSINSTALLED)|g' \
		-e 's|__LIMITS_FILE__|$(LIMITSFILE)|g' \
		-e 's|__TOOLCONFIGDIR__|$(TOOLCONFIGDIR)|g' \
		$< > $@
	@if egrep -e '__[A-Z_]+__' $@ ; then \
		echo "Found un-substituted values in processed file $@" ; \
		false ; \
	fi


build: $(ALL)
TO_CLEAN += $(RAWPROGRAMS) $(RAWCOMMANDS) $(RAWINERNALS) $(RAWBASHCOMPLETION)


install: $(ALL)
ifndef BASHCOMPDIR
	@echo No BASHCOMPDIR specified for installation
	@false
endif
ifndef BINDIR
	@echo No BINDIR specified for installation
	@false
endif
ifndef COMMANDSDIR
	@echo No COMMANDSDIR specified for installation
	@false
endif
ifndef INTERNALSDIR
	@echo No INTERNALSDIR specified for installation
	@false
endif
	mkdir -p $(BINDIR)
	install -m 555 $(ALLPROGRAMS) $(BINDIR)
	mkdir -p $(COMMANDSDIR)
	install -m 555 $(ALLCOMMANDS) $(COMMANDSDIR)
	mkdir -p $(INTERNALSDIR)
	install -m 555 $(ALLINTERNALS) $(INTERNALSDIR)
	mkdir -p $(BASHCOMPDIR)
	install -m 644 -T $(RAWBASHCOMPLETION) $(BASHCOMPDIR)/pscheduler


clean:
	rm -rf $(TO_CLEAN) *~
