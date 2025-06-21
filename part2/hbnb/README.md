**Project Overview**
====================

This project is an implementation of a data management system using the Facade pattern and in-memory data repositories.

**Directory and File Structure**
-------------------------------

* **`app`**: The main directory of the project, containing the business logic and data repositories.
	+ **`__init__.py`**: The file that initializes the module and defines the project structure.
	+ **`facade.py`**: The file that defines the `HBnBFacade` class, which provides a simplified interface for interacting with data repositories.
	+ **`repository.py`**: The file that defines the `InMemoryRepository` class, which is used to store and retrieve data in memory.
* **`persistence`**: The directory that contains the data persistence logic.
	+ **`repository.py`**: The file that defines the `InMemoryRepository` class, which is used to store and retrieve data in memory.
* **`requirements.txt`**: The file that lists the project dependencies.
* **`README.md`**: The file that contains the project description and instructions for installing and running the application.

**Installing Dependencies**
-------------------------

To install the project dependencies, run the following command in the terminal:

```bash
pip install -r requirements.txt
```

**Running the Application**
---------------------------

To run the application, execute the following command in the terminal:

```bash
python app/facade.py
```

This will start the application and allow you to interact with the data repositories through the interface provided by the `HBnBFacade` class.
