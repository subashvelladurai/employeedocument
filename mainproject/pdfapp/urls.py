from django.urls import path
from django.conf import settings
from .views import upload_page ,fetch_documents
from django.conf.urls.static import static

urlpatterns = [
    path("upload/", upload_page, name="upload_document"),
    path("fecth_documents/", fetch_documents, name="upload_document"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)