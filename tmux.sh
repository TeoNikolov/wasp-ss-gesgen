#!/bin/sh

SESSION_NAME="wasp"

CONTAINER_WEB="wasp-ss-gesgen-web-1"
CONTAINER_VISUAL="wasp-ss-gesgen-visual-1"
CONTAINER_GESGEN="wasp-ss-gesgen-gesgen-1"
CONTAINER_REDIS="wasp-ss-gesgen-redis-1"

# Check if the session already exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Session $SESSION_NAME already exists. Attaching to it."
    tmux attach-session -t $SESSION_NAME
else
    # Create a new session and name it
    tmux new-session -d -s $SESSION_NAME

    # Setup panes
    tmux split-window -t 0 -v
    tmux split-window -t 0 -h
    tmux split-window -t 2 -h

    # Show logs in panes
    tmux send-keys -t 0 "docker logs -f $CONTAINER_WEB" C-m
    tmux send-keys -t 1 "docker logs -f $CONTAINER_GESGEN" C-m
    tmux send-keys -t 2 "docker logs -f $CONTAINER_REDIS" C-m
    tmux send-keys -t 3 "docker logs -f $CONTAINER_VISUAL" C-m

    # Attach to the created session
    tmux attach-session -t $SESSION_NAME
fi
