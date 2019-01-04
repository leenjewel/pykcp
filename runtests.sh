#!/bin/sh
cd $(dirname $0)
python -m pykcp.test.kcp_test "$@"
