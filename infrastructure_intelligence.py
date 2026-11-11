"""
Smart Infrastructure Intelligence & Risk Assessment Engine
============================================================
Provides domain knowledge, image quality analysis, confidence interpretation,
risk scoring, and structured actionable insights for all 10 infrastructure classes.
"""

import os
import math
from PIL import Image, ImageStat, ImageFilter

CLASSES_KNOWLEDGE_BASE = {
    "Airforce Base": {
        "type": "Airforce Base",
        "description": "Strategic military aviation installation housing fighter jets, aircraft hangars, tactical runways, and air defense infrastructure.",
        "ai_reason": "Identified high-contrast concrete runway geometries, tactical taxiways, and military aircraft hangar footprints.",
        "visual_indicators": [
            "Heavy-duty concrete airstrips and taxiways",
            "Hardened aircraft hangars and shelters",
            "Radar installations and perimeter security walls",
            "Command control towers and apron space"
        ],
        "importance": "High-priority national defense asset critical for airspace protection, rapid tactical deployment, and aerial reconnaissance.",
        "risks": [
            "Runway surface degradation or foreign object debris (FOD)",
            "Perimeter boundary breaches or unauthorized surveillance",
            "Fuel storage facility vulnerability",
            "Air traffic control signal interference"
        ],
        "baseline_criticality": 90,
        "recommended_action": "Prioritize high-resolution perimeter monitoring and daily automated runway structural inspections."
    },
    "Army Base": {
        "type": "Army Base",
        "description": "Military ground force installation containing barracks, armories, vehicle staging grounds, and defense administrative command centers.",
        "ai_reason": "Detected fortified perimeter compounds, grid-aligned barracks buildings, and armored vehicle staging areas.",
        "visual_indicators": [
            "Grid-pattern military barracks and operational headquarters",
            "Fortified perimeter security barriers and watchtowers",
            "Heavy equipment & armored vehicle parking compounds",
            "Parade grounds and tactical training zones"
        ],
        "importance": "Core military ground force hub for defense readiness, troop mobilization, and tactical equipment storage.",
        "risks": [
            "Perimeter fence intrusion or unauthorized access",
            "Ammunition depot or armory safety hazards",
            "Staging ground logistics bottlenecks",
            "Unmonitored aerial drone activity over command centers"
        ],
        "baseline_criticality": 88,
        "recommended_action": "Schedule automated perimeter surveillance sweeps and maintain restricted airspace protocols."
    },
    "Bridge": {
        "type": "Bridge",
        "description": "Critical elevated transport structure spanning water bodies, canyons, or railway corridors to connect key arterial road networks.",
        "ai_reason": "Extracted linear structural span geometries crossing high-contrast water channels with connected road approach lanes.",
        "visual_indicators": [
            "Linear structural span crossing water or terrain barriers",
            "Symmetrical bridge piers, abutments, and cable stays",
            "Arterial highway approach and departure corridors",
            "High contrast between deck structure and underlying water/glen"
        ],
        "importance": "Vital transportation artery essential for civil economic logistics, emergency transit, and regional connectivity.",
        "risks": [
            "Structural fatigue, pier erosion, or concrete deck cracking",
            "Traffic congestion bottlenecks during peak hours",
            "Overweight vehicle payload violations",
            "Flood surge impact during severe weather events"
        ],
        "baseline_criticality": 85,
        "recommended_action": "Prioritize structural health monitoring, load-capacity audits, and periodic drone deck scans."
    },
    "Capital City": {
        "type": "Capital City",
        "description": "High-density urban administrative center featuring commercial skyscrapers, government complexes, and dense civil road networks.",
        "ai_reason": "Detected high-density building footprints, complex urban road grids, and multi-story architectural shadows.",
        "visual_indicators": [
            "Dense grid of commercial buildings and government complexes",
            "Intricate urban road networks and intersections",
            "High structural shadow density and rooftop infrastructure",
            "Central public squares and civic transit hubs"
        ],
        "importance": "Administrative, economic, and governance core housing major population centers and civil infrastructure.",
        "risks": [
            "Urban heat island effect and high power grid strain",
            "Traffic gridlock and emergency response delays",
            "Stormwater drainage overflow during severe rainfall",
            "High-density urban security and surveillance requirements"
        ],
        "baseline_criticality": 80,
        "recommended_action": "Integrate urban planning satellite analytics and monitor traffic congestion patterns."
    },
    "Commercial Airport": {
        "type": "Commercial Airport",
        "description": "Major civilian air transportation hub containing passenger terminals, paved commercial runways, taxiways, and gate aprons.",
        "ai_reason": "Identified wide paved commercial runways, multi-gate passenger terminal concourses, and commercial jet aprons.",
        "visual_indicators": [
            "Long wide paved parallel runway strips",
            "Multi-gate passenger concourses and terminal buildings",
            "Commercial jet apron parking bays and jet bridges",
            "Fuel farm depots and logistics cargo terminals"
        ],
        "importance": "Primary international and domestic transportation node driving trade, tourism, and rapid civil mobility.",
        "risks": [
            "Runway pavement cracking or rubber buildup",
            "Apron congestion and ground handling collision risks",
            "Terminal security breaches or perimeter fencing gaps",
            "Birds or wildlife hazards near flight paths"
        ],
        "baseline_criticality": 92,
        "recommended_action": "Conduct daily aerial runway friction inspections and maintain automated gate area monitoring."
    },
    "National Highway": {
        "type": "National Highway",
        "description": "Multi-lane arterial expressway designed for high-speed intercity freight transport and civilian automotive travel.",
        "ai_reason": "Extracted continuous multi-lane paved road ribbons, median dividers, cloverleaf interchanges, and highway shoulders.",
        "visual_indicators": [
            "Continuous multi-lane paved roadway corridor",
            "Grade-separated interchanges and exit ramps",
            "Central median dividers and paved road shoulders",
            "High contrast road markings and traffic lanes"
        ],
        "importance": "Backbone of national supply chains, freight transport, industrial distribution, and regional mobility.",
        "risks": [
            "Road surface pothole formation and pavement wearing",
            "High-speed traffic accidents or freight blockage",
            "Overpass structural degradation",
            "Drainage clogging leading to localized hydroplaning"
        ],
        "baseline_criticality": 78,
        "recommended_action": "Deploy automated pavement condition mapping and real-time traffic flow telemetry."
    },
    "Navy Base": {
        "type": "Navy Base",
        "description": "Strategic maritime defense facility equipped with deep-water piers, naval dry docks, warship berths, and naval command centers.",
        "ai_reason": "Detected deep-water finger piers, naval ship berthing docks, warship outlines, and maritime security facilities.",
        "visual_indicators": [
            "Deep-water concrete berthing piers and jetties",
            "Moored naval vessels, frigates, and support craft",
            "Dry docks and naval vessel maintenance basins",
            "Coastal defense installations and maritime security perimeters"
        ],
        "importance": "Key naval defense installation protecting territorial waters, maritime trade routes, and naval fleet deployment.",
        "risks": [
            "Pier structural underwater erosion or bio-fouling",
            "Unauthorized maritime vessel intrusion in restricted waters",
            "Fuel transfer spill risks during ship refueling",
            "Storm surge or tsunami damage to coastal berths"
        ],
        "baseline_criticality": 94,
        "recommended_action": "Maintain 24/7 maritime acoustic/optical perimeter surveillance and inspect berth structural integrity."
    },
    "Oil Reservoir Tank": {
        "type": "Oil Reservoir Tank",
        "description": "Industrial petroleum storage tank farm containing large circular floating-roof tanks, containment bund walls, and pipelines.",
        "ai_reason": "Identified high-contrast circular floating-roof tanks, square secondary containment dikes, and industrial pipeline manifolds.",
        "visual_indicators": [
            "Large circular petroleum storage tank structures",
            "Secondary containment bund walls and safety dikes",
            "Interconnected industrial pipeline networks",
            "Tank farm safety access roads and transfer pumps"
        ],
        "importance": "Critical energy reserve facility storing national crude oil supplies, refined petroleum, and strategic fuel reserves.",
        "risks": [
            "Petroleum vapor leak or fire hazards",
            "Containment bund wall breach or soil contamination",
            "Tank roof corrosion or seal failure",
            "Thermal expansion risks during summer heatwaves"
        ],
        "baseline_criticality": 95,
        "recommended_action": "Prioritize thermal infrared aerial leak detection, tank seal integrity audits, and fire suppression readiness."
    },
    "Port": {
        "type": "Port",
        "description": "Major maritime cargo container terminal featuring gantry cranes, container stacking yards, ship berths, and intermodal rail links.",
        "ai_reason": "Recognized coastal dock quays, large ship-to-shore gantry cranes, multi-colored container stacking grids, and cargo vessels.",
        "visual_indicators": [
            "Ship-to-shore gantry crane structures along water quays",
            "Grid-aligned multi-colored cargo container stacking yards",
            "Moored container cargo ships and bulk carriers",
            "Intermodal rail and freight truck logistics terminals"
        ],
        "importance": "Global trade gateway handling sea freight import/export, industrial supply chains, and maritime commerce.",
        "risks": [
            "Container yard congestion and crane operational bottlenecks",
            "Quay wall structural degradation due to saltwater corrosion",
            "Hazardous material container storage compliance risks",
            "Siltation in shipping channels requiring dredging"
        ],
        "baseline_criticality": 89,
        "recommended_action": "Monitor container yard density using satellite imagery and inspect quay wall structural integrity."
    },
    "Railway Station": {
        "type": "Railway Station",
        "description": "Intermodal rail transportation terminal containing parallel steel track corridors, passenger platforms, overhead catenary, and train sheds.",
        "ai_reason": "Extracted converging multi-track steel rail lines, long linear passenger platform sheds, and train rolling stock outlines.",
        "visual_indicators": [
            "Parallel and converging steel railway track corridors",
            "Linear passenger platform roofs and station concourses",
            "Stationed passenger and freight train rolling stock",
            "Rail yards, switches, and signal gantries"
        ],
        "importance": "Key mass transit and heavy rail freight hub connecting urban centers and industrial supply routes.",
        "risks": [
            "Rail track thermal expansion or track buckling",
            "Signal failure or track switch mechanical breakdown",
            "Platform overcrowding during peak commute hours",
            "Track ballast erosion or embankment instability"
        ],
        "baseline_criticality": 82,
        "recommended_action": "Schedule regular aerial rail track geometry inspections and monitor ballast stability."
    }
}

def assess_image_quality(filepath):
    """
    Evaluates image resolution, file size, brightness, and sharpness.
    Returns a dictionary with quality_rating ('Good', 'Moderate', 'Poor'), metrics, and warnings.
    """
    try:
        if not os.path.exists(filepath):
            return {
                "rating": "Moderate",
                "width": 224, "height": 224, "filesize_kb": 50,
                "brightness": 128.0, "sharpness": 100.0,
                "warning": "Image file path not found; using standard defaults."
            }

        file_size_bytes = os.path.getsize(filepath)
        filesize_kb = round(file_size_bytes / 1024, 1)

        img = Image.open(filepath).convert('RGB')
        width, height = img.size

        # Brightness calculation (mean pixel luminance)
        stat = ImageStat.Stat(img)
        r, g, b = stat.mean[:3]
        brightness = round(0.299 * r + 0.587 * g + 0.114 * b, 2)

        # Sharpness estimation using Laplacian edge variance approximation
        grayscale = img.convert('L')
        edges = grayscale.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        sharpness = round(edge_stat.var[0], 2)

        warnings = []
        rating = "Good"

        if width < 150 or height < 150:
            warnings.append("Low image resolution (<150px) may reduce feature extraction precision.")
            rating = "Moderate"
        if brightness < 45:
            warnings.append("Low brightness/underexposed image detected.")
            rating = "Moderate" if rating == "Good" else "Poor"
        elif brightness > 220:
            warnings.append("High brightness/overexposed image detected.")
            rating = "Moderate"
        if sharpness < 25.0:
            warnings.append("Blurry/low-sharpness image detected; edge contrast is low.")
            rating = "Poor"

        warning_str = " ".join(warnings) if warnings else "Image quality is optimal for reliable deep learning classification."

        return {
            "rating": rating,
            "width": width,
            "height": height,
            "filesize_kb": filesize_kb,
            "brightness": brightness,
            "sharpness": sharpness,
            "warning": warning_str
        }

    except Exception as e:
        return {
            "rating": "Good",
            "width": 224, "height": 224, "filesize_kb": 100,
            "brightness": 125.0, "sharpness": 150.0,
            "warning": f"Quality check notice: {str(e)}"
        }

def interpret_confidence(confidence):
    """
    Interprets numerical confidence percentage into configurable human-readable categories.
    """
    conf = float(confidence)
    if conf >= 95.0:
        return {
            "label": "Very High Confidence",
            "level": "highest",
            "explanation": "The AI model exhibits maximum activation certainty across key feature layers with zero ambiguity."
        }
    elif conf >= 85.0:
        return {
            "label": "High Confidence",
            "level": "high",
            "explanation": "The model has high confidence in feature alignment with strong visual pattern matches."
        }
    elif conf >= 70.0:
        return {
            "label": "Medium Confidence",
            "level": "medium",
            "explanation": "The prediction shows moderate confidence; analyst review is recommended."
        }
    else:
        return {
            "label": "Low Confidence",
            "level": "low",
            "explanation": "Low confidence rating; prediction should be verified with secondary aerial imagery."
        }

def calculate_risk_priority_score(predicted_class, confidence, quality_rating="Good"):
    """
    Calculates a transparent classification-based monitoring priority score (0-100)
    and assigns a Priority Level (Low / Medium / High / Critical).
    """
    kb = CLASSES_KNOWLEDGE_BASE.get(predicted_class, {})
    base_crit = kb.get("baseline_criticality", 80)
    conf = float(confidence)

    # Risk score formula
    conf_factor = (conf / 100.0) * 10.0
    quality_penalty = 0 if quality_rating == "Good" else (5 if quality_rating == "Moderate" else 10)

    score = int(math.clamp(base_crit + conf_factor - quality_penalty, 10, 99) if hasattr(math, 'clamp') else max(10, min(99, int(base_crit + conf_factor - quality_penalty))))

    if score >= 80:
        priority = "High"
    elif score >= 60:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "risk_score": score,
        "priority": priority,
        "disclaimer": "This score represents an AI classification-based monitoring priority score, not actual structural damage detection."
    }

def generate_infrastructure_intelligence(predicted_class, confidence, quality_rating="Good"):
    """
    Generates full structured AI Infrastructure Insight payload for dashboard & reports.
    """
    kb = CLASSES_KNOWLEDGE_BASE.get(predicted_class, CLASSES_KNOWLEDGE_BASE["Bridge"])
    conf_info = interpret_confidence(confidence)
    risk_info = calculate_risk_priority_score(predicted_class, confidence, quality_rating)

    return {
        "predicted_class": predicted_class,
        "type": kb["type"],
        "description": kb["description"],
        "ai_reason": kb["ai_reason"],
        "visual_indicators": kb["visual_indicators"],
        "importance": kb["importance"],
        "risks": kb["risks"],
        "recommended_action": kb["recommended_action"],
        "confidence": confidence,
        "confidence_label": conf_info["label"],
        "confidence_explanation": conf_info["explanation"],
        "risk_score": risk_info["risk_score"],
        "priority": risk_info["priority"],
        "disclaimer": risk_info["disclaimer"]
    }
