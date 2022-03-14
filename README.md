
<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Ice Analog Spectra Generator</h3>
  <p align="center">
  The provided scripts generate amorphous solids and manage Gaussian16 density functional theory (DFT) optimization and excited state calculations.
    <br />
    <a href="https://github.com/Awallace3/ice_analog_spectra_generator/issues">Report Bug</a>
    ·
    <a href="https://github.com/Awallace3/ice_analog_spectra_generator/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### Built With

* [Python3](https://www.python.org/)




<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

You will need to install [Python3](https://www.python.org/downloads/).
While earlier versions of python might work, the codebase has been tested for version 3.10.1.
* Python3
  ```sh
  python3 --version
  ```

Check the requirements.txt file for the versions of the dependencies.
A virtual environment is recommended for installing these dependencies
and to ensure that the scripts execute correctly.

<!-- USAGE EXAMPLES -->
## Usage

The intent of this codebase is to enable users to generate amorphous solid
datasets with ease. Therefore, the primary user interface will be through the
input.json file with an example below. Change the parameters to meet your
needs. Note that the '[]' designates arrays while '{}' designates objects.

```sh
{
  "buildGeoms": {
    "enable": false,
    "jobList": [
      {
        "dataPath": "data/test",
        "inputCartesianFiles": [
          { "file": "mon_h2o.xyz", "count": 1 },
          { "file": "mon_nh3.xyz", "count": 0 }
        ],
        "clusters": 5,
        "boxLength": 3,
        "boxGrowth": {
          "enable": true,
          "increment": 3
        },
        "minDistanceMolecules": 2,
        "optMethod": "B3LYP",
        "optBasisSet": "6-31G(d)",
        "memComFile": "1600",
        "memPBSFile": "10",
        "startNum": 1
      },
      {
        "dataPath": "data/test2",
        "inputCartesianFiles": [
          { "file": "mon_h2o.xyz", "count": 0 },
          { "file": "mon_nh3.xyz", "count": 1 }
        ],
        "clusters": 5,
        "boxLength": 3,
        "boxGrowth": {
          "enable": true,
          "increment": 3
        },
        "minDistanceMolecules": 2,
        "optMethod": "B3LYP",
        "optBasisSet": "6-31G(d)",
        "memComFile": "1600",
        "memPBSFile": "10",
        "startNum": 1
      }
    ]
  },
  "qmgr": {
    "enable": { "exc": false, "vib": false},
    "options": {
      "minDelay": 1,
      "maxResub": 1000,
      "maxQueue": 200,
      "cluster": "map"
    },
    "jobList": [
      {
        "dataPath": "data/test",
        "outName": "t1",
        "optResub": {
          "optMethod": "B3LYP",
          "optBasisSet": "6-31G(d)",
          "memComFile": "1600",
          "memPBSFile": "10"
        },
        "excList": [
          {
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-311G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "nStates": 25,
            "SCRF": ""
          }
        ],
        "vibList": [
          {
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-31G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "SCRF": ""
          }
        ]
      },
      {
        "dataPath": "data/test2",
        "outName": "t2",
        "optResub": {
          "optMethod": "B3LYP",
          "optBasisSet": "6-31G(d)",
          "memComFile": "1600",
          "memPBSFile": "10"
        },
        "excList": [
          {
            "excMethod": "wB97XD",
            "excBasisSet": "6-31G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "nStates": 25,
            "SCRF": ""
          }
        ],
        "vibList": [
          {
            "excMethod": "wB97XD",
            "excBasisSet": "6-31G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "SCRF": ""
          }
        ]
      }
    ]
  },
  "dataAnalysis": {
    "enable": true,
    "dataPath": "data/",
    "temperature": 273.15,
    "type": "exc",
    "output": {
      "numerical": {
        "enable": true,
        "type": ".json",
        "outFile": "tmp.json",
        "excList": [
          {
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-311G(d,p)",
            "nStates": 25,
            "acquiredStates": "25",
            "SCRF": ""
          },
          {
            "excMethod": "wB97XD",
            "excBasisSet": "6-311G(d,p)",
            "nStates": 25,
            "acquiredStates": "25",
            "SCRF": ""
          }
        ]
      },
      "plot": {
        "enable": true,
        "range": { "x": [1, 12], "y": [0, 1.5] },
        "x_units": "eV",
        "fileName": "data.png",
        "title": "",
        "dpi": 400,
        "dft": {
          "legendLabelBasisSet": false,
          "peaks": false,
          "excList": [
            {
              "dataPath": "data/test2",
              "excMethod": "wB97XD",
              "excBasisSet": "6-31G(d)",
              "nStates": 25,
              "acquiredStates": "25",
              "SCRF": "",
              "line": { "color": "red", "type": "-" }
            }
          ]
        },
        "exp": {
          "enable": true,
          "peaks": false,
          "expData": [
            {
              "path": "exp_data/nh3_gas.csv",
              "units": { "input": "eV", "output": "eV" },
              "line": { "color": "k", "type": "--" },
              "legendLabel": "Test 1"
            },
            {
              "path": "exp_data/nh3_solid.csv",
              "units": { "input": "eV", "output": "eV" },
              "line": { "color": "b", "type": "-" },
              "legendLabel": "Test 2"
            }
          ]
        }
      }
    }
  }
}
```

To manage more datasets with a single script running in the background
you can copy the objects below for the desired function, edit the
parameters, and insert into the correct jobList array in input.json.
Remember to add commas after the previous object and that the last object in the
array should not have a comma afterwards.


### buildGeoms jobList Object
```sh
{
        "dataPath": "data/test",
        "inputCartesianFiles": [
          { "file": "mon_h2o.xyz", "count": 1 },
          { "file": "mon_nh3.xyz", "count": 0 }
        ],
        "clusters": 5,
        "boxLength": 3,
        "boxGrowth": {
          "enable": true,
          "increment": 3
        },
        "minDistanceMolecules": 2,
        "optMethod": "B3LYP",
        "optBasisSet": "6-31G(d)",
        "memComFile": "1600",
        "memPBSFile": "10",
        "startNum": 1
}
```

### qmgr jobList Object
```sh
{
        "dataPath": "data/test",
        "outName": "t1",
        "optResub": {
          "optMethod": "B3LYP",
          "optBasisSet": "6-31G(d)",
          "memComFile": "1600",
          "memPBSFile": "10"
        },
        "excList": [
          {
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-311G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "nStates": 25,
            "SCRF": ""
          }
        ],
        "vibList": [
          {
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-31G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "SCRF": ""
          }
        ]
}
```
### qmgr jobList excList object
```sh
{
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-311G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "nStates": 25,
            "SCRF": ""
}
```

### qmgr jobList vibList object
```sh
{
            "excMethod": "CAM-B3LYP",
            "excBasisSet": "6-31G(d)",
            "memComFile": "1600",
            "memPBSFile": "10",
            "SCRF": ""
}
```

### dataAnalysis output plot dft excList object
```sh
{
    "dataPath": "data/test2",
    "excMethod": "wB97XD",
    "excBasisSet": "6-31G(d)",
    "nStates": 25,
    "acquiredStates": "25",
    "SCRF": "",
    "line": { "color": "red", "type": "-" }
}
```

### dataAnalysis output plot dft excList object
```sh
{
    "path": "exp_data/nh3_gas.csv",
    "units": { "input": "eV", "output": "eV" },
    "line": { "color": "k", "type": "--" },
    "legendLabel": "Test 1"
}
```
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Vibrational Spectroscopy Graphs
- [] Restructure qstat call based on queue type

See the [open issues](https://github.com/Awallace3/ice_analog_spectra_generator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Austin Wallace - austinwallace196@gmail.com

Project Link: [https://github.com/Awallace3/ice_analog_spectra_generator](https://github.com/Awallace3/ice_analog_spectra_generator)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Neovim](https://github.com/neovim/neovim)

If you are curious about Neovim check out my [nvim](https://github.com/Awallace3/nvim) repo!

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Awallace3/ice_analog_spectra_generator.svg?style=for-the-badge
[contributors-url]: https://github.com/Awallace3/ice_analog_spectra_generator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Awallace3/ice_analog_spectra_generator.svg?style=for-the-badge
[forks-url]: https://github.com/Awallace3/ice_analog_spectra_generator/network/members
[stars-shield]: https://img.shields.io/github/stars/Awallace3/ice_analog_spectra_generator.svg?style=for-the-badge
[stars-url]: https://github.com/Awallace3/ice_analog_spectra_generator/stargazers
[issues-shield]: https://img.shields.io/github/issues/Awallace3/ice_analog_spectra_generator.svg?style=for-the-badge
[issues-url]: https://github.com/Awallace3/ice_analog_spectra_generator/issues
[license-shield]: https://img.shields.io/github/license/Awallace3/ice_analog_spectra_generator.svg?style=for-the-badge
[license-url]: https://github.com/Awallace3/ice_analog_spectra_generator/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
