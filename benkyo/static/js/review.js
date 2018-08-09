
var currentIndex = 0;

function updateQuestion() {
    $('#question').html(reviewItems[currentIndex].question);
}

function nextQuestion() {
    currentIndex += 1;

    if (currentIndex < reviewItems.length) {
        updateQuestion();
        $('#input-answer').val('');
    } else {
    }
}

function checkAnswer() {
    var answer = $('#input-answer').val();
    var correctAnswer = reviewItems[currentIndex].answer;

    if (answer == correctAnswer) {
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