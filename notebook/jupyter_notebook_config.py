import os
from IPython.lib import passwd

# Set Jupyter Notebook's IP & port.
c.NotebookApp.ip = '*'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False

# Set a password if PASSWORD is set in the environment
# if 'PASSWORD' in os.environ:
#     c.NotebookApp.password = passwd(os.environ['PASSWORD'])
#     del os.environ['PASSWORD']

#trmntr
#c.NotebookApp.password = u'sha1:c07a3f838766:70668d9c3ecb3ed90a08e57e4e1bfc77962958dc'
