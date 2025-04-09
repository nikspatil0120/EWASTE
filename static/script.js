let questions = [];
let currentQuestionIndex = 0;
let score = 0;
let startTime;
let timerInterval;
let elapsedSeconds = 0;
let isTimerPaused = false;

const startScreen = document.getElementById('start-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultScreen = document.getElementById('result-screen');
const startBtn = document.getElementById('start-btn');
const questionText = document.getElementById('question-text');
const optionButtons = document.querySelectorAll('.option-btn');
const feedbackContainer = document.getElementById('feedback');
const feedbackText = document.getElementById('feedback-text');
const explanationText = document.getElementById('explanation-text');
const nextBtn = document.getElementById('next-btn');
const progressFill = document.querySelector('.progress-fill');
const currentQuestionNum = document.getElementById('current-question');
const scoreElement = document.getElementById('score');
const restartBtn = document.getElementById('restart-btn');
const resultMessage = document.querySelector('.result-message');
const timerDisplay = document.getElementById('timer');
const finalTimeDisplay = document.getElementById('final-time');
const highScoreMessage = document.getElementById('high-score-message');

startBtn.addEventListener('click', startQuiz);
nextBtn.addEventListener('click', nextQuestion);
restartBtn.addEventListener('click', restartQuiz);

function updateTimer() {
    if (!isTimerPaused) {
        elapsedSeconds++;
        const minutes = Math.floor(elapsedSeconds / 60);
        const seconds = elapsedSeconds % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        timerDisplay.textContent = timeString;
        return timeString;
    }
}

function pauseTimer() {
    isTimerPaused = true;
}

function resumeTimer() {
    isTimerPaused = false;
}

async function startQuiz() {
    try {
        document.body.classList.add('quiz-active');
        const response = await fetch('/api/questions');
        if (!response.ok) {
            throw new Error('Failed to fetch questions');
        }
        questions = await response.json();
        currentQuestionIndex = 0;
        score = 0;
        elapsedSeconds = 0;
        isTimerPaused = false;
        startScreen.style.display = 'none';
        quizScreen.style.display = 'block';
        
        // Start the timer
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(updateTimer, 1000);
        
        showQuestion();
    } catch (error) {
        console.error('Error fetching questions:', error);
        alert('Failed to load quiz questions. Please try again.');
    }
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function showQuestion() {
    const question = questions[currentQuestionIndex];
    questionText.textContent = question.question;
    
    // Create array of options with their original letters
    const optionsArray = [
        { letter: 'A', text: question.options.A },
        { letter: 'B', text: question.options.B },
        { letter: 'C', text: question.options.C },
        { letter: 'D', text: question.options.D }
    ];
    
    // Shuffle the options
    const shuffledOptions = shuffleArray([...optionsArray]);
    
    // Assign shuffled options to buttons with sequential numbers
    optionButtons.forEach((button, index) => {
        const option = shuffledOptions[index];
        button.textContent = `${index + 1}. ${option.text}`;
        button.dataset.option = option.letter;  // Store original letter for checking answer
        button.classList.remove('correct', 'wrong');
        button.disabled = false;
    });
    
    feedbackContainer.style.display = 'none';
    updateProgress();
}

function updateProgress() {
    const progress = ((currentQuestionIndex) / questions.length) * 100;
    progressFill.style.width = `${progress}%`;
    currentQuestionNum.textContent = currentQuestionIndex + 1;
}

optionButtons.forEach(button => {
    button.addEventListener('click', () => handleAnswer(button));
});

async function handleAnswer(selectedButton) {
    const question = questions[currentQuestionIndex];
    const selectedAnswer = selectedButton.dataset.option;
    
    // Pause timer when showing feedback
    pauseTimer();
    
    // Disable all buttons
    optionButtons.forEach(btn => btn.disabled = true);
    
    // Show correct/wrong indication
    const isCorrect = selectedAnswer === question.correct_answer;
    selectedButton.classList.add(isCorrect ? 'correct' : 'wrong');
    
    // If wrong, highlight the correct answer
    if (!isCorrect) {
        const correctButton = Array.from(optionButtons).find(
            btn => btn.dataset.option === question.correct_answer
        );
        correctButton.classList.add('correct');
    }
    
    // Update score
    if (isCorrect) score++;
    
    // Show feedback
    feedbackText.textContent = isCorrect ? '✨ Correct!' : '❌ Wrong answer';
    explanationText.textContent = question.explanation;
    feedbackContainer.style.display = 'block';
}

function nextQuestion() {
    // Resume timer when moving to next question
    resumeTimer();
    feedbackContainer.style.display = 'none';
    
    currentQuestionIndex++;
    
    if (currentQuestionIndex < questions.length) {
        showQuestion();
    } else {
        submitScore();
    }
}

async function submitScore() {
    // Stop the timer
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    const timeTaken = elapsedSeconds;
    const finalTimeString = updateTimer();
    
    try {
        const response = await fetch('/api/submit-score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                score: score,
                time_taken: timeTaken
            })
        });

        if (!response.ok) {
            throw new Error('Failed to submit score');
        }

        const result = await response.json();
        finalTimeDisplay.textContent = finalTimeString;
        
        if (result.isNewHighScore) {
            highScoreMessage.style.display = 'block';
        } else {
            highScoreMessage.style.display = 'none';
        }

        showResults();
    } catch (error) {
        console.error('Error submitting score:', error);
        alert('Failed to submit score. Please try again.');
    }
}

function showResults() {
    quizScreen.style.display = 'none';
    resultScreen.style.display = 'block';
    scoreElement.textContent = score;
    
    // Set result message based on score
    let message;
    const percentage = (score / questions.length) * 100;
    
    if (percentage === 100) {
        message = "🏆 Perfect Score! You're an e-waste expert!";
    } else if (percentage >= 80) {
        message = "🌟 Great job! You're very knowledgeable about e-waste!";
    } else if (percentage >= 60) {
        message = "👍 Good effort! You know the basics of e-waste.";
    } else if (percentage >= 40) {
        message = "📚 You're learning! Keep exploring e-waste topics.";
    } else {
        message = "🌱 Time to learn more about e-waste! Try again?";
    }
    
    resultMessage.textContent = message;
}

function restartQuiz() {
    document.body.classList.remove('quiz-active');
    resultScreen.style.display = 'none';
    startScreen.style.display = 'block';
    progressFill.style.width = '0%';
    timerDisplay.textContent = '00:00';
    highScoreMessage.style.display = 'none';
} 
