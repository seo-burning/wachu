from django.db import models
from django.contrib.auth import get_user_model

from utils.helper.model.abstract_model import TimeStampedModel, \
    ActiveModel
# Create your models here.


# to        	iOS & Android	string | string[]       	An Expo push token or an array of Expo push tokens specifying the recipient(s) of this message.
# data      	iOS & Android	Object                  	A JSON object delivered to your app.
#                                                           It may be up to about 4KiB; the total notification payload sent to Apple
#                                                           and Google must be at most 4KiB or else you will get a "Message Too Big" error.
# title	        iOS & Android	string                    	The title to display in the notification. Often displayed above the notification body
# body	        iOS & Android	string                     	The message to display in the notification.
# ttl	        iOS & Android	number                  	Time to Live: the number of seconds for which the message may be kept around for redelivery
#                                                           if it hasn't been delivered yet. Defaults to undefined in order to use the respective
#                                                            defaults of each provider (0 for iOS/APNs and 2419200 (4 weeks) for Android/FCM).
# expiration	iOS & Android	number	                    Timestamp since the UNIX epoch specifying when the message expires.
#                                                           Same effect as ttl (ttl takes precedence over expiration).
# priority  	iOS & Android	'default'/'normal'/'high'	The delivery priority of the message. Specify "default"
#                                                           or omit this field to use the default priority on each platform
#                                                           ("normal" on Android and "high" on iOS).
# subtitle	    iOS Only	    string	                    The subtitle to display in the notification below the title.
# sound     	iOS Only	    'default' | null	        Play a sound when the recipient receives this notification. Specify "default"
#                                                           to play the device's default notification sound, or omit this field to play no sound.
# badge	        iOS Only	    number	                    Number to display in the badge on the app icon. Specify zero to clear the badge.
# channelId	    Android Only	string	                    ID of the Notification Channel through which to display this notification.
#                                                           If an ID is specified but the corresponding channel does not exist on the device
#                                                           (i.e. has not yet been created by your app), the notification will not be displayed to the user.

PRIORITY_CHOICES = [('default', 'default'), ('normal', 'normal'), ('high', 'high')]

SOUND_CHOICES = [('default', 'default'), ('null', None), ]


class PushNotification(TimeStampedModel,
                       ActiveModel):
    user_scope = models.CharField(max_length=1000,
                                  default='ALL')
    title = models.CharField(max_length=100, )
    body = models.CharField(max_length=200,)
    data = models.CharField(max_length=1000, blank=True)
    ttl = models.IntegerField(blank=True, null=True)
    expiration = models.IntegerField(blank=True, null=True)
    priority = models.CharField(max_length=10,
                                choices=PRIORITY_CHOICES,
                                default='default')
    subtitle = models.CharField(max_length=100, blank=True)
    sound = models.CharField(max_length=20,
                             default='default',
                             null=True,
                             choices=SOUND_CHOICES)
    badge = models.IntegerField(default=1)
    channel_id = models.CharField(max_length=100, blank=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    thumb_image = models.ImageField(
        blank=True, null=True, upload_to='notification/%Y/%m')


class UserNotification(TimeStampedModel,
                       ActiveModel):
    publish_date = models.DateTimeField(blank=True, null=True)
    notification = models.ForeignKey(PushNotification, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    is_read = models.BooleanField(default=True)
