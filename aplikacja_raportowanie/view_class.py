from aplikacja_raportowanie.liblaries import *
from aplikacja_raportowanie.functions_to_view import *


class View_type():
    def __init__(self,request, posts, posts_to_do, list_of_posts_type):
        self.posts = posts
        self.posts_to_do = posts_to_do
        self.login_user = logged_user(request)
        self.users_list = list_of_users()
        self.list_of_posts_type =  list_of_posts_type
        self.years = years_list_to_now()
        self.today = str(todays_date())
        self.application_start_date = APPLICATION_START_DATE
        self.statuses_list = STATUS_CHOICES_LIST_WITH_CLOSE

    def __del__(self):
        pass

    def render_view(self,request):
        content = {
    		'posts': self.posts,
            'posts_to_do': self.posts_to_do,
    		'login_user': self.login_user,
    		'users_list': self.users_list,
    		'list_of_posts_type': self.list_of_posts_type,
    		'years': self.years,
    		'today': self.today,
    		'application_start_date': self.application_start_date,
    		'statuses_list': self.statuses_list,
            }
        return render(request, 'aplikacja_raportowanie/index.html', content)
