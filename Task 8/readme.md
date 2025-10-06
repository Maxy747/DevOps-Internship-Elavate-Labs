# Task 8: Simple Java Maven Build in Jenkins

This repository contains the solution for the Elevate Labs DevOps Internship Task 8. The goal was to build a simple Java application using Maven within a Jenkins Freestyle job.

## Objective

To learn the fundamentals of CI/CD by configuring a Jenkins job that automatically pulls source code from GitHub and builds a Java project using Maven.

## Steps Taken

1.  **Project Setup**: Created a simple `HelloWorld.java` application and a corresponding `pom.xml` to define the project structure and build dependencies.

2.  **Jenkins Job Creation**: A new Freestyle project was created in Jenkins to automate the build process.

3.  **Source Code Management**: The Jenkins job was configured to connect to this GitHub repository by setting the Git URL in the "Source Code Management" section. This ensures Jenkins always has the latest version of the code.

4.  **Maven Build Configuration**:
    * An "Invoke top-level Maven targets" build step was added.
    * The **Goals** were set to `clean package`.
    * In the **Advanced** settings for the build step, the **POM** field was set to `Task 8/pom.xml` to ensure Maven could locate the configuration file inside the correct sub-directory.

5.  **Debugging and Execution**:
    * Resolved an initial "MissingProjectException" by correctly pointing the Jenkins job to the `pom.xml` located in the `Task 8/` sub-folder.
    * Fixed a `COMPILATION ERROR` by renaming the Java source file from `Helloworld.java` to `HelloWorld.java` to match the public class name.
    * Ran the build again to achieve a **BUILD SUCCESS** status.

## Build Success Screenshot

Below is the screenshot of the Jenkins console output showing the successful build.

![SharedScreenshot2](https://github.com/user-attachments/assets/64e6f408-c27c-4714-b3e4-94dd68886bf5)
