from django.db import models

# Create your models here.
from django.dispatch.dispatcher import receiver
from django_facebook.models import FacebookModel
from django.db.models.signals import post_save
from django_facebook.utils import get_user_model, get_profile_model
from fbpic import settings

class MyCustomProfile(FacebookModel):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	batcam_id = models.IntegerField(null=True, blank = True)
	untameable_id = models.IntegerField(null=True, blank = True)
	trampoline_id = models.IntegerField(null=True, blank = True)

	@receiver(post_save)

	def create_profile(sender, instance, created, **kwargs):

		"""
		Create a matching profile whenever a user object is created.
		"""
		
		if sender == get_user_model():
			user = instance
			profile_model = get_profile_model()

			if profile_model == MyCustomProfile and created:
				profile, new = MyCustomProfile.objects.get_or_create(user=instance)


class BatCamPictureTag(models.Model):
	
	PICTURE_TAKEN_AT = (
		('B', 'Batcam'),
		('U', 'Untameable'),
		('T', 'Trampoline'),
	)

	CAMERA_ID = (
		
		('B1', 'Batcam'),
		('U1', 'Untameable 1'),
		('U2', 'Untameable 2'),
		('U3', 'Untameable 3'),
		('U4', 'Untameable 4'),
		('UD', 'Untameable Drone'),
		('T1', 'Trampoline 1'),
		('TD', 'Trampoline Drone'),	
		)


	complete_path = models.CharField(max_length=200)
	filename = models.CharField(max_length=30)
	batcam_id = models.CharField(max_length=10, null= True, blank = True)
	zone = models.CharField(max_length=1, choices=PICTURE_TAKEN_AT)
	timestamp_tag = models.DateField(auto_now_add=True)
	all_user_ids = models.CharField(max_length=70)
	cam_id = models.CharField(max_length=2, choices=CAMERA_ID)
	keeper = models.CharField(max_length=1, default = 'U')
	hero = models.CharField(max_length=1, default = 'U')
	posted_to_facebook = models.BooleanField()
	timestamp_facebook_post = models.DateField(auto_now=True,null=True,blank=True)
	facebook_post_id = models.CharField(null=True,blank=True)

class UserPhotoCount(models.Model):
	#userid, tagged count, posted count, keep count, hero count
	batcam_id = models.CharField(max_length=10, null= True, blank = True)
	tagged_count = models.IntegerField(default=0)
	posted_count = models.IntegerField(default=0)
	keep_count = models.IntegerField(default=0)
	hero_count = models.IntegerField(default=0)
	discard_count = models.IntegerField(default=0)
