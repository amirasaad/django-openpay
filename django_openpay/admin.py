from django.contrib import admin
from . import models, ugettext
from .utils import get_customer_model

CustomerModel = get_customer_model()


# Register your models here.
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    model = models.Address
    list_display = ('line1', 'line2', 'line3', 'city', 'state',
                    'country_code', 'postal_code')

    def get_readonly_fields(self, request, obj=None):
        return models.Address.get_readonly_fields(obj)


@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    model = CustomerModel
    list_display = ('openpay_id', 'first_name', 'last_name', 'email',
                    'phone_number', 'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Customer.get_readonly_fields(obj)


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    model = models.Card
    list_display = ('openpay_id', 'alias', 'holder', 'customer',
                    'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Card.get_readonly_fields(obj)


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    model = models.Plan
    list_display = ('openpay_id', 'name', 'amount', 'repeat_every',
                    'repeat_unit', 'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Plan.get_readonly_fields(obj)


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = models.Subscription
    list_display = ('openpay_id', 'customer', 'plan', 'card', 'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Subscription.get_readonly_fields(obj)


@admin.register(models.Refund)
class RefundAdmin(admin.ModelAdmin):
    model = models.Refund
    list_display = ('openpay_id', 'customer', 'charge', 'amount',
                    'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Refund.get_readonly_fields(obj)


@admin.register(models.Charge)
class ChargeAdmin(admin.ModelAdmin):
    model = models.Charge
    actions = ['capture', 'refund']
    list_display = ('openpay_id', 'customer', 'card', 'amount',
                    'creation_date')

    def capture(self, request, queryset):
        captured = 0
        for charge in queryset:
            charge.capture_charge()
            captured = captured + 1
        if captured == 1:
            message_bit = "1 charge was"
        else:
            message_bit = "%s charges were" % captured
        self.message_user(
            request,
            "%s successfully captured." % message_bit
        )
    capture.short_description = ugettext('Capture selected charges')

    def refund(self, request, queryset):
        refunded = 0
        for charge in queryset:
            charge.refund_charge()
            refunded = refunded + 1
        if refunded == 1:
            message_bit = "1 charge was"
        else:
            message_bit = "%s charges were" % refunded
            self.message_user(
                request,
                "%s successfully refunded." % message_bit
            )
    refund.short_description = ugettext('Refund selected charges')

    def get_readonly_fields(self, request, obj=None):
        return models.Charge.get_readonly_fields(obj)
