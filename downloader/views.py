import os
import io
import zipfile
import requests
from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# View to search and paginate images
def search_images(request):
    images = []
    query = request.GET.get("keyword", "")
    page_number = int(request.GET.get("page", 1))
    per_page = 30

    if query:
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "client_id": UNSPLASH_KEY,
            "per_page": per_page,
            "page": page_number,
        }
        response = requests.get(url, params=params)
        data = response.json()
        images = [item["urls"]["regular"] for item in data.get("results", [])]

    context = {
        "images": images,
        "keyword": query,
        "page": page_number,
        "has_next": len(images) == per_page,
    }
    return render(request, "search.html", context)

# View to download images as a zip
def download_images(request):
    if request.method == "POST":
        urls = request.POST.getlist("image_urls")
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, url in enumerate(urls):
                try:
                    response = urlopen(url)
                    img_data = response.read()
                    img_name = f"image_{i+1}.jpg"
                    zip_file.writestr(img_name, img_data)
                except Exception as e:
                    print(f"Failed to download {url}: {e}")

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=images.zip'
        return response

    return HttpResponse("Invalid request method", status=400)
