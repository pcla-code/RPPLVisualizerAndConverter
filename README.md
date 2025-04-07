# RPPL Visualizer and Converter

The **RPPL Visualizer** is a data visualization and aggregation tool designed to support professional learning through interactive dashboards, filtering, and comparative analytics. It includes both a **Visualizer** interface for exploring survey datasets and an **Admin Panel** for managing user access to CSV files. This project is tailored to run within the Stronghold secure computing environment.

https://github.com/user-attachments/assets/1245beec-de75-48d4-942b-532a355c0ce3

---

## 🔧 Setting Up the RPPL Visualizer Server (Stronghold Environment)

### 1. Connect to Stronghold (Big-IP)
- Use your Brown credentials (or any authorized credentials) to access the Stronghold environment via Big-IP.
- Link: [https://www.f5.com/trials/big-ip-virtual-edition](https://www.f5.com/trials/big-ip-virtual-edition)

### 2. Remote Desktop Access
- After connecting through Big-IP, open **Remote Desktop Connection** (pre-installed on Windows) and connect to your assigned Stronghold machine.
- Log in using the same credentials.

### 3. Upload RPPL Visualizer Files via Globus
- Visit [https://app.globus.org](https://app.globus.org) and log in with your Globus account.
- Search for and connect to **BrownU_SH_PAPAY_IMPORT** (a guest collection under **BrownU_SH_LOEB**).
![papayimport](https://github.com/user-attachments/assets/0f8b9a6f-64fa-4cb7-8dcc-cf13aef28239)
- Upload the contents of this repository (or the appropriate folder).
- The uploaded files will appear in the mapped network drive on your Stronghold machine.

### 4. Set the Server IP
- Copy the uploaded folder from the network drive to your Stronghold Desktop (or another working directory).
- Open the `RPPLVisualizer.bat` file with a text editor (e.g., Notepad).
- Run `ipconfig` in Command Prompt to find your computer’s IPv4 address.
- Replace the placeholder in the batch file with your IP:

    ```bat
    @echo off
    cd /d %~dp0
    start python libraries\server.py
    timeout /t 2
    start http://192.168.1.123:8000/pages/RPPL_LocalVisualizerCORS.html
    ```

> Replace `192.168.1.123` with the actual IP address of your machine.

### 5. Launch the Server
- Double-click `RPPLVisualizer.bat`
- The server will start and begin listening on the specified IP

---

## 🖥 Setting Up the RPPL Visualizer Client (For Other Stronghold Users)

### 1. Copy the Client Folder
- Each Stronghold user who needs access to the visualizer must have a copy of the `client/` folder.
- You can find this inside the main repository.

### 2. Configure Client IP
- Open the `start_visualizer.bat` file inside the `client` folder with a text editor.
- Update the line below to match the server’s IP:

    ```bat
    start http://192.168.1.123:8000/pages/RPPL_LocalVisualizerCORS.html
    ```

> Replace `192.168.1.123` with the IP address of the server machine (from the `ipconfig` command run on the server).
![UseStrongholdIPinRunnerFile](https://github.com/user-attachments/assets/c2e7b34e-9605-471f-9b5a-a9a002efab63)


### 3. Launch the Client
- Double-click `start_visualizer.bat`
- The client will open in a browser window and connect to the visualizer server

---

## 🧭 Features of the RPPL Visualizer

The Visualizer automatically detects the logged-in Stronghold user and displays only the datasets that user has access to, as determined by the Access Control Matrix (`admin.html`). It provides a secure, user-friendly interface to explore survey results with robust filtering and aggregation tools.

### Key Features:

- **Data Source Selection**  
  Users can select from multiple available datasets. Each user only sees the files they’ve been granted access to via the admin panel.

- **Cascading Filters**  
  - **Primary and Secondary Filters:** Filter responses based on demographic or categorical values such as organization, role, region, etc. The secondary filter list dynamically updates based on your primary filter selection.
  - **Outcome Filter:** Select a particular outcome or question of interest to analyze as the target variable in the graph.

- **Aggregation Options**  
  Choose how data is aggregated using:
  - `Mean`
  - `Median`
  - `Mode`
  - `Frequency`  
  Not all aggregation types apply to every dataset (e.g., median may not apply to categorical variables).

- **Within Org and Across Org Averages**  
  Graphs include two visual average lines:
  - A **dashed line** representing the average response for the current organization.
  - A **dotted line of x’s** representing the average of all other organizations with matching questionnaire structure.  
    > To enable this feature, ensure that datasets belonging to the same questionnaire are stored in the `/data/` folder with the same base filename and differing numeric suffixes (e.g., `SurveyA.csv`, `SurveyA2.csv`, `SurveyA3.csv`, etc.).

- **Preset Saving & Loading**  
  - Users can **export** their current visualization setup as a `.json` preset file.
  - **Import** previously saved presets to quickly reload a specific chart configuration and filters.

---

## 🛡️ The Admin Panel (Access Control Matrix)

https://github.com/user-attachments/assets/d68c5975-c8f5-4ca2-b39e-c7e3973cdf8d

The Admin Panel (`admin.html`) provides fine-grained access control over which datasets users can see.

- **User Permissions**  
  Grant or revoke access to specific `.csv` data files on a per-user basis.

- **Automatic File Detection**  
  Any `.csv` file added to the `/data/` directory is automatically detected by the panel and added as a new permission toggle column.

- **Add & Remove Users**  
  Easily manage user entries by adding new usernames or removing existing ones.

---

## 🧩 Dashboard View

https://github.com/user-attachments/assets/59356c7a-3c4d-442d-bf30-0316c1507b30

The Dashboard allows users to consolidate multiple saved visualizations into one shareable page.

- **Graph Compilation**  
  Add multiple saved presets to a dashboard using the dropdown and “Add to Dashboard” button.

- **Titles & Descriptions**  
  Each chart supports a customizable title and description area.

- **Image Rendering**  
  To preserve formatting, each chart is converted into a static image when the dashboard is refreshed.

- **Custom HTML Editing**  
  Click “Edit HTML” to gain full control over the dashboard layout and graph styling.

---

## 💾 Presets & Session State

Both the Visualizer and Dashboard support local session states and preset saving.

- **Auto-Restore**  
  While the client is running, current graphs and settings persist automatically.

- **Manual Export/Import**  
  Export presets to `.json` files to save graph configurations. Re-import them anytime to reload your analysis setup.

---

## 📂 Data Management

- **Datasets**  
  All data is stored in standard `.csv` format inside the `/data/` folder.

- **Access Matrix**  
  The `access.csv` file maps users to datasets they can access. This ensures that users can only view their authorized data.

- **Secure Comparison Logic**  
  Even though users only see their own data, the system can still compute average comparisons against other datasets without exposing raw records from other organizations.

---

## 📎 License
This project is licensed for internal use within RPPL and Brown University’s Stronghold environment.
