import requests
import json

code = """#include <stdio.h>
int main() {
    printf("Hello InvitiQ!\\n");
    printf("C is running!\\n");
    return 0;
}"""

data = {
    "code": code,
    "language": "c",
    "auto_detect": False
}

try:
    response = requests.post('http://localhost:5000/api/compile', json=data)
    result = response.json()
    
    print("=" * 50)
    print("SUCCESS:", result.get('success'))
    print("=" * 50)
    
    if 'execution' in result:
        print("\nEXECUTION STATUS:", result['execution'].get('status'))
        print("\nOUTPUT:")
        print(result['execution'].get('output', 'No output'))
        
        if result['execution'].get('errors'):
            print("\nERRORS:")
            for error in result['execution']['errors']:
                print(error)
    else:
        print("\nNo execution data")
        print(json.dumps(result, indent=2))
        
except Exception as e:
    print(f"Error: {e}")
