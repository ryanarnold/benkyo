
var currentIndex = 0;
var secondsElapsed = 0;

function updateQuestion() {
    secondsElapsed = 0;
    $('#question').html(reviewItems[currentIndex].question);
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
    $('#question').removeClass('animated shake bounce faster');

    if (currentIndex < reviewItems.length) {
        updateQuestion();
        $('#input-answer').val('');
    } else {
    }
}

function checkAnswer() {
    var answer = $('#input-answer').val();
    var correctAnswer = reviewItems[currentIndex].answer;

    if (answer.toLowerCase() == correctAnswer.toLowerCase()) {
        $('#question').addClass('animated bounce faster');
        // alert('CORRECT!');
    } else {
        $('#question').addClass('animated shake faster');
        // alert('WRONG!');
    }

    setTimeout(nextQuestion, 1000);
}

$('#btn-submit').mouseup(checkAnswer);
$('#input-answer').keyup(function (event) {
    if (event.which == 13) {
        checkAnswer();
    }
});
updateQuestion();

function updateTimer() {
    secondsElapsed += 1;
    $('#time-elapsed').text(secondsElapsed + ' secs');
}

updateTimer();
setInterval(updateTimer, 1000);
