````markdown
# Hobbit Asset Inventory

<p align="center">
  <img src="Hobbit-assest-v6.png" alt="Hobbit Asset Inventory v6 Overview" width="100%">
</p>

## About

**Hobbit Asset Inventory** is a lightweight Python-based asset inventory and discovery tool designed for teams that need a clean, simple, and practical way to manage messy assets.

It helps collect local device information, discover private network assets, organize inventory data, and export reports for documentation, SOC workflows, and GitHub sharing.

The tool runs locally in the browser and does not require a cloud account or hardcoded login credentials.

---

## Latest Version

**Hobbit Asset Inventory v6 - Help Center & LinkedIn Edition**

**Discover. Inventory. Monitor. Secure.**

---

## Key Features

- Local asset inventory management
- Local device information collector
- Private network interface discovery
- Suggested scan range based on detected interfaces
- Safe private/local network scanning
- Open port discovery for selected ports
- Add, edit, and delete assets
- Search and filter asset records
- JSON import and export
- Dashboard summary cards
- Automation log
- Help Center with full option descriptions
- About page with project and author information
- Local Lock / Logout UI
- No hardcoded username or password

---

## What This Tool Can Do

### Collect This Device

Collects information from the machine running the tool, including:

- Hostname
- Local IP address
- MAC address
- Operating system
- OS version
- Current user
- Last seen time

---

### Check Network Interfaces

Lists detected network interfaces and related information, such as:

- Interface name
- IP address
- MAC address
- Suggested private CIDR range

This helps you understand which local network ranges can be scanned safely.

---

### Suggest Scan Range

Automatically suggests a private scan range based on the detected local interface.

Example:

```text
192.168.1.0/24
````

---

### Start Safe Scan

Performs a safe scan only on private/local network ranges.

The scanner is designed for authorized internal visibility only and does not scan public internet targets.

---

### Asset Management

You can manually manage assets with fields such as:

* Hostname
* IP address
* MAC address
* Operating system
* OS version
* Owner
* Category
* Group
* Usage
* Open ports
* Source
* Status
* First seen
* Last seen

---

### Import / Export

The tool supports JSON import and export for:

* Backup
* Reporting
* Documentation
* Sharing inventory data
* Keeping GitHub examples updated

---

## Screenshot

<p align="center">
  <img src="Hobbit-Github_Pic.png" alt="Hobbit Asset Inventory Screenshot" width="100%">
</p>

---

## Usage

Run the latest version:

```bash
python3 hobbit_asset_inventory_v6_help_linkedin.py
```

Then open the local web interface:

```text
http://127.0.0.1:9282/
```

The page usually opens automatically after running the script.

---

## Project Files

```text
hobbit_asset_inventory_v6_help_linkedin.py   Latest v6 version
hobbit_assest_inv_v3.py                      Older version
Hobbit-assest-v6.png                         v6 overview image
Hobbit-Github_Pic.png                        GitHub project image
README.md                                    Project documentation
```

---

## Security Notes

This tool is intended for authorized internal use only.

Network scanning is limited to private/local ranges such as:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
127.0.0.0/8
```

Do not use this tool to scan networks you do not own or do not have permission to assess.

Hardcoded login credentials were removed in v6. The Logout / Lock UI feature only hides the dashboard locally and does not rely on stored default credentials.

---

## Roadmap

Planned future improvements:

* Risk scoring for assets
* Splunk asset lookup export
* CSV and Excel export
* SharePoint integration
* Better asset change history
* Duplicate asset detection
* SOC report generation
* Vulnerability and CVE hints
* Dark mode
* More dashboard cards
* Ticket template for high-risk assets

---

## Author

Created by **Mahtab Kasaei**

LinkedIn: [www.linkedin.com/in/mahtab-kasaei](https://www.linkedin.com/in/mahtab-kasaei)

---

## License

This project is currently released as a personal SOC tooling project.

Use it responsibly and only in authorized environments.

```
```
