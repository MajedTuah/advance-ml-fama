# 🐳 Topic 07 — API Serving & Containerization

> **Welcome to Topic 7!**  
> Your model is amazing, but it only lives on your laptop. How do you let a mobile app or a website use it? You wrap it in an **API**! And how do you make sure it runs the exact same way on the production servers as it does on your laptop? You put it in a **Docker Container**!

---

## 🎯 Learning Objectives

By the end of this 60-minute session, you will be able to:
1. **Wrap your model in an API** using **FastAPI**, so anyone on the internet can ask it for a prediction.
2. **Validate data** so that users can't crash your model by sending text when it expects a number.
3. **Write a Dockerfile** to package your model, your API, and all your Python libraries into one secure, portable box.

---

## 🧠 Core Concepts

### 1. Why APIs?
An API (Application Programming Interface) is like a waiter in a restaurant. You are the customer (the website). The model is the chef in the kitchen. You can't just walk into the kitchen! You hand your order to the waiter (the API), the waiter gives it to the chef, and then brings you back your food (the prediction).

### 2. FastAPI
FastAPI is the most popular way to build APIs in Python today. 
- It is incredibly fast.
- It automatically creates a beautiful documentation page (Swagger UI) for you.
- It uses **Pydantic** to check if the data sent to it is correct (e.g. checking that `age` is a number greater than 18).

### 3. Docker: Shipping your Kitchen
Imagine trying to move a kitchen to a new city. Instead of packing the blender, the oven, and the chef separately, **Docker** takes the entire kitchen, freezes it in a solid block of ice, moves it, and thaws it out. It guarantees that if the kitchen worked in City A, it will work exactly the same in City B.
- **Image (Blueprint):** The frozen block of ice. It never changes.
- **Container (Running App):** A thawed, running version of the image. You can have 10 identical containers running at once!

---

## 🏋️ Activities

1. **Activity 1 — Play with FastAPI:** We have provided a complete `app/` folder. You will start the FastAPI server on your laptop and test sending it data to get predictions.
2. **Activity 2 — Build the Container:** You will read the `Dockerfile`, build a Docker Image, and run your API inside an isolated container.

---

## 📝 Key Takeaways
- **No more "It works on my machine!"** Docker fixes this forever.
- **Load models ONCE.** Never load your model inside the `/predict` function. Load it when the API starts up, so predictions are lightning fast.
- **Always validate inputs.** Never trust the data the internet sends you.

---

## 📖 Further Reading
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Tutorial](https://docs.docker.com/get-started/)
