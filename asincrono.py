from django.db import models
from cms.models.pagemodel import Page
from cms.models.permissionmodels import PageUser
from django.contrib.auth.models import Permission, User
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from django_auth_ldap.backend import LDAPBackend

from cms import constants
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms import api
from django.utils.translation import activate

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def nuevousuario(sender,user,request,**kwargs):
	if user.username != "administrador":
		activate('en')
		if Page.objects.filter(created_by=user).count() <= 0:
            usuario=User.objects.get(username=user.username)
		    usuario.save()				
			api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)
			blog=NewsBlogConfig()
			blog.app_title=usuario.username
			blog.namespace=usuario.username
			blog.save()
			pagina=api.create_page(title=usuario.username,language='en',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,in_navigation=True,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
			api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
			pagina.publish('en')
			print("Usuario y blog creado")
		else:
			print("El usuario ya tiene una pagina y blog.")
