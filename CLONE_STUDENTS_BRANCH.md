# Clone the Student Branch First

Students should start by cloning the GitHub repository from the `students` branch before opening notebooks, installing dependencies, or running any course exercises.

## Step 1: Clone the repository

Use the branch name `students` in the clone command:

```bash
git clone -b students https://github.com/MajedTuah/advance-ml-fama.git
cd advance-ml-fama
```

If you already cloned the repository without the branch, switch to the course branch:

```bash
git checkout students
```

If the branch is not listed locally, fetch it first:

```bash
git fetch origin students
git checkout students
```

## Step 2: Confirm the branch

Make sure you are on the right branch:

```bash
git branch --show-current
```

You should see `students`.

## Step 3: Continue the setup

After the branch is confirmed, continue with the workshop instructions:

```bash
pip install -r requirements.txt
jupyter lab
```

> The `students` branch is the branch that contains the course materials the learners should work from.
