
<div align="center">
  <img src="assets/logo.png" alt="PresentIQ Logo" width="380" style="border-radius: 12px;"/>
  <h1>PresentIQ — AI-Powered Attendance System</h1>
  <p><strong>Automate classroom attendance using Face Recognition & Voice Recognition, powered by dlib and Resemblyzer.</strong></p>
</div>

PresentIQ is a full-stack AI attendance application built with **Streamlit**. Teachers can take attendance by uploading classroom photos (face recognition) or recording audio (voice recognition). Students self-register using a webcam and optionally enroll their voice — no passwords required.

---

## ✨ Features

### 👩‍🏫 Teacher Portal
- **Secure Login / Registration** — bcrypt-hashed password authentication
- **Subject Management** — Create subjects with code, name, and section
- **QR Code Subject Sharing** — Share a join link/QR code with students
- **Face-Based Attendance** — Upload one or more classroom photos; AI identifies enrolled students using dlib + SVM
- **Voice-Based Attendance** — Record classroom audio; AI segments speech and identifies students by voice (Resemblyzer)
- **Attendance Records** — Tabular view of all past sessions with present/total counts

### 🎓 Student Portal
- **Passwordless Login via FaceID** — Students simply look at the webcam; the trained classifier matches their face
- **Self Registration** — New students register with a webcam photo + optional voice sample, no admin action required
- **Subject Enrollment** — Enroll via QR/join code or manual entry
- **Attendance Dashboard** — Per-subject attendance stats (total classes attended vs total held)
- **Unenrollment** — Leave any subject at any time

---

## 🏗️ Architecture

```
app.py                          ← Streamlit entry point, session-state router
└── src/
    ├── screens/                ← Full-page views
    │   ├── home_screen.py      ← Role selector (Student / Teacher)
    │   ├── teacher_screen.py   ← Login, register, dashboard, 3 tabs
    │   └── student_screen.py   ← FaceID login, register, subject view
    │
    ├── components/             ← Reusable dialog & UI widgets
    │   ├── header.py           ← App header (home / dashboard variant)
    │   ├── footer.py           ← App footer
    │   ├── subject_card.py     ← Subject info card with stats
    │   ├── dialog_add_photo.py          ← Upload classroom photos
    │   ├── dialog_attendance_results.py ← Show face-scan results table
    │   ├── dialog_auto_enroll.py        ← Auto-enroll via URL join code
    │   ├── dialog_create_subject.py     ← Create a new subject
    │   ├── dialog_enroll.py             ← Manual student enrollment
    │   ├── dialog_share_subject.py      ← QR code sharing dialog
    │   └── dialog_voice_attendance.py   ← Voice attendance recording
    │
    ├── pipelines/              ← ML inference engines
    │   ├── face_pipeline.py    ← dlib detector → 128-d embedding → SVC
    │   └── voice_pipeline.py   ← Resemblyzer VoiceEncoder → cosine similarity
    │
    ├── database/
    │   ├── config.py           ← Supabase client (reads st.secrets)
    │   └── db.py               ← All Supabase table CRUD functions
    │
    └── ui/
        └── base_layout.py      ← CSS injection (fonts, colors, buttons)
```

---

## 🤖 ML Pipelines

### Face Recognition (`face_pipeline.py`)
| Step | Tool |
|---|---|
| Face Detection | `dlib` HOG frontal face detector |
| Landmark Prediction | `dlib` 68-point shape predictor |
| Embedding | `dlib` ResNet face recognition model (128-d vector) |
| Classification | `scikit-learn` SVC (linear kernel, probability=True, class_weight='balanced') |
| Threshold | Euclidean distance ≤ 0.6 |

- **Training** is triggered when a new student registers (`train_classifier()`), which clears Streamlit's `@st.cache_resource` and retrains the SVC on all embeddings from the database.
- **Prediction** iterates over all face encodings in a classroom photo and maps each to the closest enrolled student (if within threshold).

### Voice Recognition (`voice_pipeline.py`)
| Step | Tool |
|---|---|
| Embedding | `Resemblyzer` `VoiceEncoder` (GE2E-trained speaker encoder) |
| Preprocessing | `librosa` (resampled to 16 kHz) |
| Identification | Cosine similarity (dot product) |
| Threshold | Similarity ≥ 0.65 |
| Bulk Mode | Silence-split audio segments via `librosa.effects.split` (top_db=30), min 0.5 s per segment |

---

## 🗃️ Database Schema (Supabase / PostgreSQL)

| Table | Key Columns |
|---|---|
| `teachers` | `teacher_id`, `username`, `password` (bcrypt), `name` |
| `students` | `student_id`, `name`, `face_embedding` (float[128]), `voice_embedding` (float[]) |
| `subjects` | `subject_id`, `subject_code`, `name`, `section`, `teacher_id` → FK `teachers` |
| `subject_students` | `student_id` → FK `students`, `subject_id` → FK `subjects` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp` (ISO 8601), `is_present` (bool) |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com) project with the tables above
- C++ Build Tools (required by `dlib`)
  - Windows: [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Linux/Mac: `sudo apt install build-essential cmake` / `brew install cmake`

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd "AI-ML TS"
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **Note:** `face_recognition_models` is installed directly from GitHub and includes large binary model files (~100 MB). Installation may take several minutes depending on your network speed.

### 4. Configure Supabase credentials

Create `.streamlit/secrets.toml` in the project root:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-or-service-role-key"
```

> 🔒 **Never commit this file.** Add `.streamlit/secrets.toml` to your `.gitignore`.

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `dlib-bin` | Face detection & 128-d embedding |
| `face_recognition_models` | Pre-trained dlib model weights |
| `scikit-learn` | SVC classifier for face recognition |
| `resemblyzer` | Speaker encoder (GE2E) for voice recognition |
| `librosa` | Audio loading & silence-based segmentation |
| `supabase` | Supabase Python client (database & auth) |
| `bcrypt` | Password hashing for teacher accounts |
| `segno` | QR code generation for subject sharing |
| `Pillow` | Image loading and processing |
| `numpy` | Numerical arrays for embeddings |
| `pandas` | Attendance data tables |
| `setuptools<70.0.0` | Required for dlib build compatibility |

---

## 🔀 App Flow

```
Home Screen
├── Student Portal
│   ├── [Camera] → Face scan
│   │   ├── Recognized → Dashboard
│   │   │   ├── View enrolled subjects & attendance stats
│   │   │   ├── Enroll in subject (manual / QR join code)
│   │   │   └── Unenroll from subject
│   │   └── Not recognized → Registration form
│   │       ├── Enter name
│   │       ├── (Optional) Record voice sample
│   │       └── Create account → Dashboard
│   └── URL ?join-code=XYZ → Auto-enroll dialog
│
└── Teacher Portal
    ├── Login / Register (password-based)
    └── Dashboard
        ├── Tab: Take Attendance
        │   ├── Select subject
        │   ├── Add classroom photos
        │   ├── Run Face Analysis → Results dialog
        │   └── Use Voice Attendance → Record audio → Results
        ├── Tab: Manage Subjects
        │   ├── Create new subject
        │   └── Share subject (QR code dialog)
        └── Tab: Attendance Records
            └── Tabular history (grouped by session)
```

---

## 🚀 Deployment

### Streamlit Community Cloud
1. Push the project to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. In **App Settings → Secrets**, add your `SUPABASE_URL` and `SUPABASE_KEY`.
4. Deploy — Streamlit Cloud handles the Python environment and installs from `requirements.txt`.

> ⚠️ `dlib-bin` is a pre-built wheel and avoids needing C++ on the server. If using the regular `dlib` package on Linux, add a `packages.txt` file with `cmake` and `libopenblas-dev`.

---

## 🔑 Key Design Decisions

- **No student passwords** — Authentication is purely biometric (face). This lowers the barrier to entry for students.
- **Streamlit `@st.cache_resource`** — dlib models and the SVC classifier are cached globally to avoid reloading on every interaction.
- **Retraining on registration** — The face SVC is automatically retrained whenever a new student registers, keeping the model fresh without a manual step.
- **Supabase as BaaS** — All data (embeddings, logs, subjects) is stored in Supabase PostgreSQL, enabling real-time capabilities and easy scaling without self-hosting a database.
- **Cosine similarity for voice** — Dot product on unit-normalized Resemblyzer embeddings is equivalent to cosine similarity, providing a speaker-independent matching score.

---

## ⚠️ Known Limitations

- The face SVC degrades with very few students (< 2) — single-student mode falls back to that student automatically.
- Voice segmentation relies on silence detection (`top_db=30`); noisy classrooms may affect accuracy.
- The app retrains the face model synchronously on registration, which may be slow with many students.
- `st.secrets` is read at **module import time** in `config.py` — the app will crash on startup without a valid secrets file.

---

*Built with ❤️ using Streamlit, dlib, and Resemblyzer.*
