from fastapi import FastAPI, HTTPException, Query
import requests
import json
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile

app = FastAPI()

# Allow CORS for your React frontend hosted on http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get('/get_animal_info')
async def get_animal_info(
    query: str = Query(..., description="Query string for animal search")
):
    api_key = 'GEMINI API key'
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Provide a one-line brief summary and three interesting facts about {query}. Additionally, provide information in the following categories: Scientific name: Physical description: Habitat: Diet: Social structure: Conservation status: Behavior:."
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            print("API Response:", json.dumps(result, indent=2))  # Debugging line to see the API response
            animal_info_text = result['candidates'][0]['content']['parts'][0]['text']
            print("Animal Info Text:", animal_info_text)  # Debugging line to see the extracted text
            
            # Split the returned text into different parts
            lines = animal_info_text.split('\n')
            
            # Initialize a dictionary to store the parsed information
            animal_info = {
                "Brief summary": "",
                "Interesting facts": [],
                "Scientific name": "",
                "Physical description": "",
                "Habitat": "",
                "Diet": "",
                "Social structure": "",
                "Conservation status": "",
                "Behavior": ""
            }

            # Mapping of expected labels to corresponding keys in the dictionary
            label_mapping = {
                "Brief Summary": "Brief summary",
                "Interesting Facts": "Interesting facts",
                "Scientific Name": "Scientific name",
                "Physical Description": "Physical description",
                "Habitat": "Habitat",
                "Diet": "Diet",
                "Social Structure": "Social structure",
                "Conservation Status": "Conservation status",
                "Behavior": "Behavior"
            }

            current_key = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                label_found = False
                for label, key in label_mapping.items():
                    if label in line:
                        current_key = key
                        if key == "Interesting facts":
                            animal_info[current_key].append(line.replace(label, "").strip().lstrip(":").strip() + ". ")
                        else:
                            animal_info[current_key] += line.replace(label, "").strip().lstrip(":").strip() + ". " 
                        label_found = True
                        break
                
                if not label_found and current_key:
                    if current_key == "Interesting facts":
                        animal_info[current_key].append(f" {line.strip().lstrip('*').strip()}")
                    else:
                        animal_info[current_key] += f" {line.strip().lstrip('*').strip()}"

            
            for key in animal_info:
                if key != "Interesting facts":
                    animal_info[key] = animal_info[key].replace("*", "").strip()

            print("Parsed Animal Info:", animal_info)  # Debugging line to see the parsed dictionary

            return animal_info
        except (KeyError, IndexError) as e:
            raise HTTPException(status_code=500, detail=f"Error parsing response: {e}")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch animal information")

# Image fetching
@app.get('/get_image')
async def get_image(
    query: str = Query(..., description="Query string for image search"),
    min_width: int = Query(None, description="Minimum width of the image"),
    min_height: int = Query(None, description="Minimum height of the image"),
    max_width: int = Query(None, description="Maximum width of the image"),
    max_height: int = Query(None, description="Maximum height of the image")
):
    access_key = 'UNSPLASH API KEY'
    unsplash_api_url = f"https://api.unsplash.com/photos/random?query={query}&client_id={access_key}"

    # Make the GET request to the Unsplash API
    response = requests.get(unsplash_api_url)
    if response.status_code == 200:
        data = response.json()

        # Check if the response contains a valid image URL
        if "urls" in data:
            image_url = data["urls"]["raw"]

            # Add the min and max width and height parameters if provided
            if min_width is not None:
                image_url += f"&w={min_width}"
            if min_height is not None:
                image_url += f"&h={min_height}"
            if max_width is not None:
                image_url += f"&w={max_width}"
            if max_height is not None:
                image_url += f"&h={max_height}"

            # Fetch the image data
            image_response = requests.get(image_url)

            # Check if fetching the image was successful
            if image_response.status_code == 200:
                # Save the image content to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(image_response.content)
                    tmp_file_path = tmp_file.name

                # Return the temporary file using FileResponse
                return FileResponse(tmp_file_path, media_type="image/jpeg")

    # If no image is found or an error occurs, raise HTTPException
    raise HTTPException(status_code=404, detail="Image not found")
