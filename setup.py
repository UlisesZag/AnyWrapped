import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='anywrapped',
                 packages=['anywrapped'],
                 install_requires=install_requires,
                 entry_points ='''
                 [console_scripts]
                 anywrapped=myapp.main:entry_point
                 ''')