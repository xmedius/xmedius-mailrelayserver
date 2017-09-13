from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    user_options = install.user_options + [
        ('noservice', None, None),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.noservice = None

    def finalize_options(self):
        install.finalize_options(self)

    def run(self):
        install.run(self)
        if not self.noservice:
            from xmediusmailrelayserver import console
            console.install_service(['--startup', 'auto', 'install'])

setup(
    name='xmediusmailrelayserver',
    version='1.0.0',
    description='The Python module to be used to relay mail to different servers depending on patterns',
    long_description='See https://github.com/xmedius/xmedius-mailrelayserver for more information',
    url='https://github.com/xmedius/xmedius-mailrelayserver/',
    author='XMedius R&D',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Microsoft :: Windows'
    ],
    cmdclass={
        'install': PostInstallCommand
    },
    packages=['xmediusmailrelayserver'],
    package_data={'xmediusmailrelayserver': ['config.yml']},
    install_requires=['pyyaml', 'aiosmtpd'],
    dependency_links=[]
)

