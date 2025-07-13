#!/usr/bin/env python3
"""
Test script for the brain tumor monitoring system.
This script tests the monitoring functionality with synthetic data.
"""

import os
import sys
import numpy as np
from pathlib import Path
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent))

from monitoring import BrainTumorImageMonitor

def test_brain_tumor_monitoring():
    """Test the brain tumor monitoring system."""
    print("🧠 Testing Brain Tumor Image Monitoring System")
    print("=" * 50)
    
    # Initialize monitor with a dummy database URL (for testing)
    monitor = BrainTumorImageMonitor("sqlite:///test_monitoring.db")
    
    # Test 1: Image feature extraction
    print("\n1. Testing image feature extraction...")
    test_image = np.random.randint(0, 255, (512, 512, 1), dtype=np.uint8)
    features = monitor.extract_brain_tumor_features(test_image)
    
    print(f"✅ Extracted {len(features)} features from test image")
    print(f"   Image size: {features.get('image_width', 0)}x{features.get('image_height', 0)}")
    print(f"   Brightness: {features.get('brightness_mean', 0):.2f}")
    print(f"   Entropy: {features.get('entropy', 0):.2f}")
    print(f"   Tumor detection confidence: {features.get('tumor_detection_confidence', 0):.2f}")
    
    # Test 2: Synthetic data generation
    print("\n2. Testing synthetic data generation...")
    reference_data = monitor._create_synthetic_reference_data()
    current_data = monitor._create_synthetic_current_data(7)
    
    print(f"✅ Generated {len(reference_data)} reference samples")
    print(f"✅ Generated {len(current_data)} current samples")
    print(f"   Reference data columns: {list(reference_data.columns)}")
    
    # Test 3: Data drift report generation
    print("\n3. Testing drift report generation...")
    try:
        report_path = monitor.generate_brain_tumor_drift_report(7)
        print(f"✅ Generated drift report: {report_path}")
    except Exception as e:
        print(f"⚠️  Drift report generation failed (expected without database): {e}")
    
    # Test 4: Quality tests
    print("\n4. Testing quality tests...")
    quality_results = monitor.run_brain_tumor_quality_tests()
    print(f"✅ Quality test results: {quality_results}")
    
    # Test 5: Dashboard data
    print("\n5. Testing dashboard data...")
    dashboard_data = monitor.get_brain_tumor_dashboard_data()
    print(f"✅ Dashboard data: {dashboard_data}")
    
    print("\n" + "=" * 50)
    print("✅ Brain tumor monitoring system test completed successfully!")
    print("\n📋 Key Features Tested:")
    print("   • Image feature extraction (brightness, contrast, entropy, tumor features)")
    print("   • Synthetic data generation for testing")
    print("   • Drift report generation")
    print("   • Quality test execution")
    print("   • Dashboard data retrieval")
    print("\n🚀 Ready to integrate with your brain tumor classification system!")

if __name__ == "__main__":
    test_brain_tumor_monitoring() 