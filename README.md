# Creative Collaborative Workspace

Application created as part of CS4440: Emerging Database Technologies.

## Team Members

 - Avinash Athota: aathota3@gatech.edu
 - Avyesh Kapadia: akapadia31@gatech.edu
 - Dhruv Sharma: dsharma97@gatech.edu

## Learning Goals & Project Statement

The focal point of our project is the development of a collaborative workspace platform tailored to diverse groups, including freelancers, remote workers, and businesses involved in creative endeavors. This application will be equipped with a range of features designed to streamline the collaborative process inherent in creative projects. The primary learning goal is to understand and attempt to mimic the way that emerging database technologies are used in creating innovative products. By integrating emerging database technologies into our platform, we aim to gain a better understanding of optimization techniques for faster access, scalability, and reliability. Additionally, we seek to explore the intricacies of database integration within web applications, enabling essential features such as real-time messaging, file sharing, task management, and version control. Through this project, we aim to enhance our skills in implementing basic security measures and improving user experience through an intuitive interface.

## Architecture Used

We plan to use DynamoDB as the backbone for storing essential entities such as user profiles, project details, tasks, and file metadata, leveraging its flexible JSON-like storage model to efficiently manage complex relationships. It’s also capable of handling CRUD operations, ensuring data integrity and scalability. We also plan to use Amazon S3 as a reliable repository for storing file content, offering unparalleled durability and accessibility. When users upload files, their content is securely stored in S3, while metadata references are managed in DynamoDB. Since both are a part of the AWS suite, we can easily access S3 content while querying in DynamoDB. Firebase complements this architecture by providing real-time chat functionality, messaging, and user authentication. Firebase Authentication enables secure user logins, while Firebase Realtime Database or Cloud Firestore facilitates synchronous communication, ensuring seamless collaboration. We will use the UserId as the main key connection between DynamoDb and Firebase. By intricately connecting DynamoDB, Amazon S3, and Firebase services, our platform achieves a cohesive ecosystem where data management, file storage, authentication, and real-time communication converge to enhance productivity and user experience.

## Setup Instructions

1. Clone the repository to a desired location on your computer using the following command in terminal.
   - `git clone https://github.com/aviathota/creative-collaborative-workspace.git`
2. Download the `db_secrets.py` file that we'll provide you, and place it inside the project directory with all the other Python files.
3. Install the necessary dependencies by running the following command within the project directory.
   - `pip install -r requirements.txt`
4. Run the application from within the project directory.
   - `python app.py`
5. After entering the above command, you will get a `localhost` link to open up the page. Navigate to that link and begin using the app!

## Feedback

 - We'd love to hear your feedback on the app, please reach out to the emails listed in the team members section!