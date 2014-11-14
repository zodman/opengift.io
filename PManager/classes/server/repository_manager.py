__author__ = 'Tonakai'
import subprocess
class RepositoryManager(object):
	
	#remove key table and remove from projects
	def delete_user(user):
		pass

	#delete project from repository
	def delete_project(project):
		pass

	#create new project - add all users from project to repo
	#grant_access
	def add_project(project):
		pass

	#add user to project 
	#regenerate config
	def grant_access(user, project):
		pass

	#remove user from project
	#regenerate config
	def revoke_access(user, project):
		pass

	#this is where config is generated
	def generate_config():
		pass

	#add key to a user
	def add_key(user, key):
		pass

	#remove key from user
	def remove_key(user, key):
		pass