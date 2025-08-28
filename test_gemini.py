# test_full_gemini_response.py
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyDusCQl7hUDCo_hxc3gIJYAXkXmwidgvzY")
model = genai.GenerativeModel('gemini-1.5-flash')

def test_full_response():
    try:
        response = model.generate_content("Draft a comprehensive mutual NDA between TechCorp Inc. and DataSolutions LLC, effective January 1, 2024, governed by California law.")
        
        print("✅ SUCCESS: Full Gemini Response")
        print("=" * 60)
        print(f"Total Characters: {len(response.text)}")
        print(f"Total Words: {len(response.text.split())}")
        print("=" * 60)
        print("FULL CONTRACT TEXT:")
        print(response.text)  # Shows the COMPLETE response
        print("=" * 60)
        
        return response.text
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

# Run the test to see full response
full_contract = test_full_response()
