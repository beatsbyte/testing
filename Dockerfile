FROM python3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["python", "test_basic.py"]