from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json


class OAuthService(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    client_id = models.CharField(max_length=64, null=False, blank=False)
    client_secret = models.CharField(max_length=1024, null=False, blank=False)
    authorization_uri = models.URLField(null=False, blank=False)
    token_uri = models.URLField(null=False, blank=False)
    resource_uri = models.URLField(null=False, blank=False)
    redirect_uri = models.URLField(null=False, blank=False)
    revoke_uri = models.URLField(null=False, blank=False)
    scope = models.CharField(max_length=64, null=False, blank=False)

    def __unicode__(self):
        return 'OAuth Service {}, Auth URL: {}'.format(self.name, self.authorization_uri)


class OAuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(OAuthService, on_delete=models.CASCADE)
    token_json = models.TextField()

    @property
    def token_dict(self):
        return json.loads(self.token_json)

    @token_dict.setter
    def token_dict(self, value):
        self.token_json = json.dumps(value)

    class Meta:
        unique_together = [
            ('user', 'service'),     # User may only have one token here per service
            ('service', 'token_json'),   # Token+service unique ensures only one user per token/service pair
        ]
        # But we must allow user+token to be the same when the service is different


class OAuthState(models.Model):
    state = models.CharField(max_length=64, null=False, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=200, blank=True)


class DukeDSAPIToken(models.Model):
    """
    A token for a user that can be used for authentication with Duke DS
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.TextField(unique=True, blank=False, null=False) # Opaque here, but JWT in practice


class GroupManagerConnection(models.Model):
    """
    Settings used to check users GroupManager groups (this is a singleton object)
    """
    base_url = models.CharField(max_length=255, null=False, blank=False,
                                default="https://groups.oit.duke.edu/grouper-ws/servicesRest/json/v2_1_500",
                                help_text="base grouper url")
    account_id = models.IntegerField(null=False, blank=False,
                                     help_text="duke unique id to use to connect to grouper")
    password = models.CharField(max_length=255, null=False, blank=False,
                                help_text="password associated with account_id")


class DDSEndpoint(models.Model):
    """
    References a Duke Data Service instance as well as the agent key we're using
    """
    name = models.CharField(max_length=255, unique=True)
    agent_key = models.CharField(max_length=32, unique=True)
    # Formerly url in DukeDSSettings
    api_root = models.URLField(help_text="Base API URL for data service instance, "
                                         "e.g. https://api.dataservice.duke.edu/api/v1")
    portal_root = models.URLField("Base Web URL for data service isntance, "
                                  "e.g. https://dataservice.duke.edu")
    openid_provider_service_id = models.CharField(max_length=64,
                                                  help_text="The Service ID of the OpenID provider registered "
                                                  "with data service, required for GET /user/api_token")
    openid_provider_id = models.CharField(max_length=64,
                                          help_text='The ID of the OpenID provider registered '
                                                    'with data service, used for auth provider affiliate lookups')
    is_default = models.BooleanField(default=False,
                                     help_text='Set this to the default DDSEndpoint. There can be only one default')

    def save(self, *args, **kwargs):
        default_queryset = DDSEndpoint.objects.filter(is_default=True)
        default_count = default_queryset.count()
        if self not in default_queryset and self.is_default:
            # This is a new object or the field is changing
            default_count = default_count + 1
        if default_count > 1:
            raise ValidationError('Attempting to save default a DDSEndpoint, for a total of {}. There should be 1'.format(default_count))
        else:
            super(DDSEndpoint, self).save(*args, **kwargs)

    @classmethod
    def default_endpoint(cls):
        return cls.objects.get(is_default=True)

    def make_default(self):
        for endpoint in DDSEndpoint.objects.all():
            endpoint.is_default = False
            endpoint.save()
        self.is_default = True
        self.save()

    def __unicode__(self):
        return '{} - {}'.format(self.name, self.api_root, )


class DDSUserCredential(models.Model):
    """
    Contains Duke Data Service credentials for a django user
    """
    endpoint = models.ForeignKey(DDSEndpoint, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    token = models.CharField(max_length=32, unique=True)
    dds_id = models.CharField(max_length=255, unique=True)

    class Meta:
        unique_together = ('endpoint', 'user',)

    def __unicode__(self):
        return '{} - {}'.format(self.endpoint, self.user, )

