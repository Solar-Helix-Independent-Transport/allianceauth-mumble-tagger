from django.dispatch import receiver

from django.db.models.signals import pre_save, m2m_changed
from allianceauth.groupmanagement.models import GroupRequest
from allianceauth.authentication.models import UserProfile, CharacterOwnership, EveCharacter
from allianceauth.eveonline.evelinks.eveimageserver import  type_icon_url, character_portrait_url
from allianceauth.services.hooks import NameFormatter
from allianceauth.services.modules.mumble.auth_hooks import MumbleService
from django.db import transaction

from .models import TagAssociation
from django.contrib.auth.models import User

from .app_settings import mumble_active

from allianceauth.services.hooks import get_extension_logger
logger = get_extension_logger(__name__)

if mumble_active():
    from allianceauth.services.modules.mumble.models import MumbleUser
    
    def update_name(mu_instance: MumbleUser):
        try:
            logger.debug("New / updated mumble tags for %s" % mu_instance.user.profile.main_character)
            groups = mu_instance.user.groups.all()
            tags = []
            for ta in TagAssociation.objects.filter(enabled=True):
                for ta_g in ta.groups.all():
                    if ta_g in groups:
                        tags.append(ta.tag)
                        break
            if len(tags) > 0:
                old_display_name = NameFormatter(MumbleService(), mu_instance.user).format_name()
                new_display_name = "{} {}".format(old_display_name,
                                                " ".join(tags))
                logger.debug("updated display name from `{}` to `{}`".format(old_display_name, new_display_name))
                mu_instance.display_name = new_display_name
        except Exception as e:
            logger.error(e, exc_info=1)
            pass  # shits fucked... Don't worry about it...

    @receiver(pre_save, sender=MumbleUser)
    def mumble_user_presave(sender, instance: MumbleUser, **kwargs):
        instance = update_name(instance)

    @receiver(m2m_changed, sender=User.groups.through)
    def m2m_changed_user_groups(sender, instance, action, *args, **kwargs):

        def trigger_tag_update():
            if hasattr(instance, 'mumble'):
                if instance.mumble is not None:
                    mu_instance = instance.mumble
                    update_name(mu_instance)
                    signal_args = {
                        'signal': pre_save,
                        'receiver': mumble_user_presave,
                        'sender': MumbleUser, 
                    }
                    with temp_disconnect_signal(**signal_args):
                        mu_instance.save()

        if instance.pk and (action == "post_add" or action == "post_remove" or action == "post_clear"):
            logger.debug("Waiting for commit to trigger service group update for %s" % instance)
            transaction.on_commit(trigger_tag_update)


class temp_disconnect_signal():
    """ Temporarily disconnect a model from a signal """
    def __init__(self, signal, receiver, sender, dispatch_uid=None):
        self.signal = signal
        self.receiver = receiver
        self.sender = sender
        self.dispatch_uid = dispatch_uid

    def __enter__(self):
        self.signal.disconnect(
            receiver=self.receiver,
            sender=self.sender,
            dispatch_uid=self.dispatch_uid,
        )

    def __exit__(self, type, value, traceback):
        self.signal.connect(
            receiver=self.receiver,
            sender=self.sender,
            dispatch_uid=self.dispatch_uid,
            weak=False
        )
