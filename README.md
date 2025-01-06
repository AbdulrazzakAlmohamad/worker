# WorkerRMQ - RabbitMQ Consumer Management

## Project Description
**WorkerRMQ** is a Python-based microservice designed for efficient message handling and processing within a distributed system. It utilizes **RabbitMQ** for messaging and **Flask** for providing a RESTful API interface. The project enables managing queues and consumers, processing messages in real-time, and communicating with external APIs. 

This microservice is built to handle high-concurrency workloads using multithreading and is deployable via **Gunicorn** for scalable performance.

---

## Features
- **Queue Management:**
  - Create, retrieve, and delete queues.
  - Retrieve queue information.
- **Consumer Management:**
  - Create and delete consumers dynamically.
  - Handle multiple consumers for different queues.
- **Message Processing:**
  - Asynchronous message consumption from RabbitMQ queues.
  - Reliable message acknowledgment and rejection based on processing outcomes.
- **HTTP Request Handling:**
  - Sends HTTP requests to external APIs with processed message data.
- **Multithreading:**
  - Utilize threading for concurrent message processing.
  - Gunicorn ensures scalable API handling with multiple workers.
- **Robust Logging:**
  - Logs all significant events, errors, and outcomes for traceability.

---

## Requirements

### Tools and Libraries
- Python 3.8+
- Required libraries installed via `pip`:
  ```
  requests==2.24.0
  pika==1.1.0
  Flask
  python-dotenv
  py-bcrypt
  pymongo[srv]
  Flask-PyMongo
  gunicorn
  ```

---

## Setup and Execution

### 1. Install the Project
- Clone the project:
  ```bash
  git clone https://github.com/your-repo/worker-rmq.git
  cd worker-rmq
  ```
- Create and activate a virtual environment:
  ```bash
  sudo apt install python3-venv
  python3 -m venv venv
  source venv/bin/activate
  ```
- Install the required libraries:
  ```bash
  pip install -r requirements.txt
  ```

---

### 2. Configure Environment Variables
Create a `.env` file in the project root and add the necessary variables:
```env
SECRET_KEY=your_secret_key
EPINTOWER_API_PROCESS_ORDER=https://example.com/process-order
```

---

### 3. Run the Project
- Start the Flask backend with Gunicorn for production:
  ```bash
  gunicorn --bind 0.0.0.0:5000 wsgi:app
  ```
- For development purposes, you can run the Flask development server (not recommended for production):
  ```bash
  export FLASK_APP=app.py
  flask run
  ```

---

### 4. Run Helper Commands
To view all available routes:
```bash
flask routes
```

---

## API Endpoints Examples

### 1. Get Queues
- **GET Request**:
  ```http
  GET /getQueues
  ```
- **Response**:
  ```json
  [
    { "queueName": "example_queue" }
  ]
  ```

### 2. Create a Consumer
- **POST Request**:
  ```http
  POST /createConsumer
  ```
- **Request Body**:
  ```json
  {
    "queueName": "example_queue"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Consumer has been created successfully."
  }
  ```

### 3. Publish a Message
- **POST Request**:
  ```http
  POST /messagePublish
  ```
- **Request Body**:
  ```json
  {
    "queueName": "example_queue",
    "message": "Hello, World!"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Message has been published successfully."
  }
  ```

### 4. Get Connections
- **GET Request**:
  ```http
  GET /getConnections
  ```
- **Response**:
  ```json
  [
    { "connectionId": "abc123" }
  ]
  ```

---

## Core Workflow

1. **Queue Creation**:
   - Use `/createQueue` endpoint to create a new queue.
2. **Consumer Attachment**:
   - Attach a consumer to a queue with `/createConsumer`.
3. **Message Publishing**:
   - Publish messages to the queue using `/messagePublish`.
4. **Message Processing**:
   - Consumer processes the message and sends payload to the external API.
   - Logs results and acknowledges/rejects messages based on success.

---

## Project Structure
```
worker-rmq/
│
├── gateway/
│   ├── RabbitMQ.py               # RabbitMQ interface
│   ├── ConsumerThread.py         # Consumer threads for message processing
│
├── middlewares/
│   ├── Logger.py                 # Event and error logging
│   ├── Auth.py                   # Authentication middleware
│
├── services/
│   ├── DeleteConsumer.py         # Service for deleting consumers
│   ├── GetConnections.py         # Service for retrieving RabbitMQ connections
│   ├── GetConsumers.py           # Service for retrieving consumers
│   ├── GetQueues.py              # Service for retrieving queues
│   ├── Helper.py                 # Helper functions
│   ├── ResponseError.py          # Predefined error messages
│   ├── ResponseMessages.py       # Predefined success messages
│
├── WorkerRMQ.py                  # Main worker logic
├── app.py                        # Flask entry point
├── wsgi.py                       # Gunicorn entry point
├── requirements.txt              # Project dependencies
├── run.sh                        # Bash script for running the project
├── .env                          # Environment variables
└── README.md                     # Project description
```

---

## Microservice Highlights

- **Asynchronous Processing**:
  - Each message is consumed and processed independently, ensuring scalability.
- **Resilience**:
  - Messages are acknowledged only after successful processing.
- **Multithreaded Design**:
  - Concurrent message processing with RabbitMQ consumers.
- **Scalability**:
  - Deployed with Gunicorn for handling multiple requests and processes.
- **Modular Architecture**:
  - Organized into distinct modules for queue handling, logging, and message processing.

---