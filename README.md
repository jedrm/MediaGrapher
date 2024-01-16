# MediaGrapher

Open-source command-line interface program to convert images and videos into Matplotlib graph. Uses Canny edge detection algorithm and Potrace edge detection to graph Bezier curves on Matplotlib graph.

## Setup

**NOTE**: This program only works for Python 3.10 and above.

### Install system dependencies

Ubuntu

```bash
sudo apt update
sudo apt install git python3-dev python3-pip build-essential libagg-dev libpotrace-dev pkg-config
```

CentOS/RedHat

```bash
sudo yum -y groupinstall "Development Tools"
sudo yum -y install agg-devel potrace-devel python-devel
```

OSX

```bash
brew install libagg pkg-config potrace
```

For Windows instructions, please follow the instructions listed for Windows under [pypotrace](https://pypi.org/project/pypotrace/).

### Install project dependencies

UNIX

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Windows

```bash
virtualenv --python C:\Path\To\Python\python.exe env
.\env\Scripts\activate
pip install -r requirements.txt
```

## Running the Program

Run the program using the following command:

```bash
python mediagrapher.py
```

Use the `-h` or `--help` flag to get a detailed description of the options:

```bash
python mediagrapher.py --help
```

Output:

```bash
usage: MediaGrapher [-h] [-o OUTPUT] [-a {Canny,Sobel}] [-t LOW HIGH] url

Command-line interface for graphing images and videos.

positional arguments:
  url                   URL of the image.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name.
  -a {Canny,Sobel}, --algorithm {Canny,Sobel}
                        Edge detection algorithm.
  -t LOW HIGH, --thresholds LOW HIGH
                        Thresholds for the Canny edge detection algorithm. (default: 30, 200)
```

## Credits

This project is heavily influenced by the following ![GitHub repository](https://github.com/kevinjycui/DesmosBezierRenderer).
