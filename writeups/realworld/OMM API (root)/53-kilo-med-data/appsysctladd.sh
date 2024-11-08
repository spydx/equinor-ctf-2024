#!/bin/bash
#
# Usage: sudo /prog/util/sbin/appsysctladd location1 ...
#
#   For each of the disk locations, this utility will look for services under `$HOSTNAME/*.service`
#   Matching `*.service` files will be added to `/etc/systemd/system`, started and enabled
#
#   The `*.service` files must contain *User=* and *Group=* corresponding to the owner and group of the `*.service` file,
#   i.e you are restricted to create and start services under users / groups only for yourself or function key users you can become
#
PROG=$( basename $0 )
DIR=$( dirname $0 )

SYSTEMD="/etc/systemd/system"


#
# Check if interactive use
#
CONFIGTOPDIRS=""
if tty >/dev/null 2>&1
then
    CONFIGTOPDIRS="$@"
else
    #
    # just so we log where this came from when done by jetpack
    #
    echo "$PROG: Initialized from $0 at `date` as user `id -a`"

    #
    # Elevate to root for non-interactive use
    #
    [ $( id -u ) -ne 0 ] && exec /usr/bin/sudo -n "$0" $* 2>&1

    #
    # Set up to use jetpack config if available ...
    #
    PATH="${PATH}:/opt/cycle/jetpack/bin"; export PATH
    JETPACK=$( type -p jetpack )
    JETPACK=${JETPACK:-"true"} # if jetpack is not available, use true as dummy command

    # 1 - lookup from jetpack if not in environment
    [ -z "${CONFIGTOPDIRS}" ] && JETPACKCONFIG=$( ${JETPACK} config host.config.directories | tr ',;' '  ' 2> /dev/null )

    # 2 - set if not in env and jetpack had the config
    [ -n "${JETPACKCONFIG}" ] && CONFIGTOPDIRS=$( ${JETPACK} config host.config.directories | tr ',;' '  ' 2> /dev/null )

    # 3 - fallback if all above fails
    [ -z "${CONFIGTOPDIRS}" ] && CONFIGTOPDIRS="/private/f_scout_ci/actions-runners /private/f_komodo/actions-runners /private/f_omm_app/systemctl"
fi

if [ -z "${CONFIGTOPDIRS}" ]
then
    sed -ne '2,/^PROG/ s/#/  /p' ${BASH_SOURCE} | tr -d '`' >&2
    exit 1
fi

echo "$PROG: Looking up systemctl services for ${HOST} under ${CONFIGTOPDIRS}"

for TOP in ${CONFIGTOPDIRS}
do
    for SRV in ${TOP}/${HOSTNAME%%.*}/*.service
    do
        if [ -f "${SRV}" ]
        then
            U=$( stat -c '%U' "${SRV}" )
            G=$( stat -c '%G' "${SRV}" )

            if egrep -q "^User=${U}$" "${SRV}" && egrep -q "^Group=${G}$" "${SRV}"
            then
                SRVNAME=$( basename "${SRV}" )
                echo "$PROG: Setting up systemd service from ${SRV}"
                install -g root -o root -m 644 "${SRV}" "${SYSTEMD}/${SRVNAME}" && \
                systemctl daemon-reload && \
                systemctl start "${SRVNAME}" && \
                systemctl enable "${SRVNAME}"
            else
                echo "$PROG: ${SRV} was rejected. User and Group must match file user and group"
            fi
        fi
    done
done

#
# exit 0 - or CycleCloud will retry
#
exit 0
