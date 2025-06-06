#
# Makefile for pScheduler extras bundle
#

# This makefile auto-generates RPM spec and Debian control files based
# on the build list and then uses Makefile-package to build it the
# usual way.

# TODO: This bundle doesn't fix the need to have select
# repos-preinstalled into YUM.  Should maybe write a package that does
# that.

BUNDLE=none
NAME=pscheduler-bundle-minimal

PACKAGE_MAKEFILE=Makefile-package

# Name of the package that marks the end of a minimal install.  Note
# that this package will not be included in the bundle.
STOP_AT_PACKAGE=pscheduler-minimal-marker

default: build


UNIBUILD_ORDER := unibuild order \
	--file ../unibuild-order \
	--buildable \
	| sed -e '/$(STOP_AT_PACKAGE)/,//d'

SPEC=./unibuild-packaging/rpm/$(NAME).spec
$(SPEC):
	cat $(SPEC)-top > $@
	$(UNIBUILD_ORDER) \
		| egrep -e '^pscheduler-' \
		| egrep -ve '^pscheduler-bundle-' \
		| sed -e 's/^/Requires: /g' \
		>> $@
	cat $(SPEC)-bottom >> $@
TO_BUILD += $(SPEC)

CONTROL=./unibuild-packaging/deb/control
$(CONTROL):
	cat $(CONTROL)-top > $@
	$(UNIBUILD_ORDER) \
		| egrep -e '^pscheduler-' \
		| egrep -ve '^pscheduler-bundle-' \
		| sed -e 's/^/ /g; $$ ! s/$$/,/g' \
		>> $@
	cat $(CONTROL)-bottom >> $@
TO_BUILD += $(CONTROL)


# These add compatibility with the generic package makefile template's
# targets.

TO_CLEAN += $(TO_BUILD)

clean c:
	$(MAKE) $(TO_BUILD)
	$(MAKE) -f $(PACKAGE_MAKEFILE) $@
	rm -rf $(TO_CLEAN) *~

build b install i rpmdump d r cb cbd cbr cbi srpm:
	$(MAKE) $(TO_BUILD)
	$(MAKE) -f $(PACKAGE_MAKEFILE) $@

cbic cbdc cbrc:
	$(MAKE) $(TO_BUILD)
	$(MAKE) -f $(PACKAGE_MAKEFILE) $@
	$(MAKE) clean


# This is to keep the global uninstall target happy.
uninstall:
	@echo Nothing to do here.

# Unibuild triggers this.
install-products:
	$(MAKE) -f $(PACKAGE_MAKEFILE) $@
