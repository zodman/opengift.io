__author__ = 'Tonakai'

import os
import os.path
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from git import *

from tracker import settings

class GitoliteManager(object):
	KEYDIR = 'keydir'
	CONF_FILE = 'conf/gitolite.conf'
	fs = FileSystemStorage(location=settings.GITOLITE_ADMIN_REPOSITORY)

# key management
	@classmethod
	def add_key_to_user(cls, user, name, data):
		file_path = cls.get_key_file(name, user)
		if(cls.is_key_exists(file_path)):
			return False
		file_path = cls.fs.save(file_path, ContentFile(data))
		repo = Repo(settings.GITOLITE_ADMIN_REPOSITORY)
		index = repo.index
		index.add([file_path,])
		message = "Added key %s for %s" % (name, user.username)
		index.commit(message)
		repo.remotes.origin.push()
		return file_path

	@classmethod
	def remove_key_from_user(cls, key, user):
		if(not cls.is_key_exists(key.file_path)):
			return False
		cls.fs.delete(key.file_path)
		repo = Repo(settings.GITOLITE_ADMIN_REPOSITORY)
		index = repo.index
		index.add([key.file_path,])
		message = "Removed key %s for %s" % (key.name, user.username)
		index.commit(message)
		repo.remotes.origin.push()
		return True

	@classmethod
	def get_key_file(cls, name, user):
		return "%s/%s@%s.pub" % (cls.KEYDIR, user.username, name)

	@staticmethod
	def is_key_exists(keyfile):
		return os.path.isfile(keyfile)


# project creation
# project deletion
# user add
# user remove
# user delete
# user create
# git log