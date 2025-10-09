When a second user signs in, they get this error. Investigate how the project works, consult online documentation/other websites if necessary, and suggest a fix

Environment:


Request Method: GET
Request URL: http://127.0.0.1:8000/accounts/google/login/callback/?state=IWk6ABfpJ4ygsZAZ&code=4%2F0AVGzR1AxKLe4-WMLpXiZyhJEMOCYuKZRRXrPoXOk0ZCyg4M2ZSxVJnxApVtP5fbBPbkQFQ&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+openid&authuser=1&prompt=consent

Django Version: 5.2.7
Python Version: 3.13.6
Installed Applications:
['django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django.contrib.sites',
 'allauth',
 'allauth.account',
 'allauth.socialaccount',
 'allauth.socialaccount.providers.google',
 'django_app']
Installed Middleware:
['django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',
 'allauth.account.middleware.AccountMiddleware']



Traceback (most recent call last):
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/sqlite3/base.py", line 360, in execute
    return super().execute(query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above exception (UNIQUE constraint failed: auth_user.username) was the direct cause of the following exception:
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/providers/oauth2/views.py", line 102, in view
    return self.dispatch(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/providers/oauth2/views.py", line 151, in dispatch
    return complete_social_login(request, login)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/helpers.py", line 67, in complete_social_login
    return flows.login.complete_login(request, sociallogin)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/internal/flows/login.py", line 53, in complete_login
    return _authenticate(request, sociallogin)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/internal/flows/login.py", line 80, in _authenticate
    ret = process_signup(request, sociallogin)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/internal/flows/signup.py", line 124, in process_signup
    get_adapter().save_user(request, sociallogin, form=None)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/adapter.py", line 106, in save_user
    sociallogin.save(request)
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/allauth/socialaccount/models.py", line 306, in save
    user.save()
    ^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/contrib/auth/base_user.py", line 65, in save
    super().save(*args, **kwargs)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/base.py", line 902, in save
    self.save_base(
    ^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/base.py", line 1008, in save_base
    updated = self._save_table(
              
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/base.py", line 1169, in _save_table
    results = self._do_insert(
              
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/base.py", line 1210, in _do_insert
    return manager._insert(
           
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/query.py", line 1868, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/models/sql/compiler.py", line 1882, in execute_sql
    cursor.execute(sql, params)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/utils.py", line 122, in execute
    return super().execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/abreslav/codespeak/releases/0.0.1-alpha/uv1-todo-0/.venv/lib/python3.13/site-packages/django/db/backends/sqlite3/base.py", line 360, in execute
    return super().execute(query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Exception Type: IntegrityError at /accounts/google/login/callback/
Exception Value: UNIQUE constraint failed: auth_user.username
