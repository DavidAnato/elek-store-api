from rest_framework import generics
from rest_framework.response import Response
from .serializers import ConversationSerializer
from .chatbot import get_chatbot_response

class ChatBotAPIView(generics.CreateAPIView):
    serializer_class = ConversationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data.get('message')
        conversation = request.session.get('conversation', [])

        # Define the preprompt for the chatbot assistant
        preprompt ="Tu es un chatbot spécialement conçu pour améliorer l'expérience des utilisateurs sur Elek-Store, la marketplace en question. Ton rôle principal consiste à fournir une assistance individualisée aux utilisateurs en répondant à leurs questions et en leur recommandant des produits qui correspondent à leurs besoins spécifiques et à leurs préférences sur Elek-Store."

        # Get chatbot response including the preprompt
        chatbot_response = get_chatbot_response(user_message, conversation, preprompt)  

        serializer.save(user=request.user, response=chatbot_response)
        return Response({'response': chatbot_response})
