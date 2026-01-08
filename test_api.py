"""
Simple test client for Infrastructure Inspection API.
Demonstrates how to use the API programmatically.
"""

import requests
import json
from pathlib import Path


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    response = requests.get("http://localhost:8000/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_inspection(image_path: str):
    """
    Test the inspection endpoint with an image.

    Args:
        image_path: Path to the image file to inspect
    """
    print(f"Testing inspection with image: {image_path}")

    if not Path(image_path).exists():
        print(f"Error: Image not found at {image_path}")
        return

    # Prepare the file
    with open(image_path, "rb") as f:
        files = {"file": (Path(image_path).name, f, "image/jpeg")}

        # Make request
        response = requests.post(
            "http://localhost:8000/api/inspect",
            files=files
        )

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 60)
        print("INSPECTION REPORT")
        print("=" * 60)
        print(f"\nStatus: {result['status']}")
        print(f"Total Defects: {result['total_defects']}")
        print(f"Summary: {result['summary']}\n")

        if result['detections']:
            for i, detection in enumerate(result['detections'], 1):
                print(f"\n--- Defect {i} ---")
                print(f"Type: {detection['defect_type'].upper()}")
                print(f"Severity: {detection['severity']}")
                print(f"Confidence: {detection['confidence']:.2%}")
                print(f"Location: ({detection['bounding_box']['x1']:.0f}, {detection['bounding_box']['y1']:.0f}) to "
                      f"({detection['bounding_box']['x2']:.0f}, {detection['bounding_box']['y2']:.0f})")
                print(f"\nAnalysis: {detection['explanation']}")
                print(f"\nRecommended Action: {detection['recommended_action']}")
        print("\n" + "=" * 60)
    else:
        print(f"Error: {response.text}")


def main():
    """Main test function."""
    print("\n" + "=" * 60)
    print("Infrastructure Inspection API Test Client")
    print("=" * 60 + "\n")

    # Test 1: Health check
    test_health_check()

    # Test 2: Inspection (you need to provide an image path)
    # Uncomment and modify the path to test with a real image
    # test_inspection("data/sample_crack.jpg")

    print("\nTo test image inspection, uncomment the test_inspection() call")
    print("and provide a path to an infrastructure image.\n")


if __name__ == "__main__":
    main()
