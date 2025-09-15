from forecaster import forecast
import json

if __name__ == "__main__":
    output = forecast()
    print("\n=== Attack Path Forecast ===")
    print(json.dumps(output, indent=2))
