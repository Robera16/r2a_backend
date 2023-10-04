from django.shortcuts import render
from .serializers import AdminTicketSerializer, SupportTicketSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .pagination import TicketPagination
from rest_framework.permissions import IsAuthenticated
from .models import AdminTicket, SupportTicket
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404

class MyAdminRequests(ListAPIView):
    permission_classes = ([IsAuthenticated, ] )
    pagination_class = TicketPagination
    serializer_class = AdminTicketSerializer

    def get_queryset(self):
        return AdminTicket.objects.filter(user=self.request.user).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin_ticket(request):
    ticket_data = request.data
    ticket_data['user'] = request.user.id
    serialize = AdminTicketSerializer(data=ticket_data)
    if serialize.is_valid(raise_exception=True):
        serialize.save()
        return Response({"status": "ok", "msg": "created Sucessfully", "data": serialize.data }, status=status.HTTP_200_OK)
    return Response({"status": "bad", "msg": "Problem Creating", "data": serialize.data }, status=status.HTTP_412_PRECONDITION_FAILED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_admin_ticket(request, pk):
    request = get_object_or_404(AdminTicket.objects.all(), pk=pk)
    request.delete()
    return Response({"status": "ok", "msg": "Ticket Deleted", "data": ""}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin_ticket(request, pk):
    ticket_data = get_object_or_404(AdminTicket.objects.all(), pk=pk)
    serializer = AdminTicketSerializer(ticket_data)
    return Response({"status": "ok", "msg": "Ticket Data", "data": serializer.data}, status=status.HTTP_200_OK)

