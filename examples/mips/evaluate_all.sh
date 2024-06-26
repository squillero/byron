#!/usr/bin/env bash
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   -- v0.8a1 "Don Juan"             #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

# Compiles and runs a genome, kills it if it does not terminate swiftly
TIMEOUT_CMD=timeout
ALLOWED_TIME=3
re='^[0-9]+\n*+'

for file in "$@"; do
    mipsel-linux-gnu-gcc -static "$file" main.c -o onemax.out
    out="$($TIMEOUT_CMD $ALLOWED_TIME qemu-mipsel onemax.out 2>/dev/null)" || ( cp "$file" "problem-$file"; echo -1 )
    if [[ $out =~ $re ]] ; then
        echo $out
    fi
    grep -q 'nNone' "$file" && cp "$file" "nNone-$file"
done
rm onemax.out

exit 0
