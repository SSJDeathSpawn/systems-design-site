from cx_Freeze import setup, Executable

# Include the name of all folder or files in your project folder that are nessesary for the project excluding your main flask file.
# If there are multiple files, you can add them into a folder and then specify the folder name.

includefiles = ['templates', 'static', 'codes', 'libs', 'utils']
includes = ['jinja2', 'jinja2.ext']
excludes = []

setup(
 name='Code Generator',
 version='0.1',
 description='For your DSD needs.',
 options={'build_exe': {'excludes': excludes, 'include_files': includefiles, 'includes': includes}},
 executables=[Executable('main.py')]
)
