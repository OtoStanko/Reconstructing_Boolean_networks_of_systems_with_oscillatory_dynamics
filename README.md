# Reconstructing Boolean Network Models of Systems with Complex Oscillatory Dynamics

This repository contains the implementation, data, and documentation associated with my master's thesis at the [Faculty of Informatics, Masaryk University](https://www.fi.muni.cz/), Brno.

## Thesis Description

**Title**: *Reconstructing Boolean Network Models of Systems with Complex Oscillatory Dynamics*

**Author**: Oto Stanko  
**Institution**: Faculty of Informatics, Masaryk University  
**Program**: Master's Degree in Artificial intelligence and data processing, Bioinformatics and systems biology

The general topic of the thesis is the reconstruction and analysis of Boolean Networks (BNs) that reflect complex oscillatory patterns in biological systems.

## Objectives

1. **Understand Oscillatory Biological Systems**  
   Explore the oscillatory behavior of several biologically relevant systems.

2. **Design an Inference Workflow**  
   Develop a comprehensive pipeline to reconstruct Boolean Network models from:
   - Existing ODE-based differential models
   - Available experimental data
   - Formalized hypotheses about system behavior

3. **Evaluate on Case Studies**  
   Apply the workflow to biologically meaningful systems:
   - Predator-prey system
   - Bovine estrous cycle
   - Human menstrual cycle

5. **Analysis and Discussion**  
   Discuss the benefits, limitations, and potential extensions of the proposed approach

## Workflow Overview

The figure below illustrates the complete inference pipeline combining ODE models, experimental data, and formal dynamic properties:
![Workflow Diagram](workflow.png)


## Reproducibitily

The repository contains all the necessary time series for the inference process for each of the three biological systems with each of the four inference methods used in the thesis. Folder for each of the systems contains preprocessed TS before and after preprocessing (binarisation, transposition).

The main files for inference are `main.py` (Euler-like tranformation, SAILoR) and `BoolNet_inference_pp.R`, `BoolNet_inference_be.R`, `boolNet_inference_gc.R` (BoolNet) in the systems' subfolders. As SketchBook is designed in a user-friendly way with implemented GUI, there is no code reproducibility. The sketches for individual systems need to be imported from the corresponding folder of the biological system and then the inference can be run from SketchBook.

To run the inference of predator-prey model with Euler-like transformation navigate to the `main.py` file to the part marked as "Predator-prey model inference" and then "euler-like transformation" and run the corresponding function. To run the inference of a different system, navigate to the corresponding part of the main.py file and an appropriate function. For the inference with the BoolNet, see the R script in the corresponding system's\BoolNet folder.

The analysis, which includes extraction of dynamical properties and their coding to HCTL, is divided by the systems to `analysis_predator-prey.py`, `analysis_bovCycle.py` and `analysis_gynCycle.py`. The analysis column-oriented TS of the system in a .csv file and a list of Boolean networks paths.
