import subprocess
import os

def test_farasa():
    # 1. Prepare test file
    test_text = "اللغة العربية جميلة"
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(test_text)

    # 2. Run Farasa command
    try:
        subprocess.run([
            "java",
            "-Dfile.encoding=UTF-8",
            "-jar",
            "FarasaSegmenterJar.jar",
            "-i", "input.txt",
            "-o", "output.txt"
        ], check=True)
        
        # 3. Read and process results
        with open("output.txt", "r", encoding="utf-8") as f:
            result = f.read().strip()
        
        print("Raw Farasa Output:", result)
        
        # 4. Clean and verify
        tokens = result.replace("+", "").split()
        print("Cleaned Tokens:", tokens)
        
        expected = ["اللغة", "العربية", "جميلة"]
        assert tokens == expected, "Test failed - output doesn't match expected"
        print("✅ Test passed! Farasa is working correctly")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists("input.txt"):
            os.remove("input.txt")
        if os.path.exists("output.txt"):
            os.remove("output.txt")

if __name__ == "__main__":
    test_farasa()