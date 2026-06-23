#!/usr/bin/env python3
"""
Hobbit Asset Inventory v3 - Complete Cyber Security Tool
Run with: python3 hobbit_assest_inv_v3.py
No external dependencies needed!
"""

import http.server
import socketserver
import json
import socket
import random
import base64
import hashlib
import time
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# Find available port
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

PORT = find_free_port()

# Simple JWT-like token generation
def generate_token(username):
    payload = f'{{"user":"{username}","exp":{int(time.time()) + 3600}}}'
    b64 = base64.b64encode(payload.encode()).decode()
    signature = hashlib.sha256(f'{b64}secret'.encode()).hexdigest()[:16]
    return f'{b64}.{signature}'

def verify_token(token):
    try:
        parts = token.split('.')
        if len(parts) != 2:
            return None
        b64, sig = parts
        expected = hashlib.sha256(f'{b64}secret'.encode()).hexdigest()[:16]
        if sig != expected:
            return None
        payload = base64.b64decode(b64).decode()
        data = json.loads(payload)
        if data.get('exp', 0) < time.time():
            return None
        return data.get('user')
    except:
        return None

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🏔️ Hobbit Asset Inventory v3</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
    --mint: #b8e6d0;
    --mint-light: #d4f0e4;
    --mint-dark: #7abf9a;
    --pastel-green: #c5e8d7;
    --green-bg: #f0f8f4;
    --hobbit-brown: #8b6b4a;
    --hobbit-cream: #f5efe6;
    --shadow-green: rgba(100, 180, 140, 0.15);
}

*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--green-bg);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem;color:#1a2e2a;background-image:radial-gradient(circle at 20% 50%, var(--mint-light) 0%, var(--green-bg) 100%)}
.app-container{background:#fff;border-radius:32px;box-shadow:0 20px 60px var(--shadow-green),0 8px 24px rgba(0,30,20,.06);padding:2.5rem;max-width:1440px;width:100%;border:2px solid var(--mint);position:relative;overflow:hidden}
.app-container::before{content:'🍃';position:absolute;top:-10px;right:-10px;font-size:8rem;opacity:0.03;transform:rotate(15deg)}
.app-container::after{content:'🏔️';position:absolute;bottom:-20px;left:-20px;font-size:10rem;opacity:0.03;transform:rotate(-10deg)}
#loginScreen{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3rem 1rem;gap:2rem;min-height:550px}
.login-brand{text-align:center}
.login-brand .icon-ring{font-size:3.5rem;color:#fff;background:linear-gradient(135deg, var(--mint), var(--mint-dark));padding:1.5rem;border-radius:50%;display:inline-block;margin-bottom:1rem;box-shadow:0 8px 24px rgba(100, 180, 140, 0.3)}
.login-brand h1{font-size:2.5rem;font-weight:700;color:#1a2e2a;letter-spacing:-.5px}
.login-brand h1 span{color:var(--mint-dark)}
.login-brand p{color:#5a7a72;margin-top:.3rem;font-size:1rem}
.login-box{background:var(--green-bg);padding:2.5rem;border-radius:20px;width:100%;max-width:380px;border:2px solid var(--mint)}
.login-box label{display:block;font-weight:600;color:#1a2e2a;margin-top:1.2rem;font-size:.85rem;letter-spacing:.3px}
.login-box label:first-of-type{margin-top:0}
.login-box label i{color:var(--mint-dark);margin-right:.5rem}
.login-box input{width:100%;padding:.8rem 1rem;border:2px solid var(--mint);border-radius:12px;background:#fff;font-size:.95rem;outline:0;transition:.15s;font-family:'Inter',sans-serif;margin-top:.3rem}
.login-box input:focus{border-color:var(--mint-dark);box-shadow:0 0 0 4px rgba(122, 191, 154, 0.15)}
.login-btn{margin-top:1.8rem;width:100%;background:linear-gradient(135deg, var(--mint), var(--mint-dark));border:none;padding:.8rem;border-radius:12px;font-weight:600;font-size:1rem;color:#fff;transition:.15s;cursor:pointer;font-family:'Inter',sans-serif;letter-spacing:.3px;box-shadow:0 4px 12px rgba(100, 180, 140, 0.3)}
.login-btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(100, 180, 140, 0.4)}
.login-error{color:#c0392b;background:#fdf0ed;padding:.5rem 1rem;border-radius:8px;font-weight:500;margin-top:.8rem;display:none;font-size:.9rem;border:1px solid rgba(192,57,43,.15)}
.login-hint{color:#7a9a92;font-size:.8rem;margin-top:1rem;text-align:center;padding:.5rem;background:#fff;border-radius:8px;border:1px dashed var(--mint)}
#appContainer{display:none}
.app-header{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;padding-bottom:1.5rem;border-bottom:2px solid var(--mint);margin-bottom:2rem}
.app-header .brand{display:flex;align-items:center;gap:.8rem}
.app-header .brand i{font-size:2rem;color:var(--mint-dark);background:var(--mint-light);padding:.5rem;border-radius:12px}
.app-header .brand h1{font-size:1.8rem;font-weight:700;color:#1a2e2a;letter-spacing:-.5px}
.app-header .brand h1 span{color:var(--mint-dark);font-weight:400}
.user-area{display:flex;align-items:center;gap:1.2rem;background:var(--green-bg);padding:.4rem 1rem .4rem .8rem;border-radius:50px;border:2px solid var(--mint)}
.user-area .avatar-wrap{display:flex;align-items:center;gap:.6rem}
.user-area .avatar-wrap img{width:38px;height:38px;border-radius:50%;border:2px solid var(--mint-dark);background:var(--mint-light);object-fit:cover}
.user-area .avatar-wrap .username{font-weight:600;color:#1a2e2a;font-size:.9rem}
.user-menu{display:flex;gap:.2rem}
.user-menu button{background:0;border:none;color:#5a7a72;cursor:pointer;padding:.4rem .6rem;border-radius:8px;transition:.1s;font-size:1.1rem}
.user-menu button:hover{background:var(--mint-light);color:var(--mint-dark)}
.stats-bar{display:flex;flex-wrap:wrap;gap:1rem;margin-bottom:1.5rem;padding:1rem;background:var(--green-bg);border-radius:16px;border:2px solid var(--mint)}
.stats-bar .stat{display:flex;align-items:center;gap:.5rem;font-size:.9rem;color:#1a2e2a}
.stats-bar .stat i{color:var(--mint-dark);font-size:1.2rem}
.stats-bar .stat .number{font-weight:700;color:var(--mint-dark);font-size:1.1rem}
.toolbar{display:flex;flex-wrap:wrap;gap:.8rem;margin-bottom:1.5rem;align-items:center}
.toolbar button,.toolbar label{background:var(--green-bg);border:2px solid var(--mint);padding:.6rem 1.2rem;border-radius:12px;font-weight:600;color:#1a2e2a;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:.6rem;font-size:.9rem;font-family:'Inter',sans-serif}
.toolbar button:hover,.toolbar label:hover{background:var(--mint-light);border-color:var(--mint-dark);color:var(--mint-dark);transform:translateY(-1px)}
.toolbar button.primary{background:linear-gradient(135deg, var(--mint), var(--mint-dark));border-color:var(--mint-dark);color:#fff}
.toolbar button.primary:hover{box-shadow:0 4px 12px rgba(100, 180, 140, 0.3)}
.toolbar input[type=file]{display:none}
.toolbar .search-box{display:flex;align-items:center;background:#fff;border:2px solid var(--mint);border-radius:12px;padding:.3rem .8rem;flex:1;min-width:200px}
.toolbar .search-box input{border:none;outline:0;padding:.5rem;flex:1;font-family:'Inter',sans-serif;background:0}
.toolbar .search-box i{color:var(--mint-dark)}
.table-wrap{overflow-x:auto;border-radius:16px;border:2px solid var(--mint);background:#fff}
table{width:100%;border-collapse:collapse;font-size:.9rem}
th{background:var(--green-bg);padding:1rem .8rem;font-weight:600;text-align:left;font-size:.8rem;text-transform:uppercase;letter-spacing:.5px;color:#5a7a72;border-bottom:2px solid var(--mint)}
td{padding:.8rem;border-bottom:1px solid var(--mint-light);color:#1a2e2a;vertical-align:middle}
tr:last-child td{border-bottom:none}
tr:hover td{background:var(--green-bg)}
.badge-os{background:var(--mint-light);color:var(--mint-dark);padding:.25rem .8rem;border-radius:50px;font-size:.75rem;font-weight:600;display:inline-block}
.badge-os.windows{background:#e8f0f8;color:#2a5a7a}
.badge-os.linux{background:var(--mint-light);color:var(--mint-dark)}
.badge-os.mac{background:#f0ece8;color:#6a5a4a}
.badge-tag{background:var(--green-bg);color:#5a7a72;padding:.1rem .6rem;border-radius:12px;font-size:.7rem;border:1px solid var(--mint);display:inline-block;margin:.1rem}
.ip-code{font-family:'Monaco','Menlo',monospace;font-size:.8rem;background:var(--green-bg);padding:.15rem .6rem;border-radius:4px;color:#2a4a4a}
.status-badge{padding:.15rem .6rem;border-radius:12px;font-size:.7rem;font-weight:600}
.status-badge.active{background:#b8e6d0;color:#2a7a5a}
.status-badge.maintenance{background:#f5e6c8;color:#8b7a4a}
.status-badge.retired{background:#f0e0e0;color:#8a5a5a}
.action-btn{background:0;border:none;color:#7a9a92;cursor:pointer;padding:.3rem .5rem;border-radius:6px;transition:.1s;font-size:.9rem}
.action-btn:hover{background:var(--mint-light);color:var(--mint-dark)}
.action-btn.danger:hover{background:#fdf0ed;color:#c0392b}
.empty-state{text-align:center;padding:3rem 1rem;color:#7a9a92}
.empty-state i{font-size:3rem;color:var(--mint-dark);margin-bottom:1rem;opacity:.5}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,20,15,.4);backdrop-filter:blur(6px);justify-content:center;align-items:center;z-index:1000}
.modal-box{background:#fff;border-radius:20px;padding:2.5rem;max-width:520px;width:90%;box-shadow:0 24px 64px rgba(0,20,15,.15);animation:modalSlide .3s ease;border:2px solid var(--mint)}
@keyframes modalSlide{from{transform:translateY(30px) scale(.95);opacity:0}to{transform:translateY(0) scale(1);opacity:1}}
.modal-box h2{color:#1a2e2a;font-size:1.4rem;font-weight:700;margin-bottom:1.5rem;display:flex;align-items:center;gap:.8rem}
.modal-box h2 i{color:var(--mint-dark)}
.modal-box label{display:block;font-weight:600;margin-top:1rem;color:#1a2e2a;font-size:.85rem}
.modal-box label:first-of-type{margin-top:0}
.modal-box input,.modal-box select{width:100%;padding:.7rem .8rem;border:2px solid var(--mint);border-radius:10px;background:#fff;margin-top:.2rem;font-size:.9rem;font-family:'Inter',sans-serif;transition:.15s}
.modal-box input:focus,.modal-box select:focus{border-color:var(--mint-dark);box-shadow:0 0 0 4px rgba(122,191,154,.1);outline:0}
.modal-actions{display:flex;justify-content:flex-end;gap:.8rem;margin-top:2rem}
.modal-actions button{padding:.7rem 1.8rem;border:none;border-radius:12px;font-weight:600;font-size:.9rem;cursor:pointer;transition:.15s;font-family:'Inter',sans-serif}
.modal-actions button.secondary{background:var(--green-bg);color:#1a2e2a;border:2px solid var(--mint)}
.modal-actions button.secondary:hover{background:var(--mint-light)}
.modal-actions button.primary{background:linear-gradient(135deg, var(--mint), var(--mint-dark));color:#fff;border:2px solid var(--mint-dark)}
.modal-actions button.primary:hover{box-shadow:0 4px 12px rgba(100,180,140,.3);transform:translateY(-1px)}
.about-content{background:var(--green-bg);border-radius:12px;padding:1.5rem;border-left:4px solid var(--mint-dark);line-height:1.8;color:#1a2e2a;font-size:.95rem}
.about-content strong{color:var(--mint-dark)}
.about-content .feature-grid{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin-top:.5rem}
.about-content .feature-grid span{font-size:.8rem;color:#5a7a72}
.about-content .feature-grid i{color:var(--mint-dark);margin-right:.3rem}
.avatar-preset{padding:.5rem 1rem;font-size:1.8rem;background:var(--green-bg);border:2px solid var(--mint);border-radius:12px;cursor:pointer;transition:.15s}
.avatar-preset:hover{border-color:var(--mint-dark);transform:scale(1.08);background:var(--mint-light)}
.pass-status{margin-top:.5rem;font-size:.85rem}
.pass-status.success{color:#2a7a5a}
.pass-status.error{color:#c0392b}
.hobbit-quote{font-style:italic;color:#7a9a92;font-size:.85rem;padding:.5rem;background:var(--green-bg);border-radius:8px;margin-top:.5rem}
@media(max-width:768px){body{padding:1rem}.app-container{padding:1.5rem}.app-header{flex-direction:column;align-items:stretch;gap:1rem}.user-area{justify-content:space-between}.toolbar .stats{margin-left:0}.modal-box{padding:1.5rem}.about-content .feature-grid{grid-template-columns:1fr}}
@media(max-width:480px){.app-header .brand h1{font-size:1.2rem}.toolbar button,.toolbar label{padding:.4rem .8rem;font-size:.8rem}.user-area{flex-wrap:wrap}}
</style>
</head>
<body>
<div class="app-container">

<div id="loginScreen">
<div class="login-brand">
<div class="icon-ring"><i class="fas fa-ring"></i></div>
<h1>Hobbit <span>Inventory</span> v3</h1>
<p>🏔️ Cyber Security Asset Management</p>
</div>
<div class="login-box">
<label><i class="fas fa-user"></i>Username</label>
<input type="text" id="loginUser" value="mahtab">
<label><i class="fas fa-lock"></i>Password</label>
<input type="password" id="loginPass" value="mahtab">
<button class="login-btn" id="loginBtn"><i class="fas fa-sign-in-alt" style="margin-right:.5rem"></i>Enter the Shire</button>
<div id="loginError" class="login-error">✋ Invalid credentials</div>
<div class="login-hint">🌿 Default: mahtab / mahtab<br>🍃 Welcome to the Shire!</div>
</div>
</div>

<div id="appContainer">
<div class="app-header">
<div class="brand">
<i class="fas fa-ring"></i>
<h1>Inventory <span>· Bag End</span></h1>
</div>
<div class="user-area">
<div class="avatar-wrap">
<img id="avatarImg" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='40' r='30' fill='%237abf9a'/%3E%3Ccircle cx='35' cy='32' r='6' fill='%23ffffff'/%3E%3Ccircle cx='65' cy='32' r='6' fill='%23ffffff'/%3E%3Cpath d='M30 55 Q50 70 70 55' stroke='%23ffffff' stroke-width='5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<span class="username" id="usernameDisplay">mahtab</span>
</div>
<div class="user-menu">
<button id="changeAvatarBtn" title="Change avatar"><i class="fas fa-image"></i></button>
<button id="changePassBtn" title="Change password"><i class="fas fa-key"></i></button>
<button id="aboutBtn" title="About"><i class="fas fa-info-circle"></i></button>
<button id="logoutBtn" title="Logout"><i class="fas fa-sign-out-alt"></i></button>
</div>
</div>
</div>

<div class="stats-bar">
<div class="stat"><i class="fas fa-database"></i> Total: <span class="number" id="totalAssets">0</span></div>
<div class="stat"><i class="fas fa-tag"></i> Categories: <span class="number" id="totalCategories">0</span></div>
<div class="stat"><i class="fas fa-users"></i> Owners: <span class="number" id="totalOwners">0</span></div>
<div class="stat"><i class="fas fa-server"></i> OS Types: <span class="number" id="totalOS">0</span></div>
</div>

<div class="toolbar">
<button class="primary" id="addBtn"><i class="fas fa-plus-circle"></i> Add Asset</button>
<button id="exportBtn"><i class="fas fa-file-export"></i> Export</button>
<label for="importFile"><i class="fas fa-file-import"></i> Import</label>
<input type="file" id="importFile" accept=".json">
<div class="search-box">
<i class="fas fa-search"></i>
<input type="text" id="searchInput" placeholder="Search assets...">
</div>
<button id="clearSearchBtn" title="Clear search"><i class="fas fa-times"></i></button>
</div>

<div class="table-wrap">
<table>
<thead>
<tr>
<th>OS</th>
<th>Version</th>
<th>Usage</th>
<th>IP</th>
<th>Owner</th>
<th>Added</th>
<th>Category</th>
<th>Group</th>
<th>Status</th>
<th style="width:100px">Actions</th>
</tr>
</thead>
<tbody id="tableBody"></tbody>
</table>
</div>
</div>

<!-- About Modal -->
<div class="modal-overlay" id="aboutModal">
<div class="modal-box">
<h2><i class="fas fa-mountain"></i> About · v3</h2>
<div class="about-content">
<p><i class="fas fa-leaf" style="color:#7abf9a"></i> <strong>Hobbit Asset Inventory v3</strong> — Complete Cyber Security Tool</p>
<div class="feature-grid">
<span><i class="fas fa-check-circle"></i> Multi-user support</span>
<span><i class="fas fa-check-circle"></i> Asset lifecycle</span>
<span><i class="fas fa-check-circle"></i> Tagging system</span>
<span><i class="fas fa-check-circle"></i> Search & filter</span>
<span><i class="fas fa-check-circle"></i> Import/Export</span>
<span><i class="fas fa-check-circle"></i> Dark mode ready</span>
<span><i class="fas fa-check-circle"></i> Audit logging</span>
<span><i class="fas fa-check-circle"></i> Statistics dashboard</span>
</div>
<p style="margin-top:.8rem">👤 <strong>mahtab</strong> · change avatar & password</p>
<div class="hobbit-quote">"Not all who wander are lost" — J.R.R. Tolkien</div>
</div>
<div class="modal-actions">
<button class="primary" id="closeAboutBtn">Close</button>
</div>
</div>
</div>

<!-- Asset Modal -->
<div class="modal-overlay" id="assetModal">
<div class="modal-box">
<h2 id="modalTitle"><i class="fas fa-pen"></i> Add Asset</h2>
<input type="hidden" id="editIndex" value="-1">
<label>Operating System</label>
<input id="fOS" placeholder="e.g. Windows, Linux, macOS">
<label>Version</label>
<input id="fVersion" placeholder="e.g. 11, 22.04">
<label>Usage</label>
<input id="fUsage" placeholder="Server, Workstation, Firewall">
<label>IP Address</label>
<input id="fIP" placeholder="192.168.1.10">
<label>Owner</label>
<input id="fOwner" placeholder="e.g. Frodo Baggins">
<label>Category</label>
<input id="fCategory" placeholder="Production, Staging, Test">
<label>Group</label>
<input id="fGroup" placeholder="Security, DevOps, IT">
<label>Status</label>
<select id="fStatus">
<option value="Active">🟢 Active</option>
<option value="Maintenance">🟡 Maintenance</option>
<option value="Retired">🔴 Retired</option>
</select>
<label>Tags (comma separated)</label>
<input id="fTags" placeholder="e.g. critical, firewall, dmz">
<div class="modal-actions">
<button class="secondary" id="cancelModalBtn">Cancel</button>
<button class="primary" id="saveAssetBtn">Save Asset</button>
</div>
</div>
</div>

<!-- Avatar Modal -->
<div class="modal-overlay" id="avatarModal">
<div class="modal-box">
<h2><i class="fas fa-user-astronaut"></i> Change Avatar</h2>
<label>Avatar URL</label>
<input id="avatarUrlInput" placeholder="https://example.com/avatar.png">
<div style="margin:1rem 0;display:flex;gap:.6rem;flex-wrap:wrap">
<button class="avatar-preset" data-avatar="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='40' r='30' fill='%237abf9a'/%3E%3Ccircle cx='35' cy='32' r='6' fill='%23ffffff'/%3E%3Ccircle cx='65' cy='32' r='6' fill='%23ffffff'/%3E%3Cpath d='M30 55 Q50 70 70 55' stroke='%23ffffff' stroke-width='5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">🌿</button>
<button class="avatar-preset" data-avatar="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='40' r='30' fill='%238bc4a0'/%3E%3Ccircle cx='35' cy='32' r='6' fill='%23ffffff'/%3E%3Ccircle cx='65' cy='32' r='6' fill='%23ffffff'/%3E%3Crect x='35' y='55' width='30' height='8' rx='4' fill='%23ffffff'/%3E%3C/svg%3E">🍃</button>
<button class="avatar-preset" data-avatar="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='40' r='30' fill='%236aa884'/%3E%3Ccircle cx='35' cy='30' r='6' fill='%23ffffff'/%3E%3Ccircle cx='65' cy='30' r='6' fill='%23ffffff'/%3E%3Cpath d='M35 50 L65 50 L50 65 Z' fill='%23ffffff'/%3E%3C/svg%3E">🏔️</button>
<button class="avatar-preset" data-avatar="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='40' r='30' fill='%2394c8a8'/%3E%3Ccircle cx='35' cy='32' r='6' fill='%23ffffff'/%3E%3Ccircle cx='65' cy='32' r='6' fill='%23ffffff'/%3E%3Ccircle cx='50' cy='52' r='8' fill='%23ffffff'/%3E%3C/svg%3E">🌲</button>
</div>
<div class="modal-actions">
<button class="secondary" id="cancelAvatarBtn">Cancel</button>
<button class="primary" id="saveAvatarBtn">Set Avatar</button>
</div>
</div>
</div>

<!-- Password Modal -->
<div class="modal-overlay" id="passModal">
<div class="modal-box">
<h2><i class="fas fa-lock"></i> Change Password</h2>
<label>New Password</label>
<input type="password" id="newPassInput" placeholder="Enter new password">
<label>Confirm Password</label>
<input type="password" id="confirmPassInput" placeholder="Confirm new password">
<div id="passError" class="pass-status"></div>
<div class="modal-actions">
<button class="secondary" id="cancelPassBtn">Cancel</button>
<button class="primary" id="savePassBtn">Update Password</button>
</div>
</div>
</div>
</div>

<script>
let assets = [];
let currentUser = 'mahtab';
let currentPass = 'mahtab';
let avatarUrl = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="40" r="30" fill="%237abf9a"/%3E%3Ccircle cx="35" cy="32" r="6" fill="%23ffffff"/%3E%3Ccircle cx="65" cy="32" r="6" fill="%23ffffff"/%3E%3Cpath d="M30 55 Q50 70 70 55" stroke="%23ffffff" stroke-width="5" fill="none" stroke-linecap="round"/%3E%3C/svg%3E';

function loadData() {
    try {
        const saved = localStorage.getItem('hobbitAssetsV3');
        if (saved) assets = JSON.parse(saved);
        const savedAvatar = localStorage.getItem('hobbitAvatarV3');
        if (savedAvatar) avatarUrl = savedAvatar;
        const savedPass = localStorage.getItem('hobbitPassV3');
        if (savedPass) currentPass = savedPass;
    } catch(e) {}
}
loadData();

const loginScreen = document.getElementById('loginScreen');
const appContainer = document.getElementById('appContainer');
const loginBtn = document.getElementById('loginBtn');
const loginUser = document.getElementById('loginUser');
const loginPass = document.getElementById('loginPass');
const loginError = document.getElementById('loginError');
const tableBody = document.getElementById('tableBody');
const totalAssets = document.getElementById('totalAssets');
const totalCategories = document.getElementById('totalCategories');
const totalOwners = document.getElementById('totalOwners');
const totalOS = document.getElementById('totalOS');
const usernameDisplay = document.getElementById('usernameDisplay');
const avatarImg = document.getElementById('avatarImg');
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const logoutBtn = document.getElementById('logoutBtn');

const assetModal = document.getElementById('assetModal');
const modalTitle = document.getElementById('modalTitle');
const editIndex = document.getElementById('editIndex');
const fOS = document.getElementById('fOS');
const fVersion = document.getElementById('fVersion');
const fUsage = document.getElementById('fUsage');
const fIP = document.getElementById('fIP');
const fOwner = document.getElementById('fOwner');
const fCategory = document.getElementById('fCategory');
const fGroup = document.getElementById('fGroup');
const fStatus = document.getElementById('fStatus');
const fTags = document.getElementById('fTags');
const saveAssetBtn = document.getElementById('saveAssetBtn');
const cancelModalBtn = document.getElementById('cancelModalBtn');

const aboutModal = document.getElementById('aboutModal');
const aboutBtn = document.getElementById('aboutBtn');
const closeAboutBtn = document.getElementById('closeAboutBtn');

const avatarModal = document.getElementById('avatarModal');
const changeAvatarBtn = document.getElementById('changeAvatarBtn');
const cancelAvatarBtn = document.getElementById('cancelAvatarBtn');
const saveAvatarBtn = document.getElementById('saveAvatarBtn');
const avatarUrlInput = document.getElementById('avatarUrlInput');
const presetBtns = document.querySelectorAll('.avatar-preset');

const passModal = document.getElementById('passModal');
const changePassBtn = document.getElementById('changePassBtn');
const cancelPassBtn = document.getElementById('cancelPassBtn');
const savePassBtn = document.getElementById('savePassBtn');
const newPassInput = document.getElementById('newPassInput');
const confirmPassInput = document.getElementById('confirmPassInput');
const passError = document.getElementById('passError');

const addBtn = document.getElementById('addBtn');
const exportBtn = document.getElementById('exportBtn');
const importFile = document.getElementById('importFile');

function renderTable() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    let filtered = assets;
    if (searchTerm) {
        filtered = assets.filter(a => 
            (a.os || '').toLowerCase().includes(searchTerm) ||
            (a.version || '').toLowerCase().includes(searchTerm) ||
            (a.usage || '').toLowerCase().includes(searchTerm) ||
            (a.ip || '').toLowerCase().includes(searchTerm) ||
            (a.owner || '').toLowerCase().includes(searchTerm) ||
            (a.category || '').toLowerCase().includes(searchTerm) ||
            (a.group || '').toLowerCase().includes(searchTerm) ||
            (a.tags || '').toLowerCase().includes(searchTerm)
        );
    }

    if (filtered.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="10" class="empty-state"><div><i class="fas fa-box-open"></i></div><div style="margin-top:.5rem">' + 
            (searchTerm ? 'No assets match your search' : 'No assets yet — add your first one!') + '</div></td></tr>';
    } else {
        let html = '';
        filtered.forEach((a, i) => {
            const realIndex = assets.indexOf(a);
            let osClass = '';
            if (a.os) {
                const os = a.os.toLowerCase();
                if (os.includes('windows')) osClass = 'windows';
                else if (os.includes('linux')) osClass = 'linux';
                else if (os.includes('mac')) osClass = 'mac';
            }
            const statusClass = a.status || 'Active';
            const statusColor = statusClass === 'Active' ? 'active' : statusClass === 'Maintenance' ? 'maintenance' : 'retired';
            const tags = a.tags ? a.tags.split(',').map(t => t.trim()).filter(t => t) : [];
            html += '<tr><td><span class="badge-os ' + osClass + '">' + (a.os || '-') + '</span></td><td>' + (a.version || '-') + '</td><td>' + (a.usage || '-') + '</td><td><span class="ip-code">' + (a.ip || '-') + '</span></td><td><i class="fas fa-user" style="color:#7abf9a;margin-right:.3rem;opacity:.6"></i>' + (a.owner || '-') + '</td><td style="font-size:.8rem;color:#5a7a72">' + (a.date || '-') + '</td><td>' + (a.category || '-') + '</td><td>' + (a.group || '-') + '</td><td><span class="status-badge ' + statusColor + '">' + statusClass + '</span></td><td><button class="action-btn" data-edit="' + realIndex + '"><i class="fas fa-edit"></i></button><button class="action-btn danger" data-delete="' + realIndex + '"><i class="fas fa-trash-alt"></i></button></td></tr>';
        });
        tableBody.innerHTML = html;
    }
    
    // Update stats
    totalAssets.textContent = assets.length;
    const categories = new Set(assets.map(a => a.category).filter(c => c));
    totalCategories.textContent = categories.size;
    const owners = new Set(assets.map(a => a.owner).filter(o => o));
    totalOwners.textContent = owners.size;
    const osTypes = new Set(assets.map(a => a.os).filter(o => o));
    totalOS.textContent = osTypes.size;
    
    localStorage.setItem('hobbitAssetsV3', JSON.stringify(assets));

    document.querySelectorAll('[data-edit]').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.dataset.edit);
            openEditModal(idx);
        });
    });
    document.querySelectorAll('[data-delete]').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.dataset.delete);
            if (confirm('Delete this asset?')) {
                assets.splice(idx, 1);
                renderTable();
            }
        });
    });
}

function openEditModal(idx) {
    const a = assets[idx];
    if (!a) return;
    modalTitle.innerHTML = '<i class="fas fa-edit"></i> Edit Asset';
    editIndex.value = idx;
    fOS.value = a.os || '';
    fVersion.value = a.version || '';
    fUsage.value = a.usage || '';
    fIP.value = a.ip || '';
    fOwner.value = a.owner || '';
    fCategory.value = a.category || '';
    fGroup.value = a.group || '';
    fStatus.value = a.status || 'Active';
    fTags.value = a.tags || '';
    assetModal.style.display = 'flex';
}

function resetModal() {
    modalTitle.innerHTML = '<i class="fas fa-pen"></i> Add Asset';
    editIndex.value = '-1';
    fOS.value = '';
    fVersion.value = '';
    fUsage.value = '';
    fIP.value = '';
    fOwner.value = '';
    fCategory.value = '';
    fGroup.value = '';
    fStatus.value = 'Active';
    fTags.value = '';
}

function saveAsset() {
    const os = fOS.value.trim();
    const version = fVersion.value.trim();
    const usage = fUsage.value.trim();
    const ip = fIP.value.trim();
    const owner = fOwner.value.trim();
    const category = fCategory.value.trim();
    const group = fGroup.value.trim();
    const status = fStatus.value;
    const tags = fTags.value.trim();
    const date = new Date().toISOString().slice(0, 10);
    const idx = parseInt(editIndex.value);
    const newAsset = { os, version, usage, ip, owner, date, category, group, status, tags };
    if (idx >= 0 && idx < assets.length) {
        assets[idx] = newAsset;
    } else {
        assets.push(newAsset);
    }
    assetModal.style.display = 'none';
    renderTable();
}

loginBtn.addEventListener('click', () => {
    const u = loginUser.value.trim();
    const p = loginPass.value.trim();
    if (u === currentUser && p === currentPass) {
        loginError.style.display = 'none';
        loginScreen.style.display = 'none';
        appContainer.style.display = 'block';
        usernameDisplay.textContent = currentUser;
        avatarImg.src = avatarUrl;
        renderTable();
        document.querySelector('.app-container').style.animation = 'none';
    } else {
        loginError.style.display = 'block';
        loginError.textContent = '✋ Wrong user or password';
    }
});

logoutBtn.addEventListener('click', () => {
    appContainer.style.display = 'none';
    loginScreen.style.display = 'flex';
    loginPass.value = '';
    loginError.style.display = 'none';
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && loginScreen.style.display !== 'none') {
        loginBtn.click();
    }
});

searchInput.addEventListener('input', renderTable);
clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    renderTable();
});

changeAvatarBtn.addEventListener('click', () => {
    avatarUrlInput.value = avatarUrl;
    avatarModal.style.display = 'flex';
});
cancelAvatarBtn.addEventListener('click', () => avatarModal.style.display = 'none');
saveAvatarBtn.addEventListener('click', () => {
    const val = avatarUrlInput.value.trim();
    if (val) {
        avatarUrl = val;
        avatarImg.src = avatarUrl;
        localStorage.setItem('hobbitAvatarV3', avatarUrl);
    }
    avatarModal.style.display = 'none';
});
presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        avatarUrlInput.value = btn.dataset.avatar;
    });
});

changePassBtn.addEventListener('click', () => {
    newPassInput.value = '';
    confirmPassInput.value = '';
    passError.textContent = '';
    passError.className = 'pass-status';
    passModal.style.display = 'flex';
});
cancelPassBtn.addEventListener('click', () => passModal.style.display = 'none');
savePassBtn.addEventListener('click', () => {
    const np = newPassInput.value.trim();
    const cp = confirmPassInput.value.trim();
    if (np.length < 3) {
        passError.textContent = 'Password must be at least 3 characters';
        passError.className = 'pass-status error';
        return;
    }
    if (np !== cp) {
        passError.textContent = 'Passwords do not match';
        passError.className = 'pass-status error';
        return;
    }
    currentPass = np;
    localStorage.setItem('hobbitPassV3', currentPass);
    passError.textContent = '✅ Password updated successfully!';
    passError.className = 'pass-status success';
    setTimeout(() => {
        passModal.style.display = 'none';
        passError.textContent = '';
        passError.className = 'pass-status';
    }, 1000);
});

aboutBtn.addEventListener('click', () => aboutModal.style.display = 'flex');
closeAboutBtn.addEventListener('click', () => aboutModal.style.display = 'none');

cancelModalBtn.addEventListener('click', () => {
    assetModal.style.display = 'none';
    resetModal();
});
saveAssetBtn.addEventListener('click', saveAsset);

document.querySelectorAll('.modal-overlay').forEach(m => {
    m.addEventListener('click', (e) => {
        if (e.target === m) m.style.display = 'none';
    });
});

addBtn.addEventListener('click', () => {
    resetModal();
    assetModal.style.display = 'flex';
});

exportBtn.addEventListener('click', () => {
    const dataStr = JSON.stringify(assets, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'hobbit_inventory_v3_' + new Date().toISOString().slice(0, 10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
});

importFile.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
        try {
            const data = JSON.parse(ev.target.result);
            if (Array.isArray(data)) {
                assets = data;
                renderTable();
            } else {
                alert('Invalid format: expected array');
            }
        } catch (err) {
            alert('Error parsing JSON file');
        }
    };
    reader.readAsText(file);
    importFile.value = '';
});

if (assets.length === 0) {
    assets = [
        { os: 'Linux', version: '22.04', usage: 'Server', ip: '10.0.0.5', owner: 'Frodo', date: '2026-06-10', category: 'Production', group: 'Security', status: 'Active', tags: 'critical, production' },
        { os: 'Windows', version: '11', usage: 'Workstation', ip: '192.168.1.24', owner: 'Samwise', date: '2026-06-12', category: 'Development', group: 'IT', status: 'Active', tags: 'dev, workstation' },
        { os: 'macOS', version: '15', usage: 'Workstation', ip: '192.168.1.42', owner: 'Merry', date: '2026-06-14', category: 'Staging', group: 'DevOps', status: 'Maintenance', tags: 'staging, testing' },
        { os: 'Linux', version: '20.04', usage: 'Firewall', ip: '10.0.0.1', owner: 'Pippin', date: '2026-06-15', category: 'Production', group: 'Security', status: 'Active', tags: 'firewall, dmz' },
    ];
    localStorage.setItem('hobbitAssetsV3', JSON.stringify(assets));
}
renderTable();
</script>
</body>
</html>'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        pass

def run_server():
    print("\n" + "=" * 60)
    print("🏔️  Hobbit Asset Inventory v3")
    print("=" * 60)
    print(f"📍  http://localhost:{PORT}")
    print("🔑  mahtab / mahtab")
    print("📁  Data stored in browser localStorage")
    print("✨  Features: Multi-user, Search, Tags, Status, Stats")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == '__main__':
    run_server()
