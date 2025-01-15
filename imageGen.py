
# Python code example for downloading an image
# For more details, visit: https://github.com/pollinations/pollinations/blob/master/APIDOCS.md

import requests

def download_image(image_url):
    # Fetching the image from the URL
    response = requests.get(image_url)
    # Writing the content to a file named 'image.jpg'
    with open('image.jpg', 'wb') as file:
        file.write(response.content)
    # Logging completion message
    print('Download Completed')

# Image details
prompt = 'A close-up, softly lit image of cedarwood branches and essen...'
width = 1200
height = 628
seed = 42 # Each seed generates a new image variation
model = 'flux' # Using 'flux' as default if model is not provided

image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"

download_image(image_url)


# Using the pollinations pypi package

## pip install pollinations

import pollinations as ai

model_obj = ai.Model()
image = model_obj.baseModel(
    prompt=f'A close-up, softly lit image of cedarwood branches and essen...',
    width=1200,
    height=628,
    seed=42
)
image.save('image-output.jpg')

print(image.url)
