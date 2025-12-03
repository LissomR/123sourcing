# Instructions to Start the Django Project


## Hardware Configuration
Ensure that your system meets the following minimum configuration for optimal performance:

1. Ubuntu System preferable with GPU support or EC2 instance
2. RAM Memory: At least 16 GB
3. GPU Memory: 16 GB
4. CPU: 8 cores
5. Storage: At least 50 GB

Preferred AWS Instance Type: **g4dn.2xlarge**

These specifications are necessary to ensure smooth operation and efficient usage of the application.


## Software Configuration
1. Python >= 3.9
2. Docker
3. Docker compose
4. MySql Database
5. Pinecone (VectorDB)
6. unzip



## Installing docker, docker-compose and unzip on the system

```sh
sudo apt install apt-transport-https ca-certificates curl software-properties-common unzip

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

sudo apt install docker-ce

sudo apt  install docker-compose

sudo systemctl status docker
```

```sh
sudo usermod -a -G docker <username>
```


## Setup Pinecone Vector Database - AWS Pay As You Go

1. 🌐 Access AWS console
2. 🔍 Search for "Pinecone" in AWS Marketplace
3. ✅ Select "Pinecone Vector Database - Pay As You Go Pricing"
4. 📲 Click "View Purchase Options"
5. 💳 Subscribe to the Pinecone service
6. 🔗 Follow the redirection link to log in to your Pinecone account
7. 👤 Choose your AWS account organization from the menu
8. 📊 Create a new index!
9. 🔑 Update the API key and index in the env file


## Designing MySQL Database Tables for Authentication

In this process, we create two tables: sb_users for storing user data and sb_users_token for storing token information.

Here's the SQL query to create the sb_users table:

```sql
CREATE TABLE `sb_users` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_type` enum('SUPER_BO','BO') NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `status` enum('ACTIVE','INACTIVE','TERMINATE') CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mobile_code` varchar(10) DEFAULT NULL,
  `mobile_no` varchar(15) DEFAULT NULL,
  `email_id` varchar(100) NOT NULL,
  `address_one` varchar(250) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `address_two` varchar(250) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `city_code` varchar(15) DEFAULT NULL,
  `city` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `state_code` varchar(15) DEFAULT NULL,
  `state` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `country_code` varchar(15) DEFAULT NULL,
  `country` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `zip` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_id` (`email_id`),
  UNIQUE KEY `mobile_no` (`mobile_no`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

Here's the SQL query to create the sb_users_token table:

```sql
CREATE TABLE `sb_users_token` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` varchar(500) DEFAULT NULL,
  `expire_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```


## Git Clone

Clone the repository and navigate to the root directory.

```sh
git clone http://clone:<REPLACE_WITH_YOUR_TOKEN>@gitlab.sapidblue.in/ai-ml-automation/123sourcing.git
```


## Update Environment File for MySQL DB Connection and Pinecone Service

To update the environment file, navigate to the api_channel/.env file.

Please provide the following configuration details:

- DJANGO_DATABASE_SERVER: Your MySQL database host
- DJANGO_DATABASE_NAME: Your MySQL database name
- DJANGO_DATABASE_USER: Your MySQL username
- DJANGO_DATABASE_PASSWORD: Your MySQL password
- AUTH_TOKEN_EXPIRE_TIME: Time for which the user will stay logged in
- HOST_SERVER_URL: Pinecone server URL
- PINECONE_API_KEY: Pinecone API key
- PINECONE_INDEX_NAME: Pinecone index name

Be sure to replace the placeholders with the actual values.


## Download the Trained Model from AWS S3

Go to the root directory

```sh
cd 123sourcing

wget https://d2hbdgqvbu3n3g.cloudfront.net/123sourcing/trained_models.zip
```

## Extract the Compressed Models Zip File for Utilization

```sh
unzip trained_models.zip
cd trained_models/gpu-model/model
tar -xvf docprompt_params.tar
```

## Start the Docker Container

Go back to the root directory.

```sh
docker-compose up -d
```
By following these steps, you will be able to start the Django project efficiently.

## Swaggeer Documentation

Once you start the docker container, to access Swagger documentation, kindly navigate to **https://host_url/swagger** in your web browser. eg. https://123sourcing.sapidblue.in/swagger


## API Details

For Details Desciption of an API please refer this link [here](https://drive.google.com/file/d/1ciM6lzayW6SGKEqClxfwPunghSD-9vwU/view?usp=sharing).

### API Flow
![API Flow](https://d2630mfamks0ao.cloudfront.net/document-123Sourcing/flow/api_1_api_flow_1.png)
![API Flow](https://d2630mfamks0ao.cloudfront.net/document-123Sourcing/flow/api_test_2.png)

### Process Flow
![Process Flow](https://d2630mfamks0ao.cloudfront.net/document-123Sourcing/flow/process_flow1.png)



## API 1 - Add Stamp

The Add Stamp API simplifies the process of storing stamp images in VectorDB using the Pinecone service. This API allows users to embed images, transform them into compact numerical representations, and store them in a Vector Database for efficient retrieval and similarity search.

### API Request
`POST`

### Endpoint
`https://host_url/AddStamp`

### Parameters
- `files` (form-data, Filetype): Choose an image file to add to the vectorDB. This API can either use this option or provide a valid URL using the `url` parameter. (Only Images allowed)
- `url` (Text): Provide a valid URL for adding a stamp in the vectorDB. This API either uses this option or uploads an image file using the `files` parameter. (Only Images allowed)
- `companyId` (Text, minLength: 1): Provide a valid companyID for the stamp company Image.
- `Authorization` (header, required): Bearer token for authentication.

### Example Request
```http
POST /AddStamp
Authorization: Bearer XXXX
Content-Type: multipart/form-data

url: "https://d2630mfamks0ao.cloudfront.net/document-123Sourcing/stamp/test.png"
companyId: "e228f6c6-57f1-33ac-bbf5-2720de811e2c"
```


## API 2 - Data Extraction 

We look for specific pieces of information in documents:

- `shipmentId`: This is the number that tracks the shipment or Embarque number.
- `deliveryId`: This is the number associated with the delivery or entrega number.


### API Request
`POST`

### Endpoint
`https://host_url/GetDetails`


### Parameters
- `files` (form-data, Filetype): Choose a PDF or image file for data extraction. This API can either use this option or provide a valid URL using the `url` parameter. Supported image file extensions: ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']. PDF extension: '.pdf'.
- `url` (Text): Provide a valid URL for data extraction. This API either uses this option or uploads a file using the `files` parameter.
- `bool_stamp_detection` (Query-Params, Bool): Furnish a valid boolean input to include stamp details in the API response.
- `Authorization` (header, required): Bearer token for authentication.

### Example Request
```http
POST /GetDetails
Authorization: Bearer XXXX
Content-Type: multipart/form-data

url: "https://d2630mfamks0ao.cloudfront.net/document-123Sourcing/11.pdf"
bool_stamp_detection (query-param): bool_stamp_detection=true
```



### Models use for data extraction

Models are chosen based on sytem configuration.


1. **LayoutLM**

    - This model understands documents by looking at their text and layout.
    - It can also answer questions about the documents by looking at their format.
    - It's particularly good when used on a CPU and gives fast results.
    - You can check model details from [here](https://huggingface.co/impira/layoutlm-document-qa).

2. **Ernie Layout**

    - This model also understands the layout and text in documents.
    - It can handle tasks that involve answering questions about the documents.
    - It needs a powerful GPU to work effectively.
    - You can check model details from  [here](https://github.com/PaddlePaddle/PaddleNLP/tree/develop/model_zoo/ernie-layout).



## API 3 - Stamp Verification

The Stamp Verification API checks if a given stamp companyID in a document is present in our database. If present, then it will check whether the same stamp companyID is present in the provided document or not. If the companyID is found in the document, the API will return the bounding box coordinates of the stamp. This API helps ensure the authenticity of documents by verifying the presence of the stamp companyID.

### API Request
`POST`

### Endpoint
`https://host_url/StampVerification`


### Parameters
- `files` (form-data, Filetype): Choose an image file to add to the vectorDB. This API can either use this option or provide a valid URL using the `url` parameter. (Only Images allowed)
- `url` (Text): Provide a valid URL for adding a stamp in the vectorDB. This API either uses this option or uploads an image file using the `files` parameter. (Only Images allowed)
- `companyId` (Text, minLength: 1): Provide a companyID to check the existence in the document.
- `Authorization` (header, required): Bearer token for authentication.

### Example Request
```http
POST /StampVerification
Authorization: Bearer XXXX
Content-Type: multipart/form-data

url: "https://d2630mfamks0ao.cloudfront.net/document-123Sourcing/stamp/test.png"
companyId: "e228f6c6-57f1-33ac-bbf5-2720de811e2c"
```