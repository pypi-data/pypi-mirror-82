


<p align="center" width="100%">
    <img width="80%" src="docs/images/haven_logo.png"> 
</p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Havenized Results with Jupyter
![](docs/images/table2.png)

- Haven is a library for building, managing and visualizing large-scale reproducible experiments. It helps developers establish a workflow that allows them to quickly prototype a reliable codebase. It also helps them easily  scale that codebase to one that can run, manage, and visualize thousands of experiments seamlessly. 

- The library provide a wide range of functionality including best practices for defining experiments, checkpointing, visualizing and debugging experiments, and ensuring reproducible benchmarks. 

- This library could strongly boost productivity for building great products, winning machine learning competitions, and getting research papers published. 

- The only structure required is that each experiment has the following.
    * `<savedir_base>/<exp_id>/exp_dict.json` that defines a single set of hyperparamters as a python `dict`.
    * `exp_id` is the hash of that hyperparameter python `dict`.
    * `<savedir_base>/<exp_id>/score_list.pkl` that has a list of dicts where each dict contains metrics as keys with scores as their values.


## Install
```
$ pip install --upgrade git+https://github.com/haven-ai/haven-ai
```


## Havenized Projects

- COVID19: https://www.elementai.com/news/2020/accelerating-the-creation-of-ai-models-to-combat-covid-19-with-element-ai-orkestrator?fbclid=IwAR33nO8gqq7Bf8F4NyG3WYlH3c7t7QkgPAZEru4UpP2FGzSYfHZ5nnPLKZI
- LCFCN: https://github.com/ElementAI/LCFCN
- Embedding Propagation: https://github.com/ElementAI/embedding-propagation
- Bilevel Augmentation: https://github.com/ElementAI/bilevel_augment
- SSN optimizer: https://github.com/IssamLaradji/ssn
- SLS optimizer: https://github.com/IssamLaradji/sls
- Ada SLS optimizer: https://github.com/IssamLaradji/ada_sls
- SPS optimizer: https://github.com/IssamLaradji/sps
- Fish Dataset: https://github.com/alzayats/DeepFish
- Covid Weak Supervision: https://github.com/IssamLaradji/covid19_weak_supervision

## Expected structure of a Havenized project
```
project/
├── src/
│   ├── __init__.py
│   ├── datasets.py
│   └── models.py
├── scripts/
│   ├── visualize_mnist.py
│   └── train_on_single_image.py
├── exp_configs.py
├── README.md
└── trainval.py
```

# Getting Started

## 1. Run Experiments

![](docs/images/terminal.png)

### 1.1 Run experiments sequentially for MNIST across learning rates


```
python example.py -e mnist_learning_rates -sb ../results -r 1
```

results are saved in `../results/`

### 1.2 Run experiments in a cluster using [Orkestrator](https://www.elementai.com/products/ork)

```
python example.py -e mnist_learning_rates -sb ../results -r 1 -j 1
```


## 2. Visualize Results

![](docs/images/table3.png)

### 2.1 Launch a Jupyter server

```bash
jupyter nbextension enable --py widgetsnbextension --sys-prefix
jupyter notebook
```

### 2.2 Run Jupyter script to visualize dashboard

Run the following script from a Jupyter cell to launch a dashboard.


```python
from haven import haven_jupyter as hj
from haven import haven_results as hr
from haven import haven_utils as hu

# path to where the experiments got saved
savedir_base = <insert_savedir_base>
exp_list = None

# exp_list = hu.load_py(<exp_config_name>).EXP_GROUPS[<exp_group>]
# get experiments
rm = hr.ResultManager(exp_list=exp_list, 
                      savedir_base=savedir_base, 
                      verbose=0
                     )
# launch dashboard
hj.get_dashboard(rm, vars(), wide_display=True)
```




## Contributing

We love contributions!
