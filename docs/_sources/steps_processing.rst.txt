How to
=============================================

Processing steps
````````````````````````````````````

The following steps explain the process of preparing the data before the modelling stage

Information required:

- Census Data
- Previous model/analyst decisions
- Shape files of the Brazilian regions

1. Download the data from the S3 bucket. The functions that helps to do this are in :py:mod:`utils_aws`. Use of this functions can be reviewed in `download_info`
2. Use the shapes in `data/sharp` to add the sector code columns to the data base with the previous model and anlyst decisions. This allows to go from lat/long to sector code, which will be used to join the censun information to each property. The methods to perform this process are in the class :py:mod:`data_preparation_classes.CurrentLabels` . Use of this class can be reviewed in the script `initial_data_process`.
3. Solve the duplicates in the data base and unify the analyst and model decision to have only one label. The methods to perform this proces are in py:mod:`data_preparation_classes.DataWithDups`. Use of this class can be reviewed in the script `initial_data_process`.
4. Process the census information (featues creation and drop zero variance variables) and joins its information to the processed label data. The methods to perform this process are in the class :py:mod:`data_preparation_classes.FinalLabelsWithSector`. Use of this class can be reviewed in the script `initial_data_process`.


Modelling steps
````````````````````````````````````

The following steps explain the process of fitting the model based on the information processed previously.

Information required:

- Processed database with both labels and census information.

1. Fit the model using the class :py:mod:`fit_model_class.PropertyModel`.
2. Save the model using the same class from the step before. Use of the class can be reviewed in script `fit_model`.
