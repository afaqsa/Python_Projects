questions = [
    {
        "question": "What comes next in the sequence? 2, 6, 12, 20, 30, ___?",
        "options": ["a) 42", "b) 56", "c) 72", "d) 90"],
        "answer": "a"
    },
    {
        "question": "Which of the following shapes completes the pattern? 🟢🟢🟠🟠🟢🟢__?",
        "options": ["a) 🟠","b) 🔴" ,"c) 🟡" ,"d) 🟢"],
        "answer": "a"

    },
    {
        "question": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
        "options": ["a) Yes" , "b) No", "c) Can't be determined", "d) Only in specific cases"],
        "answer": "c"
    },
    {
        "question": "Pencil is to Paper as Brush is to ___?",
        "options": [
            "a) Art",
            "b) Paint",
            "c) Canvas",
            "d) Color"
        ],
        "answer": "c" 

    },
    {
        "question": "If a train travels 50 miles in 1 hour, how far will it travel in 5 hours at the same speed?",
        "options": [
            "a) 100 miles",
            "b) 200 miles",
            "c) 250 miles",
            "d) 300 miles"
            ],
        "answer": "c"

    },
    {
      "question":  "Which one of the following does not belong?",
      "options": [
          "a) 2, 4, 8, 16, 32",
          "b) 3, 6, 12, 24, 48",
          "c) 1, 2, 4, 8, 16",
          "d) 5, 10, 20, 40, 80"
            ],
        "answer": "b"
   
    },
    {
    "question": "Which of the following words is most similar to \"Paradox\"?",
    "options": [
        "a) Puzzle",
        "b) Challenge",
        "c) Symmetry",
        "d) Contradiction"
    ],
    "answer": "d"
    },
    {
   "question" : "What number completes the series: 3, 9, 27, ___?",
    "options": [
         "a) 54",
         "b) 81",
         "c) 90",
         "d) 108"
     ],
    "answer": "b"
    },
    {
    "question":"If a cube has all its faces colored blue, how many faces would you be able to see if it is rotated to show 3 of its faces?",
    "options": [
        "a) 1",
        "b) 2",
        "c) 3",
        "d) 4"
    ],
    "answer": "c"
    },
    {
    "question": "If you face east and turn 90 degrees to your right, which direction will you be facing?",
    "options": [
        "a) North",
        "b) South",
        "c) West",
        "d) East"
    ],
    "answer": "b"
    }
];
score = 0;
total_questions = len(questions);
print("-------::Welcome to the Quiz Game! ::-------");
player = input("Enter you name : ");
choise = input(f"Hello {player}, Do you want to play the quiz game? (yes/no) : ");
if choise.lower() == "yes":
    print("Great! Let's start the game.");
    for idx, q in enumerate(questions,1):
        print(f"\nQuestion {idx}: {q['question']}")
        for option in q["options"]:
            print(f"  {option}")
        answer = input("Your answer (a/b/c/d): ").lower()
        if answer == q["answer"]:
            score += 1
    
    print(f"\nYour score is {score} out of {total_questions}")
    percentage = (score / total_questions) * 100
    print(f"Your percentage is {percentage}%")
    if percentage >= 70:
        print("Congratulations! You passed the quiz.")
    else:
        print("Sorry, you did not pass the quiz.")
else:
    print("Thank you for your time! Have a great day!")