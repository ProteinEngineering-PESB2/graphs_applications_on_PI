### Configure Rosetta for the tesis

#### Install Rosetta

1. **Requirements**
* Python3

2. **Download Rosetta**
* Go to [Rosetta](https://www.rosettacommons.org/software/license-and-download)
* Click in *Academic Download*
* **User**: Academic_User **Password**: Xry3x4
* Click in *Download Rosetta 3.13*
* Download *Rosetta 3.13 source - as one bundle (5.2G)* 

3. **Install Packages**

* *apt install zlib1g-dev*
* *apt install scons*
* *apt install build-essential*

4. **Install Rosetta**

* Go to the folder where you downloaded rosetta
* *tar -xvzf rosetta[releasenumber].tar.gz*
* *cd rosetta*/main/source*
* *./scons.py mode=release bin*.
* Check the a *bin* folder was created

#### Configure Script

1. **Requirements**
* Anaconda
* Git

2. **Clone repository**
* *git clone https://github.com/ClaudioGuevara/rosetta.git*

3. **Create Virtual Environment**
* *conda create --name rosetta python=3.8.12*
* *conda activate rosetta*

4. **Install Dependencies**
* *conda install -c anaconda pymongo*
* *conda install -c anaconda pandas*
* *conda install -c schrodinger pymol-bundle*
* *conda install -c conda-forge pdbfixer*
* *conda install -c conda-forge dnspython*
* *conda install -c conda-forge biopython*

5. **Run Script**
* *python3 main.py*