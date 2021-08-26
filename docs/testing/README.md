# Testing

At this moment the YAFRA project contains two different types of tests: Unittests and Integrationtests. End-to-End-Tests (E2E) are not planned yet, but could be useful in the future.

## Unittests

For unit testing the python package *unittest* has been used.

The Unittests are located within every microservice/ subfolder. (Attention -> Some Unittests are still missing.)
The syntax for the testfolder and testfiles is the following:

* folder -> tests_FOLDERNAME_OF_FOLDER_TO_TEST
* files -> test_FILENAME_OF_FILE_TO_TEST.py

This kind of syntax is necessary, so that the *unittest* package is able to find all relevant tests automatically within the CI/ CD pipeline.

## Integrationtests

For integration testing the python package pytest_bdd has been used. This package allows so called behavior driven development.
This means, that one is able to describe the whole testcase in human readable language, before implementing the actual tests.
Therefore it is possible for contributers, who are not familiar with writing tests in python, to contribute to the quality of the project by defining new test scenarios.

The Integrationtests are located within those microservices/ subfolders, in which the logic of a whole subprocess should be tested. (Attention -> Some Integrationtests are still missing.)
The syntax for the testfolder and testfiles is the following:

* folder -> tests_integration_FOLDERNAME_OF_FOLDER_TO_TEST
    * features -> within this subfolder all .feature files are stored. The description in human readable language is stoed within those files.
    * step_defs -> within this subfolder the acutal tests are located.
* files
  * FILENAME_OF_FILE_TO_TEST.feature in the features folder
  * test_FILENAME_OF_FILE_TO_TEST.py in the step_defs folder

## Run tests local

If you want to run the tests on your local system, there are two possibilities:

* Run all tests at once -> make sure, you are in the root directory of the YAFRA project. Then just run `pytest` in the terminal.
* Run just a particular test -> step inside the directory, the test you want to run is located. In there just run `pytest test_FILENAME_OF_FILE_TO_TEST.py` in the terminal. If you want to run an integration tests you can simply call the .py test file as well. No need to call the .feature file.

### Common error when running locally -> ModuleNotFoundError

If you run into a *ModuleNotFoundError No module named ...* or similar but you have installed all requirements from the requirements.txt within your virtual environment, try the following:

* exit the virtual environment
* use pip to uninstall pytest on your computer
* activate your virtual environment again
* install pytest inside the virtual environment

This happens, because if you have pytest outside your virtual environment, it is only looking for modules on your system but not inside the virtual environment.
For further reading please visit [this medium article](https://medium.com/@dirk.avery/pytest-modulenotfounderror-no-module-named-requests-a770e6926ac5).
