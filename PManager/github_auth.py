from github import Github
from PManager.models import PM_User
import requests
from django.conf import settings
from django.contrib.auth.models import User

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2


class GithubAuth:
    def get_image_to_file(self, url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib2.urlopen(url).read())
        img_temp.flush()
        return img_temp

    @staticmethod
    def get_user_info(access_token):
        gh = Github(access_token)
        user_data = gh.get_user()
        return user_data

    @staticmethod
    def get_token(code):
        URL = "https://github.com/login/oauth/access_token"
        data = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code
        }
        resp = requests.post(URL, data=data, headers = {'Accept':'application/json'})
        answer = resp.json()
        return answer
        

    def authenticate(self, **kwargs):
        code = kwargs.get("code")

        if code:
            resp = GithubAuth.get_token(code)


            if u'error' in resp:
                return None
            else:
                access_token = resp.get("access_token")
                user_data = GithubAuth.get_user_info(access_token)

                github_id = user_data.id
                profiles = PM_User.objects.filter(github_id=github_id)
                
                if profiles.exists():
                    user= profiles[0].user
                    return user
                else:
                    # CREATE THE USER If not EXIST
                    # email user perms (user:email perms needed)
                    # https://developer.github.com/v3/users/emails/
                    email = None
                    for email_dict in user_data.get_emails():
                        if email_dict.get("primary", False):
                            email = email_dict.get("email")
                            break
                    if not email:
                        return None
                    user = PM_User.getOrCreateByEmail(email, None, None, None)
                    profile = user.profile
                    profile.github = user_data.login
                    profile.github_id = user_data.id
                    profile.save()
                    user.first_name = user_data.name or 'Unknown Github User'
                    user.save()
                    img_temp = self.get_image_to_file(user_data.avatar_url)
                    profile.avatar.save("avatar_github.jpg", File(img_temp))
                    profile.save()
                    return user
                    

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None