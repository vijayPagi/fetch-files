# fetch-files
Retrieves the images used across the repository list supplied

Use Case:
The project takes a text source URL as a argument and then provides all the images utilized in the docker files in each repository in the input source, in the Json format.

Implementation Details:
- Used python language to implement the solution.
- Utilized Github API to retrieve the Dockerfiles with FROM keyword rather direct cloning.
- Used RegEx to validate the Input URL and commit.
- Validation of URL with commit ID.
- Displays Standard Output in Json format.
- Implemented the solution as Kubernetes Job using Minikube, DockerImage(DockerHub).

The Project can be executed using minikube in the below steps.
Pre-Requisites:
1. Minikube
2. hypervisor kit
3. kubernetes

Steps to Execute:
1. Clone this repository: [Clone](https://github.com/vijayPagi/fetch-files.git)
2. Navigate to the project directory.
3. Edit the Job.yaml file with the correct source text file argument in the environment variable value for the name: ```REPOSITORY_LIST_URL```, and save.
    ```spec.template.spec.env.value```
4. Use below command to create a kubernetes job
      ``` kubectl create -f job.yaml```
5. To check the status of the Job and get the name of the job with Id, use the below command
       ```kubectl get po```
6. To get the output of the job, use the below command
       ```kubectl logs "use the job name with Id retrieved from the output of Step 5 above"```
