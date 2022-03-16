# Developer Guide
This is only for develoeprs. Users should access the documentation via https://readthedocs.com/.

To change or update the documentation, please follow the steps.
## Install Dependencis
```pip install sphinx```


Since `sphinx` need to run the source code to generate the documentation, make sure you have installed the all the necessary dependencies needed by the project(see setup.py files).

## Update the documentation html files
After you updated the documentation in the source code, run the following command to update the html files.

In docs directory:

```sphinx-apidoc -f -o . ../feathr ../*setup* ../feathr/*spark_job.py* ../feathr/*nyc_taxi_prediction.py*```

(excluding setup.py files and some other demo files, test files.)

Then rebuild the html files:

```make clean && make html```

You will see new html files generated under `_build/html/` directory and you can view `_build/html/index.html` in your browser locally.

## Upload to Readthedocs.com
(TBD)