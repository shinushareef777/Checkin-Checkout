# Time Tracker

This is a simply REST API which can be used to create/update/delete/list your expenses

## Getting Started

These instructions will help you set up and run the expense tracker docker container.

### Prerequisites

- Docker installed on your machine.

### Build and Run

1. **Clone the repository**:
   ```bash
      git clone <repository_url>

2. **Navigate to project directory**:
   ```bash
   cd directory

3. **Build the Docker image**:
   This will pull and build all the images necessary to run this project
   ```bash
   docker-compose up --build
   
4. **Run the container**:
   if you exited the container after building:
   ```bash
     docker-compose up 

5. **Run the Docker image**:

6. **Usage:**
    - Use the provided REST API endpoints to interact with the expense tracker:
        - GET /instructor: List all instructor.
        - POST /instructor: Create an instructor.
          ```{
                "name": "Instructor name"
            }
        - GET /checkin: Get all the checkin.
        - POST /checkin: Create a checkin with instructor id.
          example request body
          ```{
              "time":"9:00:00",
              "date":"2024-04-20",
              "instructor_id": 2
          }
        - GET /checkin: Get all the checkin.
        - POST /checkout: Create a checkout with instructor id.
          example request body
          ```{
              "time":"9:00:00",
              "date":"2024-04-20",
              "instructor_id": 2
          }
        - GET /summary/{month}: Get monthly summary of working hours
          eg: /summary/2 gives total in time for all the instructor for february
          


   
