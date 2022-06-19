from django.urls import path
from core.api_views import TokenView, RegisterView, QuestionView

app_name = 'core'


urlpatterns = [

    path('login/', TokenView.as_view(), name='token_obtain'),
    path('login/refresh/', TokenView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('question/', QuestionView.as_view(), name='question'),

]
