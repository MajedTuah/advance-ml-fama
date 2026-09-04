# Step 1: Start with a lightweight version of Python
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy ONLY the requirements file first.
# Why? So Docker can cache the installed libraries even if our python code changes!
COPY requirements.txt .

# Step 4: Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the actual python code into the container
COPY . /app

# Step 6: Tell Docker what port the app uses
EXPOSE 8000

# Step 7: The command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
