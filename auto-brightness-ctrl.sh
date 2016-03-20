#!/bin/bash

function print_usage {
    echo "USAGE: $0 [-a |-u | -d]"
    echo -e "options:"
    echo -e "\t-a --auto\tToggle automatic brightness adjustment"
    echo -e "\t-u --up\tIncreas brightness in manual mode"
    echo -e "\t-d --down\tDecrease brightness in manual mode"
}

if [ $# -ne 1 ]
then
    print_usage
    exit -1
else
    case "$1" in
        -a|--auto)
            echo "Switching automatic brightness adjustment"
            dbus-send --type=method_call \
                      --dest=com.github.sheinz.autobrightness \
                      /com/github/sheinz/autobrightness \
                      com.github.sheinz.autobrightness.auto_toggle
        ;;
        -u|--up)
            echo "Turning screen brightness up"
            dbus-send --type=method_call \
                      --dest=com.github.sheinz.autobrightness \
                      /com/github/sheinz/autobrightness \
                      com.github.sheinz.autobrightness.up
        ;;
        -d|--down)
            echo "Turning screen brightness down"
            dbus-send --type=method_call \
                      --dest=com.github.sheinz.autobrightness \
                      /com/github/sheinz/autobrightness \
                      com.github.sheinz.autobrightness.down
        ;;
        *)
            print_usage
            exit -1
        ;;
    esac
fi
