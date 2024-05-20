from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

class BaseData (models.Model):
    code = models.CharField(
        max_length= 20,
        null = True,
        blank = True,
        verbose_name = "code",
    )
    value = models.CharField(
        max_length= 20,
        null = True,
        blank = True,
        verbose_name = "value",
    )
    type = models.CharField(
        max_length= 20,
        null = True,
        blank = True,
        verbose_name = "type",
    )
    
    def __str__(self):
        return self.value  
    

class BaseMixin(models.Model):
    id = models.BigAutoField(
        primary_key=True, 
        editable=False
        )
    created = models.DateTimeField(
        auto_now_add=True, 
        null=True, 
        verbose_name=_("Created")
    )
    last_update = models.DateTimeField(
        auto_now=True, 
        verbose_name=_("Last Update")
        )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_%(class)s",
        editable=False,
        null=True,
        blank=True,
        verbose_name=_("created_by"),
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="updated_%(class)s",
        editable=False,
        null=True,
        blank=True,
        verbose_name=_("updated_by"),
    )

    class Meta:
        abstract = True

    def created_updated(model, request):
        # obj = model.objects.latest('pk')
        obj = model
        if (obj.created_by is None) or (obj.created_by == ""):
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


def default_account():
    return Account.objects.first()


class Account(BaseMixin, models.Model):
    is_active = models.BooleanField(
        default=True, 
        unique=True, 
        verbose_name=_("is active")
    )
    name = models.CharField(
        max_length=150, 
        verbose_name=_("name")
    )
    admin_name = models.CharField(
        max_length=150, 
        null=False, 
        verbose_name=_("admin name")
    )
    admin_contact_phone = models.CharField(
        max_length=150, 
        null=False, 
        verbose_name=_("admin phone")
    )

    class Meta:
        verbose_name_plural = _("0.0 - Accounts")
        verbose_name = _("Account")

    def __str__(self):
        return self.name
    

class Company(BaseMixin, models.Model):
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_("is active")
    )
    account = models.ForeignKey(
        Account,
        default=default_account,
        on_delete=models.PROTECT,
        verbose_name=_("account"),
    )
    company_type = models.ForeignKey(
        BaseData,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="CompanyType",
        limit_choices_to={"type": "CompanyType"},
        verbose_name=_("company type"),
    )
    name = models.CharField(
        max_length=150, 
        null=False, 
        verbose_name=_("name")
    )
    tax_id = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="CNPJ/CPF or similar TAX ID for International companies",
        verbose_name=_("tax_id"),
    )
    address_line_1 = models.TextField(
        blank=True,
        null=True, 
        verbose_name=_("address_line_1")
    )
    city = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("city")
    )  # City/Town
    province = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("province")
    )  # State/Province/Region
    zipcode = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("zipcode")
    )
    country = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name=_("country")
    )
    # Phone
    company_contact_name = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name=_("contact name")
    )
    company_contact_phone = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name=_("contact phone")
    )

    class Meta:
        verbose_name_plural = _("1.0 - Companies")
        verbose_name = _("Company")

    def __str__(self):
        return self.name
    

class Box(BaseMixin, models.Model):
    status = models.ForeignKey(
        null = True,
        blank = True,
        limit_choices_to={"type": "statusBox"},
        verbose_name = "Status",
    )
    code = models.PositiveIntegerField(
        null = True,
        unique=True,
        blank = True,
        help_text = "Texto explicativo do campo",
        verbose_name = "Record",
    )
    local = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=True,
        related_name="Company",
        verbose_name=_("Company"),
    )    

    def __str__(self):
        return self.code