# SIMBA Python API

The Simba Python Module (aesim.simba) is a Python package that contains hundreds of functions providing direct access to SIMBA such as creating a circuit, modifying parameters, running a simulation, and retrieving results. _pysimba_ is independant and does not recquire to have SIMBA installed to be used.

## Installation

`pip install aesim.simba`

## Requirements

This version of _aesim.simba_ is only compatible with Windows.

## Activation
The deployment key available in your [account profile page](https://www.simba.io/profile_account/) must be used to activate aesim.simba.

### Using Environment Variable

The easiest way to activate pysimba is to set the environement variable `SIMBA_DEPLOYMENT_KEY` value to your deployment key. 

### Code-based Activation

The _License_ API can be also used to activate _aesim.simba_.

``` python
from aesim.simba import License
License.Activate('*** YOUR DEPLOYMENT KEY ***')
```

## API Documentation
The API documentation is avaible on our [website](https://www.simba.io/doc/). 

## Example

The following example opens the Flyback Converter Example available in SIMBA, runs it, and plots the output voltage.

```
#%% Load modules...
import matplotlib.pyplot as plt
from aesim.simba import ProjectRepository

#%% Load project
project = ProjectRepository.CreateDesignExamplesRepository()
flybackConverter = project.GetDesignByName('DC/DC - Flyback Converter')

#%% Get the result object and solve the system
job = flybackConverter.TransientAnalysis.NewJob()
status = job.Run()

#%% Get results
t = job.TimePoints
Vout = job.GetSignalByName('R2 - Instantaneous Voltage').DataPoints

#%% Plot Curve
fig, ax = plt.subplots()
ax.set_title(flybackConverter.Name)
ax.set_ylabel('Vout (V)')
ax.set_xlabel('time (s)')
ax.plot(t,Vout)
```

## Public Beta
SIMBA is currently in public beta and can be **used by everyone for free**. The objective of this public beta is to gather feedback from users. Feel free to use our [public GitHub project](https://github.com/aesim-tech/simba-project) to check and contribute to our roadmap.

Copyright (c) 2019-2020 AESIM.tech