from cms.models.pagemodel import Page
from cms.models.permissionmodels import PageUser
from django.contrib.auth.models import Permission, User
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from django_auth_ldap.backend import LDAPBackend

from django.core.management.base import BaseCommand, CommandError

from cms import constants
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms import api
from django.utils.translation import activate

class Command(BaseCommand):
	
	def add_arguments(self, parser):
		parser.add_argument('user',type=str)
		 
	def handle(self, *args, **options):
		activate('en')
		user=options['user']
		usuario=LDAPBackend().populate_user(user)
		if usuario is None:
			self.stdout.write(self.style.SUCCESS('Usuario no existe'))
		else:				
			if Page.objects.filter(created_by=user).count() <= 0:
				api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)

				blog=NewsBlogConfig()
				blog.app_title=usuario.username
				blog.namespace=usuario.username
				blog.save()

				pagina=api.create_page(title=usuario.username,language='en',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,in_navigation=True,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
				api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
				pagina.publish('en')
				self.stdout.write(self.style.SUCCESS('Usuario y blog creado'))
			else:
				self.stdout.write(self.style.SUCCESS('El usuario ya tiene su página y su blog'))
