# Qur'an QA 2022 Shared Task!

## Introduction
Quran QA 2022
In this repo, we will represent our approaches to the research problem Quran_QA 2022 Architecture. Mainly, we used transformers.

## approaches
### 1.K-Fold Approach:
#### K-Fold
The Quran_QA_K_Folds notebook includes Training the model on each fold, saving the model to be used in ensemble , evaluating the result file of each fold using the competition metrics.
The notebook of this architecture has the following steps:
- Installing Packages
- Data Preparation
- Data Visualization
- Data Tokenization
- Model Training
- Model Testing
- Evaluation
- References

#### Ensemble using K-Fold Models
The Quran_Qa_ensemble_task notebook includes getting all models and executing the ensemble using the voting technique.


#### Testing on our version testing data
Our team answered the testing data to evaluate all our models on it before submitting it. This happened before the competition committee releases the testing data with answers. You can see the models' performance using the development and testing dataset in QA_results..xlsx

## Setup
This project requires GPU acceleration to run efficiently. Support is available to use either of the following two methods for accessing GPU-enabled cloud computing resources.

- Create a new environment use: create conda -n mt_env
- install all required packages inside requirements.txt file, pip install -r requirements.txt
- run the jupyter note book cells.

## Install
- transformers
- farasapy
- datasets
- arabic-reshaper
- python-bidi
- pyyaml==5.4.1

## Our Team:
- __[Marwa Matar](https://github.com/MarwaMohammad)__ : marwa.mohammad.matar@gmail.com
- __[Ahmed Wasfey Sleem](https://github.com/ahmedwasfey)__
- __[Eman Elrefai](https://github.com/EmanElrefai)__
- __[Haq Nawaz](https://github.com/haqnawaz99)__

If you have any question, please contact us:
