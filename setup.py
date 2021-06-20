with open('requirements.txt', 'r') as f_reqs:
    requirements = f_reqs.read().split('\n')

# setup(
#     name='course_manager',
#     packages=find_packages(),
#     version='0.1',
#     install_requires=requirements,
#     entry_points={
#         'console_scripts': ['project = project.main:main']
#     },
# )

setup(name='course_manager',
      version='1.0',
      description='A course management app built with Flask',
      url='https://github.com/SEG-Group-3/CourseManagerApi',
      packages=requirements,
      )
