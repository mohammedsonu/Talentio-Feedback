from flask import Flask, render_template_string, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os, json

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    creds_dict = {
        "type": "service_account",
        "project_id": "nayansaathi",
        "private_key_id": "477944b6b308e87f6ca4d4b84f4dd5fd39b47910",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVhdnLuSjZ/xMo\nq+VT9jTAdhVfK+rmhgdZnu6rp/TflBRG+/yo+aW2U1jTNe8WTfjxqoAFAkd6NwW1\nJlRLooTnWPuYMe8PJ2yC31DlNZeW1tP4DxTyexa61kGQ34YRLzLSCl4a5Mj5BnTL\nvfot1scNQV7Thk5Jsu9kNLcNuewtdaFcaQ5XECbcV/pPtqNNEqVEYJB3uKtoxi2z\nQZGm7w+yrtzjrn21QO9qyRITBwnol9ahPmCBp2Vj6uUu+OFDH/mgAwd26un1Zb7Y\nKWLIr3EdDTLGSNsLY3rlulrmn1PSkkhRBFWey76R8Hmg3gvUI1u3AFAq88BONVqi\n+MIGrt8RAgMBAAECggEACC6+d3OrkJsZUVwxCCQtxlhgHksRD+9/9ZvFGrfvhufm\nVQgQGSukAZY1F7b/6BNp4Fz/1fFN6u2T3urOnS1nuXPsBFuZhTOmEWfcckQ5AHNQ\nITf2vgogh11xmssuGJd985WpII+28fAg5rPrk/kgnK3uI94IPwPH78ejYjfHSMCg\n1xvnjg3K3Exil/rnECPvzMxdzG2GkIqaDZz2RPSC41JSWNTJFRq9ybA30/MIv+uA\niF3dBCCvHm1nse9Y4BZ+DaXYRuWel1+dCAjxrIjM2gm3rT8XaO+yVba41cI8wmCy\n+2zm9JLnooZ3qeyQQZqAQStTNXwRHJgClbZtntiL5wKBgQDvrbxA6kAqyWY7DjXz\n3Ufx6GTowjE06AKqlWqWLSj4kbO2IXJRashgilVB+foqpbjUtF5OEV38ct3L9Obm\nnVcG7hPi94R9f2GKM+62edCVTolU3qobZbQrkPKs4tQG0t1Sv/nuqCBD3/8ZowwS\nswz0GudbGiNyR2K8hD4stpm2WwKBgQDkECWtEO/l2ADK/d8rycwIJFzWKOHTWvs1\nOCLu2Dw+l9zCPTORkhhyszHChiFxIRsz4oo0/oLfuyCODmNw/woEQ42aJwlPkHJa\nFgmsg59d/T5T8dY78wonYiCPB5vzsgojEOzNqV6NDMDJF/E/ZMtl3A0YQFYhaliW\ngOMeLan0AwKBgD0iBz5XgX5oWFb/zOsiqdMd/38O6RYhh2yTJ9ieNDESmM//v/Tc\nU7esEQr/A7wVAQvf5Z3r+BkIA2KeWLbBswzldNUTZQvNjcd+b4jDkVxD5+tpz+Gl\nE0t5cSx/vqzu49zTcqBY6cHmRF75o36xhMBOjGxEQn5Hjvuej21ANfy5AoGBAJhq\nrjNOqXVreYQwTLEACWq7movKALp3CIIVxUromsKeTXxG2KsF/27QkYXWjI0Fuh9f\n3Ev0eFS7w9MMjKrc173nw7/tLMzO1Y2dQtPXl2+CKuCBNFMWZ4fQjb/pLvGb4Ch1\nTD1aXwVXK5R5etKKM2Ecwmedv7JPV2smMiNeE0IvAoGAeQOn9wplQOcDr1/pXqyE\nCd7j/u6Q8Q7FQgRplXrbK0986EogkRD3RqgNndjBsm2nGF5TqgsoKeOn+sEBHc4r\nHBfTWtQCyhqE4HlQpN/MNUuJCTV/iSsBlXqklvRMzw7Lvhxa5cwxcNR9fa3D8hAc\n631fCRzPDS8xoLe65ejLL8g=\n-----END PRIVATE KEY-----\n",
        "client_email": "talentio-form-inputs@nayansaathi.iam.gserviceaccount.com",
        "client_id": "101033883099710036821",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/talentio-form-inputs%40nayansaathi.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key("14Jkz9EFGQ3nC5iGN7pCkqu4vZY10h2PYoyLZxJuO3H4").sheet1

HEADERS = [
    "submitted_at",
    # Student details
    "student_name", "student_email", "student_id", "batch_section",
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
    # Docs
    "d1_q1","d1_q2","d1_q3","d1_q4","d1_q5",
    "d2_q1","d2_q2","d2_q3","d2_q4","d2_q5",
    "d3_q1","d3_q2","d3_q3","d3_q4","d3_q5",
    "d4_q1","d4_q2","d4_q3","d4_q4","d4_q5",
    "d5_q1","d5_q2","d5_q3","d5_q4","d5_q5",
    # Overall
    "oa_q1","oa_q2","oa_q3","oa_q4","oa_q5","oa_q6","oa_q7",
]

def ensure_headers(sheet):
    if not sheet.row_values(1):
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
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .q-block { margin-bottom: 22px; }
  label.q-label { display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 8px; color: #222; }
  label.q-label .req { color: #c0392b; margin-left: 2px; }
  .scale-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .scale-row input[type=radio] { display: none; }
  .scale-row label { padding: 6px 14px; border: 1px solid #ccc; border-radius: 6px; cursor: pointer; font-size: 0.85rem; background: #fff; transition: all .15s; user-select: none; }
  .scale-row input[type=radio]:checked + label { background: #111; color: #fff; border-color: #111; }
  .scale-row.invalid label { border-color: #e74c3c; }
  input[type=text], input[type=email], select, textarea {
    width: 100%; padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px;
    font-size: 0.875rem; background: #fff; color: #1a1a1a; margin-top: 2px;
    font-family: inherit;
  }
  input[type=text]:focus, input[type=email]:focus, select:focus, textarea:focus {
    outline: 2px solid #111; border-color: transparent;
  }
  input.invalid, select.invalid, textarea.invalid { border-color: #e74c3c !important; }
  textarea { resize: vertical; min-height: 72px; }
  .submit-btn {
    display: block; width: 100%; padding: 14px; background: #111; color: #fff;
    border: none; border-radius: 8px; font-size: 1rem; font-weight: 600;
    cursor: pointer; margin-top: 32px; transition: background .2s;
  }
  .submit-btn:hover { background: #333; }
  .submit-btn:disabled { background: #999; cursor: not-allowed; }
  .flash { background: #e8f5e9; border: 1px solid #a5d6a7; color: #2e7d32; padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 0.9rem; }
  .error-banner { background: #fdecea; border: 1px solid #f5c6c6; color: #b00020; padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 0.9rem; }
  .val-msg { color: #e74c3c; font-size: 0.78rem; margin-top: 4px; display: none; }
  hr.divider { border: none; border-top: 1px solid #e8e8e8; margin: 24px 0; }
  .subsection-title { font-weight: 600; margin-bottom: 14px; font-size: .9rem; }
</style>
</head>
<body>
<div class="container">
  <h1>Project Learning Resources — Feedback</h1>
  <p class="subtitle">All fields marked <span style="color:#c0392b">*</span> are required. &nbsp;Rating scale: 1 = Not helpful at all &nbsp;→&nbsp; 5 = Extremely helpful</p>

  {% if submitted %}
  <div class="flash">✅ Thank you, {{ name }}! Your feedback has been recorded.</div>
  {% elif error %}
  <div class="error-banner">⚠️ Something went wrong saving your response. Please try submitting again.</div>
  {% endif %}

  {% if not submitted %}
  <form id="feedbackForm" method="POST" action="/" novalidate>

    <!-- ── Student Details ── -->
    <div class="section">
      <div class="section-title">👤 Your Details</div>
      <div class="two-col">
        <div class="q-block">
          <label class="q-label" for="student_name">Full Name <span class="req">*</span></label>
          <input type="text" id="student_name" name="student_name" placeholder="e.g. Aisha Sharma" required>
          <div class="val-msg" id="err_student_name">Please enter your name.</div>
        </div>
        <div class="q-block">
          <label class="q-label" for="student_email">Email Address <span class="req">*</span></label>
          <input type="email" id="student_email" name="student_email" placeholder="e.g. aisha@example.com" required>
          <div class="val-msg" id="err_student_email">Please enter a valid email.</div>
        </div>
        <div class="q-block">
          <label class="q-label" for="student_id">Student / Roll Number <span class="req">*</span></label>
          <input type="text" id="student_id" name="student_id" placeholder="e.g. 22BCS045" required>
          <div class="val-msg" id="err_student_id">Please enter your student ID.</div>
        </div>
        <div class="q-block">
          <label class="q-label" for="batch_section">Batch / Section <span class="req">*</span></label>
          <input type="text" id="batch_section" name="batch_section" placeholder="e.g. Batch B / Section 3" required>
          <div class="val-msg" id="err_batch_section">Please enter your batch/section.</div>
        </div>
      </div>
    </div>

    <!-- ── SECTION A: Videos ── -->
    <div class="section">
      <div class="section-title">🎬 Section A — Video Resources</div>

      <!-- Video 1 -->
      <p class="subsection-title">Video 1 — Introductory Video</p>

      {% for q_id, label in [
        ("v1_q1", "Before watching: how clear were you about what the project was trying to achieve?"),
        ("v1_q2", "After watching: how clearly did you understand the overall purpose and goals?"),
        ("v1_q4", "How well did the video motivate you to engage with the rest of the material?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}

      {% for q_id, label, opts in [
        ("v1_q3", "Did the video give you a realistic sense of what you would be building or learning?", ["Yes","Partially","No"]),
        ("v1_q5", "Was the pace of the introductory video appropriate?", ["Too Fast","Just Right","Too Slow"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">What one thing, if added or changed, would have made this video more useful? <span class="req">*</span></label>
        <textarea name="v1_q6" id="v1_q6" placeholder="Your answer…" required></textarea>
        <div class="val-msg" id="err_v1_q6">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Video 2 -->
      <p class="subsection-title">Video 2 — Installation Video</p>
      <div class="q-block">
        <label class="q-label">Were you able to successfully complete the environment setup by following this video alone? <span class="req">*</span></label>
        <select name="v2_q1" id="v2_q1" required>
          <option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Needed extra help</option><option>No</option>
        </select>
        <div class="val-msg" id="err_v2_q1">Please select an option.</div>
      </div>
      {% for q_id, label in [
        ("v2_q2", "How clearly were each dependency and tool explained before being installed?"),
        ("v2_q4", "How confident did you feel about your setup being correct after watching?"),
        ("v2_q6", "Overall helpfulness of this video for getting started?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Did the video address setup for different operating systems sufficiently? <span class="req">*</span></label>
        <select name="v2_q3" id="v2_q3" required>
          <option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option>
        </select>
        <div class="val-msg" id="err_v2_q3">Please select an option.</div>
      </div>
      <div class="q-block">
        <label class="q-label">Did you encounter installation errors the video didn't help resolve? Describe briefly. <span class="req">*</span></label>
        <textarea name="v2_q5" id="v2_q5" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_v2_q5">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Video 3 -->
      <p class="subsection-title">Video 3 — Code Explanation Video</p>
      {% for q_id, label in [
        ("v3_q1", "How well did the video explain the overall structure and flow of the codebase?"),
        ("v3_q2", "Were key logic and algorithms explained clearly enough (why, not just what)?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      {% for q_id, label, opts in [
        ("v3_q3", "Did the explanation help you understand how different parts of the code connect?", ["Yes","Partially","No"]),
        ("v3_q5", "After watching, could you confidently make small modifications to the code?", ["Yes","Possibly","No"]),
        ("v3_q6", "How would you rate the depth of code explanation for your skill level?", ["Too Basic","Just Right","Too Advanced"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Were there sections of code skipped or under-explained you wished had more coverage? <span class="req">*</span></label>
        <textarea name="v3_q4" id="v3_q4" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_v3_q4">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Video 4 -->
      <p class="subsection-title">Video 4 — Execution & Output Video</p>
      {% for q_id, label in [
        ("v4_q1", "Did watching the execution video help you understand expected behavior and output?"),
        ("v4_q3", "How helpful was this video in verifying that your own execution was correct?"),
        ("v4_q5", "Was the output explanation clear enough to interpret results on your own afterwards?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      {% for q_id, label in [
        ("v4_q2", "Were all major outputs, edge cases, or output variations demonstrated clearly?"),
        ("v4_q4", "Did the video help you understand what a wrong output looks like?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          <option>Yes</option><option>Partially</option><option>No</option>
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">What additional output scenarios would you have liked to see demonstrated? <span class="req">*</span></label>
        <textarea name="v4_q6" id="v4_q6" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_v4_q6">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Video 5 -->
      <p class="subsection-title">Video 5 — Deployment Video (GitHub Pages & Streamlit)</p>
      {% for q_id, label in [
        ("v5_q1", "How clearly did the video explain the deployment process step by step?"),
        ("v5_q4", "How well did the video explain the difference between the two deployment methods?"),
        ("v5_q6", "How confident are you now in deploying similar projects on your own?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      {% for q_id, label, opts in [
        ("v5_q2", "Were both deployment options explained with equal clarity?", ["Yes","GitHub Pages was clearer","Streamlit was clearer"]),
        ("v5_q3", "Were you able to successfully deploy the project after following this video?", ["Yes","Partially","No"]),
        ("v5_q5", "Did the video cover what to do if deployment fails or produces errors?", ["Yes","Partially","No"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
    </div>

    <!-- ── SECTION B: Documentation ── -->
    <div class="section">
      <div class="section-title">📄 Section B — Documentation Resources</div>

      <!-- Doc 1 -->
      <p class="subsection-title">Doc 1 — Requirements Document</p>
      {% for q_id, label in [
        ("d1_q1", "How clearly did this document communicate what prior knowledge was expected?"),
        ("d1_q3", "Was the list of tools and versions specific enough to avoid confusion?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      {% for q_id, label, opts in [
        ("d1_q2", "Did you meet the prerequisites, or were there gaps?", ["Met all","Had minor gaps","Had significant gaps"]),
        ("d1_q4", "Did this document save you time compared to figuring out prerequisites on your own?", ["Yes","Somewhat","No"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Was there any prerequisite or tool missing that you had to discover on your own? <span class="req">*</span></label>
        <textarea name="d1_q5" id="d1_q5" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_d1_q5">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Doc 2 -->
      <p class="subsection-title">Doc 2 — Design Approach Document</p>
      {% for q_id, label in [
        ("d2_q1", "How well did this document explain WHY the project was designed as it was?"),
        ("d2_q3", "How useful were any diagrams or visual aids included? (rate 1 if none)")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      {% for q_id, label, opts in [
        ("d2_q2", "Did the architecture explanation help you see the big picture before diving into code?", ["Yes","Somewhat","No"]),
        ("d2_q4", "Did understanding the design approach make it easier to follow the code explanation video?", ["Yes","Somewhat","No"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Was there any design decision that felt unexplained or unclear? <span class="req">*</span></label>
        <textarea name="d2_q5" id="d2_q5" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_d2_q5">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Doc 3 -->
      <p class="subsection-title">Doc 3 — Implementation Steps</p>
      {% for q_id, label, opts in [
        ("d3_q1", "How well did this document align with what was shown in the videos?", ["Fully aligned","Mostly aligned","Often mismatched"]),
        ("d3_q2", "Were the implementation steps detailed enough to follow without videos?", ["Yes","Needed the videos too","No"]),
        ("d3_q4", "Did this document help you replicate the project independently?", ["Yes","Partially","No"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">Was the order of steps logical and easy to follow progressively? <span class="req">*</span></label>
        <div class="scale-row" id="row_d3_q3">
          {% for i in range(1,6) %}
          <input type="radio" name="d3_q3" id="d3_q3_{{ i }}" value="{{ i }}">
          <label for="d3_q3_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_d3_q3">Please select a rating.</div>
      </div>
      <div class="q-block">
        <label class="q-label">Were there any steps that felt too vague or skipped over? <span class="req">*</span></label>
        <textarea name="d3_q5" id="d3_q5" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_d3_q5">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Doc 4 -->
      <p class="subsection-title">Doc 4 — Testing Procedures</p>
      {% for q_id, label in [
        ("d4_q1", "How clearly did the testing procedures explain what a successful outcome looks like?"),
        ("d4_q2", "Were the test cases specific enough to give genuine confidence your project works?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      {% for q_id, label, opts in [
        ("d4_q3", "Did following the testing procedures help you catch bugs?", ["Yes","No","I didn't have bugs"]),
        ("d4_q4", "Were the testing steps practical and easy to execute given your setup?", ["Yes","Partially","No"])
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <select name="{{ q_id }}" id="{{ q_id }}" required>
          <option value="" disabled selected>Select…</option>
          {% for o in opts %}<option>{{ o }}</option>{% endfor %}
        </select>
        <div class="val-msg" id="err_{{ q_id }}">Please select an option.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">What additional tests or checkpoints would you have liked to see? <span class="req">*</span></label>
        <textarea name="d4_q5" id="d4_q5" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_d4_q5">Please fill in this field.</div>
      </div>

      <hr class="divider">

      <!-- Doc 5 -->
      <p class="subsection-title">Doc 5 — Troubleshooting Tips</p>
      <div class="q-block">
        <label class="q-label">Did you encounter any issues that required you to consult the troubleshooting document? <span class="req">*</span></label>
        <select name="d5_q1" id="d5_q1" required>
          <option value="" disabled selected>Select…</option>
          <option>Yes</option><option>No</option>
        </select>
        <div class="val-msg" id="err_d5_q1">Please select an option.</div>
      </div>
      <div class="q-block">
        <label class="q-label">If yes — were you able to resolve your issue using the tips provided?</label>
        <select name="d5_q2" id="d5_q2">
          <option value="N/A" selected>N/A — I didn't consult it</option>
          <option>Fully resolved</option><option>Partially resolved</option><option>Not resolved</option>
        </select>
      </div>
      {% for q_id, label in [
        ("d5_q3", "How comprehensive was the list of common issues covered?"),
        ("d5_q4", "Were the solutions explained clearly enough to act on without additional research?")
      ] %}
      <div class="q-block">
        <label class="q-label">{{ label }} <span class="req">*</span></label>
        <div class="scale-row" id="row_{{ q_id }}">
          {% for i in range(1,6) %}
          <input type="radio" name="{{ q_id }}" id="{{ q_id }}_{{ i }}" value="{{ i }}">
          <label for="{{ q_id }}_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_{{ q_id }}">Please select a rating.</div>
      </div>
      {% endfor %}
      <div class="q-block">
        <label class="q-label">What issue did you face that was NOT covered in the troubleshooting guide? <span class="req">*</span></label>
        <textarea name="d5_q5" id="d5_q5" placeholder="Write 'None' if not applicable." required></textarea>
        <div class="val-msg" id="err_d5_q5">Please fill in this field.</div>
      </div>
    </div>

    <!-- ── SECTION C: Overall ── -->
    <div class="section">
      <div class="section-title">📝 Section C — Overall Assessment</div>

      <div class="q-block">
        <label class="q-label">Which single resource did you find most valuable overall, and why? <span class="req">*</span></label>
        <textarea name="oa_q1" id="oa_q1" placeholder="Your answer…" required></textarea>
        <div class="val-msg" id="err_oa_q1">Please fill in this field.</div>
      </div>
      <div class="q-block">
        <label class="q-label">Which resource was least helpful or most in need of improvement? <span class="req">*</span></label>
        <textarea name="oa_q2" id="oa_q2" placeholder="Your answer…" required></textarea>
        <div class="val-msg" id="err_oa_q2">Please fill in this field.</div>
      </div>
      <div class="q-block">
        <label class="q-label">Overall quality of the project learning resources as a complete package? <span class="req">*</span></label>
        <div class="scale-row" id="row_oa_q3">
          {% for i in range(1,6) %}
          <input type="radio" name="oa_q3" id="oa_q3_{{ i }}" value="{{ i }}">
          <label for="oa_q3_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_oa_q3">Please select a rating.</div>
      </div>
      <div class="q-block">
        <label class="q-label">Did the videos and documentation feel complementary or disconnected? <span class="req">*</span></label>
        <select name="oa_q4" id="oa_q4" required>
          <option value="" disabled selected>Select…</option>
          <option>Complementary</option><option>Somewhat complementary</option>
          <option>Redundant</option><option>Disconnected</option>
        </select>
        <div class="val-msg" id="err_oa_q4">Please select an option.</div>
      </div>
      <div class="q-block">
        <label class="q-label">How confident are you in independently building and deploying a similar project from scratch? <span class="req">*</span></label>
        <div class="scale-row" id="row_oa_q5">
          {% for i in range(1,6) %}
          <input type="radio" name="oa_q5" id="oa_q5_{{ i }}" value="{{ i }}">
          <label for="oa_q5_{{ i }}">{{ i }}</label>
          {% endfor %}
        </div>
        <div class="val-msg" id="err_oa_q5">Please select a rating.</div>
      </div>
      <div class="q-block">
        <label class="q-label">Would you recommend these resources to a peer at the same skill level? <span class="req">*</span></label>
        <select name="oa_q6" id="oa_q6" required>
          <option value="" disabled selected>Select…</option>
          <option>Definitely</option><option>Probably</option>
          <option>Probably Not</option><option>Definitely Not</option>
        </select>
        <div class="val-msg" id="err_oa_q6">Please select an option.</div>
      </div>
      <div class="q-block">
        <label class="q-label">What is the single most impactful change to improve this entire learning package? <span class="req">*</span></label>
        <textarea name="oa_q7" id="oa_q7" placeholder="Your answer…" required></textarea>
        <div class="val-msg" id="err_oa_q7">Please fill in this field.</div>
      </div>
    </div>

    <button type="submit" class="submit-btn" id="submitBtn">Submit Feedback →</button>
  </form>
  {% endif %}
</div>

<script>
// All radio groups that are required
const radioGroups = [
  "v1_q1","v1_q2","v1_q4",
  "v2_q2","v2_q4","v2_q6",
  "v3_q1","v3_q2",
  "v4_q1","v4_q3","v4_q5",
  "v5_q1","v5_q4","v5_q6",
  "d1_q1","d1_q3",
  "d2_q1","d2_q3",
  "d3_q3",
  "d4_q1","d4_q2",
  "d5_q3","d5_q4",
  "oa_q3","oa_q5"
];

document.getElementById("feedbackForm").addEventListener("submit", function(e) {
  e.preventDefault();
  let valid = true;

  // Validate text/email inputs
  const textFields = ["student_name","student_email","student_id","batch_section"];
  textFields.forEach(id => {
    const el = document.getElementById(id);
    const err = document.getElementById("err_" + id);
    if (!el.value.trim() || (id === "student_email" && !el.value.includes("@"))) {
      el.classList.add("invalid");
      err.style.display = "block";
      valid = false;
    } else {
      el.classList.remove("invalid");
      err.style.display = "none";
    }
  });

  // Validate selects
  this.querySelectorAll("select[required]").forEach(sel => {
    const err = document.getElementById("err_" + sel.name);
    if (!sel.value) {
      sel.classList.add("invalid");
      if (err) err.style.display = "block";
      valid = false;
    } else {
      sel.classList.remove("invalid");
      if (err) err.style.display = "none";
    }
  });

  // Validate textareas
  this.querySelectorAll("textarea[required]").forEach(ta => {
    const err = document.getElementById("err_" + ta.name);
    if (!ta.value.trim()) {
      ta.classList.add("invalid");
      if (err) err.style.display = "block";
      valid = false;
    } else {
      ta.classList.remove("invalid");
      if (err) err.style.display = "none";
    }
  });

  // Validate radio groups
  radioGroups.forEach(name => {
    const checked = document.querySelector(`input[name="${name}"]:checked`);
    const row = document.getElementById("row_" + name);
    const err = document.getElementById("err_" + name);
    if (!checked) {
      if (row) row.classList.add("invalid");
      if (err) err.style.display = "block";
      valid = false;
    } else {
      if (row) row.classList.remove("invalid");
      if (err) err.style.display = "none";
    }
  });

  if (!valid) {
    // Scroll to first error
    const first = document.querySelector(".invalid, .scale-row.invalid");
    if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  // All good — disable button and submit
  const btn = document.getElementById("submitBtn");
  btn.disabled = true;
  btn.textContent = "Submitting…";
  this.submit();
});
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    submitted = False
    error = False
    name = ""
    if request.method == "POST":
        try:
            save_response(dict(request.form))
            submitted = True
            name = request.form.get("student_name", "")
        except Exception as e:
            print(f"Error saving response: {e}")
            error = True
    return render_template_string(FORM_HTML, submitted=submitted, error=error, name=name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
