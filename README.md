# Docker Image for OpenPose

A docker build file for CMU openpose with Python API support.

Credits: https://hub.docker.com/r/cwaffles/openpose

## Disclaimer
The openpose repo was adjusted to successfully build it. The models that need to be downloaded aren't hosted anymore, so i uploaded them myself on dropbox. It is important that the download link has dl=1 at the end, so it directly downloads the file. The dropbox download link simply needs to be put in CMakeLists.txt like this:
```bash
download_model("BODY_25" ${DOWNLOAD_BODY_25_MODEL} https://www.dropbox.com/scl/fi/pfl1nonefgd2r3w42e2ij/pose_iter_584000.caffemodel?rlkey=hnj53tdg47d4fzgm9fz967tnb&st=n58uhf5p&dl=1
  78287B57CF85FA89C03F1393D368E5B7) # Body (BODY_25)
```
and in models/getModels.sh like this:
```bash
BODY_25_FOLDER=${POSE_FOLDER}"body_25/"
BODY_25_MODEL="https://www.dropbox.com/scl/fi/pfl1nonefgd2r3w42e2ij/pose_iter_584000.caffemodel?rlkey=hnj53tdg47d4fzgm9fz967tnb&st=n58uhf5p&dl=1"
BODY_25_FILENAME="pose_iter_584000.caffemodel"
mkdir -p ${BODY_25_FOLDER}
wget -c ${BODY_25_MODEL} -O ${BODY_25_FOLDER}${BODY_25_FILENAME}
```

## Requirements

- https://docs.nvidia.com/cuda/wsl-user-guide/index.html
- https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

## Getting started

### Clone the repo

```bash
git clone https://github.com/bypschroeder/openpose_docker.git
```

### Build the image using dockerfile
```bash
cd ./openpose_docker
sudo docker build -t openpose .
```

### Start docker env

```bash
sudo docker run --gpus all --name openpose -it openpose_v1:latest /bin/bash
```

### Build python openpose
```bash
cd /openpose/build/python/openpose
make install
```

### Setup env for pyopenpose
```bash
cd /openpose/build/python/openpose
cp ./pyopenpose.cpython-38-x86_64-linux-gnu.so /usr/local/lib/python3.8/dist-packages
cd /usr/local/lib/python3.8/dist-packages
ln -s pyopenpose.cpython-38-x86_64-linux-gnu.so pyopenpose
export LD_LIBRARY_PATH=/openpose/build/python/openpose
```

To test if pyopenpose works simply do:
```bash
python3
>>> import pyopenpose as op
```
If there is no error shown the pyopenpose has successfully been setup.

### Download models
```bash
cd /openpose/models
bash getModels.sh
```

### Run examples
```bash
cd /openpose/examples/tutorial_api_python
python3 01_body_from_image.py
```