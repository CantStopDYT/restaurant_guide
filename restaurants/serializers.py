from rest_framework import serializers

from restaurants.models import *


class DietaryOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DietaryOptions
        fields = ['dietary_options']

    def to_representation(self, instance):
        return instance.get_dietary_options_display()

    def to_internal_value(self, data):
        for dietary_option in DietaryOptions.DietaryOptions:
            if dietary_option.label == data:
                return dietary_option


class PickupOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PickupOptions
        fields = ['pickup_options']

    def to_representation(self, instance):
        return instance.get_pickup_options_display()

    def to_internal_value(self, data):
        for pickup_option in PickupOptions.PickupOptions:
            if pickup_option.label == data:
                return pickup_option


class DeliveryOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryOptions
        fields = ['delivery_options']

    def to_representation(self, instance):
        return instance.get_delivery_options_display()

    def to_internal_value(self, data):
        for delivery_method in DeliveryOptions.DeliveryMethods:
            if delivery_method.label == data:
                return delivery_method


class OrderMethodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderMethods
        fields = ['order_methods']

    def to_representation(self, instance):
        return instance.get_order_methods_display()

    def to_internal_value(self, data):
        for order_method in OrderMethods.OrderMethods:
            if order_method.label == data:
                return order_method


class OpeningHoursSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpeningHours
        fields = ['weekday', 'from_hour', 'to_hour']


class LocationSerializer(serializers.ModelSerializer):
    hours = OpeningHoursSerializer(many=True)

    class Meta:
        model = Location
        fields = ['street_address', 'city', 'zipcode', 'phone_number', 'hours']


class RestaurantSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    order_methods = OrderMethodsSerializer(many=True)
    delivery_options = DeliveryOptionsSerializer(many=True)
    pickup_options = PickupOptionsSerializer(many=True)
    dietary_options = DietaryOptionsSerializer(many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Restaurant
        fields = ['name', 'status', 'website_url', 'menu_url',
                  'locations', 'order_methods', 'delivery_options',
                  'pickup_options', 'dietary_options']

    def create(self, validated_data):
        locations = validated_data.pop('locations')
        order_methods = validated_data.pop('order_methods')
        delivery_options = validated_data.pop('delivery_options')
        pickup_options = validated_data.pop('pickup_options')
        dietary_options = validated_data.pop('dietary_options')

        restaurant = Restaurant.objects.create(
            name=validated_data['name'],
            status=validated_data['get_status_display'],
            website_url=validated_data['website_url'],
            menu_url=validated_data['menu_url'],
        )

        for location in locations:
            hours = location.pop('hours')
            loc = Location.objects.create(
                restaurant=restaurant,
                street_address=location['street_address'],
                city=location['city'],
                zipcode=location['zipcode'],
                phone_number=location['phone_number']
            )
            # TODO: populate hours at each location

        for order_method in order_methods:
            OrderMethods.objects.create(
                order_methods=order_method,
                restaurant=restaurant
            )

        for delivery_option in delivery_options:
            DeliveryOptions.objects.create(
                delivery_options=delivery_option,
                restaurant=restaurant
            )

        for pickup_option in pickup_options:
            PickupOptions.objects.create(
                pickup_options=pickup_option,
                restaurant=restaurant
            )

        for dietary_option in dietary_options:
            DietaryOptions.objects.create(
                dietary_options=dietary_option,
                restaurant=restaurant
            )

        return restaurant