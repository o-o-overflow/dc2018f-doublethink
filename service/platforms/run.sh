#!/bin/bash -e

PLATFORM=$1
PLATDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/$PLATFORM >/dev/null && pwd )"
shift

if [ -z "$FLAG" ]
then
	FLAG=$1
	shift
fi

if [ -z "$SHELLCODE" ]
then
	SHELLCODE=$(cat $1 | base64)
fi

TMPDIR=$(mktemp -d)
trap "echo Cleaning up...; rm -rf $TMPDIR" EXIT
cd $TMPDIR
echo "$FLAG" > flag
echo -n "$SHELLCODE" | base64 -d > shellcode

echo "[*] Running $PLATFORM..."
env -i - PLATDIR=$PLATDIR script -q result -c "$PLATDIR/run ./flag ./shellcode"
echo "[*] $PLATFORM shellcode terminated. Checking results."
cat result | tr 'A-Z' 'a-z' > results.lower
if grep -q ${FLAG,,} results.lower
then
	echo "FLAG GOTTEN!"
	exit 0
else
	echo "NO FLAG!"
	exit 1
fi
