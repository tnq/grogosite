from django.contrib.auth.backends import RemoteUserBackend

class TNQRemoteUserBackend(RemoteUserBackend):
    create_unknown_user = False