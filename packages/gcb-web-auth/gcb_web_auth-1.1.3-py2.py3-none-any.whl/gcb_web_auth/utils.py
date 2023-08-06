from __future__ import print_function
import requests
from ddsc.core.ddsapi import ContentType
from ddsc.config import Config
from requests_oauthlib import OAuth2Session
from gcb_web_auth.models import OAuthToken, OAuthService, DukeDSAPIToken, DDSEndpoint
from jwt import decode, InvalidTokenError
from django.core.exceptions import ObjectDoesNotExist
from gcb_web_auth.exceptions import *
import logging

logger = logging.getLogger(__name__)


def get_default_dds_endpoint():
    """
    Get the default DDSEndpoint object, or raise DDSConfigurationException
    if none found
    :return: A DDSEndpoint object
    """
    try:
        endpoint = DDSEndpoint.default_endpoint()
    except DDSEndpoint.DoesNotExist:
        raise DDSConfigurationException('No DDSEndpoint is configured')
    return endpoint


def get_default_oauth_service():
    """
    Get the default OAuthService object, or raise OAuthConfigurationException
    if none found
    :return: An OAuthService object
    """
    service = OAuthService.objects.first()
    if not service:
        raise OAuthConfigurationException('No OAuthService is configured')
    return service


def check_jwt_token(token):
    """
    Uses PyJWT to parse and verify the token expiration
    :param token: A JWT token to check
    :return: The decoded token, or raises if invalid/expired
    """
    # jwt.decode will verify the expiration date of the token
    # We won't have the secret so we can't verify the signature, but we should verify everything else
    return decode(token, options={'verify_signature': False})


def make_oauth_session(oauth_service):
    return OAuth2Session(oauth_service.client_id,
                         redirect_uri=oauth_service.redirect_uri,
                         scope=oauth_service.scope.split())


def make_refreshing_oauth_session(oauth_service, user):
    extra = { # Extra arguments required by refresh
        'client_id': oauth_service.client_id,
        'client_secret': oauth_service.client_secret,
    }

    def token_saver(updated_token):
        save_token(oauth_service, updated_token, user)
    token = OAuthToken.objects.get(user=user, service=oauth_service)
    client = OAuth2Session(client_id=oauth_service.client_id,
                           token=token.token_dict,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=oauth_service.token_uri,
                           token_updater=token_saver
                           )
    return client


def authorization_url(oauth_service):
    oauth = make_oauth_session(oauth_service)
    return oauth.authorization_url(oauth_service.authorization_uri) # url, state


def get_token_dict(oauth_service, authorization_response):
    """
    :param oauth_service: An OAuthService model object
    :param authorization_response: the full URL containing code and state parameters
    :return: A token dictionary, containing access_token and refresh_token
    """
    oauth = make_oauth_session(oauth_service)
    # Use code or authorization_response
    if oauth_service.token_uri[-1] == '/':
        logger.warn("Token URI '{}' ends with '/', this has been a problem with Duke OAuth".format(oauth_service.token_uri))

    token = oauth.fetch_token(oauth_service.token_uri,
                              authorization_response=authorization_response,
                              client_secret=oauth_service.client_secret)
    return token


def current_user_details(oauth_service, user):
    """
    A simple method to make an OAuth request to the user details endpoint, that will automatically refresh the token
    :param oauth_service: An OAuthService model object
    :param user: a django model user
    :return:
    """
    session = make_refreshing_oauth_session(oauth_service, user)
    return fetch_user_details(oauth_service, session)


def user_details_from_token(oauth_service, token_dict):
    """
    Fetches user details from the oauth_service's resource URI, using only a token dict
    :param oauth_service: An OAuthService model object
    :param token_dict: a dict containing the access_token
    :return:
    """
    session = make_oauth_session(oauth_service)
    session.token = token_dict
    return fetch_user_details(oauth_service, session)


def fetch_user_details(oauth_service, session):
    response = session.post(oauth_service.resource_uri)
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise OAuthException(e)


def save_token(oauth_service, token_dict, user):
    # If we already have an OAuthToken for this user, update it
    token, created = OAuthToken.objects.get_or_create(user=user,
                                                      service=oauth_service)
    token.token_dict = token_dict
    token.save()
    return token


def revoke_token(token):
    """
    Revokes a token using it's service's revoke_uri and the refresh_token
    :param token: an OAuthToken object
    :return: JSON response of the revoke status
    """
    service = token.service
    auth = (service.client_id, service.client_secret,)
    # Revoking the refresh token will revoke its parents too
    data = {'token': token.token_dict.get('refresh_token')}
    response = requests.post(service.revoke_uri, auth=auth, data=data)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise OAuthException(e)


def get_oauth_token(user):
    """
    Gets the OAuth token object for the specified user, and refreshes if needed
    :param user:
    :return:
    """
    service = get_default_oauth_service()
    try:
        current_user_details(service, user)
    except OAuthException as e:
        raise NoTokenException(e)
    return OAuthToken.objects.get(user=user, service=service)


def get_local_dds_token(user):
    """
    Gets a user's DukeDSAPIToken object if they have one
    :param user: A django user
    :return: The DukeDSAPIToken for the user, or None if invalid or not present
    """
    # If user has an existing token, check to see if it's valid
    try:
        for token in DukeDSAPIToken.objects.filter(user=user):
            checked = check_jwt_token(token.key)
            if checked:
                return token
    except InvalidTokenError:
        token.delete()

    return None

def get_dds_token_from_oauth(oauth_token):
    """
    Presents an OAuth token to DukeDS, obtaining an api_token
    :param oauth_token: An OAuthToken object
    :return: The dictionary from JSON returned by the /user/api_token endpoint
    """
    endpoint = get_default_dds_endpoint()
    authentication_service_id = endpoint.openid_provider_service_id
    headers = {
        'Content-Type': ContentType.json,
    }
    access_token = oauth_token.token_dict.get('access_token')

    data = {
        "access_token": access_token,
        "authentication_service_id": authentication_service_id,
    }
    url = endpoint.api_root + "/user/api_token"
    response = requests.get(url, headers=headers, params=data)
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise NoTokenException(e)


def get_dds_token(user):
    """
    Returns a DukeDS api_token for the specified user, provided one can be found locally or obtained from DukeDS via OAuth.
    Raises NoTokenException on error
    :param user: A django user
    :return: A DukeDSAPI token object
    """
    dds_token = get_local_dds_token(user)
    if dds_token:
        return dds_token
    # No local token, now get from OAuth
    oauth_token = get_oauth_token(user)
    dds_token_json = get_dds_token_from_oauth(oauth_token)
    dds_token = save_dukeds_token(user, dds_token_json['api_token'])
    return dds_token


def get_local_user(token):
    """
    Given a token, find a user that matches it
    :param token: An API token to search for in the local store
    :return: A DukeDSAPIToken object if one found, otherwise
    """
    try:
        local_token = get_local_token(token)
        return local_token.user
    except ObjectDoesNotExist as e:
        return None


def get_local_token(token):
    """
    Given a JWT token, get the corresponding DukeDSAPIToken object, may raise ObjectDoesNotExist
    :param token: a token string
    :return: A DukeDSAPIToken object
    """
    return DukeDSAPIToken.objects.get(key=token)


def make_auth_config(token):
    """
    Returns a DukeDS config object populated with URL and such
    from this application's django settings
    :param token: The authorization token for DukeDS
    :return: a ddsc.config.Config
    """
    config = Config()
    endpoint = get_default_dds_endpoint()
    config.update_properties({
        Config.URL: endpoint.api_root,
    })
    config.values[Config.AUTH] = token
    return config


def save_dukeds_token(user, token):
    """
    Saves a DukeDSAPIToken object containing the provided token for the specified user
    :param user: A django User
    :param token: the token text to save
    :return: The newly created token
    """
    remove_invalid_dukeds_tokens(user)
    return DukeDSAPIToken.objects.create(user=user, key=token)


def remove_invalid_dukeds_tokens(user):
    """
    Examines a user's DukeDSAPITokens, removing any that are invalid JWTs (e.g. expired)
    :param user: a django User
    :return: None
    """
    for token in DukeDSAPIToken.objects.filter(user=user):
        try:
            check_jwt_token(token.key)
        except InvalidTokenError as e:
            token.delete()


def create_config_for_endpoint(endpoint_cred):
    """
    Given a dds endpoint create ddsclient Config object filling in agent key and api root.
    The returned config still requires user_key or auth to be filled in.
    :param endpoint_cred: DDSEndpoint: endpoint to create agent and api root config
    :return: ddsc.config.Config: settings to use with ddsclient
    """
    config = Config()
    config.update_properties({'agent_key': endpoint_cred.agent_key})
    config.update_properties({'url': endpoint_cred.api_root})
    return config


def get_dds_config_for_credentials(user_cred):
    """
    Given a DukeDS user credential object create complete Config for use with ddsc
    :param user_cred: DDSUserCredential: user credential to create config based upon
    :return: ddsc.config.Config: settings to use with ddsclient
    """
    config = create_config_for_endpoint(user_cred.endpoint)
    config.update_properties({'user_key': user_cred.token})
    return config


def main():
    duke_service = get_default_oauth_service()
    auth_url, state = authorization_url(duke_service)
    print('Please go to {} and authorize access'.format(auth_url))
    authorization_response = raw_input('Enter the full callback URL: ')
    token = get_token_dict(duke_service, authorization_response)
    print('Token: {}'.format(token))
    user_details = user_details_from_token(duke_service, token)
    print(user_details)

if __name__ == '__main__':
    main()

