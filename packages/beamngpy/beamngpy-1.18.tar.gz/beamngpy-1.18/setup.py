import sys
from setuptools import setup


def setup_package():
    entry_points = {
        'console_scripts': [
            'beamngpy = beamngpy.main:cli'
        ]
    }

    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(setup_requires=['pyscaffold'] + sphinx,
          entry_points=entry_points, include_package_data=True,
          use_pyscaffold=True)


if __name__ == "__main__":
    setup_package()
