# AI-Driven Deep Learning for Aerial Infrastructure Classification

An end-to-end deep learning web platform for automated recognition, classification, and monitoring intelligence of strategic infrastructure from aerial imagery. The system leverages state-of-the-art Convolutional Neural Networks (**DenseNet121**, **MobileNetV2**, and **VGG16**) combined with AI explainability (**Grad-CAM Attention Heatmaps**) and an interactive Flask web dashboard.

---

## 📌 Project Overview

Aerial infrastructure classification plays a critical role in urban planning, transport management, defense reconnaissance, and civil engineering asset monitoring. This project provides an AI-assisted pipeline that ingests aerial and satellite imagery, preprocesses the inputs, infers the infrastructure category across 10 distinct classes, generates visual attention heatmaps, and records an audit log in a persistent SQLite database with printable PDF inspection reports.

> **Disclaimer:** This system provides AI-assisted classification and monitoring priority based on predicted classes and predefined monitoring criteria. It does not detect confirmed physical damage, structural failure, or military threat intelligence.

---

## ✨ Key Features

- **Multi-Class Infrastructure Identification:** Accurate classification across 10 strategic infrastructure categories.
- **Deep Learning Transfer Learning:** Incorporates and compares **DenseNet121**, **MobileNetV2**, and **VGG16** architectures.
- **Top-3 Probability Rankings:** Delivers granular confidence scores and probability distributions for the top 3 predictions.
- **AI Explainability (Grad-CAM Heatmaps):** Generates visual attention heatmaps highlighting region features that influenced the model's prediction.
- **Image Quality Assessment:** Evaluates resolution, brightness, and contrast of uploaded aerial scans before classification.
- **AI-Assisted Monitoring Priority:** Computes a continuous Monitoring Score (0–100) and categorizes priority into *High*, *Medium*, or *Low*.
- **Role-Based Authentication:** Clean authentication portal supporting *Administrator*, *Analyst*, and *Defense Officer* roles.
- **Persistent Audit Log:** SQLite database (`infrastructure_intelligence.db`) storing all historical inspections with continuous serial numbers and search/filtering.
- **Inspection Report Generation:** Instant generation of standardized, printable PDF inspection reports containing query scans, heatmaps, and metrics.
- **Model Analytics Dashboard:** Evaluation slides showing accuracy curves, loss curves, and per-class performance comparisons.

---

## 🏷️ 10 Infrastructure Classes

1. **Airforce Base** - Military hangars, airfields, and tactical runway facilities.
2. **Army Base** - Military barracks, perimeter installations, and troop grounds.
3. **Bridge** - River crossings, viaducts, and highway overpasses.
4. **Capital City** - High-density urban architecture and metro administrative hubs.
5. **Commercial Airport** - Civil aviation terminals, passenger runways, and gate aprons.
6. **National Highway** - Multi-lane interstates, expressways, and transport arteries.
7. **Navy Base** - Coastal naval facilities, docks, and warship moorings.
8. **Oil Reservoir Tank** - Circular industrial petroleum storage and refinery tanks.
9. **Port** - Commercial maritime docks, container terminals, and cargo cranes.
10. **Railway Station** - Train passenger terminals, rail tracks, and switching yards.

---

## 🧠 Deep Learning Architectures

The training and evaluation pipeline evaluates and compares three leading transfer learning architectures:

| Model Architecture | Strengths & Characteristics |
| :--- | :--- |
| **DenseNet121** | Feature reuse via dense connectivity between layers; mitigates vanishing gradient; high parameter efficiency. |
| **MobileNetV2** | Lightweight inverted residual structure with linear bottlenecks; optimized for fast inference on low-power edge devices. |
| **VGG16** | Deep convolutional pipeline using uniform $3\times3$ filter kernels; excellent spatial feature extraction for complex terrain. |

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3 (Glassmorphism Dark Theme), JavaScript (Vanilla JS), FontAwesome 6
- **Backend:** Python 3.10+, Flask Web Framework, Werkzeug
- **Deep Learning & Computer Vision:** TensorFlow / Keras, OpenCV (`cv2`), PIL (Pillow), NumPy
- **Data & Plotting:** Matplotlib, Seaborn, Scikit-Learn
- **Database:** SQLite3
- **Reporting:** HTML5 / CSS Print Engine (PDF Export)

---

## 📁 Project Directory Structure

```text
aerial_infrastructure_classification/
│── dataset/                              # 10 subdirectories for each infrastructure class
│   ├── Airforce Base/
│   ├── Army Base/
│   ├── Bridge/
│   ├── Capital City/
│   ├── Commercial Airport/
│   ├── National Highway/
│   ├── Navy Base/
│   ├── Oil Reservoir Tank/
│   ├── Port/
│   └── Railway Station/
│── instance/
│   └── infrastructure_intelligence.db   # SQLite audit trail & user database
│── models/
│   └── model.h5                         # Saved model weights & evaluation metadata
│── sample_test_images/                   # High-resolution test scans for each class
│── static/
│   ├── css/
│   │   └── style.css                     # Custom glassmorphic styling
│   ├── uploads/                          # Stored user uploads and generated heatmaps
│   ├── accuracy_comparison.png           # Comparative accuracy graph
│   ├── accuracy_loss_line.png            # Training loss & accuracy curves
│   ├── class_identification_chart.png    # Class recognition accuracy benchmark
│   └── model_comparison_bar.png          # Architecture comparison bar chart
│── templates/
│   ├── analytics.html                    # Model Analytics evaluation slides
│   ├── applications.html                 # Practical system positioning & use cases
│   ├── dashboard.html                    # Classification Portal interface
│   ├── docs.html                         # Full architectural system documentation
│   ├── history.html                      # Inspection History audit dashboard
│   ├── index.html                        # Main landing page
│   ├── login.html                        # Authentication page
│   ├── report.html                       # Standardized printable PDF report
│   └── viva.html                         # Technical Viva & viva voce Q&A guide
│── app.py                                # Main Flask application server & routing
│── database.py                           # SQLite schema, queries, and auth management
│── dataset_generator.py                  # Generates baseline structured sample datasets
│── explainability.py                     # Grad-CAM attention heatmap generator
│── generate_graphs.py                    # Generates benchmark evaluation charts
│── infrastructure_intelligence.py        # Domain-specific class metadata & priority logic
│── predict.py                            # Standalone command-line inference script
│── train.py                              # Model training, comparison & evaluation script
│── requirements.txt                      # Python library dependencies
│── .gitignore                            # Git exclusion rules
└── README.md                             # Comprehensive project documentation
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/swatimagadum/Ai-driven-deep-learning-for-aerial-infrastructure-classification-.git
cd Ai-driven-deep-learning-for-aerial-infrastructure-classification-
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows (PowerShell / Command Prompt)
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Project

### Start the Web Application
```bash
# Using Python
python app.py

# Or using the Python Launcher on Windows
py app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Default Login Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` |
| **Analyst** | `analyst` | `analyst123` |
| **Defense Officer** | `officer` | `officer123` |
| **Standard User** | `user` | `user123` |

---

## 🔬 CLI Training & Inference

### Train and Benchmark Models
```bash
python train.py --epochs 10
```
This trains MobileNetV2, VGG16, and DenseNet121, computes Accuracy, Precision, Recall, and F1-Score, generates comparison curves, and saves the top performer to `models/model.h5`.

### Run Standalone CLI Prediction
```bash
python predict.py --image sample_test_images/sample_commercial_airport.jpg
```

---

## 📊 Expected Output & Flow

1. **Authentication:** Secure login redirects to the main landing page.
2. **Classification Portal (`/dashboard`):** Drag and drop an aerial scan to view:
   - Primary Predicted Class
   - Confidence percentage & Top-3 distribution
   - Grad-CAM visual attention heatmap
   - Image quality assessment (Resolution, Brightness, Contrast)
   - AI Monitoring Score (0–100) and suggested monitoring priority
3. **Inspection History (`/history`):** Complete historical audit table with continuous serial numbering, search filtering, and record deletion.
4. **PDF Inspection Report (`/report/<id>`):** Concise, 2-page print-ready technical summary.
5. **Model Analytics (`/analytics`):** Interactive slide deck presenting model benchmarks and evaluation graphs.

---

## 📄 License
This project is developed for educational, academic, and research purposes.
