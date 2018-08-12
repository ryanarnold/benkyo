
var currentIndex = 0;
var secondsElapsed = 0;

$question = $('#question');
$inputAnswer = $('#input-answer');
$timeElapsed = $('#time-elapsed');
$btnSubmit = $('#btn-submit');

function updateQuestion() {
    secondsElapsed = 0;
    $question.html(reviewItems[currentIndex].question);
}

function finishReview() {
    var currentPath = window.location.pathname;

    $.ajax({
        url: currentPath + 'assessment/',
        dataType: 'json',
        data: {
            reviewItems: JSON.stringify(reviewItems)
        },
        success: function(result) {
            window.location.href = currentPath + 'end/';
        },
        error: function(xhr, status, error) {
          alert(error);
        }
    });
}

function nextQuestion() {
    currentIndex += 1;
    $question.removeClass('animated shake bounce faster');

    if (currentIndex < reviewItems.length) {
        updateQuestion();
        $inputAnswer.val('');
    } else {
        finishReview();
    }
}

function checkAnswer() {
    var answer = $inputAnswer.val();
    var correctAnswer = reviewItems[currentIndex].answer;

    if (answer.toLowerCase() == correctAnswer.toLowerCase()) {
        $question.addClass('animated bounce faster');
        reviewItems[currentIndex].correct = true;
    } else {
        $question.addClass('animated shake faster');
        reviewItems[currentIndex].correct = false;
    }

    reviewItems[currentIndex].timeToAnswer = secondsElapsed;

    setTimeout(nextQuestion, 1000);
}

$btnSubmit.mouseup(checkAnswer);

$inputAnswer.keyup(function (event) {
    if (event.which == 13) {
        checkAnswer();
    }
});

updateQuestion();

function updateTimer() {
    secondsElapsed += 1;
    $timeElapsed.text(secondsElapsed + ' secs');
}

updateTimer();
setInterval(updateTimer, 1000);
