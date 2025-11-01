Prerequisites:
- install picamera2 using system package manager

Run once when setting up the virtual environment to get access to picamera2:
`uv venv --system-site-packages`

To run the server:
`uv run server.py`

To run the server in the background:
`nohup uv run server.py &`
