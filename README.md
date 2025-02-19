# Minecraft-Modpack-Downloader 🎲

[![License](https://shields.io/github/license/m-stasiak/Minecraft-Modpack-Downloader?label=License)](https://www.gnu.org/licenses/gpl-3.0.html) [![Language](https://img.shields.io/badge/Language-Python-blue)](https://www.python.org/)

A Python tool to automatically download mods for Minecraft modpacks from `.zip` or `.mrpack` files exported from **CurseForge** or **Modrinth**.

## ✨ Features

✅ Supports both **CurseForge** and **Modrinth** modpacks\
✅ Automatically organizes resource packs and shaders (for Modrinth)\
✅ Simple CLI usage\
✅ Works as a standalone executable or Python script

---

## 📌 Requirements

- **Python 3.x** (if running as a script)
- **Internet connection** (for downloading mods)
- **PyInstaller** (only if building the application manually)

---

## 💾 Installation

### 🔹 Download Prebuilt Binary

The easiest way to use the application is to download the latest release:

➡️ [**Latest Release**](https://github.com/M-Stasiak/Minecraft-Modpack-Downloader/releases/latest)

### 🔹 Build Using PyInstaller

To build the application manually, follow these steps:

```bash
# Clone the repository
git clone https://github.com/M-Stasiak/Minecraft-Modpack-Downloader.git
cd Minecraft-Modpack-Downloader

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install pyinstaller

# Build executable
pyinstaller --onefile --name MinecraftModPackDownloader main.py
```

✅ The built file will be available in the `dist` directory.

### 🔹 Run as a Python Script

If you prefer to run the script directly:

```bash
# Clone the repository
git clone https://github.com/M-Stasiak/Minecraft-Modpack-Downloader.git
cd Minecraft-Modpack-Downloader

# Run the script
python main.py -h
```

---

## 📃 Usage

### 🔹 Command-Line Help

```text
usage: MinecraftModPackDownloader [-h] [--curseforge | --modrinth] file

Download mods for a Minecraft modpack.

Positional arguments:
  file          Path to .zip / .mrpack file

Options:
  -h, --help    Show this help message and exit
  --curseforge  Download mods from CurseForge
  --modrinth    Download mods from Modrinth
```

### 🔹 Example Usage

```bash
# Download mods for a CurseForge modpack
MinecraftModPackDownloader "Modpack.zip" --curseforge

# Download mods for a Modrinth modpack
MinecraftModPackDownloader "Modpack.mrpack" --modrinth
```

The mods will be downloaded to the directory: `{Modpack_Name}/overrides/mods`

If the modpack includes resource packs or shaders:

- **Modrinth**: These will automatically be separated into the appropriate folders: `resourcepacks` and `shaders`.
- **CurseForge**: All files will be downloaded into the `mods` folder. You will need to manually check for resource packs or shaders and move them to their respective folders (`resourcepacks` and `shaders`).

---

## 📜 License

This project is licensed under the **GPL-3.0 License**. See the [LICENSE](LICENSE) file for details.

```text
Copyright © 2025  Mateusz Stasiak

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```