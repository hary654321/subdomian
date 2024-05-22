#!/bin/bash

/usr/local/domain2brute/shutdown.sh
/usr/local/domain2brute/monitor.sh >/dev/null 2>&1 &

echo "monitor.sh restart successed."

exit 0
