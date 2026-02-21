from flask import Flask, render_template_string, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os, json

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    return client.open_by_key(sheet_id).sheet1

HEADERS = [
    "submitted_at",
    # Video 1
    "v1_q1","v1_q2","v1_q3","v1_q4","v1_q5","v1_q6",
    # Video 2
    "v2_q1","v2_q2","v2_q3","v2_q4","v2_q5","v2_q6",
    # Video 3
    "v3_q1","v3_q2","v3_q3","v3_q4","v3_q5","v3_q6",
    # Video 4
    "v4_q1","v4_q2","v4_q3","v4_q4","v4_q5","v4_q6",
    # Video 5
    "v5_q1","v5_q2","v5_q3","v5_q4","v5_q5","v5_q6",
    # Doc 1–5
    "d1_q1","d1_q2","d1_q3","d1_q4","d1_q5",
    "d2_q1","d2_q2","d2_q3","d2_q4","d2_q5",
    "d3_q1","d3_q2","d3_q3","d3_q4","d3_q5",
    "d4_q1","d4_q2","d4_q3","d4_q4","d4_q5",
    "d5_q1","d5_q2","d5_q3","d5_q4","d5_q5",
    # Overall
    "oa_q1","oa_q2","oa_q3","oa_q4","oa_q5","oa_q6","oa_q7",
]

def ensure_headers(sheet):
    first_row = sheet.row_values(1)
    if not first_row:
        sheet.append_row(HEADERS)

def save_response(form_data):
    sheet = get_sheet()
    ensure_headers(sheet)
    row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    for key in HEADERS[1:]:
        val = form_data.get(key, "")
        if isinstance(val, list):
            val = ", ".join(val)
        row.append(val)
    sheet.append_row(row)

# ── HTML Template ─────────────────────────────────────────────────────────────
FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Project Learning Resources – Feedback</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f7f7f8; color: #1a1a1a; line-height: 1.6; }
  .container { max-width: 780px; margin: 48px auto; padding: 0 20px 80px; }
  h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
  .subtitle { color: #555; font-size: 0.9rem; margin-bottom: 36px; }
  .section { margin-bottom: 40px; }
  .section-title { font-size: 1.05rem; font-weight: 700; color: #111; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; margin-bottom: 20px; }
  .q-block { margin-bottom: 22px; }
  label.q-label { display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 8px; color: #222; }
  .scale-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .scale-row input[type=radio] { display: none; }
  .scale-row label { padding: 6px 14px; border: 1px solid #ccc; border-radius: 6px; cursor: pointer; font-size: 0.85rem; background: #fff; transition: all .15s; }
  .scale-row input[type=radio]:checked + label { background: #111; color: #fff; border-color: #111; }
  select, textarea { width: 100%; padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; font-size: 0.875rem; background: #fff; color: #1a1a1a; margin-top: 2px; }
  select:focus, textarea:focus { outline: 2px solid #111; border-color: transparent; }
  textarea { resize: vertical; min-height: 72px; }
  .submit-btn { display: block; width: 100%; padding: 14px; background: #111; color: #fff; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; margin-top: 32px; transition: background .2s; }
  .submit-btn:hover { background: #333; }
  .flash { background: #e8f5e9; border: 1px solid #a5d6a7; color: #2e7d32; padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 0.9rem; }
  .error { background: #fdecea; border: 1px solid #f5c6c6; color: #b00020; padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 0.9rem; }
  .hint { font-size: 0.78rem; color: #888; margin-top: 4px; }
  hr.divider { border: none; border-top: 1px solid #e8e8e8; margin: 24px 0; }
</style>
</head>
<body>
<div class="container">
  <h1>Project Learning Resources — Feedback</h1>
  <p class="subtitle">Rating scale: 1 = Strongly Disagree / Not Helpful &nbsp;→&nbsp; 5 = Strongly Agree / Extremely Helpful</p>

  {% if submitted %}
  <div class="flash">✅ Thank you! Your feedback has been recorded.</div>
  {% elif error %}
  <div class="error">⚠️ Something went wrong saving your response. Please try again.</div>
  {% endif %}

  <form method="POST" action="/">

    <!-- ── SECTION A: Videos ── -->
    <div class="section">
      <div class="section-title">🎬 Section A — Video Resources</div>

      <!-- Video 1 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Video 1 — Introductory Video</p>

      {% for q_id, label in [
        ("v1_q1", "Before watching: how clear were you about what the project was trying to achieve?"),
        ("v1_q2", "After watching: how clearly did you understand the overall purpose and goals?"),
        ("v1_q4", "How well did the video motivate you to engage with the rest of the material?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}

      <div class="q-block">
        <label class="q-label">Did the video give you a realistic sense of what you would be building or learning?</label>
        <select name="v1_q3" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Was the pace of the introductory video appropriate?</label>
        <select name="v1_q5" required><option value="" disabled selected>Select…</option>
          <option>Too Fast</option><option>Just Right</option><option>Too Slow</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">What one thing, if added or changed, would have made this video more useful?</label>
        <textarea name="v1_q6" placeholder="Your answer…"></textarea>
      </div>

      <hr class="divider">

      <!-- Video 2 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Video 2 — Installation Video</p>
      <div class="q-block">
        <label class="q-label">Were you able to successfully complete the environment setup by following this video alone?</label>
        <select name="v2_q1" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Needed extra help</option><option>No</option></select>
      </div>
      {% for q_id, label in [
        ("v2_q2", "How clearly were each dependency and tool explained before being installed?"),
        ("v2_q4", "How confident did you feel about your setup being correct after watching?"),
        ("v2_q6", "Overall helpfulness of this video for getting started?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Did the video address setup for different operating systems sufficiently?</label>
        <select name="v2_q3" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Did you encounter installation errors the video didn't help resolve? Describe briefly.</label>
        <textarea name="v2_q5" placeholder="Leave blank if none…"></textarea>
      </div>

      <hr class="divider">

      <!-- Video 3 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Video 3 — Code Explanation Video</p>
      {% for q_id, label in [
        ("v3_q1", "How well did the video explain the overall structure and flow of the codebase?"),
        ("v3_q2", "Were key logic and algorithms explained clearly enough (why, not just what)?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Did the explanation help you understand how different parts of the code connect?</label>
        <select name="v3_q3" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Were there sections of code skipped or under-explained you wished had more coverage?</label>
        <textarea name="v3_q4" placeholder="Your answer…"></textarea>
      </div>
      <div class="q-block">
        <label class="q-label">After watching, could you confidently make small modifications to the code?</label>
        <select name="v3_q5" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Possibly</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">How would you rate the depth of code explanation for your skill level?</label>
        <select name="v3_q6" required><option value="" disabled selected>Select…</option>
          <option>Too Basic</option><option>Just Right</option><option>Too Advanced</option></select>
      </div>

      <hr class="divider">

      <!-- Video 4 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Video 4 — Execution & Output Video</p>
      {% for q_id, label in [
        ("v4_q1", "Did watching the execution video help you understand expected behavior and output?"),
        ("v4_q3", "How helpful was this video in verifying that your own execution was correct?"),
        ("v4_q5", "Was the output explanation clear enough to interpret results on your own afterwards?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      {% for q_id, label in [
        ("v4_q2", "Were all major outputs, edge cases, or output variations demonstrated clearly?"),
        ("v4_q4", "Did the video help you understand what a wrong output looks like?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <select name="{{ q_id }}" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">What additional output scenarios would you have liked to see demonstrated?</label>
        <textarea name="v4_q6" placeholder="Your answer…"></textarea>
      </div>

      <hr class="divider">

      <!-- Video 5 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Video 5 — Deployment Video (GitHub Pages & Streamlit)</p>
      {% for q_id, label in [
        ("v5_q1", "How clearly did the video explain the deployment process step by step?"),
        ("v5_q4", "How well did the video explain the difference between the two deployment methods?"),
        ("v5_q6", "How confident are you now in deploying similar projects on your own?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Were both deployment options explained with equal clarity?</label>
        <select name="v5_q2" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>GitHub Pages was clearer</option><option>Streamlit was clearer</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Were you able to successfully deploy the project after following this video?</label>
        <select name="v5_q3" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Did the video cover what to do if deployment fails or produces errors?</label>
        <select name="v5_q5" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
    </div>

    <!-- ── SECTION B: Documentation ── -->
    <div class="section">
      <div class="section-title">📄 Section B — Documentation Resources</div>

      <!-- Doc 1 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Doc 1 — Requirements Document</p>
      {% for q_id, label in [
        ("d1_q1", "How clearly did this document communicate what prior knowledge was expected?"),
        ("d1_q3", "Was the list of tools and versions specific enough to avoid confusion?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Did you meet the prerequisites, or were there gaps?</label>
        <select name="d1_q2" required><option value="" disabled selected>Select…</option>
          <option>Met all</option><option>Had minor gaps</option><option>Had significant gaps</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Did this document save you time compared to figuring out prerequisites on your own?</label>
        <select name="d1_q4" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Somewhat</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Was there any prerequisite or tool missing that you had to discover on your own?</label>
        <textarea name="d1_q5" placeholder="Leave blank if none…"></textarea>
      </div>

      <hr class="divider">

      <!-- Doc 2 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Doc 2 — Design Approach Document</p>
      {% for q_id, label in [
        ("d2_q1", "How well did this document explain WHY the project was designed as it was?"),
        ("d2_q3", "How useful were any diagrams or visual aids included?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        {% if q_id == "d2_q3" %}<p class="hint">Rate 1–5, or skip if no diagrams were included.</p>{% endif %}
      </div>
      {% endfor %}
      {% for q_id, label in [
        ("d2_q2", "Did the architecture explanation help you see the big picture before diving into code?"),
        ("d2_q4", "Did understanding the design approach make it easier to follow the code explanation video?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <select name="{{ q_id }}" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Somewhat</option><option>No</option></select>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Was there any design decision that felt unexplained or unclear?</label>
        <textarea name="d2_q5" placeholder="Your answer…"></textarea>
      </div>

      <hr class="divider">

      <!-- Doc 3 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Doc 3 — Implementation Steps</p>
      <div class="q-block">
        <label class="q-label">How well did this document align with what was shown in the videos?</label>
        <select name="d3_q1" required><option value="" disabled selected>Select…</option>
          <option>Fully aligned</option><option>Mostly aligned</option><option>Often mismatched</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Were the implementation steps detailed enough to follow without videos?</label>
        <select name="d3_q2" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Needed the videos too</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Was the order of steps logical and easy to follow progressively? (1–5)</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="d3_q3" id="d3_q3_{{ i }}" value="{{ i }}" required>
          <label for="d3_q3_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      <div class="q-block">
        <label class="q-label">Did this document help you replicate the project independently?</label>
        <select name="d3_q4" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Were there any steps that felt too vague or skipped over?</label>
        <textarea name="d3_q5" placeholder="Your answer…"></textarea>
      </div>

      <hr class="divider">

      <!-- Doc 4 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Doc 4 — Testing Procedures</p>
      {% for q_id, label in [
        ("d4_q1", "How clearly did the testing procedures explain what a successful outcome looks like?"),
        ("d4_q2", "Were the test cases specific enough to give genuine confidence your project works?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Did following the testing procedures help you catch bugs?</label>
        <select name="d4_q3" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>No</option><option>I didn't have bugs</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">Were the testing steps practical and easy to execute given your setup?</label>
        <select name="d4_q4" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">What additional tests or checkpoints would you have liked to see?</label>
        <textarea name="d4_q5" placeholder="Your answer…"></textarea>
      </div>

      <hr class="divider">

      <!-- Doc 5 -->
      <p style="font-weight:600;margin-bottom:14px;font-size:.9rem;">Doc 5 — Troubleshooting Tips</p>
      <div class="q-block">
        <label class="q-label">Did you encounter any issues that required you to consult the troubleshooting document?</label>
        <select name="d5_q1" required><option value="" disabled selected>Select…</option>
          <option>Yes</option><option>No</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">If yes — were you able to resolve your issue using the tips provided?</label>
        <select name="d5_q2"><option value="N/A" selected>N/A</option>
          <option>Fully resolved</option><option>Partially resolved</option><option>Not resolved</option></select>
      </div>
      {% for q_id, label in [
        ("d5_q3", "How comprehensive was the list of common issues covered?"),
        ("d5_q4", "Were the solutions explained clearly enough to act on without additional research?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }}</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}" required>
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">What issue did you face that was NOT covered in the troubleshooting guide?</label>
        <textarea name="d5_q5" placeholder="Leave blank if none…"></textarea>
      </div>
    </div>

    <!-- ── SECTION C: Overall ── -->
    <div class="section">
      <div class="section-title">📝 Section C — Overall Assessment</div>

      <div class="q-block">
        <label class="q-label">Which single resource did you find most valuable overall, and why?</label>
        <textarea name="oa_q1" placeholder="Your answer…" required></textarea>
      </div>
      <div class="q-block">
        <label class="q-label">Which resource was least helpful or most in need of improvement?</label>
        <textarea name="oa_q2" placeholder="Your answer…" required></textarea>
      </div>
      <div class="q-block">
        <label class="q-label">Overall quality of the project learning resources as a complete package? (1–5)</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="oa_q3" id="oa_q3_{{ i }}" value="{{ i }}" required>
          <label for="oa_q3_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      <div class="q-block">
        <label class="q-label">Did the videos and documentation feel complementary or disconnected?</label>
        <select name="oa_q4" required><option value="" disabled selected>Select…</option>
          <option>Complementary</option><option>Somewhat complementary</option>
          <option>Redundant</option><option>Disconnected</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">How confident are you in independently building and deploying a similar project from scratch? (1–5)</label>
        <div class="scale-row">
          {% for i in range(1,6) %}
          <input type="radio" name="oa_q5" id="oa_q5_{{ i }}" value="{{ i }}" required>
          <label for="oa_q5_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
      </div>
      <div class="q-block">
        <label class="q-label">Would you recommend these resources to a peer at the same skill level?</label>
        <select name="oa_q6" required><option value="" disabled selected>Select…</option>
          <option>Definitely</option><option>Probably</option>
          <option>Probably Not</option><option>Definitely Not</option></select>
      </div>
      <div class="q-block">
        <label class="q-label">What is the single most impactful change to improve this entire learning package?</label>
        <textarea name="oa_q7" placeholder="Your answer…" required></textarea>
      </div>
    </div>

    <button type="submit" class="submit-btn">Submit Feedback →</button>
  </form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    submitted = False
    error = False
    if request.method == "POST":
        try:
            save_response(dict(request.form))
            submitted = True
        except Exception as e:
            print(f"Error saving response: {e}")
            error = True
    return render_template_string(FORM_HTML, submitted=submitted, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)