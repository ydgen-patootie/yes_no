from rest_framework import generics, status
from .models import Question
from .serializers import TokenSerializer, RegisterSerializer, QuestionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .services import AnswerFromYesno


class TokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class QuestionView(generics.CreateAPIView):
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = self.request.user
        self.perform_create(serializer)

        answer = AnswerFromYesno(serializer.instance)
        answer.get_answer()
        answer_text = answer.answer_text
        answer.save_answer()
        if answer.success:
            headers = self.get_success_headers(serializer.data)
            return Response({'answer': answer_text}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': f'Request to yesno failed'}, status=status.HTTP_400_BAD_REQUEST)
