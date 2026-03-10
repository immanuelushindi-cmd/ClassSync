# ClassSync 🎓

> **Real-time classroom doubt management. Students ask anonymously. Votes surface what matters. Teachers see the truth.**

---

## The Problem

Every classroom has students who are lost but too embarrassed to raise their hand. Teachers keep teaching, assuming everyone understands. The confusion never gets addressed — and students fall behind in silence.

## The Solution

ClassSync gives every student a voice — anonymously. Teachers create a live session and get a shareable PIN. Students join from any device with no account and no installation. They ask questions freely, classmates upvote the ones they share, and the teacher's dashboard automatically surfaces the most urgent confusion in real time — during the lecture, when it can still be fixed.

---

## Features

- 🔴 **Live doubt queue** — updates every 3 seconds, sorted by votes automatically
- 👆 **Anonymous upvoting** — students vote on shared doubts without revealing identity
- 👩‍🏫 **Teacher dashboard** — confusion score, open doubts, answered count, students online
- 📊 **Session analytics** — confusion heatmap by topic tag, top doubts leaderboard
- 📱 **QR code join** — students scan and land directly in the classroom, no PIN typing needed
- ✅ **Mark as answered** — resolved doubts disappear from everyone's screen instantly
- 🟢 **Students Online counter** — live presence tracking, updates every 30 seconds
- 📜 **Session history** — browse all past and live sessions with analytics
- 🔒 **100% anonymous** — no accounts, no names, no login required for students

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 (Python) |
| Database | SQLite |
| Frontend | Bootstrap 5.3, Vanilla JavaScript |
| Icons | Bootstrap Icons |
| Charts | Chart.js |
| QR Codes | qrcode + Pillow |
| Fonts | Syne, DM Sans (Google Fonts) |

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- The virtual environment is already included in the `class_` folder

### Installation & Setup

**1. Clone or download the project**
```bash
cd ClassSync
```

**2. Install dependencies**
```powershell
.\class_\Scripts\pip.exe install -r requirements.txt
```

**3. Apply database migrations**
```powershell
.\class_\Scripts\python.exe manage.py migrate
```

**4. (Optional) Seed demo data for presentations**
```powershell
.\class_\Scripts\python.exe manage.py seed_demo
```

**5. Start the server**

For personal use only (localhost):
```powershell
.\class_\Scripts\python.exe manage.py runserver
```

For students to connect via QR code or WiFi:
```powershell
.\class_\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

**6. Open your browser**
```
http://127.0.0.1:8000
```

---

## How to Use

### As a Teacher
1. Click **"I'm a Teacher"** on the home page
2. Fill in your session title, subject, and name
3. Click **"Launch Session"** — you'll land on your live dashboard
4. Share the **4-digit PIN** or show the **QR code** on the projector
5. Watch doubts appear and rise by votes in real time
6. Click **"Done"** on any doubt once you've addressed it
7. Click **"End Session"** when class is over to view analytics

### As a Student
1. Go to `/join` or scan the teacher's QR code
2. Enter the 4-digit PIN (or skip it if you scanned the QR)
3. Type your doubt anonymously and click **"Submit Anonymously"**
4. Upvote other students' doubts that you also have
5. Watch the teacher address the most popular questions live

---

## Connecting Students via QR Code

For students to scan the QR code and connect from their phones:

1. Make sure your laptop and students' devices are on the **same WiFi network**
2. Run the server with `0.0.0.0:8000` (see above)
3. Open the teacher dashboard and click **"QR Code"**
4. Students scan it — they land directly in the student room

> **Hotspot tip:** For a guaranteed connection at any venue, turn on your phone's hotspot, connect your laptop to it, and tell students to connect their phones to the same hotspot.

---

## Project Structure

```
ClassSync/
├── manage.py                          # Django control panel
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
├── class_/                            # Virtual environment
├── classsync_project/
│   ├── settings.py                    # App configuration
│   └── urls.py                        # Root URL router
└── classsync/
    ├── models.py                      # Database models
    ├── views.py                       # All business logic
    ├── urls.py                        # App URL patterns
    ├── admin.py                       # Django admin config
    ├── migrations/                    # Database migrations
    ├── static/classsync/
    │   └── style.css                  # Custom static styles
    ├── templates/classsync/
    │   ├── base.html                  # Base layout + all CSS
    │   ├── home.html                  # Landing page
    │   ├── create_session.html        # Teacher session creation
    │   ├── teacher_dashboard.html     # Live teacher view
    │   ├── student_room.html          # Student doubt room
    │   ├── join.html                  # Student PIN entry
    │   ├── analytics.html             # Post-session analytics
    │   └── history.html               # All sessions list
    └── management/commands/
        └── seed_demo.py               # Demo data seeder
```

---

## Database Models

**Session** — one per classroom session, holds the PIN and active status

**Doubt** — one per student question, tracks text, topic tag, vote count, and answered status

**Vote** — one per upvote, enforces one vote per student per doubt anonymously

**StudentPresence** — tracks online students via 30-second pings, powers the live counter

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/session/<pin>/api/` | GET | Live doubts, stats, online count |
| `/session/<pin>/submit/` | POST | Submit a new doubt |
| `/session/<pin>/ping/` | POST | Student presence heartbeat |
| `/session/<pin>/qr/` | GET | Generate QR code image |
| `/doubt/<id>/upvote/` | POST | Upvote a doubt |
| `/doubt/<id>/answer/` | POST | Mark doubt as answered |

---

## How Real-Time Works

ClassSync uses **HTTP polling** — no WebSockets required:

- The teacher dashboard calls `/api/` every **3 seconds** to refresh the doubt queue and stats
- The student room calls `/api/` every **4 seconds** to refresh the live feed
- Each student's browser pings `/ping/` every **30 seconds** to register their presence
- Students who haven't pinged in 90 seconds are considered offline

This approach is lightweight, reliable, and works on any network without special server configuration.

---

## Anonymity

Students never create an account. On first visit to the student room, Django assigns them a random UUID stored in their browser session cookie. This UUID is used only to prevent double voting — it is never linked to any personal information. The teacher sees only question text, never who asked it.

---

## Roadmap

- [ ] WebSocket support via Django Channels for instant updates
- [ ] Recurring doubt detection across multiple sessions
- [ ] Google Classroom / Moodle integration
- [ ] Teacher account system for session management
- [ ] Export analytics to PDF or CSV
- [ ] Mobile app (React Native)

---

## Built With ❤️ at a Hackathon

ClassSync was designed and built to solve a real problem in every classroom — giving every student the courage to ask, and every teacher the clarity to respond.

> *"The loudest voice in the room is rarely the most confused one."*
