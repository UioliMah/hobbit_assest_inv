#!/usr/bin/env python3
"""
Hobbit Asset Inventory v6 - Help Center & LinkedIn Edition
Run with: python3 hobbit_asset_inventory_v6_help_linkedin.py
No external dependencies needed.

What is new:
- No login page / no username-password in UI
- Browser opens automatically when the server starts
- Local host inventory collection
- Network interface discovery
- Safe private-network scanning only
- Asset list, import/export, save to local JSON
"""

import concurrent.futures
import http.server
import ipaddress
import json
import os
import platform
import re
import socket
import socketserver
import subprocess
import sys
import threading
import time
import uuid
import webbrowser
from datetime import datetime
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 9282
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hobbit_assets_v6.json")
MAX_SCAN_HOSTS = 512
DEFAULT_PORTS = [22, 80, 135, 139, 443, 445, 3389, 5900, 8000, 8080, 8443]

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hobbit Asset Inventory v6</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#eef5f0;--card:#ffffff;--ink:#13201b;--muted:#668276;--line:#dcebe3;--green:#237a55;--green2:#0f5f3f;--soft:#e8f7ef;--warn:#a96800;--danger:#bd3030;--blue:#286f9e;--shadow:0 22px 80px rgba(17,50,35,.12)}
*{box-sizing:border-box} body{margin:0;font-family:Inter,system-ui,-apple-system,sans-serif;background:radial-gradient(circle at top left,#dff7e9 0,#eef5f0 34%,#f8fbf9 100%);color:var(--ink);min-height:100vh}.wrap{width:min(1500px,calc(100% - 34px));margin:22px auto}.top{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:18px}.brand{display:flex;gap:14px;align-items:center}.logo{width:54px;height:54px;border-radius:19px;background:linear-gradient(135deg,#1f8a5b,#123d2d);display:grid;place-items:center;color:white;box-shadow:0 12px 30px rgba(35,122,85,.25)}.brand h1{font-size:24px;margin:0;letter-spacing:-.7px}.brand p{margin:3px 0 0;color:var(--muted);font-size:13px}.clock{background:rgba(255,255,255,.7);border:1px solid var(--line);border-radius:18px;padding:11px 15px;color:var(--muted);font-weight:700;min-width:230px;text-align:center;backdrop-filter:blur(12px)}.grid{display:grid;grid-template-columns:320px 1fr;gap:18px}.panel,.main{background:rgba(255,255,255,.86);border:1px solid rgba(220,235,227,.95);border-radius:26px;box-shadow:var(--shadow);backdrop-filter:blur(16px)}.panel{padding:18px;position:sticky;top:18px;height:calc(100vh - 36px);overflow:auto}.main{padding:20px;min-height:calc(100vh - 108px)}.section-title{font-size:12px;text-transform:uppercase;letter-spacing:.9px;font-weight:800;color:var(--muted);margin:18px 0 10px}.status-card{background:linear-gradient(135deg,#f8fffb,#eef8f2);border:1px solid var(--line);border-radius:20px;padding:16px;margin-bottom:12px}.status-card strong{display:block;font-size:22px}.status-card span{color:var(--muted);font-size:12px}.btn{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:14px;padding:11px 13px;font-weight:750;cursor:pointer;transition:.14s;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;gap:8px}.btn:hover{transform:translateY(-1px);border-color:#9dccb7;box-shadow:0 10px 24px rgba(28,80,55,.09)}.btn.primary{background:var(--green);border-color:var(--green);color:white}.btn.primary:hover{background:var(--green2)}.btn.ghost{background:#f7fbf9}.btn.danger{color:var(--danger)}.btn.full{width:100%;margin-bottom:9px}.scan-box{display:grid;gap:8px}label{font-size:12px;font-weight:800;color:var(--muted)}input,select,textarea{width:100%;border:1px solid var(--line);background:#fff;border-radius:14px;padding:11px 12px;font-family:inherit;color:var(--ink);outline:none}input:focus,select:focus,textarea:focus{border-color:#72b996;box-shadow:0 0 0 4px rgba(35,122,85,.09)}.hint{font-size:12px;color:var(--muted);line-height:1.6}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}.tab{padding:10px 13px;border-radius:999px;border:1px solid var(--line);background:#fff;font-weight:800;font-size:13px;cursor:pointer;color:var(--muted)}.tab.active{background:var(--green);color:#fff;border-color:var(--green)}.hero{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}.metric{border:1px solid var(--line);border-radius:20px;padding:15px;background:#fff}.metric i{color:var(--green);margin-bottom:8px}.metric .n{font-size:24px;font-weight:850}.metric .t{font-size:12px;color:var(--muted);font-weight:700}.toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:12px 0}.search{max-width:340px;margin-left:auto}.table-wrap{border:1px solid var(--line);border-radius:18px;overflow:auto;background:#fff}table{width:100%;border-collapse:collapse;font-size:13px;min-width:1050px}th{position:sticky;top:0;background:#f6fbf8;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.6px;text-align:left;padding:13px;border-bottom:1px solid var(--line)}td{padding:12px 13px;border-bottom:1px solid #eef5f1;vertical-align:middle}tr:hover td{background:#fbfefc}.pill{display:inline-flex;align-items:center;gap:5px;border-radius:999px;padding:4px 9px;font-size:11px;font-weight:850;background:var(--soft);color:var(--green)}.pill.win{background:#e9f3fb;color:#1d6a9a}.pill.mac{background:#f3eee7;color:#7b5d3b}.pill.unknown{background:#f1f1f1;color:#666}.ip{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#f5faf7;padding:4px 7px;border-radius:8px}.ports{display:flex;gap:4px;flex-wrap:wrap}.port{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;background:#eef6f2;color:#236b4e;border-radius:7px;padding:3px 6px}.empty{text-align:center;padding:48px;color:var(--muted)}.log{height:240px;overflow:auto;background:#0d1712;color:#cdeedd;border-radius:18px;padding:14px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;line-height:1.55}.log div{border-bottom:1px solid rgba(255,255,255,.06);padding:4px 0}.modal{display:none;position:fixed;inset:0;background:rgba(6,18,12,.42);backdrop-filter:blur(7px);z-index:20;align-items:center;justify-content:center}.modal-card{background:#fff;border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:22px;width:min(560px,calc(100% - 28px));max-height:90vh;overflow:auto}.modal-card h2{margin:0 0 14px}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.actions{display:flex;justify-content:flex-end;gap:8px;margin-top:15px}.hide{display:none!important}.toast{position:fixed;right:22px;bottom:22px;background:#10251a;color:#dfffee;border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:13px 16px;box-shadow:var(--shadow);display:none;z-index:50}.iface{padding:10px;border:1px solid var(--line);border-radius:14px;background:#fff;margin-bottom:8px}.iface b{display:block}.iface span{font-size:12px;color:var(--muted)}.owner-card{margin-top:14px;border:1px solid var(--line);background:linear-gradient(135deg,#ffffff,#edf9f2);border-radius:20px;padding:15px}.owner-card h3{margin:0 0 6px;font-size:16px}.owner-card p{margin:0 0 10px;color:var(--muted);font-size:12px;line-height:1.5}.linkedin{display:inline-flex;align-items:center;gap:7px;text-decoration:none;color:white;background:#0a66c2;border-radius:12px;padding:9px 11px;font-weight:850;font-size:13px}.help-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}.help-card,.about-card{border:1px solid var(--line);background:#fff;border-radius:20px;padding:16px}.help-card i,.about-card i{color:var(--green);margin-bottom:8px}.help-card h3,.about-card h3{margin:0 0 8px;font-size:15px}.help-card p,.about-card p{margin:0;color:var(--muted);font-size:12px;line-height:1.55}.about-layout{display:grid;grid-template-columns:1.1fr .9fr;gap:14px}.about-hero{background:linear-gradient(135deg,#0e3b2b,#237a55);color:white;border-radius:24px;padding:22px;min-height:260px;display:flex;flex-direction:column;justify-content:space-between}.about-hero p{color:#d6f3e5;line-height:1.7}.about-hero a{color:white}.mini-list{margin:9px 0 0;padding:0;list-style:none}.mini-list li{padding:7px 0;border-top:1px solid #eef5f1;color:var(--muted);font-size:12px}.lock-screen{position:fixed;inset:0;background:radial-gradient(circle at top left,#dff7e9 0,#eef5f0 38%,#ffffff 100%);z-index:100;display:none;align-items:center;justify-content:center;padding:20px}.lock-card{width:min(460px,100%);background:rgba(255,255,255,.9);border:1px solid var(--line);border-radius:28px;padding:28px;box-shadow:var(--shadow);text-align:center}.lock-card .logo{margin:0 auto 15px}.lock-card h2{margin:0 0 8px}.lock-card p{color:var(--muted);line-height:1.6}.kbd{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#f3faf6;border:1px solid var(--line);border-radius:8px;padding:2px 6px;color:var(--green);font-weight:850}@media(max-width:1000px){.grid{grid-template-columns:1fr}.panel{position:static;height:auto}.hero{grid-template-columns:repeat(2,1fr)}.search{margin-left:0;max-width:none}.top{align-items:flex-start;flex-direction:column}.clock{text-align:left}}@media(max-width:1000px){.help-grid{grid-template-columns:repeat(2,1fr)}.about-layout{grid-template-columns:1fr}}@media(max-width:560px){.hero{grid-template-columns:1fr}.form-grid{grid-template-columns:1fr}.wrap{width:min(100% - 18px,1500px)}.help-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="brand"><div class="logo"><i class="fa-solid fa-ring fa-lg"></i></div><div><h1>Hobbit Asset Inventory <span style="color:var(--green)">v6</span></h1><p>No hardcoded login · Auto-open · Help Center · Asset collector</p></div></div>
    <div class="clock" id="clock">Loading time…</div>
  </div>
  <div class="grid">
    <aside class="panel">
      <div class="status-card"><strong id="assetTotal">0</strong><span>Total assets in inventory</span></div>
      <div class="status-card"><strong id="liveHosts">0</strong><span>Live hosts discovered this session</span></div>
      <div class="section-title">Automation</div>
      <button class="btn primary full" id="collectSelf"><i class="fa-solid fa-laptop-code"></i> Collect This Device</button>
      <button class="btn full" id="loadNetwork"><i class="fa-solid fa-network-wired"></i> Check Network Interfaces</button>
      <button class="btn full" id="suggestRange"><i class="fa-solid fa-wand-magic-sparkles"></i> Suggest Scan Range</button>
      <div class="section-title">Network Scan</div>
      <div class="scan-box">
        <label>Private CIDR Range</label>
        <input id="cidr" placeholder="192.168.1.0/24">
        <label>Ports</label>
        <input id="ports" value="22,80,135,139,443,445,3389,8080,8443">
        <label>Scan Limit</label>
        <select id="limit"><option>64</option><option selected>256</option><option>512</option></select>
        <button class="btn primary" id="scanBtn"><i class="fa-solid fa-radar"></i> Start Safe Scan</button>
        <div class="hint">Only private, loopback, or link-local ranges are allowed. Use it only on networks you own or are authorized to assess.</div>
      </div>
      <div class="section-title">Interfaces</div>
      <div id="interfaces"><div class="hint">Click “Check Network Interfaces”.</div></div>
      <div class="section-title">Profile</div>
      <div class="owner-card">
        <h3>Mahtab Kasaei</h3>
        <p>SOC Lead mindset · creative security operations · asset visibility for messy environments.</p>
        <a class="linkedin" href="https://www.linkedin.com/in/mahtab-kasaei" target="_blank" rel="noopener"><i class="fa-brands fa-linkedin"></i> LinkedIn Profile</a>
      </div>
      <div class="section-title">Session</div>
      <button class="btn full" id="aboutQuick"><i class="fa-solid fa-circle-info"></i> About</button>
      <button class="btn full" id="helpQuick"><i class="fa-solid fa-life-ring"></i> Help Center</button>
      <button class="btn danger full" id="logoutBtn"><i class="fa-solid fa-right-from-bracket"></i> Log Out / Lock UI</button>
    </aside>
    <main class="main">
      <div class="hero">
        <div class="metric"><i class="fa-solid fa-server"></i><div class="n" id="mServers">0</div><div class="t">Servers / Network</div></div>
        <div class="metric"><i class="fa-brands fa-windows"></i><div class="n" id="mWindows">0</div><div class="t">Windows-like</div></div>
        <div class="metric"><i class="fa-brands fa-linux"></i><div class="n" id="mLinux">0</div><div class="t">Linux / Unix</div></div>
        <div class="metric"><i class="fa-solid fa-shield-halved"></i><div class="n" id="mOpenPorts">0</div><div class="t">Open ports found</div></div>
      </div>
      <div class="tabs"><button class="tab active" data-view="assets">Assets</button><button class="tab" data-view="logs">Automation Log</button><button class="tab" data-view="about">About</button><button class="tab" data-view="help">Help Center</button></div>
      <section id="assetsView">
        <div class="toolbar">
          <button class="btn primary" id="addBtn"><i class="fa-solid fa-plus"></i> Add Asset</button>
          <button class="btn" id="exportBtn"><i class="fa-solid fa-file-export"></i> Export JSON</button>
          <label class="btn" for="importFile"><i class="fa-solid fa-file-import"></i> Import JSON</label><input class="hide" type="file" id="importFile" accept=".json,application/json">
          <button class="btn danger" id="clearBtn"><i class="fa-solid fa-trash"></i> Clear</button>
          <input class="search" id="search" placeholder="Search assets, IP, owner, ports…">
        </div>
        <div class="table-wrap"><table><thead><tr><th>Status</th><th>Hostname</th><th>IP</th><th>MAC</th><th>OS</th><th>Version</th><th>Usage</th><th>Owner</th><th>Category</th><th>Group</th><th>Open Ports</th><th>Source</th><th>Last Seen</th><th>Actions</th></tr></thead><tbody id="tbody"></tbody></table></div>
      </section>
      <section id="logsView" class="hide"><div class="log" id="log"></div></section>
      <section id="aboutView" class="hide">
        <div class="about-layout">
          <div class="about-hero">
            <div>
              <div style="font-size:38px;margin-bottom:12px"><i class="fa-solid fa-ring"></i></div>
              <h2 style="margin:0 0 10px">Hobbit Asset Inventory</h2>
              <p>A lightweight local asset visibility tool for SOC teams that need fast inventory, network awareness, and clean reporting without exposing credentials in the interface.</p>
            </div>
            <div>
              <a class="linkedin" href="https://www.linkedin.com/in/mahtab-kasaei" target="_blank" rel="noopener"><i class="fa-brands fa-linkedin"></i> Mahtab Kasaei on LinkedIn</a>
            </div>
          </div>
          <div style="display:grid;gap:12px">
            <div class="about-card"><i class="fa-solid fa-user-shield"></i><h3>Built for SOC workflow</h3><p>Collect assets, check local interfaces, discover open service ports, and keep a clean inventory for security operations.</p></div>
            <div class="about-card"><i class="fa-solid fa-lock"></i><h3>No hardcoded UI password</h3><p>The old login-style username/password is removed. Logout locks the UI locally without storing a visible default password.</p></div>
            <div class="about-card"><i class="fa-solid fa-database"></i><h3>Local-first data</h3><p>Inventory is saved beside the script in JSON format, so you can export, import, review, and version it easily.</p></div>
          </div>
        </div>
      </section>
      <section id="helpView" class="hide">
        <div class="help-grid">
          <div class="help-card"><i class="fa-solid fa-laptop-code"></i><h3>Collect This Device</h3><p>Collects hostname, local IP, MAC, OS, version, current user, and last-seen time from the machine running the script.</p></div>
          <div class="help-card"><i class="fa-solid fa-network-wired"></i><h3>Check Network Interfaces</h3><p>Lists detected interfaces, IP addresses, MAC address, and suggested CIDR ranges for authorized scanning.</p></div>
          <div class="help-card"><i class="fa-solid fa-wand-magic-sparkles"></i><h3>Suggest Scan Range</h3><p>Uses the detected private interface to fill the scan range automatically, usually like <span class="kbd">192.168.1.0/24</span>.</p></div>
          <div class="help-card"><i class="fa-solid fa-radar"></i><h3>Start Safe Scan</h3><p>Scans only private/local ranges and selected ports. It is designed for authorized internal visibility, not public targets.</p></div>
          <div class="help-card"><i class="fa-solid fa-plus"></i><h3>Add Asset</h3><p>Manually adds an asset when discovery is incomplete, such as owner, category, group, usage, or known ports.</p></div>
          <div class="help-card"><i class="fa-solid fa-edit"></i><h3>Edit Asset</h3><p>Updates hostname, IP, MAC, OS, owner, category, group, usage, and open ports without creating duplicates.</p></div>
          <div class="help-card"><i class="fa-solid fa-file-export"></i><h3>Export JSON</h3><p>Downloads the current inventory as a JSON file for backup, reporting, sharing, or GitHub documentation.</p></div>
          <div class="help-card"><i class="fa-solid fa-file-import"></i><h3>Import JSON</h3><p>Imports an existing inventory and merges matching assets by IP, MAC, or hostname to reduce duplicate rows.</p></div>
          <div class="help-card"><i class="fa-solid fa-magnifying-glass"></i><h3>Search</h3><p>Filters the table by any visible asset field: hostname, IP, OS, owner, category, group, source, ports, or status.</p></div>
          <div class="help-card"><i class="fa-solid fa-chart-simple"></i><h3>Dashboard Cards</h3><p>Shows total assets, live hosts, server/network assets, Windows, Linux/macOS, and total open ports.</p></div>
          <div class="help-card"><i class="fa-solid fa-terminal"></i><h3>Automation Log</h3><p>Shows what the tool has done during this browser session: load, collect, scan, import, export, and errors.</p></div>
          <div class="help-card"><i class="fa-solid fa-right-from-bracket"></i><h3>Log Out / Lock UI</h3><p>Hides the dashboard and returns to a local lock screen. Re-entering does not require a password because credentials are intentionally removed.</p></div>
        </div>
      </section>
    </main>
  </div>
</div>

<div class="modal" id="assetModal"><div class="modal-card"><h2 id="modalTitle">Add Asset</h2><input id="editId" type="hidden"><div class="form-grid">
<div><label>Hostname</label><input id="fHostname"></div><div><label>IP</label><input id="fIp"></div><div><label>MAC</label><input id="fMac"></div><div><label>OS</label><input id="fOs"></div><div><label>Version</label><input id="fVersion"></div><div><label>Usage</label><input id="fUsage" placeholder="Server / Workstation / Firewall"></div><div><label>Owner</label><input id="fOwner"></div><div><label>Category</label><input id="fCategory" placeholder="Production / Staging / Test"></div><div><label>Group</label><input id="fGroup" placeholder="SOC / IT / DevOps"></div><div><label>Open Ports</label><input id="fPorts" placeholder="22,443"></div></div><div class="actions"><button class="btn" id="cancelModal">Cancel</button><button class="btn primary" id="saveModal">Save</button></div></div></div>
<div class="lock-screen" id="lockScreen"><div class="lock-card"><div class="logo"><i class="fa-solid fa-ring fa-lg"></i></div><h2>Hobbit UI Locked</h2><p>The dashboard is hidden locally. No default username/password is stored or displayed in the page.</p><button class="btn primary full" id="unlockBtn"><i class="fa-solid fa-unlock"></i> Open Dashboard</button></div></div>
<div class="toast" id="toast"></div>
<script>
let assets=[];let networkInfo=null;const $=id=>document.getElementById(id);
function now(){return new Date().toLocaleString()}function log(m){const d=document.createElement('div');d.textContent='['+now()+'] '+m;$('log').prepend(d)}function toast(m){$('toast').textContent=m;$('toast').style.display='block';setTimeout(()=>$('toast').style.display='none',2600)}
function tick(){$('clock').textContent=new Date().toLocaleString(undefined,{weekday:'short',year:'numeric',month:'short',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'})}setInterval(tick,1000);tick();
async function api(path,opts={}){const r=await fetch(path,{headers:{'Content-Type':'application/json'},...opts});const j=await r.json();if(!j.ok)throw new Error(j.error||'Request failed');return j}
function normalize(a){a.id=a.id||crypto.randomUUID();a.hostname=a.hostname||'';a.ip=a.ip||'';a.mac=a.mac||'';a.os=a.os||'Unknown';a.version=a.version||'';a.usage=a.usage||'';a.owner=a.owner||'';a.category=a.category||'';a.group=a.group||'';a.open_ports=Array.isArray(a.open_ports)?a.open_ports:((a.open_ports||'').toString().split(',').map(x=>x.trim()).filter(Boolean));a.status=a.status||'unknown';a.source=a.source||'manual';a.last_seen=a.last_seen||new Date().toISOString();return a}
function mergeAssets(newItems){let added=0,updated=0;newItems.map(normalize).forEach(n=>{const idx=assets.findIndex(a=>(n.ip&&a.ip===n.ip)||(n.mac&&a.mac&&a.mac.toLowerCase()===n.mac.toLowerCase())||(n.hostname&&a.hostname===n.hostname));if(idx>=0){assets[idx]={...assets[idx],...n,id:assets[idx].id};updated++}else{assets.push(n);added++}});saveAssets();render();return{added,updated}}
async function loadAssets(){try{const j=await api('/api/assets');assets=(j.assets||[]).map(normalize);render();log('Inventory loaded from local JSON file.')}catch(e){log('Could not load local inventory: '+e.message)}}
async function saveAssets(){try{await api('/api/assets',{method:'POST',body:JSON.stringify({assets})})}catch(e){log('Save failed: '+e.message)}}
function osClass(os){os=(os||'').toLowerCase();if(os.includes('windows'))return'win';if(os.includes('linux')||os.includes('unix'))return'';if(os.includes('mac')||os.includes('darwin'))return'mac';return'unknown'}
function render(){const q=$('search').value.toLowerCase().trim();const rows=assets.filter(a=>JSON.stringify(a).toLowerCase().includes(q));$('assetTotal').textContent=assets.length;$('liveHosts').textContent=assets.filter(a=>a.status==='live').length;$('mServers').textContent=assets.filter(a=>/(server|firewall|router|switch|network)/i.test(a.usage||'')).length;$('mWindows').textContent=assets.filter(a=>/windows/i.test(a.os||'')).length;$('mLinux').textContent=assets.filter(a=>/(linux|unix|darwin|macos)/i.test(a.os||'')).length;$('mOpenPorts').textContent=assets.reduce((s,a)=>s+(a.open_ports||[]).length,0);if(rows.length===0){$('tbody').innerHTML='<tr><td colspan="14" class="empty"><i class="fa-solid fa-box-open fa-2x"></i><br><br>No assets yet. Collect this device or scan an authorized private range.</td></tr>';return}$('tbody').innerHTML=rows.map(a=>`<tr><td><span class="pill ${a.status==='live'?'':'unknown'}"><i class="fa-solid ${a.status==='live'?'fa-circle-check':'fa-circle-question'}"></i>${a.status}</span></td><td><b>${esc(a.hostname)||'-'}</b></td><td><span class="ip">${esc(a.ip)||'-'}</span></td><td>${esc(a.mac)||'-'}</td><td><span class="pill ${osClass(a.os)}">${esc(a.os)||'Unknown'}</span></td><td>${esc(a.version)||'-'}</td><td>${esc(a.usage)||'-'}</td><td>${esc(a.owner)||'-'}</td><td>${esc(a.category)||'-'}</td><td>${esc(a.group)||'-'}</td><td><div class="ports">${(a.open_ports||[]).map(p=>`<span class="port">${esc(p)}</span>`).join('')||'-'}</div></td><td>${esc(a.source)||'-'}</td><td>${a.last_seen?new Date(a.last_seen).toLocaleString():'-'}</td><td><button class="btn" onclick="editAsset('${a.id}')"><i class="fa-solid fa-edit"></i></button> <button class="btn danger" onclick="delAsset('${a.id}')"><i class="fa-solid fa-trash"></i></button></td></tr>`).join('')}
function esc(x){return (x??'').toString().replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
async function collectSelf(){try{log('Collecting local device asset data…');const j=await api('/api/self');const r=mergeAssets([j.asset]);toast('This device collected');log('Local device collected: '+(j.asset.hostname||j.asset.ip));}catch(e){toast(e.message);log('Collect local failed: '+e.message)}}
async function loadNetwork(){try{log('Checking network interfaces…');const j=await api('/api/network');networkInfo=j;$('interfaces').innerHTML=(j.interfaces||[]).map(i=>`<div class="iface"><b>${esc(i.name)}</b><span>IP: ${esc(i.ip)} · CIDR: ${esc(i.cidr||'-')} · MAC: ${esc(i.mac||'-')}</span></div>`).join('')||'<div class="hint">No interface detected.</div>';toast('Network checked');}catch(e){toast(e.message);log('Network check failed: '+e.message)}}
async function suggestRange(){if(!networkInfo)await loadNetwork();const candidate=(networkInfo.interfaces||[]).find(i=>i.cidr&&i.cidr.includes('/'));if(candidate){$('cidr').value=candidate.cidr;toast('Range suggested: '+candidate.cidr);log('Suggested scan range '+candidate.cidr)}else{toast('No CIDR found')}}
async function scan(){try{const cidr=$('cidr').value.trim();const ports=$('ports').value.split(',').map(x=>parseInt(x.trim())).filter(Boolean);const limit=parseInt($('limit').value);if(!cidr){toast('Enter a CIDR range first');return}log('Starting safe private-range scan: '+cidr+' ports '+ports.join(','));$('scanBtn').disabled=true;$('scanBtn').innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Scanning…';const j=await api('/api/scan',{method:'POST',body:JSON.stringify({cidr,ports,limit})});const r=mergeAssets(j.assets||[]);toast(`Scan done: ${r.added} added, ${r.updated} updated`);log(`Scan completed: ${j.scanned} checked, ${(j.assets||[]).length} live/interesting hosts.`)}catch(e){toast(e.message);log('Scan failed: '+e.message)}finally{$('scanBtn').disabled=false;$('scanBtn').innerHTML='<i class="fa-solid fa-radar"></i> Start Safe Scan'}}
function openModal(){['editId','fHostname','fIp','fMac','fOs','fVersion','fUsage','fOwner','fCategory','fGroup','fPorts'].forEach(id=>$(id).value='');$('modalTitle').textContent='Add Asset';$('assetModal').style.display='flex'}
function editAsset(id){const a=assets.find(x=>x.id===id);if(!a)return;$('modalTitle').textContent='Edit Asset';$('editId').value=a.id;$('fHostname').value=a.hostname;$('fIp').value=a.ip;$('fMac').value=a.mac;$('fOs').value=a.os;$('fVersion').value=a.version;$('fUsage').value=a.usage;$('fOwner').value=a.owner;$('fCategory').value=a.category;$('fGroup').value=a.group;$('fPorts').value=(a.open_ports||[]).join(',');$('assetModal').style.display='flex'}
function saveModal(){const a=normalize({id:$('editId').value||crypto.randomUUID(),hostname:$('fHostname').value,ip:$('fIp').value,mac:$('fMac').value,os:$('fOs').value,version:$('fVersion').value,usage:$('fUsage').value,owner:$('fOwner').value,category:$('fCategory').value,group:$('fGroup').value,open_ports:$('fPorts').value,status:'manual',source:'manual',last_seen:new Date().toISOString()});const idx=assets.findIndex(x=>x.id===a.id);if(idx>=0)assets[idx]=a;else assets.push(a);$('assetModal').style.display='none';saveAssets();render();toast('Asset saved')}
function delAsset(id){if(!confirm('Delete this asset?'))return;assets=assets.filter(a=>a.id!==id);saveAssets();render();toast('Asset deleted')}
function clearAll(){if(!confirm('Clear all assets?'))return;assets=[];saveAssets();render();toast('Inventory cleared')}
function exportJson(){const blob=new Blob([JSON.stringify(assets,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='hobbit_inventory_'+new Date().toISOString().slice(0,10)+'.json';a.click();URL.revokeObjectURL(url)}
function importJson(e){const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=ev=>{try{const data=JSON.parse(ev.target.result);if(!Array.isArray(data))throw new Error('Expected JSON array');const m=mergeAssets(data);toast(`Imported: ${m.added} added, ${m.updated} updated`);log('JSON import completed.')}catch(err){toast('Import failed: '+err.message)}};r.readAsText(f);e.target.value=''}
$('collectSelf').onclick=collectSelf;$('loadNetwork').onclick=loadNetwork;$('suggestRange').onclick=suggestRange;$('scanBtn').onclick=scan;$('addBtn').onclick=openModal;$('saveModal').onclick=saveModal;$('cancelModal').onclick=()=>$('assetModal').style.display='none';$('assetModal').onclick=e=>{if(e.target===$('assetModal'))$('assetModal').style.display='none'};$('exportBtn').onclick=exportJson;$('importFile').onchange=importJson;$('clearBtn').onclick=clearAll;$('search').oninput=render;function showView(view){document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x.dataset.view===view));['assets','logs','about','help'].forEach(v=>$(v+'View').classList.toggle('hide',v!==view));}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>showView(t.dataset.view));$('aboutQuick').onclick=()=>showView('about');$('helpQuick').onclick=()=>showView('help');$('logoutBtn').onclick=()=>{$('lockScreen').style.display='flex';log('UI locked by local logout action.');};$('unlockBtn').onclick=()=>{$('lockScreen').style.display='none';toast('Dashboard opened');};
loadAssets().then(()=>{collectSelf();loadNetwork();});
</script>
</body>
</html>'''


def run_cmd(cmd, timeout=3):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception:
        return ""


def load_assets():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_assets(assets):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(assets, f, ensure_ascii=False, indent=2)


def guess_usage_from_ports(open_ports):
    ports = set(int(p) for p in open_ports if str(p).isdigit())
    if 3389 in ports or 445 in ports or 135 in ports:
        return "Windows / Server"
    if 22 in ports:
        return "Linux / Server"
    if 80 in ports or 443 in ports or 8080 in ports or 8443 in ports:
        return "Web / Network Service"
    if 5900 in ports:
        return "Remote Access"
    return "Network Asset" if ports else "Host"


def guess_os_from_ports(open_ports):
    ports = set(int(p) for p in open_ports if str(p).isdigit())
    if 3389 in ports or 445 in ports or 135 in ports or 139 in ports:
        return "Windows-like"
    if 22 in ports:
        return "Linux/Unix-like"
    return "Unknown"


def local_ips():
    ips = set()
    try:
        host = socket.gethostname()
        for item in socket.getaddrinfo(host, None, socket.AF_INET):
            ips.add(item[4][0])
    except Exception:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return [ip for ip in ips if not ip.startswith("127.")]


def get_default_ip():
    ips = local_ips()
    return ips[0] if ips else "127.0.0.1"


def get_mac_for_interface():
    mac = uuid.getnode()
    return ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))


def get_interfaces():
    interfaces = []
    system = platform.system().lower()
    if system == "darwin":
        out = run_cmd(["ifconfig"], 4)
        current = None
        blocks = re.split(r"\n(?=\w)", out)
        for block in blocks:
            name_match = re.match(r"([^:\s]+):", block)
            if not name_match:
                continue
            name = name_match.group(1)
            inet = re.search(r"inet (\d+\.\d+\.\d+\.\d+) netmask 0x([0-9a-fA-F]+)", block)
            mac = re.search(r"ether ([0-9a-fA-F:]{17})", block)
            if inet:
                ip = inet.group(1)
                mask_hex = inet.group(2)
                try:
                    mask_int = int(mask_hex, 16)
                    prefix = bin(mask_int).count("1")
                    cidr = str(ipaddress.ip_interface(f"{ip}/{prefix}").network)
                except Exception:
                    cidr = ""
                if not ip.startswith("127."):
                    interfaces.append({"name": name, "ip": ip, "mac": mac.group(1) if mac else "", "cidr": cidr})
    elif system == "windows":
        out = run_cmd(["ipconfig", "/all"], 5)
        current = {"name": "Windows Interface", "ip": "", "mac": "", "cidr": ""}
        for line in out.splitlines():
            if "adapter" in line.lower() and line.strip().endswith(":"):
                if current.get("ip"):
                    interfaces.append(current)
                current = {"name": line.strip().strip(":"), "ip": "", "mac": "", "cidr": ""}
            if "Physical Address" in line:
                current["mac"] = line.split(":", 1)[-1].strip().replace("-", ":").lower()
            if "IPv4 Address" in line:
                m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if m:
                    current["ip"] = m.group(1)
            if "Subnet Mask" in line and current.get("ip"):
                m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if m:
                    try:
                        prefix = ipaddress.IPv4Network(f"0.0.0.0/{m.group(1)}").prefixlen
                        current["cidr"] = str(ipaddress.ip_interface(f"{current['ip']}/{prefix}").network)
                    except Exception:
                        pass
        if current.get("ip"):
            interfaces.append(current)
    else:
        out = run_cmd(["ip", "-o", "-4", "addr", "show"], 4) or run_cmd(["ifconfig"], 4)
        for line in out.splitlines():
            m = re.search(r"\d+:\s+([^\s]+).*inet\s+(\d+\.\d+\.\d+\.\d+/\d+)", line)
            if m:
                name, ipif = m.group(1), m.group(2)
                ip = ipif.split('/')[0]
                if not ip.startswith("127."):
                    interfaces.append({"name": name, "ip": ip, "mac": "", "cidr": str(ipaddress.ip_interface(ipif).network)})
    if not interfaces:
        for ip in local_ips():
            try:
                cidr = str(ipaddress.ip_interface(f"{ip}/24").network)
            except Exception:
                cidr = ""
            interfaces.append({"name": "default", "ip": ip, "mac": get_mac_for_interface(), "cidr": cidr})
    return interfaces


def get_local_asset():
    hostname = socket.gethostname()
    ip = get_default_ip()
    return {
        "id": str(uuid.uuid4()),
        "hostname": hostname,
        "ip": ip,
        "mac": get_mac_for_interface(),
        "os": platform.system() or "Unknown",
        "version": platform.release() or platform.version(),
        "usage": "This Device",
        "owner": os.getenv("USER") or os.getenv("USERNAME") or "",
        "category": "Local",
        "group": "Inventory Collector",
        "open_ports": [],
        "status": "live",
        "source": "self-collector",
        "last_seen": datetime.utcnow().isoformat() + "Z",
    }


def is_allowed_cidr(cidr):
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except Exception:
        raise ValueError("Invalid CIDR range")
    if net.version != 4:
        raise ValueError("Only IPv4 ranges are supported in this version")
    if net.num_addresses > MAX_SCAN_HOSTS + 2:
        raise ValueError(f"Range is too large. Maximum allowed hosts: {MAX_SCAN_HOSTS}")
    if not (net.is_private or net.is_loopback or net.is_link_local):
        raise ValueError("Only private, loopback, or link-local ranges are allowed")
    return net


def valid_ports(ports):
    clean = []
    for p in ports or DEFAULT_PORTS:
        try:
            pi = int(p)
            if 1 <= pi <= 65535 and pi not in clean:
                clean.append(pi)
        except Exception:
            pass
    return clean[:40] or DEFAULT_PORTS


def tcp_check(ip, port, timeout=0.45):
    try:
        with socket.create_connection((str(ip), int(port)), timeout=timeout):
            return True
    except Exception:
        return False


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except Exception:
        return ""


def arp_mac(ip):
    out = run_cmd(["arp", "-a", str(ip)], 2)
    patterns = [r"(([0-9a-fA-F]{1,2}:){5}[0-9a-fA-F]{1,2})", r"(([0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2})"]
    for pat in patterns:
        m = re.search(pat, out)
        if m:
            return m.group(1).replace("-", ":").lower()
    return ""


def scan_host(ip, ports):
    open_ports = []
    for p in ports:
        if tcp_check(ip, p):
            open_ports.append(p)
    if not open_ports:
        return None
    ip_s = str(ip)
    return {
        "id": str(uuid.uuid4()),
        "hostname": reverse_dns(ip_s),
        "ip": ip_s,
        "mac": arp_mac(ip_s),
        "os": guess_os_from_ports(open_ports),
        "version": "",
        "usage": guess_usage_from_ports(open_ports),
        "owner": "",
        "category": "Discovered",
        "group": "Network Scan",
        "open_ports": open_ports,
        "status": "live",
        "source": "safe-port-scan",
        "last_seen": datetime.utcnow().isoformat() + "Z",
    }


def scan_network(cidr, ports, limit):
    net = is_allowed_cidr(cidr)
    ports = valid_ports(ports)
    hosts = list(net.hosts())[: min(int(limit or 256), MAX_SCAN_HOSTS)]
    assets = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        futures = [executor.submit(scan_host, ip, ports) for ip in hosts]
        for future in concurrent.futures.as_completed(futures):
            item = future.result()
            if item:
                assets.append(item)
    assets.sort(key=lambda x: tuple(int(part) for part in x["ip"].split(".")))
    return assets, len(hosts)


class Handler(http.server.SimpleHTTPRequestHandler):
    server_version = "HobbitAssetInventory/6.0"

    def _json(self, payload, code=200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
            return
        if path == "/api/assets":
            self._json({"ok": True, "assets": load_assets()})
            return
        if path == "/api/self":
            self._json({"ok": True, "asset": get_local_asset()})
            return
        if path == "/api/network":
            self._json({"ok": True, "interfaces": get_interfaces()})
            return
        self._json({"ok": False, "error": "Not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._read_body()
            if path == "/api/assets":
                assets = body.get("assets", [])
                if not isinstance(assets, list):
                    raise ValueError("assets must be a list")
                save_assets(assets)
                self._json({"ok": True, "saved": len(assets)})
                return
            if path == "/api/scan":
                cidr = body.get("cidr", "")
                ports = body.get("ports", DEFAULT_PORTS)
                limit = int(body.get("limit", 256))
                assets, scanned = scan_network(cidr, ports, limit)
                self._json({"ok": True, "assets": assets, "scanned": scanned})
                return
            self._json({"ok": False, "error": "Not found"}, 404)
        except Exception as e:
            self._json({"ok": False, "error": str(e)}, 400)

    def log_message(self, fmt, *args):
        return


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def run_server():
    url = f"http://{HOST}:{PORT}/"
    print("\n" + "=" * 64)
    print("🌿 Hobbit Asset Inventory v6 - Help Center & LinkedIn Edition")
    print("=" * 64)
    print(f"📍 Local server: {url}")
    print("🔓 Hardcoded login removed: use local lock/logout only.")
    print("🌐 Network scanning is limited to private/local ranges only.")
    print(f"💾 Inventory file: {DATA_FILE}")
    print("=" * 64)
    print("Press Ctrl+C to stop the server.\n")
    threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    with ReusableTCPServer((HOST, PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")


if __name__ == "__main__":
    run_server()
