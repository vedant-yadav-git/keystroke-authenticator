Project Roadmap: Keystroke Dynamics Authentication

Phase 1: Data Collection (Week 1)
Goal: Collect clean keystroke data from yourself
Tasks:

Build basic keylogger (keystroke_collector.py)

Use pynput to capture key press/release events
Record: key, press timestamp, release timestamp
Save to CSV with sessions labeled by date/time
Add start/stop functionality (don't log passwords!)


Data collection protocol

Collect 3-5 sessions of 10-15 minutes each
Different contexts: coding, writing prose, chatting
Same keyboard/environment for consistency
Aim for ~1000-2000 keypresses total



Deliverable: Raw keystroke data CSV with columns: session_id, key, press_time, release_time

Phase 2: Feature Engineering (Week 1-2)
Goal: Transform raw keystrokes into ML features
Start Simple - Extract These Features:

Dwell time: release_time - press_time for each key
Flight time: Time between consecutive key presses
Digraph timing: Time between specific key pairs (for common pairs only)

Per-session aggregates:

Mean, std, median, min, max of dwell times
Mean, std, median of flight times
Overall typing speed (keys per second)
Total number of backspaces (error rate)

Implementation:
python# Pseudocode structure
def extract_features(session_data):
    features = {
        'mean_dwell': ...,
        'std_dwell': ...,
        'mean_flight': ...,
        'std_flight': ...,
        'typing_speed': ...,
        'backspace_ratio': ...
    }
    return features
Deliverable: Feature extraction script + CSV with one row per session, ~10-15 features

Phase 3: Baseline Model (Week 2)
Goal: Build simplest working anomaly detector
Approach: One-Class SVM (sklearn)

Train on YOUR data only
Use default parameters first
Simple train/test split (80/20 of your sessions)

Evaluation (without impostor data yet):

Reconstruction accuracy on your own held-out data
Visualize feature distributions
Set initial threshold

Code structure:
pythonfrom sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Train
model = OneClassSVM(nu=0.1, kernel='rbf')
model.fit(X_scaled)

# Predict on test set (should be mostly 1s)
predictions = model.predict(X_test_scaled)
Deliverable: Trained model that scores your typing sessions, basic accuracy metrics

Phase 4: Impostor Data Collection (Week 2-3)
Goal: Get "attack" samples to properly evaluate
Minimal approach:

Ask 2-3 friends/family to type for 5-10 minutes each
Give them same prompts you used (copy a paragraph, write an email)
Label as impostor_1, impostor_2, etc.

Alternative if no volunteers:

Type intentionally differently yourself (one hand, hunt-and-peck, etc.)
Less realistic but still useful for testing

Deliverable: Impostor keystroke data, processed into same features

Phase 5: Evaluation & Tuning (Week 3)
Goal: Measure real security performance
Metrics to calculate:

False Accept Rate (FAR): % of impostor sessions accepted
False Reject Rate (FRR): % of your sessions rejected
Equal Error Rate (EER): Where FAR = FRR
ROC curve if you have confidence scores

Tuning:

Adjust threshold to balance FAR/FRR based on use case
Try different nu values in One-Class SVM
Feature selection: which features matter most?

Deliverable: Model with <10% FAR and <10% FRR (reasonable baseline)

Phase 6: Simple Demo (Week 3-4)
Goal: Make it usable/demonstrable
Option A - Offline Analysis:
Command-line tool that:

Loads trained model
Collects live typing for 2-3 minutes
Extracts features
Returns: "Legitimate user" or "Anomaly detected"

Option B - Real-time Monitoring (more impressive):
Background script that:

Monitors typing in real-time
Analyzes in sliding windows (e.g., last 50 keystrokes)
Prints alert if anomaly detected
Logs results to file

Start with Option A, it's much simpler.
Deliverable: Working demo script you can show someone

Minimal Viable Project (MVP) Checklist:

 Data collection script works reliably
 Collected 1000+ keystrokes from yourself
 Feature extraction produces consistent features
 One-Class SVM trains without errors
 Model achieves >80% accuracy on your own data
 Collected impostor data from 2+ sources
 FAR and FRR both under 15%
 Demo script runs and makes predictions
 Basic visualization of your typing patterns
 README with results and methodology


Future Scalability (After MVP):
Easy Extensions:

More sophisticated features (n-grams, rhythm patterns)
Try different models (Isolation Forest, Autoencoder)
Longer-term monitoring (track concept drift)
Multiple context models (coding vs writing)

Medium Extensions:

Mouse movement patterns
Browser extension for web forms
Mobile app for phone typing patterns
Dashboard with live monitoring

Advanced Extensions:

Deep learning with LSTMs for sequences
Multi-user system (family members)
Adaptive thresholds based on context
Integration with OS authentication


Recommended Weekly Breakdown:
Week 1:

Mon-Tue: Build collector, start collecting data
Wed-Thu: Feature engineering
Fri: Data exploration/visualization

Week 2:

Mon-Tue: Train baseline model
Wed-Thu: Collect impostor data
Fri: Initial evaluation

Week 3:

Mon-Tue: Tune model and improve metrics
Wed-Thu: Build demo
Fri: Polish and document

Week 4 (buffer):

Testing, bug fixes, improvements
Write-up of results


Tech Stack (Keep It Simple):
Required:

pynput - keystroke capture
pandas - data handling
numpy - numerical operations
scikit-learn - One-Class SVM
matplotlib - basic plotting

Optional (add later):

seaborn - prettier visualizations
pickle - save/load trained models
argparse - CLI interface for demo


Success Criteria for MVP:

✅ Can collect your typing data reliably
✅ Features are extracted correctly and make sense
✅ Model trains and makes predictions
✅ FAR < 20% (doesn't let impostors in often)
✅ FRR < 20% (doesn't lock you out often)
✅ Demo works end-to-end
✅ You understand why it works (or doesn't!)