#!/bin/bash
# Serve the lab shell for the terminal slides (<Term />) on http://127.0.0.1:7681.
# Loopback only: this is a writable shell, never expose it on the network.
cd "$(dirname "$0")"
exec ttyd -W -i 127.0.0.1 -p "${TERM_PORT:-7681}" \
  -t fontSize=19 -t rendererType=dom -t disableLeaveAlert=true -t 'theme={"background":"#1c1c1c"}' \
  bash --rcfile ../lab/demo.rc -i
