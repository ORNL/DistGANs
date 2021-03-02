# DistGANs
Distributed computed training fo Generative Adversarial Neural Networks

This is a code implemented in collaboration with:

- Massimiliano Lupo Pasini at Oak Ridge National Laboratory (lupopasinim@ornl.gov)
- Vittorio Gabbi at Politecnico di Milano (vittorio.gabbi@mail.polimi.it)
- Vitaliy Starchenko at Oak Ridge National Laboratory (starchenkov@ornl.gov)
- Andrey Prokpenko at Oak Ridge National Laboratory (prokopenkoav@ornl.gov)

## Code style

To keep similar code style, it should be formatted using [black](https://github.com/psf/black):

```
black -S -l 79 {source_file_or_directory}
```

## Quick start conda setup
```
conda create --name {env_name} python=3.7
conda install -n {env_name} matplotlib docopt ipython mpi4py
conda install -n {env_name} -c anaconda pyyaml
conda install -n {env_name} pytorch torchvision -c pytorch
conda install -n {env_name} tensorboardx -c conda-forge
```

Optional, if NVIDIA gpu is present:
```
pip install pycuda
```

## Models

All models should be located in `GANs_dir`. The class and the file that contains the class should have identic name. For example, class:
```
class CNN_model(GANs_abstract_object.GANs_model):
    ...
```
File:
```
CNN_model.py
```
