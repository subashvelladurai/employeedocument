import os
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mainproject import settings
from .models import Document


@csrf_exempt
def upload_page(request):
    if request.method == "GET":
        return render(request, "upload.html")

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception:
        return JsonResponse({"error": "Could not read file"}, status=400)
    df.rename(columns={
        "title": "title_name",
        "description": "description_name",
        "pdf": "pdf_name",
    }, inplace=True)

    mandatory_columns = ["title_name", "description_name", "pdf_name"]
    df[mandatory_columns] = df[mandatory_columns].replace("", pd.NA)
    df["missing_fields"] = df[mandatory_columns].isnull().any(axis=1)

    valid_df = df[~df["missing_fields"]]
    invalid_df = df[df["missing_fields"]]

    document_list = []
    missing_pdfs = []

    for _, row in valid_df.iterrows():
        pdf_filename = row["pdf_name"]
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
        if os.path.exists(full_path):
            document_list.append(Document(
                title=row["title_name"],
                description=row["description_name"],
                pdf_file=os.path.join( pdf_filename),
                status=1,
            ))
        else:
            missing_pdfs.append(pdf_filename)

    try:
        Document.objects.bulk_create(document_list)
    except Exception as e:
        return JsonResponse({"error": "Database error", "detail": str(e)}, status=500)

    return JsonResponse({
        "status": "success",
        "uploaded": len(document_list),
        "invalid_rows": int(df["missing_fields"].sum()),
        "missing_pdfs": missing_pdfs,
    })

@csrf_exempt
def fetch_documents(request):
    docs = list(Document.objects.filter(status=1).values(
        "id", "title", "description", "pdf_file"
    ))
    for doc in docs:
        doc["pdf_url"] = request.build_absolute_uri(
            settings.MEDIA_URL + doc["pdf_file"]
        )
    return render(request, "fetch_template.html", {"documents": docs})