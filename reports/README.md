# Exam template for 02476 Machine Learning Operations

This is the report template for the exam. Please only remove the text formatted as with three dashes in front and behind
like:

```--- question 1 fill here ---```

Where you instead should add your answers. Any other changes may have unwanted consequences when your report is
auto-generated at the end of the course. For questions where you are asked to include images, start by adding the image
to the `figures` subfolder (please only use `.JPG`, `.jpg` or `.jpeg`) and then add the following code in your answer:

`![my_image](figures/<image>.<extension>)`

In addition to this markdown file, we also provide the `report.py` script that provides two utility functions:

Running:

```bash
python report.py html
```

Will generate a `.html` page of your report. After the deadline for answering this template, we will auto-scrape
everything in this `reports` folder and then use this utility to generate a `.html` page that will be your serve
as your final hand-in.

Running

```bash
python report.py check
```

Will check your answers in this template against the constraints listed for each question e.g. is your answer too
short, too long, or have you included an image when asked. For both functions to work you mustn't rename anything.
The script has two dependencies that can be installed with

```bash
pip install typer markdown
```

## Overall project checklist

The checklist is *exhaustive* which means that it includes everything that you could do on the project included in the
curriculum in this course. Therefore, we do not expect at all that you have checked all boxes at the end of the project.
The parenthesis at the end indicates what module the bullet point is related to. Please be honest in your answers, we
will check the repositories and the code to verify your answers.

### Week 1

* [x] Create a git repository (M5)
* [x] Make sure that all team members have write access to the GitHub repository (M5)
* [x] Create a dedicated environment for you project to keep track of your packages (M2)
* [x] Create the initial file structure using cookiecutter with an appropriate template (M6)
* [x] Fill out the `data.py` file such that it downloads whatever data you need and preprocesses it (if necessary) (M6)
* [x] Add a model to `model.py` and a training procedure to `train.py` and get that running (M6)
* [x] Remember to fill out the `requirements.txt` and `requirements_dev.txt` file with whatever dependencies that you
    are using (M2+M6)
* [ ] Remember to comply with good coding practices (`pep8`) while doing the project (M7)
* [x] Do a bit of code typing and remember to document essential parts of your code (M7)
* [x] Setup version control for your data or part of your data (M8)
* [x] Add command line interfaces and project commands to your code where it makes sense (M9)
* [x] Construct one or multiple docker files for your code (M10)
* [x] Build the docker files locally and make sure they work as intended (M10)
* [x] Write one or multiple configurations files for your experiments (M11)
* [x] Used Hydra to load the configurations and manage your hyperparameters (M11)
* [x] Use profiling to optimize your code (M12)
* [x] Use logging to log important events in your code (M14)
* [x] Use Weights & Biases to log training progress and other important metrics/artifacts in your code (M14)
* [x] Consider running a hyperparameter optimization sweep (M14)
* [ ] Use PyTorch-lightning (if applicable) to reduce the amount of boilerplate in your code (M15)

### Week 2

* [x] Write unit tests related to the data part of your code (M16)
* [x] Write unit tests related to model construction and or model training (M16)
* [x] Calculate the code coverage (M16)
* [x] Get some continuous integration running on the GitHub repository (M17)
* [x] Add caching and multi-os/python/pytorch testing to your continuous integration (M17)
* [x] Add a linting step to your continuous integration (M17)
* [x] Add pre-commit hooks to your version control setup (M18)
* [x] Add a continues workflow that triggers when data changes (M19)
* [x] Add a continues workflow that triggers when changes to the model registry is made (M19)
* [x] Create a data storage in GCP Bucket for your data and link this with your data version control setup (M21)
* [x] Create a trigger workflow for automatically building your docker images (M21)
* [x] Get your model training in GCP using either the Engine or Vertex AI (M21)
* [x] Create a FastAPI application that can do inference using your model (M22)
* [x] Deploy your model in GCP using either Functions or Run as the backend (M23)
* [x] Write API tests for your application and setup continues integration for these (M24)
* [x] Load test your application (M24)
* [ ] Create a more specialized ML-deployment API using either ONNX or BentoML, or both (M25)
* [x] Create a frontend for your API (M26)

### Week 3

* [x] Check how robust your model is towards data drifting (M27)
* [x] Deploy to the cloud a drift detection API (M27)
* [x] Instrument your API with a couple of system metrics (M28)
* [x] Setup cloud monitoring of your instrumented application (M28)
* [x] Create one or more alert systems in GCP to alert you if your app is not behaving correctly (M28)
* [x] If applicable, optimize the performance of your data loading using distributed data loading (M29)
* [x] If applicable, optimize the performance of your training pipeline by using distributed training (M30)
* [ ] Play around with quantization, compilation and pruning for you trained models to increase inference speed (M31)

### Extra

* [x] Write some documentation for your application (M32)
* [x] Publish the documentation to GitHub Pages (M32)
* [ ] Revisit your initial project description. Did the project turn out as you wanted?
* [ ] Create an architectural diagram over your MLOps pipeline
* [ ] Make sure all group members have an understanding about all parts of the project
* [ ] Uploaded all your code to GitHub

## Group information

### Question 1
> **Enter the group number you signed up on <learn.inside.dtu.dk>**
>
Group 2

### Question 2
> **Enter the study number for each member in the group**
>
- Minh Nguyen: 13018310
- Euna Goo: 12957195
- Theerdha Sara: 12971850


### Question 3
> **A requirement to the project is that you include a third-party package not covered in the course. What framework**
> **did you choose to work with and did it help you complete the project?**
>
We used the third-party framework 'Ultralytics' in our project for Brain Tumor detection using the YOLO model. The Ultralytics package provides a user-friendly interface and tools for implementing object detection YOLO models with minimal setup. We used the functionality for loading pretrained YOLOv8 models, which allowed us to fine-tune the model on our custom dataset of Brain Tumor scan. Additionally, we leveraged built-in training and validation tools offered by the package to evaluate model performance and adjust hyperparameters efficiently. This significantly accelerated the development process and helped us achieve accurate detection of brain tumors in medical images. Overall, the Ultralytics framework was essential to our project, as it provided a powerful and flexible foundation for applying deep learning techniques to a real-world medical imaging task.


## Coding environment

> In the following section we are interested in learning more about you local development environment. This includes
> how you managed dependencies, the structure of your code and how you managed code quality.

### Question 4

> **Explain how you managed dependencies in your project? Explain the process a new team member would have to go**
> **through to get an exact copy of your environment.**
>
 We manage all dependencies with a combination of locked requirement files and Docker. For each service (training, inference, frontend, hyperparameter sweep) we maintain a requirements.txt (or package.json for JS) that was auto‑generated via pip freeze > requirements.txt
For a new team member to reproduce the exact environment, they can run pip intall -r requirements.txt to access the prpject or go to the root directory to run <br>
docker-compose build <br>
docker-compose up -d <br>
This will build each image and start containers in the right order.


### Question 5

> **We expect that you initialized your project using the cookiecutter template. Explain the overall structure of your**
> **code. What did you fill out? Did you deviate from the template in some way?**
>
From the cookiecutter template, we set up essential files and folders such as `.gitignore`, `pyproject.toml`, `docs`, `dockerfiles`, `.github`, and `tests` to ensure good project hygiene, documentation, containerization, and CI/CD support. However, we deviated from the standard template by restructuring the project into a monorepo, organizing the codebase into separate top-level folders for each microservice: `backend`, `frontend`, `ml`, and `monitoring`. This means our repository contains all services in a single place (monorepo), while each service is developed as an independent component (microservice architecture). This structure allows each service to be developed, tested, and deployed independently, while sharing a single repository for easier management and collaboration. It supports scalability and modularity, making it easier for our team to work on different parts of the system simultaneously.


### Question 6

> **Did you implement any rules for code quality and format? What about typing and documentation? Additionally,**
> **explain with your own words why these concepts matters in larger projects.**
>
We used Ruff for linting and enforcing code quality in our non-frontend (Python) codebase, and ESLint for maintaining code standards in our frontend (TypeScript/JavaScript) code. For typing, we relied on Python's built-in typing library to add type hints and improve code clarity and safety. For documentation, we used MkDocs to generate and maintain clear, accessible project documentation.<br>
These practices are especially important in larger projects because they help maintain a consistent code style, catch errors early, and make the codebase easier to understand for all team members. Linting tools like Ruff and ESLint automatically flag style issues and potential bugs, reducing technical debt. Typing helps prevent type-related bugs and improves IDE support, making refactoring and collaboration safer and more efficient. Good documentation with MkDocs ensures that both current and future contributors can quickly understand the system, onboard faster, and maintain or extend the project with confidence.

## Version control

> In the following section we are interested in how version control was used in your project during development to
> corporate and increase the quality of your code.

### Question 7

> **How many tests did you implement and what are they testing in your code?** (Theerdha, Minh)
>
In total we have implemented 12 tests. 3 unit tests, 1 performance test and 8 integration tests. The 3 unit tests make sure that the data is in place and have labels (test_data), make sure enabling wandb logging will trigger only one wandb login, if no arguments are given prediction function should return none, and the normalization of images has the expected shape (test_model), validating the training entrypoints without really touching the dependencies (test_train)In total we have implemented 12 tests. 3 unit tests, 1 performance test and 8 integration tests. The 3 unit tests make sure that the data is in place and have labels (test_data), make sure enabling wandb logging will trigger only one wandb login, if no arguments are given prediction function should return none, and the normalization of images has the expected shape (test_model), validating the training entrypoints without really touching the dependencies (test_train)

### Question 8

> **What is the total code coverage (in percentage) of your code? If your code had a code coverage of 100% (or close**
> **to), would you still trust it to be error free? Explain you reasoning.**
>
Total coverage report of the unit tests are 99%, which includes all source code. We are very close to the optimalcode coverage. But this does not mean that the codes are error free. The tests mostly take care of the fundamental set up before the training can be done. Theere could still be corners in the code that is not covered by the tests and will result in an error.

### Question 9

> **Did you workflow include using branches and pull requests? If yes, explain how. If not, explain how branches and**
> **pull request can help improve version control.**
>
Yes, our workflow included using branches and pull requests to manage version control effectively. We created several branches, each assigned to specific tasks such as cloud integration, command-line interface development, API implementation, and so on. Each team member worked independently on their assigned branch, allowing parallel development without interfering with the main codebase. Once a task was completed, the developer created a pull request to merge their changes into the main branch. The rest of the team then read that pull request, checking what was processed in the branch, examining code changes, and ensuring non-confliction. During this review, any conflicts or issues were identified and resolved collaboratively. This process helped maintain a clean and stable main branch, improved code quality through peer reviews, and minimized integration problems.


### Question 10

> **Did you use DVC for managing data in your project? If yes, then how did it improve your project to have version**
> **control of your data. If no, explain a case where it would be beneficial to have version control of your data.**
>
We used DVC (Data Version Control) in our project to manage our datasets and connected it to a Google Cloud Platform (GCP) bucket for remote storage. By integrating DVC, we were able to version control large data files and track changes efficiently, similar to how git tracks code. The connection to a GCP bucket allowed us to store and share data remotely, making it easy for all team members to access the same datasets regardless of their local environment. This setup improved collaboration, ensured data consistency, and made our experiments reproducible, as each experiment could be linked to a specific version of the data stored in the cloud. Overall, using DVC with a GCP bucket streamlined our workflow and provided transparency and reliability in handling data throughout the project pipeline.


### Question 11

> **Discuss you continuous integration setup. What kind of continuous integration are you running (unittesting,**
> **linting, etc.)? Do you test multiple operating systems, Python  version etc. Do you make use of caching? Feel free**
> **to insert a link to one of your GitHub actions workflow.**
>

We have organized our continuous integration into 4 files.
- Linting: runs on every push/PR and lints the code with Flake8 and Black, ensuring style consistency.
- Testing: runs pytest for unit and integration tests on every push and pull requests
- Precommit: invokes our Pre-commit hooks (e.g. sorting imports, formatting, simple auto‑fixes) to guarantee that all commits adhere to project conventions.
We run the CI tests on multiple operating systems and Python versions in these files. We have included the possibility of running on multiple systems through code that looks like this: <br>
```
# jobs:
#   build:
#     runs-on: ${{ matrix.os }}
#     strategy:
#       fail-fast: false
#       matrix:
#         os: [ ubuntu-latest, windows-latest, macos-latest ]
#         python-version: [ "3.10", "3.11", "3.12" ]
```
We have also included caching as it is important for continuous integration steps. We included caching in the 'steps'command:
```
#     steps:
#       - name: Check out repo
#         uses: actions/checkout@v4

#       - name: Set up Python
#         uses: actions/setup-python@v5
#         with:
#           python-version: ${{ matrix.python-version }}
#           cache: 'pip'                                  # <-- enable pip caching
#           cache-dependency-path: |
#             backend/requirements.txt
#             ml/requirements.txt
#             tests/requirements_tests.txt
```
An example of a triggered github action can be seen here:
https://github.com/minhNgnn/MedView-LMU-MLOps-SoSe25-GroupB/actions/runs/16289911255

## Running code and tracking experiments

> In the following section we are interested in learning more about the experimental setup for running your code and
> especially the reproducibility of your experiments.

### Question 12

> **How did you configure experiments? Did you make use of config files? Explain with coding examples of how you would**
> **run a experiment.**
>
Yes, we made a config.yaml file in the following structure:<br>
```
|--ml
|  |--configs
|     |--model
|     	 |--config.yaml
|     	 |--config_cloud.yaml
|     |--data_config
|     	 |--data.yaml
|     	 |--data_cloud.yaml
|--train.py
```
In the train.py, we used a hydra library to call hyperparameter setting written in configs/model/config.yaml file. There are 4 hyperparameters in the config.yaml file, and hydra calls those parameters. In this way, we can edit hyperparameters easily without editing a train.py file directly.


### Question 13

> **Reproducibility of experiments are important. Related to the last question, how did you secure that no information**
> **is lost when running experiments and that your experiments are reproducible?**
>
To ensure our experiments were reproducible and no information was lost, we used a config.yaml file to store all key hyperparameters and settings of our model. This file included values such as learning rate, batch size, number of epochs, model type. Whenever an experiment was run, the script automatically read from the config.yaml file to apply consistent configurations throughout training and evaluation. This made it easy to keep track of experiment setups and reduced the chance of manual errors. Additionally, we saved model checkpoints and evaluation results for each run. To reproduce an experiment, one simply needs to use the same config.yaml file and run the training script again.


### Question 14

> **Upload 1 to 3 screenshots that show the experiments that you have done in W&B (or another experiment tracking**
> **service of your choice). This may include loss graphs, logged images, hyperparameter sweeps etc. You can take**
> **inspiration from [this figure](figures/wandb.JPG). Explain what metrics you are tracking and why they are**
> **important.**
>
Because of training environment, it was impossible to train with a large dataset and large epoch. You can see the result of training with simple subset of data and only 10 epochs. Therefore, the model was not trained well and the model couldn't predict detection.

![Alt text](images/Q14_wandb_screenshot1.JPG)
In the first image you can see tracking of key metrics such as precision, recall, and mAP (mean Average Precision) over training epochs. Precision and recall provide insight into the model’s ability to correctly detect tumors without generating too many false positives or negatives, while mAP gives an overall measure of detection accuracy across various confidence thresholds.

![Alt text](images/Q14_wandb_screenshot2.JPG)
In the second image, you can see that at each epoch, predictions was made and it was drawn with ground truth labels. This visual feedback helped us qualitatively assess how well the model was identifying tumors on unseen MRI scans. It allowed us to spot cases where the model either missed a tumor or incorrectly flagged a non-tumor region.

![Alt text](images/Q14_wandb_screenshot4.JPG)
In third image, it shows the loss curves from multiple hyperparameter sweep runs, each representing a different configuration. We monitored distribution focal loss, classification loss and box regression loss to understand how different settings impacted convergence and model stability. In this case, it looks like that tough-sweep-7 setting is performing the best.


### Question 15

> **Docker is an important tool for creating containerized applications. Explain how you used docker in your**
> **experiments/project? Include how you would run your docker images and include a link to one of your docker files.**
>
For our project we developed 5 images:
-Training: builds training image with all ML libraries and project code.
-Hyperparameter sweep: uses an entrypoint.sh and uses that as an entrypoint to create the sweep image
-Inference: creates an image of the prediction in the training and all the processes that go on in the backend of the app
-Frontend: creates an image of all the processes that go on in the frontend with Nginx to serve the compiled static files
-Prometheus: creates an image of the processes that go behind finding metrics and how often it scrapes them etc.

we used docker to build images based on the files copied in dockerfile formats. These images are containers for different parts of the project.
Given the docker image for training was mlops_train, the run function would look like:
```
docker build -f docker/Dockerfile.train -t mlops_train .
docker run --rm \
  -v $(pwd)/data:/app/data \
  -e EPOCHS=10 \
  mlops_train
```

### Question 16

> **When running into bugs while trying to run your experiments, how did you perform debugging? Additionally, did you**
> **try to profile your code or do you think it is already perfect?**
>
For debugging, we primarily use the Python debugger, which allows us to set breakpoints, inspect variables, and step through code to identify where things deviate from our expectations. To streamline debugging in our development environment, we also configure a `launch.json` file to ensure the correct Python path is set, making it easier to start debugging sessions directly from our IDE. For small or quick bugs, we often rely on simple logging or printing to the terminal to quickly check values or program flow. When deeper inspection is needed, the debugger is invaluable for examining the state of the application in detail.

Regarding profiling, we mainly focused on profiling the prediction and training steps of our machine learning model. However, since our model is based on a pre-trained YOLO implementation from Ultralytics, most of the heavy lifting is handled by the external library. As a result, profiling mainly showed the import and execution of these library functions, and we did not identify significant custom bottlenecks in our own code.


### Question 17

> **List all the GCP services that you made use of in your project and shortly explain what each service does?**
>
- API Gateway (apigateway.googleapis.com) – This service was used to expose our model as a secure and scalable API endpoint, allowing users to send requests and receive predictions.

- Service Management (servicemanagement.googleapis.com) – This handled the configuration and deployment of managed services, ensuring that our APIs were properly registered and discoverable.

- Service Control (servicecontrol.googleapis.com) – Used for managing access control, logging, and monitoring of our API usage, helping us keep track of service reliability and performance.

- Artifact Registry (artifactregistry.googleapis.com) – This was used to store and manage our Docker container images securely, which we later deployed on GCP.

- Cloud Build (cloudbuild.googleapis.com) – Cloud Build automated the process of building and packaging our code into Docker images, streamlining continuous integration.

- AI Platform (aiplatform.googleapis.com) – We used this service to deploy and manage our trained machine learning model in a production-ready environment with scalable infrastructure.


### Question 18

> **The backbone of GCP is the Compute engine. Explained how you made use of this service and what type of VMs**
> **you used?**
>
We used the Compute Engine to run our brain tumor detection model and support various backend services during development and testing. Specifically, we used a virtual machine with the type n1-standard-1, which provides 1 vCPU. This configuration was sufficient for lightweight tasks such as hosting our API and performing model inference on smaller test inputs.
We started the VM using a custom Docker container, which included our trained YOLO model, necessary dependencies, and scripts for handling prediction requests. Using Compute Engine allowed us to have full control over the runtime environment and scale resources when needed.


### Question 19

> **Insert 1-2 images of your GCP bucket, such that we can see what data you have stored in it.**
> **You can take inspiration from [this figure](figures/bucket.JPG).**
>
![Alt text](images/Q19_1.JPG)


### Question 20

> **Upload 1-2 images of your GCP artifact registry, such that we can see the different docker images that you have**
> **stored. You can take inspiration from [this figure](figures/registry.JPG).**
>
![Alt text](images/Q20_2.JPG)
```
|--train-registry/
|  |--train: docker image to run train_cloud.py code
|  |--distributed
```


### Question 21

> **Upload 1-2 images of your GCP cloud build history, so we can see the history of the images that have been build in**
> **your project. You can take inspiration from [this figure](figures/build.JPG).**
>
![Alt text](images/Q21_1.JPG)


### Question 22

> **Did you manage to train your model in the cloud using either the Engine or Vertex AI? If yes, explain how you did**
> **it. If not, describe why.**
>
No, we didn't use cloud to train our model. Our model is composed with very large weights and parameters and used large image dataset, which requires GPU for training. However, it was impossible to use GPU server in GCP. Therefore, we used kaggle notebook instead, where we can use free GPU for limited amount. After training the model in the kaggle notebook, we downloaded the best weights file(.pt) and put it in our repository.<br>
Link to kaggle notebook: https://www.kaggle.com/code/eunai9/brain-tumor-detection-with-yolov8-de6d81<br>
![Alt text](images/Q22_1.JPG)
But at least, we made a setting to train the model with docker image using Vertex AI. In order to confirm if it works well, we create a small subset of data named 'Simple'.


## Deployment

### Question 23

> **Did you manage to write an API for your model? If yes, explain how you did it and if you did anything special. If**
> **not, explain how you would do it.**
>
Yes, we managed to write an API for our model and related services. The API includes endpoints for interacting with a tabular database of patients, allowing users to retrieve a list of all patients or fetch details for a specific patient by ID. Due to the scope of the project, we have currently implemented only the read (GET) endpoints for the patient database, but the structure allows for easy extension to full CRUD (Create, Read, Update, Delete) operations in the future.

In addition to the database endpoints, we implemented a `predict` endpoint that calls the model's prediction function. This endpoint accepts an input image, runs the prediction using our machine learning model, and returns the annotated image with the prediction results overlaid. This makes it easy for users to visualize the model's output directly.

We also included a router for the monitoring system, which is designed to support system health checks and future monitoring features. Overall, the API is modular and organized, making it straightforward to extend with additional endpoints or features as the project evolves.


### Question 24

> **Did you manage to deploy your API, either in locally or cloud? If not, describe why. If yes, describe how and**
> **preferably how you invoke your deployed service?**
>
For deployment, we built a Docker image for our API and deployed it on Google Cloud Run. This approach allows us to run our FastAPI backend in a fully managed, scalable environment without worrying about server management. The Docker image is built using our `dockerfiles/api.Dockerfile`, which includes all necessary dependencies, model weights, and code.

To invoke the deployed API on Cloud Run, you simply send HTTP requests to the public URL provided by Cloud Run after deployment. For example, if your Cloud Run service URL is:

```
https://gcp-test-app-351704569398.europe-west1.run.app
```

you can check the health of the API with:

```bash
curl https://gcp-test-app-351704569398.europe-west1.run.app/health
```

To use the prediction endpoint, you can send a POST request with an image file:

```bash
curl -X POST -F "file=@path/to/image.jpg" \
  https://gcp-test-app-351704569398.europe-west1.run.app/predict
```

This will return the prediction result or the annotated image, depending on your API implementation.

### Question 25

> **Did you perform any unit testing and load testing of your API? If yes, explain how you did it and what results for**
> **the load testing did you get. If not, explain how you would do it.**
>
Yes, we performed both integration and load testing of our API. For integration testing, we created a suite of tests in the `tests/integrationtests/` folder that cover key API endpoints such as `/patients`, `/patients/{id}`, and `/predict`. These tests verify that the endpoints return correct responses, handle edge cases, and maintain stability as the codebase evolves.

For load testing, we used Locust to simulate multiple users interacting with the API concurrently. Our load test script downloads a random image from a GCP bucket and sends it to the `/predict` endpoint, as well as tests the `/patients` endpoint and error handling by sending invalid files. The results showed that our API could handle multiple simultaneous requests without significant slowdowns or failures, and that error handling worked as intended for invalid inputs. Overall, these tests gave us confidence in the reliability and scalability of our API under realistic usage scenarios.


### Question 26

> **Did you manage to implement monitoring of your deployed model? If yes, explain how it works. If not, explain how**
> **monitoring would help the longevity of your application.**
>
Yes, we implemented a comprehensive monitoring system for our deployed model. When the monitoring app is initialized, it uses the first 50 images from the training dataset stored in our GCP bucket as the reference dataset for drift detection. Each time a new prediction is made, the input image and its extracted features are logged to an external database, which in our case is Supabase. This allows us to track all predictions and monitor for data drift over time.

We also developed a UI for the monitoring system. When a user presses the 'Generate Report' button in the UI, the backend generates a drift report by comparing the current data (recent predictions) to the reference data. This report is generated as an HTML file using Evidently and is then stored in a Supabase bucket for easy access and sharing. The UI can then display the generated report directly to users, providing clear visualizations of data drift and model performance. This setup ensures that our monitoring is automated, transparent, and accessible to all stakeholders.


## Overall discussion of project

> In the following section we would like you to think about the general structure of your project.

### Question 27

> **How many credits did you end up using during the project and what service was most expensive? In general what do**
> **you think about working in the cloud?**
>
![Alt text](images/Q27_1.JPG)
We used most of the our cost to use Virtual Maschine(Compute Engine). And second most used section is for container registry. It is for saving docker images inside the GCP.
If we can use GPU through VM, it would be very beneficial for our project. However, we couldn't use GPU with free trial account, so it wasn't worth at all. But it was very comfortable to run train code on the VM or Vertex AI, because it was running on the background and I don't need to take care of it during training.


### Question 28

> **Did you implement anything extra in your project that is not covered by other questions? Maybe you implemented**
> **a frontend for your API, use extra version control features, a drift detection service, a kubernetes cluster etc.**
> **If yes, explain what you did and why.**
>
For the frontend, we chose to use React with TypeScript. This combination allows us to build a more scalable and maintainable user interface, following modern best practices in frontend development. TypeScript provides type safety and better tooling, which helps prevent bugs and makes the codebase easier to manage as the project grows.<br>

For data storage, we use Supabase to handle tabular patient data. This choice was made to create a more comprehensive system where doctors and users can easily scroll through and access patient records via the UI. Additionally, we store the generated monitoring reports (HTML files from Evidently) in Supabase buckets. This makes it straightforward to retrieve and display these reports directly in the frontend, ensuring that monitoring insights are easily accessible to users.<br>

For documentation, we used MkDocs, as it is a modern and user-friendly static site generator that is well-suited for project documentation. We wanted to try a robust tool that could handle the extra requirements of the project and provide professional-quality documentation. After generating the documentation with MkDocs, we uploaded it to GitHub Pages to make it easily accessible and shareable with all stakeholders.<br>

We also did distributed data loading and implemented distributed data parallel in our training process and deployed the DDP training on GCP.


### Question 29 (Theerdha)

> **Include a figure that describes the overall architecture of your system and what services that you make use of.**
> **You can take inspiration from [this figure](figures/overview.JPG). Additionally, in your own words, explain the**
> **overall steps in figure.**
>
> Recommended answer length: 200-400 words
>
> Example:
>
> *The starting point of the diagram is our local setup, where we integrated ... and ... and ... into our code.*
> *Whenever we commit code and push to GitHub, it auto triggers ... and ... . From there the diagram shows ...*
>
> Answer:

--- question 29 fill here ---

### Question 30

> **Discuss the overall struggles of the project. Where did you spend most time and what did you do to overcome these**
> **challenges?**
>
- Euna: The biggest challenges in the project was all of works related to Google Cloud. Especially, I was struggled building a docker image and pushing it to the Artifact Registry of GCP. I couldn't understand the role of Dockerfile and cloudbuild.yaml at first, so it was hard to understand errors happening.
- Theerdha: The biggest challenge for me was using Vertex AI to train on the docker images we created on the Artifact Registry of the cloud. It took me many rounds of debugging to get the Engine to train on Vertex AI.


### Question 31

> **State the individual contributions of each team member. This is required information from DTU, because we need to**
> **make sure all members contributed actively to the project. Additionally, state if/how you have used generative AI**
> **tools in your project.**
>
**Minh Nguyen**
- Set up version control for the dataset (e.g., DVC or Git-LFS)
- Performed code profiling to optimize performance
- Added pre-commit hooks
- Built workflow triggers for data change detection
- Created a GCP bucket for data storage and linked it to the data versioning tool
- Built and deployed a FastAPI inference application
- Deployed the model using GCP Cloud Functions or Cloud Run
- Wrote API tests and implemented CI for them
- Conducted load testing of the deployed API
- Developed a frontend interface for the API (M26)
- Analyzed model robustness to data drift
- Deployed a drift detection API
- Added system metrics instrumentation to the API
- Set up GCP Cloud Monitoring for system metrics and application behavior
- Adding a linting step to CI (with Theerdha)
- Used ChatGPT and Cursor

**Euna Goo**
- Implemented the model in model.py and the training procedure in train.py
- Added command-line interfaces and relevant project commands
- Wrote and managed experiment configuration files
- Used Hydra for configuration management and hyperparameter loading
- Integrated logging to track important events
- Used Weights & Biases (W&B) to track training progress, metrics, and artifacts
- Ran a hyperparameter optimization sweep using W&B
- Created a workflow trigger that responds to model registry changes
- Set up a Docker image auto-build trigger
- Trained the model using GCP Vertex AI
- Set up GCP alerts to detect abnormal application behavior
- Used ChatGPT

**Theerdha Sara**
- Wrote Dockerfiles for the project
- Built and tested Dockerfiles locally to ensure functionality
- Wrote unit tests for both the data pipeline and model training/construction
- Calculated code coverage
- Set up continuous integration (CI) on GitHub
- Enhanced CI with caching, multi-OS, and PyTorch/Python version testing
- Added a linting step (in collaboration with Minh)
- Worked on pre-commit hook integration
- Optimized data loading performance using distributed data loading
- Improved training pipeline performance using distributed training
- Trained the DDP model using GCP on Vertex AI
- Used ChatGPT
