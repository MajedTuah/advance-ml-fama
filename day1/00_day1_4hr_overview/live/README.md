# Day 1 live session

This runs the Day 1 deck from your laptop on the venue Wi-Fi.

- **Participants:** each one opens the deck on their own device. Their screen follows your slides. Activities and games run on their device.
- **You:** the Control Center shows who is connected, the poll results, % correct per activity, the game leaderboard, and the ideas posted to the Open Channel boards.

## Run it
```bash
cd /Users/majed/Repos/advance-ml-fama
./day1/00_day1_4hr_overview/live/run.sh
```
`run.sh` uses the repo's `.venv`. Homebrew Python refuses a global `pip install` (the "externally-managed-environment" error), so the script creates `.venv` if it's missing, installs `requirements.txt` into it, and starts the server.

The terminal prints two links:

| Who | URL | Notes |
|---|---|---|
| Participants | `http://<your-LAN-IP>:8000` | Also shown as a QR code on slide 1 |
| Trainer | `http://<your-LAN-IP>:8000/?host=<token>` | Open this on the projector laptop and keep it private |

The token is saved in `live/.host_token`, so the trainer link stays the same across restarts and you can bookmark it. Delete that file to get a new token.

## While presenting
| Key | Action |
|---|---|
| → ← | Move the whole room |
| C | Control Center |
| N | Speaker notes |
| F | Fullscreen |

**Starting a fresh class:** use Reset session in the Control Center, or stop the server and delete `live_state.json`.

## Settings (environment variables)
- `PORT=8080 ./run.sh`: use a different port.
- `LIVE_HOST_TOKEN=mysecret ./run.sh`: choose your own trainer password.
- `LIVE_JOIN_URL=http://10.0.0.5:8000 ./run.sh`: override the detected address if the QR code shows the wrong IP, for example when you are on VPN.

## Troubleshooting
- **"Port 8000 is already in use."** Usually an old `python3 -m http.server 8000` is still running. Press Ctrl+C in that terminal, or run `lsof -nP -iTCP:8000 -sTCP:LISTEN` and `kill <PID>`. Or start on another port: `PORT=8080 ./run.sh`.
- **macOS asks "Allow incoming connections?"** Click **Allow**. Otherwise phones can't reach your laptop.
- **Participants can't load the page.** Some venue or guest Wi-Fi networks stop devices from reaching each other (client isolation). Turn on your phone's hotspot, connect the laptop and the participants to it, then restart the server so it picks up the new IP.
- **The server crashed or the laptop slept.** Run `./run.sh` again. The state comes back from `live_state.json`, and every browser reconnects on its own.
