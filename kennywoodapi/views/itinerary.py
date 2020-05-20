from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction, Itinerary, Customer


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction')
        depth = 2


class Itineraries(ViewSet):

    def create(self, request):

        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        attraction = Attraction.objects.get(pk=request.data['attraction_id'])
        new_itinerary_item.attraction = attraction
        customer = Customer.objects.get(user=request.auth.user)
        new_itinerary_item.customer = customer
        new_itinerary_item.save()

        serializer = ItinerarySerializer(
            new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(
                itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        itinerary_item = Itinerary.objects.get(pk=pk)
        itinerary_item.starttime = request.data["starttime"]
        attraction = Attraction.objects.get(pk=request.data['attraction_id'])
        itinerary_item.attraction = attraction
        customer = Customer.objects.get(user=request.auth.user)
        itinerary_item.customer = customer
        itinerary_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            itinerary_item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        itinerary_items = Itinerary.objects.all()
        serializer = ItinerarySerializer(
            itinerary_items,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)