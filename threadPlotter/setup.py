
import setuptools
from setuptools import setup, find_packages

setup(
    name='threadPlotter',
    version='0.0.1b3',
    description='a toolkit for designing plotter-compatible embroidery patterns',
    long_description="Supplementary material for the paper:Plotting with Thread:Fabricating Delicate Punch Needle Embroidery with X-Y Plotters.",
    url="http://eyesofpanda.com/projects/thread_plotter/",
    author='Shiqing Licia He',
    author_email='heslicia@umich.edu',
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Manufacturing',
        'Topic :: Adaptive Technologies',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='punch needle embroidery; plotter embroidery',
    project_urls={
        'Documentation': 'https://github.com/LiciaHe/threadPlotter',
        'Project Site': 'http://eyesofpanda.com/projects/thread_plotter/',
        'Source': 'https://github.com/LiciaHe/threadPlotter',
    },
    packages=setuptools.find_packages(),
    python_requires='~=3.6',
    install_requires=[
       'Pillow >=7.1.2',
       'pyclipper>=1.1.0.post3',
        'svgpathtools>=1.3.3',
        'bs4 >=0.0.1',
        'scipy',
        'numpy'
    ],
    data_files=[('threadCsv', ['TP_punchneedle/embroidery_thread_color.csv']),('threadColorPkl',['TP_punchneedle/threadColor.pkl']),('originalList',['TP_punchneedle/original_only.pkl'])],

)





